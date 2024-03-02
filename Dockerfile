# syntax=docker/dockerfile:1

FROM ghcr.io/linuxserver/baseimage-kasmvnc:debianbookworm

# set version label
ARG BUILD_DATE
ARG VERSION
ARG TARGETPLATFORM
LABEL build_version="version:- ${VERSION} Build-date:- ${BUILD_DATE}"
LABEL maintainer="YuCat-OVO"
LABEL org.opencontainers.image.source="https://github.com/linuxserver/docker-baseimage-kasmvnc"

ENV \
    CUSTOM_PORT="8080" \
    CUSTOM_HTTPS_PORT="8181" \
    HOME="/config" \
    TITLE="Baidunetdisk"

COPY url.json /tmp/

RUN \
    TARGETPLATFORM=${TARGETPLATFORM:-linux/amd64} && \
    echo "**** arch: ${TARGETPLATFORM} ****" && \
    echo "**** add icon ****" && \
    curl -o \
    /kclient/public/icon.png \
    https://raw.githubusercontent.com/YuCat-OVO/BaiduNetdisk-Docker/master/docs/baidunetdisk.png && \
    echo "**** fix trusted.gpg ****" && \
    mv /etc/apt/trusted.gpg /etc/apt/trusted.gpg.d/docker.gpg && \
    echo "**** install runtime packages ****" && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
    wget \
    fonts-wqy-microhei \
    fonts-wqy-zenhei \
    desktop-file-utils && \
    echo "**** install BaiduNetdisk ****" && \
    if [ "${TARGETPLATFORM}" == "linux/amd64" ]; then \
    echo "**** ${TARGETPLATFORM}, reading from url.json ****"; \
    BAIDUNETDISK_VERSION=$(jq -r ".[-2]" /tmp/url.json); \
    BAIDUNETDISK_URL=$(jq -r ".[-2]" /tmp/url.json); \
    elif [ "${TARGETPLATFORM}" == "linux/arm64" ]; then \
    echo "**** ${TARGETPLATFORM}, reading from url.json ****"; \
    BAIDUNETDISK_VERSION=$(jq -r ".[-1]" /tmp/url.json); \
    BAIDUNETDISK_URL=$(jq -r ".[-1]" /tmp/url.json); \
    else \
    echo "**** err, use default url ****" && \
    BAIDUNETDISK_URL="https://issuepcdn.baidupcs.com/issue/netdisk/LinuxGuanjia/4.17.7/baidunetdisk_4.17.7_amd64.deb"; \
    fi && \
    echo "***** Getting ${BAIDUNETDISK_URL} ****" && \
    curl -o \
    /tmp/baidunetdisk.deb -L \
    "$BAIDUNETDISK_URL" && \
    for i in \
    $(dpkg -I /tmp/baidunetdisk.deb | grep "Depends" | cut -c11- | awk -F ', ' '{ for(i=1; i<=NF; i++) print $i }'); \
    do \
    if [ -n "$(dpkg -l | grep ^ii | grep $i)" ]; \
    then \ 
    echo "${i} installed,skip"; \
    else \
    apt-get install -y --no-install-recommends ${i}; \
    fi \
    done && \
    dpkg -i /tmp/baidunetdisk.deb && \
    echo "**** cleanup ****" && \
    apt-get clean && \
    rm -rf \
    /tmp/* \
    /var/lib/apt/lists/* \
    /var/tmp/*

# add local files
COPY root/ /