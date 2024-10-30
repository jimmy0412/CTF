#!/bin/bash
rm /tmp/aa
mkfifo /tmp/aa
exec 21<> /tmp/aa  ## open fd 21
echo "zsyjgibx" >&21 & /challenge/embryoio_level94

#https://stackoverflow.com/questions/7082001/how-do-file-descriptors-work



