# AirSane Scanner

## About

This add-on exposes configured SANE scanners to AirScan/eSCL clients such as macOS Image Capture, Preview, and iOS/iPadOS scanner pickers.

It is designed around a generated configuration model:

- Home Assistant add-on options define scanners at a high level
- the add-on generates Brother backend, SANE, and AirSane config files at startup
- AirSane publishes working SANE devices on the local network

## Current scope

This first version targets Brother network scanners through the open-source `brscan` backend and publishes them through AirSane.

That means each configured scanner is expected to be reachable over the network, so `host` is currently required for every scanner entry.

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
- `host`: Scanner IP address or hostname. Required in the current implementation because this add-on currently supports network scanners only.
- `model`: Known built-in model name
- `enabled`: Optional, defaults to `true`
- `defaults.mode`: Optional AirSane/SANE default mode hint. Supported values: `color`, `gray`, `bw`
- `defaults.resolution`: Optional AirSane/SANE default resolution hint
- `model_override`: Advanced escape hatch for unsupported models

### Model override semantics

`model_override` does **not** switch the add-on into a USB-connected mode.

The current add-on still expects a **network** scanner and still requires `host`.
The `usb_id` field here is unfortunate but intentional: it is Brother backend **model metadata** used to generate the `brscan` model catalog, even for network scanners.

So in practice:

- `host` answers **where the scanner is on the network**
- `model` or `model_override` answers **which Brother backend definition to use**
- `usb_id` is part of that Brother model definition, not a transport selector

USB-connected scanners are **not** a supported configuration mode in this add-on today.

Example override:

```yaml
scanners:
  - name: custom_brother
    host: 192.168.1.50
    enabled: true
    model_override:
      usb_id: 0x4f9:0x02ce
      series: 14
      type: 2
      model_name: DCP-7055W
```

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
- `/usr/share/sane/brother/models2/zz-hass-models.ini`
- `/usr/share/sane/brother/brsanenetdevice2.cfg`
- `/etc/default/airsane`
- `/etc/airsane/options.conf`
- `/etc/airsane/access.conf`
- `/etc/airsane/ignore.conf`

Users should configure the add-on through Home Assistant options, not by editing generated files directly.

## Notes

- This add-on currently focuses on Brother network scanners
- Higher scan resolutions may be device-dependent and can be slow on older scanners
- AirSane only works once the underlying SANE backend can see the device
- Setting add-on `log_level` to `debug` or `trace` also enables AirSane's own debug output
