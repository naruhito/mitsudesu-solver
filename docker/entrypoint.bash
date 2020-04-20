#!/bin/bash
set -e

export DISPLAY=:0

function main() {
  if [ -z "${URL}" ]; then
    echo "URL is empty."
    exit 1
  fi
  create-display
  run-solver
}

function create-display() {
  local W=1024
  local H=768
  local D=24
  Xvfb ${DISPLAY} -screen 0 ${W}x${H}x${D} &
  x11vnc -display ${DISPLAY} -listen 0.0.0.0 -forever -xkb -shared -nopw -bg
  firefox ${URL} &
}

function run-solver() {
  python3 /repo/solver.py
}

main
