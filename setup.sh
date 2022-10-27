if ! [ -x "$(command -v docker)" ]; then
  echo 'Error: Docker is not installed.' >&2
  exit 1
fi

cd s3-scrape-cli && pip3 install -r requirements.txt && cd ..
cd s3-dashboard && docker build -t ilulale/s3-dashboard . && cd ..
