#!/bin/bash

# ./sketchcopy.sh 5 -> a.py b.py c.py d.py e.py

if [ -z "$1" ]; then
    echo "How many?"
    exit 1
fi

for i in $(seq "$1"); do
    cp sketch.py "$(printf "\x$(printf %x $((96+$i)))").py"
done
