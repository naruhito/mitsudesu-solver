#!/bin/bash
set -e

export DISPLAY=:1
readonly URL="http://gamingchahan.com/mitsudesu/"

function main() {
  create-display
  print-help
  run-solver
}

function create-display() {
  local -r W=1024
  local -r H=768
  local -r D=24
  Xvfb ${DISPLAY} -screen 0 ${W}x${H}x${D} &
  x11vnc -display ${DISPLAY} -listen 0.0.0.0 -forever -xkb -shared -nopw -bg
  firefox ${URL} &
}

function print-help() {
  local -r IP=$(hostname -i)
  cat <<EOS

------------------

Successfully started up.

VNC connection is available:

${IP}:5900

Client applications can be downloaded here:
https://www.realvnc.com/en/connect/download/viewer/

------------------

EOS
}

function run-solver() {
  python /mitsudesu/solver.py &
  PID=$!
  trap "kill -9 ${PID}" 2
  while kill -0 ${PID}; do
    sleep 1
  done
}

main
