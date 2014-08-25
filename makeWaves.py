#!/usr/bin/env python

from generation_game import *
ri = raw_input
import pprint

gen = []
for i in range(5):
    o = Creature()
    o.voice.make_voice(freq_range=(10,10000), length_range=(0.1,5))
    gen.append(o)

def write_c(crets):
    for i,c in enumerate(crets):
        print "Writing " + str(i + 1) + " with " + str(c.voice.no_of_active_waves) + " active waves"
        c.voice.write_to_wav("samples/fishface/gen-"+ str(c.generation) + "-creature-" + str(i+1) + ".wav", 7)

write_c(gen)

the_gen = gen

while True:
    #[print_vars(c) for c in gen]

    for i,g in enumerate(the_gen):
        g.fitness = int(ri("Fitness of creature " + str(i+1) + "?"))

    shag_list = sorted(the_gen, key=lambda x: x.fitness, reverse=True)
    new_gen = []

    for i in range(len(the_gen)):
        alpha = choose_partners(the_gen[:],1)[0]
        out = alpha.copulate(shag_list, alpha.no_of_partners)
        new_gen.append(out)

    write_c(new_gen)
    
    the_gen = new_gen
