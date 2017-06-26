#!/usr/bin/env bash

if [ -z "$1" ] ; then
    echo "develop: install for developers"
    echo "release: install standard"
    echo "sdist: release dist files"
elif [ $1 = "develop" ] ; then
    echo "start install in develop mod..."
    mkdir ~/karlooper
    cp -r ./ ~/karlooper
    cd ~/karlooper
    python setup.py install
    cd -
    rm -rf ~/karlooper
elif [ $1 = "sdist" ] ; then
    echo "start install in develop mod..."
    mkdir ~/karlooper
    cp -r ./ ~/karlooper
    cd ~/karlooper
    python setup.py sdist
    cd dist
    tar -zxvf karlooper*.tar.gz
    cd ./karlooper*
    python setup.py install_lib
elif [ $1 = "release" ] ; then
    echo "start install..."
    python setup.py install
fi