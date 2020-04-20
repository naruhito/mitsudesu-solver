#!/bin/bash
set -eu

URL="http://gamingchahan.com/mitsudesu/"

DISPLAY=:0
W=1024
H=768
D=24

function main() {
  create-display
}

function create-display() {
  Xvfb ${DISPLAY} -screen 0 ${W}x${H}x${D} -listen tcp -ac &
  x11vnc -display ${DISPLAY} -listen 0.0.0.0 -forever -xkb -shared -nopw -bg
  DISPLAY=${DISPLAY} firefox ${URL}
}

function run-solver() {
  DISPLAY=${DISPLAY} python3 /usr/local/bin/solver.py
}

main
