#!/bin/bash

# URL Base
BASE_URL="http://localhost:8080"

# if you put -i to curl, you will cannot parse json using jq, because the result will include http status
POST_RESPONSE=$(curl -s -X POST "$BASE_URL/test1" \
    -H "Content-Type: application/json" \
    -d '{"test": "test post"}')
echo "POST RESPONSE: $POST_RESPONSE"
TEST_ID=$(echo "$POST_RESPONSE" | jq -r '.data.id')
echo "TEST ID: $TEST_ID";

GETBYID_RESPONSE=$(curl -s -X GET "$BASE_URL/test1/$TEST_ID")

UPDATE_RESPONSE=$(curl -s -X PUT "$BASE_URL/test1" \
    -H "Content-Type: application/json" \
    -d "{\"id\": $TEST_ID, \"test\": \"test put\"}")
echo "UPDATE RESPONSE: $UPDATE_RESPONSE"

DELETE_RESPONSE=$(curl -i -s -X DELETE "$BASE_URL/test1" \
    -H "Content-Type: application/json" \
    -d "{\"id\": $TEST_ID}")
echo "DELETE RESPONSE: $DELETE_RESPONSE"