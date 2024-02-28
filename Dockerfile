# syntax=docker/dockerfile:1

FROM ghcr.io/linuxserver/baseimage-kasmvnc:debianbookworm

# set version label
ARG BUILD_DATE
ARG VERSION
ARG BAIDUNETDISK_VERSION
LABEL build_version="version:- ${VERSION} Build-date:- ${BUILD_DATE}"
# LABEL maintainer=""

# https://issuepcdn.baidupcs.com/issue/netdisk/LinuxGuanjia/4.17.7/baidunetdisk_4.17.7_amd64.deb

ENV \
    CUSTOM_PORT="8080" \
    CUSTOM_HTTPS_PORT="8181" \
    HOME="/config" \
    TITLE="Baidunetdisk"

RUN \
    echo "**** add icon ****" && \
    curl -o \
    /kclient/public/icon.png \
    https://raw.githubusercontent.com/YuCat-OVO/BaiduNetdisk-Docker/master/docs/baidunetdisk.png && \
    echo "**** install runtime packages ****" && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
    wget \
    fonts-wqy-microhei \
    fonts-wqy-zenhei \
    libgtk-3-0 \
    libnotify4 \
    libatspi2.0-0 \
    libsecret-1-0 \
    desktop-file-utils && \
    echo "**** install BaiduNetdisk ****" && \
    if [ -z ${BAIDUNETDISK_VERSION+x} ]; then \
    BAIDUNETDISK_URL="https://issuepcdn.baidupcs.com/issue/netdisk/LinuxGuanjia/4.17.7/baidunetdisk_4.17.7_amd64.deb"; \
    else \
    BAIDUNETDISK_URL="https://issuepcdn.baidupcs.com/issue/netdisk/LinuxGuanjia/${BAIDUNETDISK_VERSION}/baidunetdisk_${BAIDUNETDISK_VERSION}_amd64.deb"; \
    fi && \
    echo "***** Getting $BAIDUNETDISK_URL ****" && \
    curl -o \
    /tmp/baidunetdisk.deb -L \
    "$BAIDUNETDISK_URL" && \
    dpkg -i /tmp/baidunetdisk.deb && \
    echo "**** cleanup ****" && \
    apt-get clean && \
    rm -rf \
    /tmp/* \
    /var/lib/apt/lists/* \
    /var/tmp/*

# add local files
COPY root/ /