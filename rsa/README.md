# RSA

## Create 1024 Rsa private key
    openssl genpkey -algorithm RSA -out private_key.pem

## Create 1024 Rsa private key (ECDSA (Elliptic Curve) with kurva secp256r1)
    openssl genpkey -algorithm EC -pkeyopt ec_paramgen_curve:secp256r1 -out private_key.pem


## Create 1024 Rsa public key
    openssl rsa -pubout -in private_key.pem -out public_key.pem

## Create 1024 Rsa public key (ECDSA (Elliptic Curve) with kurva secp256r1)
    openssl ec -pubout -in private_key.pem -out public_key.pem

## Convert to PKCS#8
    openssl pkcs8 -topk8 -nocrypt -in private_key.pem -out private_key_pkcs8.pem
if you want to encrypted with password:
    openssl pkcs8 -topk8 -v2 aes-256-cbc -in private_key.pem -out private_key_pkcs8_encrypted.pem

## Verify private key using 
    openssl pkey -in private_key.pem -text -noout

## Verify public key using
    openssl pkey -pubin -in public_key.pem -text -noout

## verify private key PKCS#8 using
    openssl pkcs8 -in private_key_pkcs8.pem -nocrypt -text -noout

## Create 2048 Rsa private key
    openssl genpkey -algorithm RSA -pkeyopt rsa_keygen_bits:2048 -out private_key.pem
or
    openssl genrsa -out private_key.pem 2048

## Create public key
    openssl rsa -pubout -in private_key.pem -out public_key.pem

## Convert to PKCS#8
    openssl pkcs8 -topk8 -nocrypt -in private_key.pem -out private_key_pkcs8.pem
with AES-256-CBC (need password)
    openssl pkcs8 -topk8 -v2 aes-256-cbc -in private_key.pem -out private_key_pkcs8_encrypted.pem

## Verify private key using
    openssl rsa -in private_key.pem -text -noout

## Verify public key using
    openssl rsa -pubin -in public_key.pem -text -noout

## Verify private key PKCS#8 using
    openssl pkcs8 -in private_key_pkcs8.pem -nocrypt -text -noout

## curl test
    curl -i -X GET  \
        -H "Content-Type: application/json" \
        -d '{"message": "test message"}' \
        http://localhost:8080/rsa/sign
    curl -i -X GET  \
        -H "Content-Type: application/json" \
        -d '{"message": "test message", "signature": "t1czqXMdLh54YwdXyQAtNia6W7T7miG6VrYZ8wW3w66ejXDOeG5t9rk30MAo1QYvOOosuumPy3rR7DDOhKv5kw9vUFzLlHbd3SACjoa1FTrhADSOoV5s1vOhAqQ9uI1Nzc6B+RhwYujE2Fiw1+VmIRgO2Rr4qlX18Y4DyzwdiUXhWcUgiumtuZk4m01Ip0hWwj6Frj3AKgptjB5wk+oJ1A2bat8LOfxiNUlHvbIkf6emnNNfKY7UxC4TO1NlTDG0/+q+/KOuX+a03opn8q+jaIpdWsXuUya+awyTDtUrUzCWgfSU/kkhL8Jf+oJkcRxSFZ73KBbJX/otqqBXhMJt+w=="}' \
        http://localhost:8080/rsa/verify