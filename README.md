# BaiduNetdisk-Docker
<img src="https://raw.githubusercontent.com/YuCat-OVO/BaiduNetdisk-Docker/main/docs/baidunetdisk.png" style="width: 120px">

一款基于 [Linuxserver.io](https://www.linuxserver.io/) 的 [KasmVNC 基础镜像](https://github.com/linuxserver/docker-baseimage-kasmvnc)以及百度网盘官方客户端的 Docker 镜像，支持 amd64 和 arm64 架构。

## 镜像设置

该镜像部署了百度网盘桌面应用程序，并通过浏览器中的 KasmVNC 服务器提供其界面。该接口位于 `http://your-ip:8080` 或者 `https://your-ip:8181`。

默认情况下，主 GUI 没有设置密码。可选环境变量 `PASSWORD` 将允许为用户 `abc` 设置 http auth 密码。

### 所有基于 KasmVNC 的 GUI 容器中的选项 

该容器基于 [Docker Baseimage KasmVNC](https://github.com/linuxserver/docker-baseimage-kasmvnc)，这意味着有额外的环境变量和运行配置来启用或禁用特定功能。

#### 可选环境变量 

|     Variable      | Description                                                                                                                                                                                               |
| :---------------: | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
|    CUSTOM_PORT    | 容器侦听 http 的内部端口（如果需要更改默认的 8080 端口）。                                                                                                                                                |
| CUSTOM_HTTPS_PORT | 容器侦听 https 的内部端口（如果需要更改默认的 8181 端口）。                                                                                                                                               |
|    CUSTOM_USER    | HTTP 基本身份验证用户名，默认为 abc。                                                                                                                                                                     |
|     PASSWORD      | HTTP 基本身份验证密码，默认为 abc。如果未设置，则不会进行身份验证                                                                                                                                         |
|     SUBFOLDER     | 应用程序的 subfolder 参数（如果为容器运行了子文件夹反向代理），需要使用两个斜线包裹 例如： `/subfolder/`                                                                                                  |
|       TITLE       | Web 浏览器上显示的页面标题，默认为 “KasmVNC Client”。                                                                                                                                                     |
|      FM_HOME      | 这是文件管理器的主目录（默认主目录），默认为“/config”。                                                                                                                                                   |
|   START_DOCKER    | 如果设置为 false，具有特权的容器将不会自动启动 DinD Docker 设置。                                                                                                                                         |
|      DRINODE      | 如果在 /dev/dri 中挂载了支持硬件加速的 GPU 设备（详见：[DRI3 GPU Acceleration](https://www.kasmweb.com/kasmvnc/docs/master/gpu_acceleration.html)），这个变量允许您指定设备，例如： `/dev/dri/renderD128` |
|      LC_ALL       | 设置容器中运行的语言，例如：`zh_CN.UTF-8` `en_US.UTF-8`                                                                                                                                                   |
|     NO_DECOR      | 如果设置，应用程序将在没有窗口边框的情况下运行，以用作 PWA。                                                                                                                                              |
|      NO_FULL      | 使用 openbox 时不要自动全屏应用程序。                                                                                                                                                                     |

#### 可选的运行配置

|                    Variable                    | Description                                                                                                                                                                      |
| :--------------------------------------------: | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
|                 `--privileged`                 | 将在容器内启动 Docker in Docker (DinD) 设置，以便在隔离环境中使用 docker。为了提高性能，可以将容器内的 Docker 目录挂载到主机，例如：-v /home/user/docker-data:/var/lib/docker 。 |
| `-v /var/run/docker.sock:/var/run/docker.sock` | 安装在主机的 Docker 套接字中，以通过 CLI 与其交互或使用支持 Docker 的应用程序。                                                                                                  |
|          `--device /dev/dri:/dev/dri`          | 将 GPU 安装到容器中，这可以与 `DRINODE` 环境变量结合使用，以利用主机显卡来实现 GPU 加速应用程序。仅支持开源驱动程序，例如：（Intel、AMDGPU、Radeon、ATI、Nouveau）               |

### 无损模式

通过将流质量预设更改为“Extreme”，该容器能够以高帧速率向您的 Web 浏览器提供真正的无损图像，更多信息请参见[此处](https://www.kasmweb.com/docs/latest/how_to/lossless.html#technical-background)。为了从非 localhost 端点使用此模式，需要使用 8181 上的 HTTPS 端口。如果使用端口 8080 的反向代理，则需要按照[此处](https://github.com/linuxserver/docker-baseimage-kasmvnc#lossless)所述设置特定标头。.

## 如何部署

为了帮助您开始从此镜像创建容器，您可以使用 docker-compose 或 docker cli。

### Docker 部署：

#### docker-compose (推荐, [点击这里查看更多信息](https://docs.linuxserver.io/general/docker-compose))

```yaml
---
services:
  baidunetdisk:
    image: docker.io/yucatovo/baidunetdisk-docker:latest
    container_name: baidunetdisk
    security_opt:
      - seccomp:unconfined #可选
    environment:
      - PUID=1000
      - PGID=1000
      - TZ=Asia/Shanghai
      - PASSWORD= #可选
      - CLI_ARGS= #可选
    volumes:
      - /配置文件位置:/config/
      - /下载位置:/config/baidunetdiskdownload
    ports:
      - 8080:8080
      - 8181:8181
    restart: unless-stopped
```

#### docker CLI ([点击这里查看更多信息](https://docs.docker.com/engine/reference/commandline/cli/))

```bash
docker run -d \
  --name=baidunetdisk \
  --security-opt seccomp=unconfined `#可选` \
  -e PUID=1000 \
  -e PGID=1000 \
  -e TZ=Asia/Shanghai \
  -e PASSWORD= `#可选` \
  -e CLI_ARGS= `#可选` \
  -p 8080:8080 \
  -p 8181:8181 \
  -v /配置文件位置:/config \
  -v /下载位置:/config/baidunetdiskdownload \
  --restart unless-stopped \
  docker.io/yucatovo/baidunetdisk-docker:latest
```

### Podman 部署:
#### CLI
```shell
podman run -d \
  --name=baidunetdisk \
  -e PUID=1000 \
  -e PGID=1000 \
  -e TZ=Asia/Shanghai \
  -e PASSWORD= `#可选` \
  -e CLI_ARGS= `#可选` \
  -p 8080:8080 \
  -p 8181:8181 \
  -p 8081:8081 \
  -v /配置文件位置:/config \
  -v /下载位置:/config/baidunetdiskdownload \
  --restart unless-stopped \
  docker.io/yucatovo/baidunetdisk-docker:latest
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
          image: docker.io/yucatovo/baidunetdisk-docker:latest
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
            - name: DRINODE # 可选
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

### 反代示例
#### Nginx
```
server {
    listen 443 ssl;
    listen [::]:443 ssl;
    http2 on;
    server_name 主机;

    # Allow big files
    client_max_body_size 128M;

    # SSL
    ssl_certificate /your/cert.pem;
    ssl_certificate_key /your/key.pem;
    ssl_session_cache shared:SSL:50m;
    ssl_session_timeout 4h;

    # Specify cipher
    ssl_protocols TLSv1.2 TLSv1.3;
    # 卡拉搜索推荐打开以加速 但是密钥轮换带来的加速并不明显 所以让客户端自行选择
    ssl_prefer_server_ciphers off;
    # 卡拉搜索推荐的列表:
    # ssl_ciphers 'EECDH+AESGCM:EDH+AESGCM:AES256+EECDH:AES256+EDH';
    # Mozilla中级推荐的列表:
    # ssl_ciphers 'ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-CHACHA20-POLY1305:ECDHE-RSA-CHACHA20-POLY1305:DHE-RSA-AES128-GCM-SHA256:DHE-RSA-AES256-GCM-SHA384:DHE-RSA-CHACHA20-POLY1305';
    ssl_ciphers 'ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-CHACHA20-POLY1305:ECDHE-RSA-CHACHA20-POLY1305';
    # 关闭无法使用前向加密的功能
    # 详见 https://github.com/mozilla/server-side-tls/issues/135 https://www.imperialviolet.org/2013/06/27/botchingpfs.html
    ssl_session_tickets off;

    # OCSP
    ssl_stapling on;
    ssl_stapling_verify on;
    ssl_trusted_certificate /your/cert.pem;

    # To serve smaller requests (json/html/images etc) smaller ssl_buffer_size reduces latency but adds overhead
    # larger value decreases overhead but adds latency. Thus if TTFB is critical, use a smaller value (<=4K). See:
    # https://github.com/igrigorik/istlsfastyet.com/issues/63
    ssl_buffer_size 4k;

    location / {
        # 自己判断需要填写的后端地址
        set $baidunetdisk baidunetdisk;
        proxy_pass https://$baidunetdisk:8181;

        # 应用Wiki的配置
        # https://kasmweb.com/docs/latest/how_to/reverse_proxy.html
        # The following configurations must be configured when proxying to Kasm Workspaces
        # WebSocket Support
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";

        # Host and X headers
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        # Connectivity Options
        proxy_http_version 1.1;
        proxy_read_timeout 1800s;
        proxy_send_timeout 1800s;
        proxy_connect_timeout 1800s;
        proxy_buffering off;

        # Allow large requests to support file uploads to sessions
        client_max_body_size 10M;
        
        # Lossless 
        # https://github.com/linuxserver/docker-baseimage-kasmvnc
        add_header 'Cross-Origin-Embedder-Policy' 'require-corp';
        add_header 'Cross-Origin-Opener-Policy' 'same-origin';
        add_header 'Cross-Origin-Resource-Policy' 'same-site';
    }
}

```

## 注意事项
- KasmVNC 对于 Firefox 的支持不够好，推荐使用 Chromium 作为核心的浏览器获得最佳体验（比如 KasmVNC 的无缝剪贴板）。
- Podman 如果需要启用硬件加速，可能需要往 `/etc/containers/containers.conf.d/` 添加配置（详见：[containers.conf.5](https://github.com/containers/common/blob/main/docs/containers.conf.5.md)）：
```
 [containers]
 devices = ["/dev/dri/card1:rwm","/dev/dri/renderD128:rwm"]
 ```
- 如果遇到 `Failed to close file descriptor for child process (Operation not permitted)` 的错误，请使用 `--security-opt seccomp=unconfined` 启动（[来源](https://gist.github.com/nathabonfim59/b088db8752673e1e7acace8806390242)），可能会有安全问题。
- Linuxserver.io 镜像不设置 `PUID` 和 `PGID` 变量的时候会默认使用 `911` 作为运行用户和组 ID，请确认用户权限正确。
- 由于本人手上并没有可以进行测试的 arm64 设备，所以对于 arm64 的支持可能有不足。如果您在使用的时候遇到了问题，可以直接下载百度网盘[Linux版本](https://pkg-ant.baidu.com/issue/netdisk/LinuxGuanjia/4.17.7/baidunetdisk_4.17.7_amd64.deb)或者尝试使用其他大佬所编写的镜像 [[eMUQI/baidunetdisk-arm64-vnc](https://github.com/eMUQI/baidunetdisk-arm64-vnc)] [[gshang2017/docker](https://github.com/gshang2017/docker)] 查看是否能够正常运行。

## 感谢以下项目：
- [KasmVNC Base Images from LinuxServer](https://github.com/linuxserver/docker-baseimage-kasmvnc)
- [eMUQI/baidunetdisk-arm64-vnc](https://github.com/eMUQI/baidunetdisk-arm64-vnc)
- [gshang2017/docker](https://github.com/gshang2017/docker)

## 截图
![arm64](https://raw.githubusercontent.com/YuCat-OVO/BaiduNetdisk-Docker/main/docs/arm.png)

## 其他
同时也感谢参与反馈与测试的所有人
