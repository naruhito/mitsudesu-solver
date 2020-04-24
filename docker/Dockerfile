FROM python:3.7-slim-stretch

RUN apt update && apt install -y \
  xvfb \
  x11vnc \
  firefox-esr \
  && rm -rf /var/lib/apt/lists/*

RUN python -m pip install \
  opencv-python \
  pillow \
  numpy \
  python-xlib

COPY solver.py /usr/local/bin/solver.py
COPY entrypoint.bash /usr/local/bin/entrypoint.bash
ENTRYPOINT ["entrypoint.bash"]
