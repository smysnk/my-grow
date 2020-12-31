ROOT=mygrow
REMOTE_PATH=/home/josh/${ROOT}
IP=192.168.0.108
USER=josh
export RSHELL_PORT?=/dev/ttyUSB0
export PYTHONPATH=.

sync: clean
	rsync . ${USER}@${IP}:${REMOTE_PATH} -r --verbose --exclude=node_modules --exclude=.git --delete

remote: sync
	ssh -t ${USER}@${IP} "cd ${REMOTE_PATH} && make ${COMMAND}"

erase:
	esptool.py --chip esp32 --port ${RSHELL_PORT} erase_flash

image:
	esptool.py --chip esp32 --port ${RSHELL_PORT} --baud 460800 write_flash -z 0x1000 esp32-idf4-20200902-v1.13.bin

rsync: clean
	rshell rsync root /pyboard
	rshell rsync src /pyboard/src

repl:
	rshell repl

clean:
	find . -type d -name __pycache__ -prune -exec rm -rf {} \;

install:
	python setup.py install

datadog: install
	python cli.py

test:
	cd src && pytest

test-dev:
	cd src && ptw --poll
