# download elasticsearch if directory does not exist
version="7.4.0" # specify elasticsearch
if [ ! -d elasticsearch-${version} ]; then
  if [[ "$OSTYPE" == "linux-gnu" ]]; then
    wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-${version}-linux-x86_64.tar.gz
    tar -zxvf elasticsearch-${version}-linux-x86_64.tar.gz
    rm elasticsearch-${version}-linux-x86_64.tar.gz
  elif [[ "$OSTYPE" == "darwin"* ]]; then
    wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-${version}-darwin-x86_64.tar.gz
    tar -zxvf elasticsearch-${version}-darwin-x86_64.tar.gz
    rm elasticsearch-${version}-darwin-x86_64.tar.gz
  else
    echo "Manually download elasticsearch according to your operating system from https://www.elastic.co/downloads/elasticsearch"
  fi
fi

# serve elasticsearch backend
cd elasticsearch-${version}
bin/elasticsearch
