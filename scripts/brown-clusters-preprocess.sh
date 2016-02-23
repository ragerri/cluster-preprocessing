#!/bin/sh

cat $1 | perl -pe 's/ /\n/g' | sed '/^[[:punct:]]/d' | perl -pe 's/^\n/JAR!!/g' | perl -pe 's/\n/ /g' | perl -pe 's/JAR!!/\n/g'