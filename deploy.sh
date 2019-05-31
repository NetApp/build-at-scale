#!/bin/bash -e
# Deploy Script for Devops@Scale product

version=$1
docker_registry=$2

web_service_image_name="devops-at-scale:${version}"

# Tag image
docker tag $web_service_image_name $docker_registry/$web_service_image_name

# Push to private registry
docker push $docker_registry/$web_service_image_name
