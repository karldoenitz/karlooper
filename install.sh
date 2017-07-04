#!/usr/bin/env bash

if [ -z "$1" ] ; then
    echo "develop: install for developers"
    echo "release: install standard"
    echo "lib: install dist files lib"
    echo "sdist: upload distribute file to pypi"
elif [ $1 = "develop" ] ; then
    echo "start install in develop mod..."
    mkdir ~/karlooper-tmp-folder
    cp -r ./ ~/karlooper-tmp-folder
    cd ~/karlooper-tmp-folder
    python setup.py install
    cd -
    rm -rf ~/karlooper-tmp-folder
elif [ $1 = "lib" ] ; then
    echo "start install in develop mod..."
    mkdir ~/karlooper-tmp-folder
    cp -r ./ ~/karlooper-tmp-folder
    cd ~/karlooper-tmp-folder
    python setup.py sdist
    cd dist
    tar -zxvf karlooper*.tar.gz
    cd ./karlooper*
    python setup.py install_lib
    cd ~
    rm -rf ~/karlooper-tmp-folder
elif [ $1 = "sdist" ] ; then
    echo "start distribute package..."
    python setup.py sdist
    echo "upload to pypi..."
    twine upload dist/*
    echo "remove dist file in local..."
    rm -rf ./dist/ ./karlooper.egg-info/
    echo "files be removed"
elif [ $1 = "release" ] ; then
    echo "start install..."
    python setup.py install
fi