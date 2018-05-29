#!/bin/bash

for i in $(ls); do
  #statements
  if [[ ${i:0:2} -eq "__" ]]; then
    #statements
    continue
  elif [[ ${i:0:6} -eq "gitadd" ]]; then
      #statements
    continue
  else
    git add $i
  fi
done