# WEBRTC

## install coturn
    docker run -d --name coturn-turn-auth \
        -p 3478:3478/udp \
        -p 3478:3478/tcp \
        -p 49160-49200:49160-49200/udp \
        instrumentisto/coturn \
        -n --log-file=stdout \
        --min-port=49160 --max-port=49200 \
        --realm=example.com \
        --user=username:password \
        --lt-cred-mech \
        --fingerprint \
        --simple-log
    
    docker run -d --network=host coturn/coturn \
           -n --log-file=stdout \
           --min-port=49160 --max-port=49200 \
           --lt-cred-mech --fingerprint \
           --no-multicast-peers --no-cli \
           --no-tlsv1 --no-tlsv1_1 \
           --realm=my.realm.org \  

    docker run -d --name coturn -p 3478:3478 -p 3478:3478/udp -p 5349:5349 -p 5349:5349/udp -p 49160-49200:49160-49200/udp coturn/coturn --min-port=49160 --max-port=49200 --realm=example.com --user=admin:12345 --lt-cred-mech

    check docker log: docker logs coturn