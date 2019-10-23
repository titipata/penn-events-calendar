#!/bin/bash

# download GROBID if directory does not exist
declare -r version="0.5.5"

if [ ! -d grobid-${version} ]; then
  wget https://github.com/kermitt2/grobid/archive/${version}.zip
  unzip "${version}.zip"
  rm "${version}.zip"
fi

# run GROBID
cd grobid-${version} || exit
./gradlew run
