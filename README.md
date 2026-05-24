# ishioni Home Assistant Add-ons

Custom Home Assistant add-ons for network printing and scanning.

[![Open your Home Assistant instance and add this repository.](https://my.home-assistant.io/badges/supervisor_repository.svg)](https://my.home-assistant.io/redirect/supervisor_repository/?repository_url=https%3A%2F%2Fgithub.com%2Fishioni%2Fhass-addons)

## Add this repository to Home Assistant

### Option 1: One-click button

Use the button above from a device that is signed in to your Home Assistant instance.

### Option 2: Manually in Home Assistant

1. Open **Settings → Add-ons → Add-on Store**
2. Open the **three-dot menu**
3. Choose **Repositories**
4. Add:

   ```text
   https://github.com/ishioni/hass-addons
   ```

## Available add-ons

| Add-on            | Description                                                                                                                                                     | Docs                                                   |
| ----------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------ |
| `CUPS`            | A CUPS print server add-on with working AirPrint for local network printer sharing.                                                                             | [`cups/DOCS.md`](./cups/DOCS.md)                       |
| `AirSane Scanner` | Publishes configured SANE scanners to macOS and other AirScan/eSCL clients. Current scope is Brother network scanners through the open-source `brscan` backend. | [`airsane-scanner/DOCS.md`](./airsane-scanner/DOCS.md) |

## Notes

- Add-ons in this repository target `amd64` and `aarch64` where supported by each add-on.
- Some add-ons intentionally use `host_network: true` for mDNS/DNS-SD service advertisement.
- Add-on-specific setup, limitations, and configuration live in each add-on's `DOCS.md`.

## Repository metadata

- Repository file: [`repository.yaml`](./repository.yaml)
- License: [`LICENSE`](./LICENSE)
