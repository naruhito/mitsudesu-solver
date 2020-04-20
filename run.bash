#!/bin/bash
set -eu

IMAGE="mitsudesu-solver:latest"
NAME="mitsudesu-solver"

for PROG in "docker" "vncviewer"; do
  if ! which ${PROG} > /dev/null 2>&1; then
    echo "${PROG} is not installed."
    exit 1
  fi
done

CONTAINER=$(docker run -d --rm --name ${NAME} -h ${NAME} ${IMAGE} -v $PWD/docker:/repo)

trap "docker rm -f ${CONTAINER}" 0 2 3 15

while ! docker exec ${CONTAINER} ps | grep x11vnc > /dev/null 2>&1; do
  docker logs ${CONTAINER}
done

IP=$(docker inspect ${CONTAINER} | grep -E --color=never "IPAddress.+172" | cut -d\" -f4 | sort | uniq)

vncviewer ${IP}
