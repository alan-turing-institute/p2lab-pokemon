#!/bin/bash

node pokemon-showdown start --no-security &

while ! curl -I -s 0.0.0.0:8000; do
  sleep 1
done

p2lab
