FROM python:3.8-slim-buster

RUN apt update && apt install -y \
  xvfb \
  x11vnc \
  firefox-esr \
  python3-opencv \
  procps

RUN python3 -m pip install \
  numpy \
  opencv-python \
  pillow \
  python-xlib

ENTRYPOINT ["/repo/entrypoint.bash"]
