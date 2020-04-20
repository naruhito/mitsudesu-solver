#!/bin/bash
set -e

NAME="mitsudesu-solver"
IMAGE="${NAME}:latest"

for PROG in "docker" "vncviewer"; do
  if ! which ${PROG} > /dev/null 2>&1; then
    echo "${PROG} is not installed."
    exit 1
  fi
done

if [ -z "${DISPLAY}" ]; then
  echo "DISPLAY is not available."
  exit 1
fi

CONTAINER=$(docker run -d --rm --name ${NAME} -v ${PWD}/docker:/repo ${IMAGE})

trap "docker rm -f ${CONTAINER}" 0 2 3 15

while ! docker exec ${CONTAINER} ps | grep x11vnc > /dev/null 2>&1; do
  docker logs ${CONTAINER}
  sleep 1
done

IP=$(docker inspect ${CONTAINER} | grep -E --color=never "IPAddress.+172" | cut -d\" -f4 | sort | uniq)

vncviewer ${IP}
