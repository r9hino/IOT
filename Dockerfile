FROM nodered/node-red
RUN npm install node-red-configurable-ping 
RUN npm install node-red-contrib-postgresql
RUN npm install node-red-contrib-s7
RUN npm install node-red-contrib-aedes
RUN npm install node-red-contrib-soap-plus
RUN npm install node-red-contrib-whatsapp-cmb
RUN npm install node-red-node-email
