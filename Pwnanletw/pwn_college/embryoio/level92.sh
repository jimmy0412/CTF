#!/bin/bash
rm /tmp/aa
mkfifo /tmp/aa
rm /tmp/bb
mkfifo /tmp/bb
echo "eoqeftjo" > /tmp/aa &
/challenge/embryoio_level92 < /tmp/aa > /tmp/bb &
cat < /tmp/bb