#!/usr/bin/env bash

readonly STRING="prefix-something-suffix"
echo ${STRING#"prefix-"}
echo ${STRING#*-}
echo ${STRING%-*}
echo ${STRING%"-suffix"}
