#!/usr/bin/env bash

if [ -z "$1" ] ; then
    echo "develop: install for developers"
    echo "release: install standard"
elif [ $1 = "develop" ] ; then
    echo "start install in develop mod..."
    mkdir ~/karlooper
    cp -r ./ ~/karlooper
    cd ~/karlooper
    python setup.py install
    cd -
    rm -rf ~/karlooper
elif [ $1 = "release" ] ; then
    echo "start install..."
    python setup.py install
fi