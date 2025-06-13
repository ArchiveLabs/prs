#!/bin/bash

./docker/configure.sh

if [[ "$1" == "--dev" ]]; then
    echo "Running in development mode..."
    if [ ! -f ./env/bin/activate ]; then
        virtualenv env
    fi
    source ./env/bin/activate
    pip install --index-url --index-url "${PIP_INDEX_URL:-https://pypi.org/simple}" --no-cache-dir -r requirements.txt
    source ./env/bin/activate
    uvicorn api.app:app --reload
else
    echo "Running in production mode..."
    export $(grep -v '^#' prs.env | xargs)
    HTTP_PROXY="$HTTP_PROXY" HTTPS_PROXY="$HTTPS_PROXY" APT_MIRROR="$APT_MIRROR" PIP_INDEX_URL="$PIP_INDEX_URL" docker compose -p api up -d
fi
