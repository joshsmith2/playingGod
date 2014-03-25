#!/usr/bin/env python

"""generation_game.py

The tools to create and manipulate generations of Voices - soon, creatures."""

from wavegen import *
from freqtools import *
from random import uniform, randint




def make_voice(number_of_waves=(1,30), 
               wave_length=(0,60), 
               freq_range=(20,4000), 
               amplitude=(0.5,0.5), 
               prewait(0,60),
               postwait(0,60),
               shape="sine",
               operation="+",):
    """Construct a Voice from a random number of waves, with various shapes, 
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



def make_generation(age=0):
    pass    

