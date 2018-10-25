#!/bin/bash -x

DOCKER_SOCKET=/var/run/docker.sock
DOCKER_GROUP=docker
AIRFLOW_USER=airflow

if [ -S ${DOCKER_SOCKET} ]; then
    DOCKER_GID=$(stat -c '%g' ${DOCKER_SOCKET})
    groupadd -or -g ${DOCKER_GID} ${DOCKER_GROUP}
    usermod -aG ${DOCKER_GROUP} ${AIRFLOW_USER}
fi

# Change to regular user and run the rest of the entry point
su ${AIRFLOW_USER} -c "/usr/bin/env bash /entrypoint.sh ${@}"