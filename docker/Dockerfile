FROM python:3.7-slim-stretch

RUN apt update && apt install -y \
  xvfb \
  x11vnc \
  firefox-esr

RUN python -m pip install \
  opencv-python \
  pillow \
  numpy \
  python-xlib

COPY python /mitsudesu
COPY entrypoint.bash /usr/local/bin/entrypoint.bash
ENTRYPOINT ["entrypoint.bash"]
