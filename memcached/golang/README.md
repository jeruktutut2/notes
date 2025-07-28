# MEMCACHED

## library
    go get github.com/labstack/echo/v4
    go get github.com/bradfitz/gomemcache/memcache

## docker
    docker run --name project-memcached -p 11211:11211 -d memcached
    docker run -d --name memcached-container -p 11211:11211 memcached memcached -m 64 -vv
    -m 64: limiting memory to 64 MB.
    -vv: using verbose logging.

    docker exec -it -u root project-memcached bash
    connect to memcached using telnet 127.0.0.1 11211 or if it doesn't connect, install below tools
    apt-get update && apt-get install -y telnet

    <!-- apk add busybox-extras # for alphine based -->
    <!-- apt-get update && apt-get install -y telnet  # for debian/ubuntu based -->