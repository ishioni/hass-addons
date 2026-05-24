#!/usr/bin/env python3

from __future__ import annotations

import json
import os
import re
from collections import defaultdict
from pathlib import Path
from typing import Any

ROOT_DIR = Path(os.environ.get("AIRSANE_SCANNER_ROOT", "/"))
VALID_SCANNER_NAME_RE = re.compile(r"^[A-Za-z0-9._-]+$")
MODE_OPTION_VALUES = {
    "color": "Color",
    "gray": "Gray",
    "bw": "Lineart",
}


def rooted(path: str) -> Path:
    return ROOT_DIR / path.lstrip("/")


OPTIONS_PATH = Path(
    os.environ.get("AIRSANE_SCANNER_OPTIONS_PATH", str(rooted("/data/options.json")))
)
KNOWN_MODELS_PATH = Path(
    os.environ.get(
        "AIRSANE_SCANNER_KNOWN_MODELS_PATH",
        str(rooted("/usr/local/share/airsane-scanner/known_models.json")),
    )
)
BROTHER_SHARE_DIR = rooted("/usr/share/sane/brother")
BROTHER_NETDEV_FILE = BROTHER_SHARE_DIR / "brsanenetdevice2.cfg"
SANE_DLL_CONF = rooted("/etc/sane.d/dll.conf")
AIRSANE_DEFAULTS = rooted("/etc/default/airsane")
AIRSANE_DIR = rooted("/etc/airsane")
AIRSANE_OPTIONS = AIRSANE_DIR / "options.conf"
AIRSANE_ACCESS = AIRSANE_DIR / "access.conf"
AIRSANE_IGNORE = AIRSANE_DIR / "ignore.conf"


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def normalize_bool(value: Any, default: bool) -> bool:
    if value is None:
        return default
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.lower() in {"1", "true", "yes", "on"}
    return bool(value)


def normalize_scanners(raw_scanners: Any) -> list[dict[str, Any]]:
    if raw_scanners is None:
        return []
    if not isinstance(raw_scanners, list):
        raise ValueError("'scanners' must be a list")

    scanners: list[dict[str, Any]] = []
    seen_names: set[str] = set()

    for index, raw_scanner in enumerate(raw_scanners):
        if not isinstance(raw_scanner, dict):
            raise ValueError(f"scanner at index {index} must be an object")

        scanner = dict(raw_scanner)
        name = str(scanner.get("name", "")).strip()
        if not name:
            raise ValueError(f"scanner at index {index} is missing a name")
        if not VALID_SCANNER_NAME_RE.fullmatch(name):
            raise ValueError(
                f"scanner '{name}' must use only letters, numbers, '.', '_' or '-'"
            )
        if name in seen_names:
            raise ValueError(f"scanner name '{name}' is duplicated")
        seen_names.add(name)

        host = str(scanner.get("host", "")).strip()
        if not host:
            raise ValueError(f"scanner '{name}' is missing a host")

        model = str(scanner.get("model", "")).strip()
        if not model:
            raise ValueError(f"scanner '{name}' is missing a model")

        normalized: dict[str, Any] = {
            "name": name,
            "host": host,
            "model": model,
            "enabled": normalize_bool(scanner.get("enabled"), True),
        }

        defaults = scanner.get("defaults") or {}
        if defaults and not isinstance(defaults, dict):
            raise ValueError(f"scanner '{name}' defaults must be an object")
        normalized_defaults: dict[str, Any] = {}
        if "mode" in defaults and defaults.get("mode") is not None:
            mode = str(defaults["mode"]).strip().lower()
            if mode not in MODE_OPTION_VALUES:
                raise ValueError(
                    f"scanner '{name}' defaults.mode must be one of: {', '.join(MODE_OPTION_VALUES)}"
                )
            normalized_defaults["mode"] = mode
        if "resolution" in defaults and defaults.get("resolution") is not None:
            try:
                resolution = int(defaults["resolution"])
            except (TypeError, ValueError) as exc:
                raise ValueError(
                    f"scanner '{name}' defaults.resolution must be an integer"
                ) from exc
            if resolution <= 0:
                raise ValueError(
                    f"scanner '{name}' defaults.resolution must be positive"
                )
            normalized_defaults["resolution"] = resolution
        if normalized_defaults:
            normalized["defaults"] = normalized_defaults

        scanners.append(normalized)

    return scanners


def resolve_model(
    scanner: dict[str, Any], known_models: dict[str, Any]
) -> dict[str, Any]:
    model_name = scanner["model"]
    if model_name not in known_models:
        raise ValueError(
            f"scanner '{scanner['name']}' uses unknown model '{model_name}'"
        )
    return dict(known_models[model_name])


def resolve_scanners(
    scanners: list[dict[str, Any]], known_models: dict[str, Any]
) -> list[dict[str, Any]]:
    rendered: list[dict[str, Any]] = []
    for scanner in scanners:
        if not scanner["enabled"]:
            continue
        rendered.append(
            {**scanner, "_resolved_model": resolve_model(scanner, known_models)}
        )
    return rendered


