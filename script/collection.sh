#!/bin/bash

# map
declare -A map
arr=()

key="key"
value="value"

function assert_map() {
  if [ "${map[$key]}" == $value ]; then
    echo value is set
  fi
  if [[ -z "${map[$key]}" ]]; then
    echo empty map
  fi
}

echo before setting value
assert_map
map[$key]=$value
echo after setting value
assert_map

map[key1]=value1
map[key2]=value2

echo
echo keys
echo "${!map[@]}"
echo values
echo "${map[@]}"

echo
echo array
echo "${arr[@]}" should be empty
arr+=(10)
echo "${arr[@]}" should not be empty
