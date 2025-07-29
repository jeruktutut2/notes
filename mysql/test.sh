#!/bin/bash

# URL Base
BASE_URL="http://localhost:8080"

# GETBYID=$(curl -s -X POST "$BASE_URL/test1/7" \
#   -H "Content-Type: application/json")

# echo "GETBYID: $GETBYID"

# if you put -i to curl, you will cannot parse json using jq, because the result will include http status
POST_RESPONSE=$(curl -s -X POST "$BASE_URL/test1" \
    -H "Content-Type: application/json" \
    -d '{"test": "test post"}')
echo "POST RESPONSE: $POST_RESPONSE"
TEST_ID=$(echo "$POST_RESPONSE" | jq -r '.data.id')
# BOOK_ID=$(echo "$BOOK_RESPONSE" | jq -r '.data.id')
# echo "Fetched Book ID: $BOOK_ID"
echo "TEST ID: $TEST_ID";

# # TEST_ID=7
GETBYID_RESPONSE=$(curl -s -X GET "$BASE_URL/test1/$TEST_ID")

# echo "GETBYID RESPONSE: $GETBYID_RESPONSE"

UPDATE_RESPONSE=$(curl -s -X PUT "$BASE_URL/test1" \
    -H "Content-Type: application/json" \
    -d "{\"id\": $TEST_ID, \"test\": \"test put\"}")
echo "UPDATE RESPONSE: $UPDATE_RESPONSE"

DELETE_RESPONSE=$(curl -i -s -X DELETE "$BASE_URL/test1" \
    -H "Content-Type: application/json" \
    -d "{\"id\": $TEST_ID}")
echo "DELETE RESPONSE: $DELETE_RESPONSE"

# # Cek apakah login berhasil (status code 200)
# if [[ $(echo "$GETBYID" | jq -r '.status') != "200" ]]; then
#   echo "Login failed!"
#   exit 1
# fi
