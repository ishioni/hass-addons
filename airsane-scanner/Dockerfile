FROM ghcr.io/hassio-addons/debian-base:9.3.0 AS builder

ARG AIRSANE_REF=v.0.4.10
ARG BRSCAN_REF=v1.0.1

LABEL io.hass.version="1.0" io.hass.type="addon" io.hass.arch="aarch64|amd64"

SHELL ["/bin/bash", "-o", "pipefail", "-c"]

RUN apt update \
    && apt install -y --no-install-recommends \
        build-essential \
        ca-certificates \
        cmake \
        curl \
        libavahi-client-dev \
        libjpeg-dev \
        libncurses-dev \
        libpng-dev \
        libsane-dev \
        libusb-1.0-0-dev \
        libusb-dev \
        patch \
        pkg-config \
        tar \
    && rm -rf /var/lib/apt/lists/*

COPY patches /tmp/patches

RUN mkdir -p /tmp/src \
    && curl -L "https://github.com/dmikushin/brscan/archive/refs/tags/${BRSCAN_REF}.tar.gz" -o /tmp/src/brscan.tar.gz \
    && tar -xzf /tmp/src/brscan.tar.gz -C /tmp/src \
    && mv "/tmp/src/brscan-${BRSCAN_REF#v}" /tmp/brscan \
    && for patch_file in /tmp/patches/brscan/*.patch; do \
        [ -e "$patch_file" ] || continue; \
        patch -d /tmp/brscan -p1 < "$patch_file"; \
      done \
    && mkdir -p /tmp/brscan/build \
    && cmake -S /tmp/brscan -B /tmp/brscan/build -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX=/usr \
    && cmake --build /tmp/brscan/build -j"$(nproc)" \
    && cmake --install /tmp/brscan/build \
    && printf '/usr/lib/sane\n' > /etc/ld.so.conf.d/brscan-sane.conf \
    && rm -rf /tmp/brscan /tmp/src

RUN mkdir -p /tmp/src \
    && curl -L "https://github.com/SimulPiscator/AirSane/archive/refs/tags/${AIRSANE_REF}.tar.gz" -o /tmp/src/airsane.tar.gz \
    && tar -xzf /tmp/src/airsane.tar.gz -C /tmp/src \
    && mv /tmp/src/AirSane-* /tmp/AirSane \
    && cmake -S /tmp/AirSane -B /tmp/AirSane-build -DCMAKE_BUILD_TYPE=Release \
    && cmake --build /tmp/AirSane-build -j"$(nproc)" \
    && cmake --install /tmp/AirSane-build \
    && rm -rf /tmp/AirSane /tmp/AirSane-build /tmp/src /tmp/patches

FROM ghcr.io/hassio-addons/debian-base:9.3.0

LABEL io.hass.version="1.0" io.hass.type="addon" io.hass.arch="aarch64|amd64"

SHELL ["/bin/bash", "-o", "pipefail", "-c"]

RUN apt update \
    && apt install -y --no-install-recommends \
        avahi-daemon \
        ca-certificates \
        dbus \
        jq \
        libnss-mdns \
        libusb-0.1-4 \
        libusb-1.0-0 \
        python3 \
        sane-utils \
    && rm -rf /var/lib/apt/lists/*

COPY --from=builder /usr/local/bin/airsaned /usr/local/bin/airsaned
COPY --from=builder /usr/lib/sane/libsane-brother.so.1 /usr/lib/sane/libsane-brother.so.1
COPY --from=builder /usr/share/sane/brother /usr/share/sane/brother
COPY --from=builder /etc/ld.so.conf.d/brscan-sane.conf /etc/ld.so.conf.d/brscan-sane.conf

COPY rootfs /

RUN chmod a+x \
    /run.sh \
    /usr/local/bin/render-config.py \
    /etc/s6-overlay/s6-rc.d/initialization/up \
    /etc/s6-overlay/s6-rc.d/dbus-daemon/run \
    /etc/s6-overlay/s6-rc.d/avahi-daemon/run \
    && ldconfig

EXPOSE 8090

CMD ["/run.sh"]