# IOT
Gateway for IOT application using Docker containers: timescaleDB, node-red, Grafana

## To-do:
1. Define phone numbers in database.
2. Send Whatsapp to list of phone numbers.
3. Connect to DGA.
4. Phone numbers and API key on environment variables?
5. Programmatically set user id on compose.yaml file for Grafana.
6. Create database structure automatically when initializing Timescale container.

## Setting up the gateway
### Get project repository from Github
1. Use pi as default user, then go to home directory
2. Clone repository: ```git clone https://github.com/r9hino/IOT-Docker-Script.git```
3. Change folder name from IOT-Docker-Script to IOT: ```mv IOT-Docker-Script IOT```

### Containers initialization with docker compose
1. Go to project folder: ```cd /home/pi/IOT```
2. Add the .env file.
3. Check ownership of node-red/data folder on server side, it must be 1000:1000: ```sudo chown -R 1000:1000 path/to/your/node-red/data```
4. Check user id on linux and use the same id for user in the Grafana section of compose.yaml file: ```id -u```
5. Build custom image from Dockerfile and initialize all containers: ```docker compose up -d```
6. Additional checks:
    - Check that Grafana has defined userid to 1000.
    - [Add login to node-red](https://nodered.org/docs/user-guide/runtime/securing-node-red):
        * Enter node-red cointainer: ```docker exec -it nodered /bin/bash```
        * Edit /data/settings.js file: ```nano /data/settings.js```
        * Add user and hashed password in the section "adminAuth". For hashing the password, inside the container, use: ```node-red admin hash-pw```
7. Install python environment and libraries (only if they aren't installed):
    - sudo apt install -y python3-virtualenv
    - Create virtual environment: ```virtualenv /home/pi/IOT/.venv```
    - Activate virtual environment: ```source .venv/bin/activate```
    - Install python libraries on this virtual environment: ```pip3 install adafruit-circuitpython-ads1x15 RPi.GPIO paho-mqtt```
    - Deactivate virtual environment: ```diactivate```
8. Add python script to system services:
    - Copy service: cp /home/pi/IOT/python_i2c_mqtt.service /etc/systemd/system/python_i2c_mqtt.service
    - Initialize service:
        * sudo systemctl daemon-reload
        * sudo systemctl enable python_i2c_mqtt.service
        * sudo systemctl start python_i2c_mqtt.service
        * sudo systemctl status python_i2c_mqtt.service
        * journalctl -u python_i2c_mqtt.service


### Updating images and containers in docker
1. Stop containers: ```docker compose down```
2. Remove images: ```docker images``` & ```docker rmi id```
3. docker pull new images: ```docker pull image```
4. Run containers: ```docker compose up -d```

## Github commands
1. Clone repository: ```git clone -b main https://github.com/r9hino/ACM.git```
2. Github commit:
    * ```git add .```
    * ```git commit -m "Description"```
    * ```git push origin main```

## Backup Ubuntu OS while running
### Mount storage device
1. Create mounting point: ```mkdir /mnt/SD```
2. Check if device was detected and what is it partition: ```lsblk```
3. Mount the device: ```sudo mount /dev/sda1 /mnt/SD```
4. Check if device was correctly mounted: ```lsblk```
### Make an Ubuntu image and store it on the mounted device
1. Download [PiSafe](https://github.com/RichardMidnight/pi-safe):
    * ```wget https://raw.githubusercontent.com/RichardMidnight/pi-safe/main/pisafe -O pisafe```
    * ```bash pisafe install```
2. Stop all processes:
    * ```pm2 stop all```
    * ```cd /home/pi/Code/ACM/Docker```
    * ```docker-compose -f docker-nodered-influxdb-pigpiod.yml --env-file ./../.env stop```
3. Run PiSafe: ```pisafe```
4. On Settings turn off "hide root device"
5. Go to Backup
6. Choose Ubuntu OS partition
7. Set destination path to /mnt/SD
8. After finishing the image creation, unmount device: ```sudo umount /mnt/SD```
9. Check unmounting: ```lsblk```
