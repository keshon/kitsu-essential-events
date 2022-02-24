# Read .env
if [ -f .env ]
then
    export $(cat .env | sed 's/#.*//g' | xargs)
else
    echo ".env file not found!"
    exit 0
fi


# Git
if [ $GIT != "false" ]
then
    # - remove old git project
    rm -rf ./src
    # - make a new git clone
    git clone ${GIT_URL} src
else
    if [ ! -d "./src" ]
    then
        echo "src dir not found!"
        exit 0
    fi
fi


# Docker
# - stop container
docker stop ${ALIAS}
docker rm ${ALIAS}

# - remove old image (if there is any)
docker rmi $(docker images --filter=reference="*:${ALIAS}-image" -q)

# - build new docker image from Dockerfile
docker build -t ${ALIAS}-image .

# - start new container using docker-compose
docker-compose up -d

# remove unused images
docker image prune -a