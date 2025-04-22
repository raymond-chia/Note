#!/usr/bin/env bash

curl https://sandbox.itunes.apple.com/verifyReceipt --header "Content-Type: application/json" --data "{\"receipt-data\": \"$1\"}"
# curl https://buy.itunes.apple.com/verifyReceipt --header "Content-Type: application/json" --data "{\"receipt-data\": \"$1\"}"
