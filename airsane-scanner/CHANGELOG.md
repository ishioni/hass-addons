# Changelog

## 0.1.1

- Harden runtime config rendering with stricter scanner normalization and clearer validation errors
- Add local path overrides to `render-config.py` so generated config can be validated outside Home Assistant
- Emit generated config summary at startup for easier troubleshooting
- Enable AirSane debug mode automatically when add-on `log_level` is `debug` or `trace`
- Apply `defaults.mode` and `defaults.resolution` to generated AirSane device options when the scanner model can be matched unambiguously
- Avoid generating misleading per-device AirSane options when multiple configured scanners share the same Brother model string
- Clarify in docs that `host` is mandatory because the add-on currently supports network scanners only, while `model_override.usb_id` is Brother backend model metadata rather than a USB transport selector

## 0.1.0

- Initial scaffold for AirSane scanner add-on
- Add Home Assistant options schema for configured scanners and AirSane settings
- Build AirSane and brscan from pinned release archives instead of git clones
- Use the exact upstream AirSane release tag name (`v.0.4.10`) and robust archive extraction for reproducible source downloads
- Apply local brscan source patch during image build for missing Brother model entries
