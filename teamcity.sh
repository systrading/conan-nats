#!/bin/bash


image=821543356141.dkr.ecr.ap-southeast-2.amazonaws.com/symbio2-devtools:latest

eval $(aws ecr get-login --profile=prod --region ap-southeast-2 | sed -e 's/-e none//g')

docker pull ${image}

docker run \
  -v${PWD}:/app:Z \
  ${image} \
  ./package.sh
