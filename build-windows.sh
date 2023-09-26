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
docker build -f Dockerfile-windows -t gkbuild:win .
cd ..
docker run -v "$(pwd)/:/src/" --name gkbuildwin gkbuild:win
docker container stop gkbuildwin && docker container rm gkbuildwin && docker image rm gkbuild:win
