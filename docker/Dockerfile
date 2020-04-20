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

COPY entrypoint.bash /usr/local/bin/entrypoint.bash
COPY solver.py /usr/local/bin/solver.py

ENTRYPOINT ["/usr/local/bin/entrypoint.bash"]
