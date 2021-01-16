ROOT=
USER=
REMOTE_PATH=/home/${USER}/${ROOT}
IP=
PATH_TEST=test
ESP_IMAGE=esp32-idf4-20200902-v1.13.bin
ESP_IMAGE_URL=https://micropython.org/resources/firmware/${ESP_IMAGE}
export RSHELL_PORT?=/dev/ttyUSB0

rase:
	esptool.py --chip esp32 --port ${RSHELL_PORT} erase_flash

image:
	(test ! -f ${ESP_IMAGE} && wget ${ESP_IMAGE_URL}) || true
	esptool.py --chip esp32 --port ${RSHELL_PORT} --baud 460800 write_flash -z 0x1000 ${ESP_IMAGE}

rsync: clean
	rshell rsync src /pyboard

repl:
	rshell repl

clean:
	find . -type d -name __pycache__ -prune -exec rm -rf {} \;

install:
	python setup.py install

test:
	PYTHONPATH=src pytest

test-dev:
	PYTHONPATH=src ptw --poll

.PHONY: test
	