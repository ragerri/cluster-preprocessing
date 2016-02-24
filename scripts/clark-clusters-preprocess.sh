#!/bin/bash

#input is tokenized text one sentence per line.

file=$1

cat $file | sed 's/ /\n/g' | sed '/^[[:punct:]]/d' | awk ' { print tolower($0) } '

