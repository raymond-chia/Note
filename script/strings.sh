#!/usr/bin/env bash

readonly STRING="prefix-something-suffix"
# trim prefix
echo ${STRING#"prefix-"}
echo ${STRING#*-}
# trim suffix
echo ${STRING%-*}
echo ${STRING%"-suffix"}
# get suffix
echo ${STRING##*-}
# get prefix
echo ${STRING%%-*}

# https://stackoverflow.com/questions/918886/how-do-i-split-a-string-on-a-delimiter-in-bash
# use `read` to parse: https://www.shellcheck.net/wiki/SC2206
IFS=" " read -ra split <<< ${STRING//-/ }
echo "${split[0]} / ${split[1]} / ${split[2]}"
