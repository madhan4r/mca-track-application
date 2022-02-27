#! /usr/bin/env sh

docker stack ps ${STACK_NAME} > /dev/null

if [ $? -eq 0 ]
then
  echo "removing the stack"
  docker stack rm ${STACK_NAME}
  EXIT_STATUS="0"
  while [  $EXIT_STATUS -eq 0 ]; do
     echo The EXIT_STATUS is $EXIT_STATUS
     docker stack ps ${STACK_NAME} > /dev/nnull
     let EXIT_STATUS=$?
     echo "stack still running"
     sleep 5
  done
  echo "stack removed"
else
  echo "stack not running"
fi

# Exit in case of error
set -e

DOMAIN=${DOMAIN} \
TRAEFIK_TAG=${TRAEFIK_TAG} \
STACK_NAME=${STACK_NAME} \
TAG=${TAG} \
docker-compose \
-f docker-compose.shared.admin.yml \
-f docker-compose.shared.base-images.yml \
-f docker-compose.shared.depends.yml \
-f docker-compose.shared.env.yml \
-f docker-compose.deploy.command.yml \
-f docker-compose.deploy.images.yml \
-f docker-compose.deploy.labels.yml \
-f docker-compose.deploy.networks.yml \
-f docker-compose.deploy.volumes-placement.yml \
config > docker-stack.yml

docker-auto-labels docker-stack.yml


docker stack deploy -c docker-stack.yml --with-registry-auth ${STACK_NAME}