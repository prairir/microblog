# build the latest image of the updated code
docker build -t microblog:latest .
echo "#######Image built"

# # run the docker container on local 5000.
docker run --name microblog -d -p 5000:5000 --rm microblog:latest

echo "#######Container running"

