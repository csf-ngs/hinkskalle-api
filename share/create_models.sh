#!/bin/bash

curl localhost:7660/swagger | 
  spotta -v DEBUG - python \
    -c Collection \
    -c Container \
    -c Entity \
    -c User \
    -c Group \
    -c Manifest \
    -c TagData \
    -c Token \
    -t hinkskalle_api/auto \
    -o hinkskalle_api/auto/models.py


