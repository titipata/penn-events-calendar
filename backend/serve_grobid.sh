# download GROBID if directory does not exist
version="0.5.5"
if [ ! -d grobid-${version} ]; then
  wget https://github.com/kermitt2/grobid/archive/${version}.zip
  unzip ${version}.zip
  rm ${version}.zip
fi

# run GROBID
cd grobid-${version}
./gradlew run
