#!/bin/sh

IMAGE=$(sirius docker_image_name | head -n 1)

docker tag -f ${IMAGE} docker.neg/${IMAGE}

docker push docker.neg/${IMAGE}

sirius docker_deploy:netscalersentinel,netscaler_sentinel:0.0.1,server=scdfis01,ports="9000;8080"
