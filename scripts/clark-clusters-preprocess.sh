#!/bin/bash

file=$1

sed 's/ /\n/g' $file | sed '/^[[:punct:]]/d' | awk ' { print tolower($0) } ' | sed 's/^[[:blank:]]*//g' | sed 's/[[:blank:]]*$//g' | tr -s " "
