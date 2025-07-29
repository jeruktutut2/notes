# SERVER SENT EVENT

## library
    go get github.com/labstack/echo/v4
    go get github.com/google/uuid

## curl
    curl -N http://localhost:8080/sse/handle-sse-without-channel

## problem that may happen
    if you use sse in ordinary html css js, there will be no problem
    if you use sse in nuxtjs, there will be 5 minutes idle timeout, i dont know is this because using nitro (as a reverse proxy) or it just nuxtjs, since i built frontend and backend services
    if you use nextjs, the idle timeout is just 1 minute
    ultimatelly, if you want to deploy frontend and backend behind nginx, you must set the nginx timeout longer, e.g: 

    location /events {
    proxy_pass http://localhost:8080;
    proxy_set_header Connection keep-alive;  
    proxy_buffering off;  
    proxy_read_timeout 600s;
    proxy_send_timeout 600s;  
    keepalive_timeout 600s;  
    chunked_transfer_encoding on;

    or do ping every 5 minutes or less, to keep the sse connected
}
