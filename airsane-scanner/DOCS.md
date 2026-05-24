# AirSane Scanner

## About

This add-on exposes configured SANE scanners to AirScan/eSCL clients such as macOS Image Capture, Preview, and iOS/iPadOS scanner pickers.

It is designed around a generated configuration model:

- Home Assistant add-on options define scanners at a high level
- the add-on generates Brother network backend, SANE, and AirSane config files at startup
- AirSane publishes working SANE devices on the local network

## Current scope

This first version targets curated Brother network scanners through the open-source `brscan` backend and publishes them through AirSane.

That means each configured scanner is expected to be reachable over the network, so `host` is required for every scanner entry.

This add-on does **not** currently support:

- USB-connected scanner configuration
- arbitrary manual Brother model definitions through add-on options

Supported models are the ones shipped in the add-on's built-in model catalog and corresponding patched `brscan` data.

That catalog is now derived from Brother's `brscan4` ini files (main file plus extension ini files), rather than from a tiny hand-maintained subset.

## Configuration

Example:

```yaml
log_level: info
airsane:
  port: 8090
  mdns_announce: true
  web_interface: true
  compatible_path: true
  local_scanners_only: false
scanners:
  - name: office_brother
    host: 192.168.1.4
    model: DCP-7055W
    enabled: true
    defaults:
      mode: color
      resolution: 300
```

### Scanner fields

- `name`: Friendly identifier used in generated config and logs. Use only letters, numbers, `.`, `_`, or `-`.
- `host`: Scanner IP address or hostname. Required because this add-on currently supports network scanners only.
- `model`: Known built-in Brother model name from the add-on catalog.
- `enabled`: Optional, defaults to `true`
- `defaults.mode`: Optional AirSane/SANE default mode hint. Supported values: `color`, `gray`, `bw`
- `defaults.resolution`: Optional AirSane/SANE default resolution hint

### Notes about defaults

When AirSane can uniquely match a configured scanner model, the add-on writes `defaults.mode` and `defaults.resolution` into `options.conf` as backend defaults.

If you configure multiple scanners that share the same Brother model string, AirSane cannot reliably distinguish them with the current matching approach. In that case, the add-on skips per-device defaults for that model and logs a warning instead of generating misleading config.

## Networking

This add-on uses `host_network: true` because:

- AirSane publishes scanners over mDNS/Avahi
- scanner discovery and client interoperability are best on the host network
- scanners are expected to be reachable directly on the local LAN

Port exposed:

- `8090/tcp` — AirSane web UI and eSCL endpoint

## Generated files

The add-on generates runtime files for:

- `/etc/sane.d/dll.conf`
- `/usr/share/sane/brother/brsanenetdevice2.cfg`
- `/etc/default/airsane`
- `/etc/airsane/options.conf`
- `/etc/airsane/access.conf`
- `/etc/airsane/ignore.conf`

Users should configure the add-on through Home Assistant options, not by editing generated files directly.

## Notes

- This add-on currently focuses on Brother network scanners
- The built-in model catalog is broad because it is derived from Brother's `brscan4` ini inventory; actual success still depends on your device supporting network scanning
- Higher scan resolutions may be device-dependent and can be slow on older scanners
- AirSane only works once the underlying SANE backend can see the device
- Setting add-on `log_level` to `debug` or `trace` also enables AirSane's own debug output
- If you need a model that is not in the built-in catalog yet, the right fix is to add it to the shipped catalog and patch, rather than defining it ad hoc in add-on options
