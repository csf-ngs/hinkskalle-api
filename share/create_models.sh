#!/bin/bash

set -eo pipefail

url=${1:-https://pkg.ngs.vbcf.ac.at/swagger}

curl -f $url | 
  spotta -v DEBUG - python \
    -c Collection \
    -c Container \
    -c Entity \
    -c Image \
    -c User \
    -c Group \
    -c GroupMember \
    -c Manifest \
    -c TagData \
    -c Token \
    -t hinkskalle_api/auto \
    -o hinkskalle_api/auto/models.py

