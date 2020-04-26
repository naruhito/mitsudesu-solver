#!/bin/bash
set -e

readonly DISPLAYS=(:1 :2 :3)
readonly VNCPORTS=(5900 5901 5902)
readonly W=700
readonly H=750
readonly D=24
readonly URL="http://gamingchahan.com/mitsudesu/"

function main() {
  create-displays
  print-help
  run-solver
}

function create-displays() {
  for i in $(seq 0 $(expr ${#DISPLAYS[@]} - 1)); do
    local DISPLAY=${DISPLAYS[$i]}
    local VNCPORT=${VNCPORTS[$i]}
    if [ $i -eq 0 ]; then
      local WW=$(expr ${W} \* 2)
    else
      local WW=${W}
    fi
    Xvfb ${DISPLAY} -screen 0 ${WW}x${H}x${D} &
    while ! x11vnc -display ${DISPLAY} -listen 0.0.0.0 -forever -xkb -shared -nopw -bg -rfbport ${VNCPORT} > /tmp/x11vnc-${i}.log 2>&1; do
      echo "creating DISPLAY=${DISPLAY}"
      sleep 1
    done
  done
  DISPLAY=${DISPLAYS[1]} firefox ${URL} &
  DISPLAY=${DISPLAYS[0]} fluxbox > /tmp/fluxbox.log 2>&1 &
  DISPLAY=${DISPLAYS[0]} xtigervncviewer localhost::${VNCPORTS[1]} > /tmp/tiger-vncviewer-1.log 2>&1 &
  DISPLAY=${DISPLAYS[0]} xtigervncviewer localhost::${VNCPORTS[2]} > /tmp/tiger-vncviewer-2.log 2>&1  &
}

function print-help() {
  local -r IP=$(hostname -i)
  cat <<EOS

------------------

Successfully started up.

VNC connection is available:

${IP}:${VNCPORTS[0]}

Client applications can be downloaded here:
https://www.realvnc.com/en/connect/download/viewer/

------------------

EOS
}

function run-solver() {
  PYTHONPATH="/mitsudesu:${PYTHONPATH}" python -m mitsudesu.solver \
            --display-width=${W} \
            --display-height=${H} \
            --display-x11=${DISPLAYS[1]} \
            --display-debug=${DISPLAYS[2]}
  local -r PID=$!
  trap "kill -9 ${PID}" 2
  while kill -0 ${PID}; do
    sleep 1
  done
}

main
