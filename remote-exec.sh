#!/bin/sh -v

export ROOT=mygrow
export RSHELL_PORT=/dev/ttyUSB0
export REMOTE_PATH=/home/josh/${ROOT}
export IP=192.168.0.108
#ssh ${USER}@${IP} mkdir -p ${REMOTE_PATH}
rsync . ${USER}@${IP}:${REMOTE_PATH} -r --verbose --exclude=node_modules --exclude=.git --delete
ssh -t ${USER}@${IP} "cd ${REMOTE_PATH} && RSHELL_PORT=${RSHELL_PORT} rshell rsync src /pyboard"
ssh -t ${USER}@${IP} "cd ${REMOTE_PATH} && RSHELL_PORT=${RSHELL_PORT} rshell repl"
