# stop the container
docker stop $(docker ps -q --filter name=microblog) || true && docker rm $(docker ps -q --filter name=microblog) || true

# remove the microblog image specifically (do not want to remove the jenkins image by accident)
docker image prune -af --filter "label!=org.opencontainers.image.vendor=Jenkins project"