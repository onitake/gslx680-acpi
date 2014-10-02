#! /usr/bin/python
from subprocess import *
import sys
import os

if len(sys.argv) != 2:
    print "Firware extractor.\n"
    print "Requires elf file (driver) argument"
    sys.exit(1)

filename = sys.argv[1]

p = Popen(['/bin/sh', '-c', 'readelf -S '+ filename + ' | grep .rodata\ '], stdout=PIPE)

args = p.stdout.readlines()

if len(args) != 1:
    print "No simple .rodata section found"
    sys.exit(1)

rodata = args[0]

args = rodata.split()

offset = int(args[4], 16)

p = Popen(['/bin/sh', '-c', 'readelf -s '+ filename +' | grep -i fw'], stdout=PIPE)

for line in p.stdout:
    args = line.split()

    print "Found", args[7], "offset", offset + int(args[1],16), "count", args[2]
    call(['dd','if='+filename,'bs=1','count='+args[2], 'skip='+str(offset + int(args[1],16)),'of='+args[7] + ".fw"])
