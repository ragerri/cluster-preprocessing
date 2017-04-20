#!/bin/sh

sed 's/ /\n/g' $1 | sed '/^[[:punct:]]/d' | sed 's/^[[:blank:]]*$/zidorrarr/g' | tr "\n" " " | awk -vRS=" zidorrarr" -vORS="\n" 1 | sed 's/^[[:blank:]]*//g' | sed 's/[[:blank:]]*$//g' | tr -s " "