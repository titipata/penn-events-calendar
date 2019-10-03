#!/bin/bash

# download elasticsearch if directory does not exist
declare -r version="7.4.0"
declare -r dl_url="https://artifacts.elastic.co/downloads/elasticsearch"
declare -r app_path="elasticsearch-${version}"

getDownloadName() {
  local osname

  if [[ "$OSTYPE" == "linux-gnu" ]]; then
    osname=linux
  elif [[ "$OSTYPE" == "darwin"* ]]; then
    osname=darwin
  else
    echo "Manually download elasticsearch according to your operating system from https://www.elastic.co/downloads/elasticsearch"
    exit 1
  fi

  echo elasticsearch-${version}-${osname}-x86_64
}

download() {
  local dl_name

  dl_name="$(getDownloadName)"

  wget ${dl_url}/"${dl_name}".tar.gz
  tar -zxvf "${dl_name}".tar.gz
  rm "${dl_name}".tar.gz
}

main() {
  # main logic happens here
  if [ ! -d "${app_path}" ]; then
    download
  fi

  # serve elasticsearch backend
  cd "${app_path}" || exit
  bin/elasticsearch
}

main
