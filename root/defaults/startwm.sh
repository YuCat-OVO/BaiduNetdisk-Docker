#!/bin/bash

# 启动openbox会话
cp /defaults/autostart "$HOME/.config/openbox/"
if [ -n "${RESOLUTION}" ]; then
  sudo sed -i 's/"resize": "remote"/"resize": "scale"/g' /kclient/public/config.json
fi
/usr/bin/openbox-session