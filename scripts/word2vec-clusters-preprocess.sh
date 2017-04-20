#!/bin/bash

#input is tokenized text one sentence per line.

file=$1

sed 's/ /\n/g' $file | sed '/^[[:punct:]]/d' | awk ' { print tolower($0) } ' | tr "\n" " " | tr -s " "
