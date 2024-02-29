# BaiduNetdisk-Docker

一款基于 [Linuxserver.io](https://www.linuxserver.io/) 的 [KasmVNC 基础镜像](https://github.com/linuxserver/docker-baseimage-kasmvnc)以及百度网盘官方客户端的 Docker 镜像

## 部署方式

### Docker 部署:
```shell
docker run -d \
       --name baidunetdisk \
       -p 8080:8080 \
       -p 8181:8181 \
       -v /配置文件位置:/config \
       -v /下载位置:/config/baidunetdiskdownload \
       --restart unless-stopped \
       ghcr.io/yucat-ovo/baidunetdisk-docker:latest
```

### Podman 部署:
#### CLI
```shell
podman run -d \
       --name baidunetdisk \
       -p 8080:8080 \
       -p 8181:8181 \
       -v /配置文件位置:/config \
       -v /下载位置:/config/baidunetdiskdownload \
       --restart unless-stopped \
       ghcr.io/yucat-ovo/baidunetdisk-docker:latest
```
#### Deployment
```shell
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: baidunetdisk-deployment
  annotations:
    io.containers.autoupdate: registry
spec:
  replicas: 1
  selector:
    matchLabels:
      app: baidunetdisk
  template:
    metadata:
      labels:
        app: baidunetdisk
    spec:
      restartPolicy: always
      containers:
        - name: baidunetdisk
          image: ghcr.io/yucat-ovo/baidunetdisk-docker:latest
          volumeMounts:
            - name: config-path
              mountPath: /config/
            - name: download-path
              mountPath: /config/baidunetdiskdownload/
          ports:
            - containerPort: 8080
              hostPort: 8080
              protocol: TCP
            - containerPort: 8181
              hostPort: 8181
              protocol: TCP
          env:
            - name: TZ
              value: "Asia/Shanghai"
            - name: DRINODE
              value: "/dev/dri/renderD128"
      volumes:
        - name: config-path
          hostPath:
            path: /配置文件位置
            type: Directory
        - name: download-path
          hostPath:
            path: /下载位置
            type: Directory
```

## 使用方式
打开 `http://localhost:8080` 或者 `http://localhost:8080`。

注意: 目前 KasmVNC 对于 Firefox 的支持貌似有问题，推荐使用 Chrome 获得最佳体验。

## 感谢以下项目:
- [KasmVNC Base Images from LinuxServer](https://github.com/linuxserver/docker-baseimage-kasmvnc)
- [baidunetdisk-arm64-vnc](https://github.com/eMUQI/baidunetdisk-arm64-vnc)
- [gshang2017/docker](https://github.com/gshang2017/docker)