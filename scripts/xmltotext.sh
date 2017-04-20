#!/bin/bash

infile=$1

perl -pe 's/<.*?>//g' $infile | perl -MHTML::Entities -pe 'decode_entities($_);' | perl -pe 's/^\n//g' | perl -pe "s/&apos;/\'/g" | perl -pe 's/&quot;/"/g' | perl -pe 's/&lt;/\</g' |  perl -pe 's/&gt;/>/g' | perl -pe 's/&amp;/&/g'