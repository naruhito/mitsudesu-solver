#!/bin/bash
set -e

export DISPLAY=:0
export URL="http://gamingchahan.com/mitsudesu/"

function main() {
  create-display
  print-help
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

function print-help() {
  local IP=$(cat /proc/net/fib_trie | grep -B1 '/32 host' | grep 172.17 | awk '{ print $2 }' | sort | uniq)
  cat <<EOS

------------------

Successfully started up.

VNC connection is available:

${IP}:5900

Client applications are available here:
https://www.realvnc.com/en/connect/download/viewer/

------------------

EOS
}

function run-solver() {
  python /mitsudesu/solver.py
}

main
