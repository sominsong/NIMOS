#init/setup.sh
sleep 5 | echo "Waiting for the servers to start..."
mongo mongodb://localhost:27017 ./init/setReplication.js