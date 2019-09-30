# download elasticsearch if directory does not exist
if [ ! -d elasticsearch-7.3.2 ]; then
  wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-7.3.2-darwin-x86_64.tar.gz
  tar -zxvf elasticsearch-7.3.2-darwin-x86_64.tar.gz
  rm elasticsearch-7.3.2-darwin-x86_64.tar.gz
fi

# serve elasticsearch
cd elasticsearch-7.3.2
bin/elasticsearch
