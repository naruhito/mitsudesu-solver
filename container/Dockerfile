FROM python:3.7-slim-stretch

RUN apt-get update && apt-get install --no-install-recommends -y \
  xvfb \
  x11vnc \
  firefox-esr \
  && rm -rf /var/lib/apt/lists/*

RUN python -m pip install \
  opencv-python \
  pillow \
  numpy \
  python-xlib

COPY python /mitsudesu
COPY entrypoint.bash /usr/local/bin/entrypoint.bash
ENTRYPOINT ["entrypoint.bash"]
