#!/usr/bin/bash
for file in ./src/*.py; do
  clear
  python3 "$file" --graph
done
clear