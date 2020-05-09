#!/bin/sh

wget https://www.python.org/ftp/python/3.7.7/Python-3.7.7.tgz

mv Python-3.7.7.tgz /usr/local/Python-3.7.7.tgz
cd /usr/local/
tar -zxvf Python-3.7.7.tgz
cd Python-3.7.7
./configure LD_RUN_PATH=/usr/local/lib LDFLAGS="-L/usr/local/lib" CPPFLAGS="-I/usr/local/include"
make LD_RUN_PATH=/usr/local/lib
sudo make install
