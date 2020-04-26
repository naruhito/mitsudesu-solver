FROM python:3.7-slim-stretch

RUN apt-get update && apt-get install --no-install-recommends -y \
  firefox-esr \
  fluxbox \
  tigervnc-viewer \
  xvfb \
  x11vnc \
  && rm -rf /var/lib/apt/lists/*

RUN python -m pip install \
  numpy \
  opencv-python \
  pillow \
  python-xlib

COPY python /mitsudesu
COPY data /mitsudesu/data
COPY entrypoint.bash /usr/local/bin/entrypoint.bash
ENTRYPOINT ["entrypoint.bash"]
