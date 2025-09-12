#!/usr/bin/env bash

# Enable Nvidia GPU support if detected
if which nvidia-smi; then
  export LIBGL_KOPPER_DRI2=1
  export MESA_LOADER_DRIVER_OVERRIDE=zink
  export GALLIUM_DRIVER=zink
fi

# Use a default resolution if unset
if [ -z ${RESOLUTION+x} ]; then
  RESOLUTION="1100x725"
fi
if [[ ${RESOLUTION} != "1100x725" ]]; then
  sudo sed -i 's/resize=remote/resize=scale/g' /kclient/public/index.html
fi
/usr/bin/openbox-session