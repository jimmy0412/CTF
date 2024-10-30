#!/bin/bash
rm /tmp/aa
mkfifo /tmp/aa
rm /tmp/bb
mkfifo /tmp/bb

/challenge/embryoio_level93 < /tmp/aa > /tmp/bb &
cat < /tmp/bb &
cat > /tmp/aa 