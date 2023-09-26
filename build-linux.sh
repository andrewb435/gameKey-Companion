#!/bin/sh

function yes_or_no {
    while true; do
        read -p "$* [y/n]: " yn
        case $yn in
            [Yy]*) return 0  ;;
            [Nn]*) echo "No $*" ; return  1 ;;
        esac
    done
}

cd docker-build
docker build -f Dockerfile-linux -t gkbuild:lin .
cd ..
docker run -v "$(pwd)/:/src/" --name gkbuildlin gkbuild:lin
docker container stop gkbuildlin && docker container rm gkbuildlin && docker image rm gkbuild:lin
