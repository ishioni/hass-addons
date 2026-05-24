# Home Assistant Add-on: AirSane Scanner

AirSane scanner add-on for Home Assistant.

This add-on is intended to expose configured SANE scanners to Apple Image Capture, Preview, and other AirScan/eSCL clients.

Current scope is **Brother network scanners**. The add-on does not currently support a separate USB-connected scanner configuration mode or manual runtime model overrides.

## Current status

The add-on scaffold now includes:

- pinned AirSane and `brscan` source builds
- runtime-generated Brother network, SANE, and AirSane config
- stricter scanner option normalization and validation
- startup logging for rendered config output
- best-effort application of scanner default mode/resolution settings
- curated built-in Brother model support instead of runtime model override definitions
- a broad built-in Brother model catalog derived from Brother's `brscan4` ini inventory

## Files

- `config.yaml` — add-on metadata and Home Assistant configuration
- `CHANGELOG.md` — version history
- `DOCS.md` — usage and setup documentation
- `Dockerfile` — container build definition
