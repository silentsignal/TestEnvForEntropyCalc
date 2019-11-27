#!/bin/bash

cd leakjs
npm install
node leak.js &

service apache2 start

cd ..

while true;
	do
		python test.py
	done
