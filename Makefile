SOURCE = ../muleAI
RPI_ADDR = pi@mule
RPI_DIR = /home/pi/.mule/
DESTINATION = ${RPI_ADDR}:${RPI_DIR}
.PHONY: sync
sync:
	rsync -avz --exclude "*egg_info*" --exclude "*__pycache__*" --exclude "*.so*" --exclude "build*" --exclude "*.log"  ${SOURCE} ${DESTINATION}
