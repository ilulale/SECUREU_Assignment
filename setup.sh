if ! [ -x "$(command -v docker)" ]; then
  echo 'Docker is not installed.Installing Docker ....' >&2
  sudo apt install docker.io
  sudo groupadd docker
  sudo usermod -aG docker $USER
  echo 'Restart session to enable docker'
  exit 1
fi

cd s3-scrape-cli && pip3 install -r requirements.txt && cd ..
cd s3-dashboard && docker build -t ilulale/s3-dashboard . && cd ..
