# Changelog

## 0.1.0

- Initial scaffold for AirSane scanner add-on
- Add Home Assistant options schema for configured scanners
- Build AirSane and brscan from pinned release archives instead of git clones
- Use the exact upstream AirSane release tag name (`v.0.4.10`) and robust archive extraction for reproducible source downloads
- Apply local brscan source patch during image build for missing Brother model entries
- Harden runtime config rendering with stricter scanner normalization and clearer validation errors
- Add local path overrides to `render-config.py` so generated config can be validated outside Home Assistant
- Emit generated config summary at startup for easier troubleshooting
- Enable AirSane debug mode automatically when add-on `log_level` is `debug` or `trace`
- Apply `defaults.mode` and `defaults.resolution` to generated AirSane device options when the scanner model can be matched unambiguously
- Avoid generating misleading per-device AirSane options when multiple configured scanners share the same Brother model string
- Clarify in docs that `host` is mandatory because the add-on currently supports network scanners only
- Remove runtime Brother model override support from add-on options
- Stop generating a runtime `zz-hass-models.ini`; rely on curated shipped Brother model data instead
- Simplify the renderer to require a known built-in model for every configured scanner
- Clarify docs around the network-only scope and curated model support strategy
- Expand the built-in Brother model catalog to cover the full model inventory found in Brother's `brscan4` ini files
- Replace the narrow hand-picked model subset with a much broader curated catalog derived from Brother package metadata
- Broaden the local `brscan` patch so shipped backend model data tracks the same expanded Brother `brscan4` inventory
- Add `SUPPORTED_MODELS.md` and link to it from the docs so users can choose exact built-in model names
- Refactor the Docker build into builder/runtime stages so compiler toolchains and development headers stay out of the final image
- Add explicit S6 services for D-Bus and Avahi plus an Avahi config file instead of backgrounding those daemons manually in `run.sh`
- Fix the multi-stage runtime image to include `brscan` companion libraries (`libbrcolm*`, `libbrscandec*`) needed when opening scanners
- Mirror the builder image's Brother library symlink layout in the final runtime image and eliminate `ldconfig` warnings
- Pass AirSane hotplug-related flags through from generated config instead of silently relying on upstream defaults
- Default AirSane `network_hotplug` to `false` in this add-on to avoid startup reloads triggered by IPv6/link-local address churn in the Home Assistant host-network environment
- Simplify the add-on configuration schema to focus on configured scanners instead of exposing upstream AirSane daemon flags
- Keep the AirSane runtime behavior fixed internally with mDNS announcement enabled, a compatible `/eSCL` path, and network-hotplug reloads disabled for Home Assistant host-network stability
- Add Home Assistant-style scanner icon and logo assets based on `mdi:scanner`
