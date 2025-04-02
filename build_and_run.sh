cd /Users/roman/sphinx-local
docker rm -f sphinx_container
docker buildx build --cache-to type=inline,mode=max -t sphinx:latest .
docker run -d -p 8080:80 --name sphinx_container sphinx:latest
sleep 1
open -a "Google Chrome" http://localhost:8080