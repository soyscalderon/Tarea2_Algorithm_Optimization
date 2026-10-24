#!/usr/bin/bash
for file in ./src/algorithms/*.py; do
  clear
  echo "Running $file"
  echo

  python3 "$file"
  
  echo
  read -n1 -r -p "Press any key to continue..."
done
  clear
