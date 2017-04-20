#!/bin/bash

lang=$1
folder=$2
for i in $folder/*; do time cat $i | java -jar ixa-pipe-tok-1.8.5-exec.jar tok -l $lang -o oneline > $i.tok ; done