def write_sane_dll_conf() -> None:
    ensure_dir(SANE_DLL_CONF.parent)
    SANE_DLL_CONF.write_text("brother\n", encoding="utf-8")


def write_brother_netdev_file(scanners: list[dict[str, Any]]) -> None:
    ensure_dir(BROTHER_SHARE_DIR)
    lines: list[str] = []
    for scanner in scanners:
        model = scanner["_resolved_model"]
        lines.append(
            f'DEVICE={scanner["name"]} , "{model["model_name"]}" , {model["usb_id"]} , IP-ADDRESS={scanner["host"]}'
        )
    BROTHER_NETDEV_FILE.write_text(
        "\n".join(lines) + ("\n" if lines else ""), encoding="utf-8"
    )


def write_airsane_defaults(options: dict[str, Any]) -> None:
    ensure_dir(AIRSANE_DEFAULTS.parent)
    airsane = options.get("airsane") or {}
    port = int(airsane.get("port", 8090))
    interface = str(airsane.get("interface") or "")
    hotplug = str(normalize_bool(airsane.get("hotplug"), True)).lower()
    network_hotplug = str(normalize_bool(airsane.get("network_hotplug"), False)).lower()
    reload_delay = int(airsane.get("reload_delay", 1))
    mdns_announce = str(normalize_bool(airsane.get("mdns_announce"), True)).lower()
    announce_base_url = str(airsane.get("announce_base_url") or "")
    web_interface = str(normalize_bool(airsane.get("web_interface"), True)).lower()
    compatible_path = str(normalize_bool(airsane.get("compatible_path"), True)).lower()
    local_scanners_only = str(
        normalize_bool(airsane.get("local_scanners_only"), False)
    ).lower()

    content = f"""INTERFACE={interface}
LISTEN_PORT={port}
UNIX_SOCKET=
ACCESS_LOG=-
HOTPLUG={hotplug}
NETWORK_HOTPLUG={network_hotplug}
RELOAD_DELAY={reload_delay}
MDNS_ANNOUNCE={mdns_announce}
ANNOUNCE_SECURE=false
ANNOUNCE_BASE_URL={announce_base_url}
WEB_INTERFACE={web_interface}
RESET_OPTION=false
DISCLOSE_VERSION=true
RANDOM_PATHS=false
COMPATIBLE_PATH={compatible_path}
LOCAL_SCANNERS_ONLY={local_scanners_only}
OPTIONS_FILE=/etc/airsane/options.conf
IGNORE_LIST=/etc/airsane/ignore.conf
ACCESS_FILE=/etc/airsane/access.conf
"""
    AIRSANE_DEFAULTS.write_text(content, encoding="utf-8")


def write_airsane_aux_files(scanners: list[dict[str, Any]]) -> list[str]:
    ensure_dir(AIRSANE_DIR)
    warnings: list[str] = []
    lines = ["# Generated by AirSane Scanner add-on", ""]
    scanners_by_model: dict[str, list[dict[str, Any]]] = defaultdict(list)

    for scanner in scanners:
        scanners_by_model[scanner["_resolved_model"]["model_name"]].append(scanner)

    for model_name in sorted(scanners_by_model):
        matching_scanners = scanners_by_model[model_name]
        if len(matching_scanners) > 1:
            warnings.append(
                f"skipped AirSane per-device defaults for model '{model_name}' because {len(matching_scanners)} configured scanners share the same model string"
            )
            lines.append(
                f"# Skipped per-device AirSane defaults for model '{model_name}' because multiple configured scanners share that model string."
            )
            lines.append("")
            continue

        scanner = matching_scanners[0]
        lines.append(f"device ^{re.escape(model_name)}$")
        lines.append(f"location {scanner['name']}")

        defaults = scanner.get("defaults") or {}
        if defaults.get("mode"):
            lines.append(f"mode {MODE_OPTION_VALUES[defaults['mode']]}")
        if defaults.get("resolution"):
            lines.append(f"resolution {defaults['resolution']}")
        lines.append("")

    AIRSANE_OPTIONS.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
    AIRSANE_ACCESS.write_text(
        "# Generated by AirSane Scanner add-on\nallow local on *\n", encoding="utf-8"
    )
    AIRSANE_IGNORE.write_text(
        "# Generated by AirSane Scanner add-on\n", encoding="utf-8"
    )
    return warnings


def main() -> None:
    options = load_json(OPTIONS_PATH) if OPTIONS_PATH.exists() else {}
    known_models = load_json(KNOWN_MODELS_PATH)
    scanners = normalize_scanners(options.get("scanners"))
    rendered = resolve_scanners(scanners, known_models)

    write_sane_dll_conf()
    write_brother_netdev_file(rendered)
    write_airsane_defaults(options)
    warnings = write_airsane_aux_files(rendered)

    print(
        json.dumps(
            {
                "configured_scanners": [scanner["name"] for scanner in rendered],
                "generated_netdev_file": str(BROTHER_NETDEV_FILE),
                "generated_options_file": str(AIRSANE_OPTIONS),
                "warnings": warnings,
            }
        )
    )


if __name__ == "__main__":
    main()
