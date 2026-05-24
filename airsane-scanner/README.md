# Home Assistant Add-on: AirSane Scanner

AirSane scanner add-on for Home Assistant.

This add-on is intended to expose configured SANE scanners to Apple Image Capture, Preview, and other AirScan/eSCL clients.

Current scope is **Brother network scanners**. The add-on does not currently support a separate USB-connected scanner configuration mode.

## Current status

The add-on scaffold now includes:

- pinned AirSane and `brscan` source builds
- runtime-generated Brother, SANE, and AirSane config
- stricter scanner option normalization and validation
- startup logging for rendered config output
- best-effort application of scanner default mode/resolution settings

## Files

- `config.yaml` — add-on metadata and Home Assistant configuration
- `CHANGELOG.md` — version history
- `DOCS.md` — usage and setup documentation
- `Dockerfile` — container build definition
