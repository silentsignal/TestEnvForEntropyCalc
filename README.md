# Testing environment for CVE-2019-6976
This repository contains all the files and information to set up an environment with the vulnerable libvips library to play around with CVE-2019-6976. 

File descriptions
=================

#### Dockerfile
This is the Dockerfile which was used to build the docker image.

#### reqiurements.txt
This contains all the neccessary modules for the python server on the docker container.

#### restart.sh
Creates a while loop which continuously restarts the python server whenever it crashes.

#### test.py
Code for the python server.

Build your own image
====================
To tweak around or customize the docker image simply do a git clone to this repo

``git clone --single-branch --branch multi https://github.com/silentsignal/TestEnvForEntropyCalc``

Grab the referenced submodules:

``git submodule init && git submodule update``

make the neccessary changes to the Dockerfile/test.py or whatever you want, and rebuild the docker image with the following command:

``docker build --tag=<your tag> .``

and stat the newly created container.
