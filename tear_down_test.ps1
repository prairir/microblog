# stop the container
docker stop $(docker ps -q --filter name=microblog)
echo "#######Container microblog stopped"

# remove the microblog image specifically (do not want to remove the jenkins image by accident)
docker image prune -af --filter "label!=org.opencontainers.image.vendor=Jenkins project"

echo "#######Image microblog pruned"

