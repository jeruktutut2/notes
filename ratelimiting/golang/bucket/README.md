# RATE LIMITING

# install
```bash
go mod init bucket
```

# run
```bash
go run main.go
```

# test
```bash
curl -X POST http://localhost:8080/api/v1/test

for i in {1..50}; do
  curl -s -o /dev/null -w "%{http_code}\n" http://localhost:8080/api/v1/test
done
wait

for i in {1..100}; do
  curl -s -o /dev/null -w "%{http_code}\n" http://localhost:1323/
  sleep 0.1
done
wait
```
    Penjelasan:
    -s → silent
    -o /dev/null → buang body
    -w "%{http_code}\n" → hanya cetak status code

# note
    reverse proxy (nginx / traefik) mengirim header X-Forwarded-For