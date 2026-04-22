#!/bin/bash
set -e

docker-compose up -d

sleep 10

curl --fail http://localhost:8000/health

#docker-compose down
