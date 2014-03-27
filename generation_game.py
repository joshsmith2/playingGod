#!/usr/bin/env python

"""generation_game.py

The tools to create and manipulate generations of Voices - soon, creatures."""

from wavegen import *
from freqtools import *
from random import uniform, randint
import os

def check_limits(name, value):
    """
    Given a variable and it's defined values in make_voice, will error if these
    values are outside the bounds set here.
    Note: 'None' means no limit."""
    
    limits = {'number_of_waves':(0, None),
              'wave_length':(0,None),
              'freq_range':(0,None),
              'amplitude':(0,1),
              'prewait':(0,None),
              'postwait':(0,None),}

    if name == 'shape':
        if value not in possible_shapes:
            print "You have tried to generate a wave with shape " + value+\
                  ". Possible shapes are " + ', '.join(possible_shapes) + "."
            """TURN THIS INTO AN EXCEPTION"""

    elif name == 'operation':
        if value not in possible_operations:
            print "You have tried to merge waves with operation " +\
                  value + ". Possible operations are " +\
                  ', '.join(possible_operations) + "."

    elif value < limits[name][0]:
         print "You have tried to define a voice with a " + name + " of " +\
               str(value) + ". " + name + " has a lower limit of " +\
               str(limits[name][0]) + " and an upper limit of " +\
               str(limits[name][1]) + "."

    elif limits[name][1]:
         if value > limits[name][1]:
             print "You have tried to define a voice with a " + name + " of " +\
                   str(value) + ". " + name + " has a lower limit of " +\
                   str(limits[name][0]) + " and an upper limit of " +\
                   str(limits[name][1]) + "."

def make_voice(number_of_waves=(1,30), 
               wave_length=(0,60), 
               freq_range=(100,4000), 
               amplitude=(0.1,0.9), 
               prewait=(0,70000),
               postwait=(0,60000),
               shape="sine",
               operation="+",):
    """
    Construct a Voice from a random number of waves, with various shapes, 
    frequencies and amplitudes, all within predefined boundaries.
 
    Each argument is a tuple of minumum and maximum values. The resulting
    voice's attributes will be a random value from this range. 
    
    Variables:
    number_of_waves(min,max): tuple of ints
         The number of waves to be merged into the voice
    wave_length(min,max): tuple of floats
         The duration of the audible portion of each wave
    freq_range(min,max): tuple of ints
         The minimum and maximum possible frequencies, in Hz, for each wave.
    amplitude(min,max): 
         The amplitude of each wave
    prewait(min,max):
         The number of ticks to wait before writing the audible part of the 
         wave.
    postwait(min,max):
         The number of ticks to wait after writing the audible part of the 
         wave.
    shape: str
         The shape of each wave. A value from possible_shapes.
    operation: str
         The operation (e.g addition) with which to merge the waves together
    """

    """Write something to cycle through variables and check them against their
    defined vals"""
    
    #Convert freq values to mils...
    mils_range=(freq_to_mils(freq_range[0]),freq_to_mils(freq_range[1]))
    
    #Roll dice for values
    number_of_waves_out = randint(number_of_waves[0], number_of_waves[1])
    
    constituent_waves=[]  
 
    for n in range(number_of_waves_out): 
        wave_length_out = uniform(wave_length[0], wave_length[1])
        amplitude_out = uniform(amplitude[0], amplitude[1])
        prewait_out = randint(prewait[0], prewait[1])
        postwait_out = randint(postwait[0], postwait[1])
        
        mils_out = randint(mils_range[0], mils_range[1])
        freq_out = mils_to_freq(mils_out)

        if shape == 'any':
            shape_out = possible_shapes[randint(0,len(possible_shapes)-1)]
        else:
            shape_out = shape
        if operation == 'any':
            operation_out = possible_operations[randint(0,len(possible_operations)-1)]
        else:
            operation_out = operation
        
        constituent_waves.append(Wave(freq_out,wave_length_out,amplitude_out,
                                      prewait=prewait_out,
                                      postwait=postwait_out,
                                      shape=shape_out)) 

    return merge(constituent_waves)

def make_generation(age=0, number_of_voices=10):
    for i in range(number_of_voices):
        print "Building wave", i
        sample_root = os.path.abspath("./samples")
        generation_folder = "Generation " + str(age)
        full_root = os.path.join(sample_root,generation_folder)
        if not os.path.exists(full_root):
            os.mkdir(full_root)
        out_path = os.path.join(full_root,"Voice "+ str(i)+".wav")
        shpl=possible_shapes.append("any")
        shp=[randint(0,len(possible_shapes))]
        opl=possible_operations.append("any")
        op=[randint(0,len(possible_operations))]
        make_voice(number_of_waves=(3,20), wave_length=(0.1,10), operation=op).write_to_wav(out_path,length=20)

make_generation(age=3, number_of_voices=10)
