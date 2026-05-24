#!/usr/bin/with-contenv bashio

set -euo pipefail

bashio::log.info "Rendering scanner and AirSane configuration"
render_output="$(/usr/local/bin/render-config.py)"
bashio::log.info "Render result: ${render_output}"

bashio::log.info "Starting D-Bus system daemon"
mkdir -p /run/dbus
if [ ! -f /run/dbus/pid ]; then
  dbus-daemon --system --fork
fi

bashio::log.info "Starting Avahi daemon"
mkdir -p /run/avahi-daemon
if [ ! -S /run/avahi-daemon/socket ]; then
  avahi-daemon --daemonize --no-chroot
fi

if [ -f /etc/ld.so.conf.d/brscan-sane.conf ]; then
  ldconfig
fi

source /etc/default/airsane

airsane_args=(
  "--listen-port=${LISTEN_PORT}"
  "--mdns-announce=${MDNS_ANNOUNCE}"
  "--web-interface=${WEB_INTERFACE}"
  "--compatible-path=${COMPATIBLE_PATH}"
  "--local-scanners-only=${LOCAL_SCANNERS_ONLY}"
  "--options-file=${OPTIONS_FILE}"
  "--ignore-list=${IGNORE_LIST}"
  "--access-file=${ACCESS_FILE}"
)

log_level="info"
if [ -f /data/options.json ]; then
  log_level="$(jq -r '.log_level // "info"' /data/options.json 2>/dev/null || printf 'info')"
fi
if [ "${log_level}" = "debug" ] || [ "${log_level}" = "trace" ]; then
  bashio::log.info "Enabling AirSane debug logging"
  airsane_args+=("--debug=true")
fi

if [ -n "${INTERFACE}" ]; then
  airsane_args+=("--interface=${INTERFACE}")
fi

if [ -n "${ANNOUNCE_BASE_URL}" ]; then
  airsane_args+=("--announce-base-url=${ANNOUNCE_BASE_URL}")
fi

bashio::log.info "Enumerating SANE scanners"
scanimage -L || bashio::log.warning "scanimage -L did not report any scanners"

bashio::log.info "Starting airsaned"
exec airsaned "${airsane_args[@]}"
