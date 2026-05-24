# AirSane Scanner Add-on Plan

## Goal

Create a Home Assistant add-on that:

- configures Brother network scanners through the open-source `brscan` backend
- publishes them through `AirSane` as AirScan/eSCL scanners
- uses Home Assistant add-on options as the source of truth
- generates network backend, SANE, and AirSane config files at runtime

## Current status

The following has been proven:

- `brscan` builds on `aarch64`
- the Brother `DCP-7055W` works over the network through the open-source backend
- real grayscale and color scans work from a Debian arm64 VM
- a local Docker image for this add-on builds successfully
- generated config inside the built image can enumerate the real scanner
- AirSane can start and publish the scanner over eSCL from the built image

## Known implementation choices

- use release archives for both `brscan` and `AirSane`
- patch `brscan` during image build for missing Brother model entries
- keep the add-on runtime simple (`run.sh`), matching the style of the existing `cups` add-on
- generate runtime config from `/data/options.json`
- use host networking for AirSane and mDNS/Avahi
- rely on a curated built-in Brother model catalog rather than runtime model overrides
- derive that catalog from Brother's `brscan4` ini files instead of maintaining a tiny hand-written subset

## Known quirks / caveats

- the Home Assistant base image expects Supervisor APIs during normal startup, so plain local `docker run` is not a perfect simulation of in-HA boot
- AirSane's web UI intentionally shows a reduced resolution list even when the backend/eSCL capabilities expose more values
- very high resolutions on older Brother devices may be unstable or too slow; 600 dpi looked reasonable in testing
- current scaffold uses the repo's `BRSANESUFFIX=2` layout, so generated Brother files currently target `brsanenetdevice2.cfg`

## Next steps

### 1. Tighten add-on configuration schema

- validate nested `scanners` entries more strictly
- decide how much of AirSane should be user-configurable in v1
- consider whether model selection should be restricted to an enumerated catalog in UI/docs

### 2. Improve built-in model catalog

- keep `known_models.json` in sync with Brother `brscan4` package metadata
- document the source of model IDs and series/type mappings
- consider upstreaming missing models to `brscan`

### 3. Runtime hardening

- verify `run.sh` behavior under a real Home Assistant Supervisor environment
- improve startup logging and failure messages
- consider whether `scanimage -L` should be mandatory or warning-only at boot

### 4. AirSane behavior

- decide whether to patch AirSane's web UI to expose all discrete resolutions from SANE
- verify macOS/iOS behavior against published `ScannerCapabilities`

### 5. Add-on polish

- add icon/logo assets if desired
- improve docs and examples
- test install flow in an actual HA add-on environment

## Files of interest

- `Dockerfile`
- `config.yaml`
- `DOCS.md`
- `rootfs/run.sh`
- `rootfs/usr/local/bin/render-config.py`
- `rootfs/usr/local/share/airsane-scanner/known_models.json`
- `patches/brscan/0001-add-brother-brscan4-models.patch`
