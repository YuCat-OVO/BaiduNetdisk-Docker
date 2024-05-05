# syntax=docker/dockerfile:1
FROM docker.io/library/alpine:edge as download

RUN \
    sed -i 's/dl-cdn.alpinelinux.org/mirrors.lzu.edu.cn/g' /etc/apk/repositories && \
    apk update && \
    apk add wget curl jq &&\
    wget -nv $(curl 'https://yun.baidu.com/disk/cmsdata?platform=linux&page=1&num=1' | jq -r '.["list"][0]["url_1"]') -O /tmp/baidunetdisk.deb

FROM ghcr.io/linuxserver/baseimage-kasmvnc:debianbookworm-062d5346-ls56

LABEL org.opencontainers.image.source="https://github.com/YuCat-OVO/BaiduNetdisk-Docker"

ENV \
    CUSTOM_PORT="8080" \
    CUSTOM_HTTPS_PORT="8181" \
    HOME="/config" \
    TITLE="Baidunetdisk"

COPY --from=download /tmp/baidunetdisk.deb /tmp/baidunetdisk.deb
# add local files
COPY root/ /

RUN \
    sed -i "s/deb.debian.org/mirror.bfsu.edu.cn/g" /etc/apt/sources.list &&\
    sed -i "s/security.debian.org/mirror.bfsu.edu.cn/g" /etc/apt/sources.list &&\
    echo "**** fix trusted.gpg ****" && \
    mv /etc/apt/trusted.gpg /etc/apt/trusted.gpg.d/docker.gpg && \
    apt-get update -y && \
    apt-get -yy -qq install --no-install-recommends --no-install-suggests --fix-missing \
    fonts-wqy-microhei \
    fonts-wqy-zenhei \
    desktop-file-utils && \
    \
    echo "**** install BaiduNetdisk ****" && \
    for i in \
    $(dpkg -I /tmp/baidunetdisk.deb | grep "Depends" | cut -c11- | awk -F ', ' '{ for(i=1; i<=NF; i++) print $i }'); \
    do \
    if [ -n "$(dpkg -l | grep ^ii | grep $i)" ]; \
    then \ 
    echo "${i} installed,skip"; \
    else \
    apt-get -yy -qq install --no-install-recommends --no-install-suggests --fix-missing ${i}; \
    fi \
    done && \
    dpkg -i /tmp/baidunetdisk.deb && \
    chmod +x /usr/bin/mytest && \
    echo "**** cleanup ****" && \
    apt-get clean && \
    rm -rf \
    /tmp/* \
    /var/lib/apt/lists/* \
    /var/tmp/*
