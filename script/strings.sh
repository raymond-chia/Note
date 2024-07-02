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
