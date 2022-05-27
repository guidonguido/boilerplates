#!/bin/bash

LOG_FILE=./update_images_logs/update_log$(date +%Y_%m_%d__%H:%M:%S).txt

touch $LOG_FILE

chown guido:guido $LOG_FILE

for dcdir in ./*; do 
  if [ -f "${dcdir}/docker-compose.yml" ]; then 
    echo "${dcdir}/docker-compose.yml exists, updating all images" | tee -a $LOG_FILE
    echo "docker-compose -f ${dcdir}/docker-compose.yml pull #called" | tee -a $LOG_FILE

    sudo docker-compose -f ${dcdir}/docker-compose.yml pull 2&>1 | tee -a $LOG_FILE

    echo "docker-compose -f ${dcdir}/docker-compose.yml up -d #called" | tee -a $LOG_FILE

    sudo docker-compose -f ${dcdir}/docker-compose.yml up -d 2&>1 | tee -a $LOG_FILE

    echo "DONE for file ${dcdir}/docker-compose.yml \n\n" | tee -a $LOG_FILE
  fi
done

echo "Images Update is done" | tee -a $LOG_FILE
