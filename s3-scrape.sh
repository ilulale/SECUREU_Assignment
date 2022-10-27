cd s3-scrape-cli && python3 s3-scrape.py && cd ..
docker kill s3dash > /dev/null 2>&1
docker rm s3dash > /dev/null 2>&1
docker run -d -p 8080:3000 --name s3dash ilulale/s3-dashboard > /dev/null
