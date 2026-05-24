# CUPS

## About

This add-on provides a CUPS print server inside Home Assistant.

It is intended for exposing printers on your local network and includes support for AirPrint-related components such as Avahi/mDNS.

## Features

- Runs a CUPS print server
- Exposes IPP on port `631`
- Supports local-network printer discovery via mDNS/Avahi
- Persists CUPS configuration across restarts

## Networking

This add-on runs with `host_network: true`.

It exposes:

- `631/tcp` — IPP / CUPS web interface and printer access
- `631/udp` — printer-related network traffic on the local network

Because it uses the host network, make sure port `631` is available on your Home Assistant host.

## Persistent data

On first start, the add-on copies the default CUPS configuration into persistent storage and then uses that stored configuration on subsequent starts.

CUPS configuration is persisted under the add-on data directory.

## USB access

This add-on requests USB access (`usb: true`) so locally attached USB printers can be made available to CUPS.

## Home Assistant / Supervisor access

This add-on uses the Supervisor API during startup to detect the host OS version and adjust runtime behavior.

## Initial setup

After starting the add-on:

1. Open the CUPS web interface on your Home Assistant host at port `631`
2. Add and configure your printers
3. Verify the printer is reachable from other devices on your network

## Notes

- This add-on is intended for use on a trusted local network
- Since it uses host networking, any CUPS service it exposes is available directly on your Home Assistant host
