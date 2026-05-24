# Changelog

## 0.1.0

- Initial scaffold for AirSane scanner add-on
- Add Home Assistant options schema for configured scanners and AirSane settings
- Build AirSane and brscan from pinned release archives instead of git clones
- Use the exact upstream AirSane release tag name (`v.0.4.10`) and robust archive extraction for reproducible source downloads
- Apply local brscan source patch during image build for missing Brother model entries
