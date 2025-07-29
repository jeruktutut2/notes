# POSTGRESQL

## install library
to parse json
    brew install jq
to do benchmarking
    brew install wrk
    wrk --version

## change file execute
    chmod +x test.sh
    ./test.sh

## benchmark using wrk
    wrk -t10 -c100 -d30s http://localhost:8080/test1/25
    wrk -t5 -c10 -d60s http://localhost:8080/api/v1/test1/25
    wrk -t10 -c10 -d60s http://localhost:8080/api/v1/test1/25
    wrk -t1 -c1 -d60s http://localhost:8080/api/v1/test1/25

## postgres process
    check status DATABASE:

    SELECT datname, usename, application_name, client_addr, state, count(*) as connections
    FROM pg_stat_activity
    GROUP BY datname, usename, application_name, client_addr, state
    ORDER BY connections DESC;
    
    SELECT datname, usename, application_name, client_addr, state
    FROM pg_stat_activity;


## postgresql
    docker exec -it project-postgres bash
    psql -h localhost -d project_users -U postgres -W
    \list \l
    \c project_users
    \dt

    CREATE DATABASE ecommercev2;
    \c ecommercev2
    \c test1
    \dt

    CREATE TABLE users (
  	    id SERIAL PRIMARY KEY,
  	    username varchar(50) NOT NULL UNIQUE,
  	    email varchar(100) NOT NULL UNIQUE,
  	    password varchar(100) NOT NULL,
  	    created_at bigint NOT NULL
    );

    # please don't use " in insert values, use ' instead, or error will accoured, There is a column named "username" in table "users", but it cannot be referenced from this part of the query.
    INSERT INTO users (id,username,email,password,created_at) VALUES (1,'username','email@email.com','$2a$10$MvEM5qcQFk39jC/3fYzJzOIy7M/xQiGv/PAkkoarCMgsx/rO0UaPG',1695095017);

## curl test
    curl -i -X GET -H "Content-Type: application/json" http://localhost:8080/api/v1/test1/1
    curl -i -X POST \
        -H "Content-Type: application/json" \
        -d '{"test": "test post"}' \
        http://localhost:8080/api/v1/test1
    curl -i -X PUT \
        -H "Content-Type: application/json" \
        -d '{"id": 6, "test": "test put 6"}' \
        http://localhost:8080/api/v1/test1
    curl -i -X DELETE \
        -H "Content-Type: application/json" \
        -d '{"id": 6}' \
        http://localhost:8080/api/v1/test1

## another tutorial
    is_apply_constrain_unique = true, it is use to implement unique constraint for selected data.

    CREATE TABLE users (
        id SERIAL PRIMARY KEY,
        username TEXT NOT NULL,
        email TEXT NOT NULL,
        is_apply_constrain_unique BOOLEAN DEFAULT false
    );

    CREATE UNIQUE INDEX unique_email_if_applied
        ON users (email)
    WHERE is_apply_constrain_unique = true;

    make sure that only row data with is_apply_constrain_unique = true that only has unique email

    -- ✅ Diterima karena tidak terikat constraint
    INSERT INTO users (username, email, is_apply_constrain_unique)
    VALUES ('user1', 'john@example.com', false);

    -- ✅ Diterima karena pertama kali email ini digunakan dalam constraint
    INSERT INTO users (username, email, is_apply_constrain_unique)
    VALUES ('user2', 'john@example.com', true);

    -- ❌ Ditolak karena email yang sama digunakan lagi saat is_apply_constrain_unique = true
    INSERT INTO users (username, email, is_apply_constrain_unique)
    VALUES ('user3', 'john@example.com', true);

    SELECT * FROM users;
