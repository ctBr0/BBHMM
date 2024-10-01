# BitchBetterHaveMyMoney

### Splitwise Clone

## Instructions for Docker

### Build the docker image
`docker build --platform linux/arm64 --tag python-docker .`

### Run the image as a container
`docker run -d -p 5000:5000 python-docker`