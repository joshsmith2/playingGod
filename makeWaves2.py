#!/usr/bin/env python

from wavegen import *

voice_list=[]

voice_list.append(Voice())

b=Wave(440,3,prewait=873)

voice_list.append(b)

out=merge(voice_list)

while True:
    print out.points.next()
    raw_input()
#out.write_to_wav("~/Desktop/text.wav", 3)

