#!/bin/bash

mkfifo /tmp/aa
echo "kcqqepcz" > /tmp/aa &
/challenge/embryoio_level90 < /tmp/aa