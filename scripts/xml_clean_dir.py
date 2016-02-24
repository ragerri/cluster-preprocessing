#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Cleans xml tags for every file in a given directory. It also works taking a file as an input.
Usage: python xml_clean_dir.py dir|file

Rodrigo Agerri (ragerri@apache.org)
24/10/2010
"""

import sys
import re
import os
import time
import getopt

rexml = re.compile(r"<.*?>") # target XML tags
badrexml = re.compile(r"<.*")# target bad remaining XML tags
#intext = sys.argv[1] # this is dealt by the main() function below

def progressdot():
    sys.stdout.write(".")
    sys.stdout.flush()
    #time.sleep(.1)

def clean_dir(intext):
    for dirpath, dirs, docs in os.walk(intext):
        for doc in docs:
            progressdot()
            infile = open(os.path.join(dirpath,doc),"r").readlines()
            infile = "".join(infile)
            """removes xml tags"""
            infile = rexml.sub("",infile)
            infile = badrexml.sub("",infile)
            infile1 = infile.split("\n")
            tnt = []
            for line in infile1:
                if len(line) != 0:
                    tnt.append(line)
            tnt = [line.strip() for line in tnt]
            outfile = open(os.path.join(dirpath,doc),"w+")
            for line in tnt:
                outfile.write(line +"\n")
            outfile.close()

def clean_file(intext):
    infile = open(intext).readlines()
    infile = "".join(infile)
    """removes xml tags"""
    infile = rexml.sub("",infile)
    infile = badrexml.sub("",infile)
    infile1 = infile.split("\n")
    tnt = []
    for line in infile1:
        if len(line) != 0:
            tnt.append(line)
    tnt = [line.strip() for line in tnt]
    outfile = open(intext+".txt","w+")
    for line in tnt:
        outfile.write(line +"\n")
    outfile.close()

def main(input):
    try:
        opts, args = getopt.getopt(sys.argv[1:], "h", ["help"])
    except getopt.error, msg:
        print msg
        print "for help use --help"
        sys.exit(2)
    # process options
    for o, a in opts:
        if o in ("-h", "--help"):
            print __doc__
            sys.exit(0)
    # process arguments
    for arg in args:
        if os.path.isdir(input) == True:
            clean_dir(input)
        else:
            clean_file(input)

if __name__ == "__main__":
    main(sys.argv[1])
