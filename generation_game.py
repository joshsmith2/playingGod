#!/usr/bin/env python

"""generation_game.py

The tools to create and manipulate generations of Voices - soon, creatures."""

from wavegen import *
from freqtools import *
import random
import os

def to_gen(a_list):
    """Converts a list to a generator"""
    for i in     

class Creature:
    """An object which can be evolved. 

    voice: Voice
        The creature's voice
    no_of_partners: int
        How many other creatures this one mates with when it copulates.
    x_points:
        Number of crossover points to be used while copulating
    """

    def __init__(self, voice=Voice(), no_of_partners=1, x_points=1):
        self.no_of_partners = no_of_partners
        self.voice = voice
        self.no_of_x_points = x_points

    def copulate(self, voices_to_combine, 
                 mut_rate=0.05, 
                 attributes=['frequency','time','prewait','postwait'],
                 ):
        """Mixes the attributes of alpha with that of each voice in other.
        Returns a new voice. 

        alpha: Voice
            The 'primary' voice. Its' 'number of partners' is         
        others: list of Voices
        """
        self.x_points
        voices_to_combine.append(self)
        
        #Pick crossover points
        possible_points = len(waves_per_voice) * len(attributes)
        x_points = random.sample(range(possible_points), no_of_x_points)
    
        point_index = 0
        out_voice = Voice()
        
        #Choose the voices who will pass on their genes this time...
        fertile_list = random.sample(voices_to_combine, no_of_x_points+1)
        fertile_voices = iter(fertile_list)
        #...and the one being written now.
        dominant_voice=fertile_voices.next()

        for wave in self.waves:
            out_wave = Wave()
            for attr in attributes:
                if point_index in x_points:
                    dominant_voice = fertile_voices.next()
        



def activate(waves, no_active):
    """Given a list of waves, returns a list with exactly no_active of these
       activated."""
    try:
        activate_these = random.sample(waves, no_active)
    except ValueError as e:
        print "Error: " + str(e) + "\n" +\
              "Waves activated: " + str(no_active) + "\n" +\

              "Waves in voices: " + str(len(waves)) + "\n" +\
              "Activating them all"
        activate_these = waves

    for wave in waves:
        if wave in activate_these:
            wave.active = True
        else:
            wave.active = False

    return waves

def check_limits(name, value):
    """
    Given a variable and it's defined values in make_voice, will error if these
    values are outside the bounds set here.
    Note: 'None' means no limit."""

    limits = {'no_of_waves':(0, None),
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
         print "You have tried to define a voice with a " + name +\
               " of " + str(value) + ". "+\
               name + " has a lower limit of " + str(limits[name][0]) +\
               " and an upper limit of " + str(limits[name][1]) + "."

    elif limits[name][1]:
         if value > limits[name][1]:
             print "You have tried to define a voice with a " + name + " of "+\
                   str(value) + ". " + name + " has a lower limit of "+\
                   str(limits[name][0]) + " and an upper limit of "+\
                   str(limits[name][1]) + "."

def make_voice(no_of_waves=30,
               no_of_active_waves=None,
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

    no_of_waves: int
         The number of waves to be merged into the voice. Should be the same
         across all voices in a generation.

    no_of_active_waves: tuple of ints
         The number of waves you will actually hear.

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

    #Define no of active waves if not done already.
    if not no_of_active_waves:
        no_of_active_waves = (0, no_of_waves)

    #Convert freq values to mils...
    mils_range=(freq_to_mils(freq_range[0]),freq_to_mils(freq_range[1]))

    no_of_active_waves_out = random.randint(no_of_active_waves[0],
                                            no_of_active_waves[1])
    
    print no_of_active_waves_out, "active waves"

    constituent_waves=[]

    for n in range(no_of_waves):
    
        #Generate definitive values for wave attributes
        wave_length_out = random.uniform(wave_length[0], wave_length[1])
        amplitude_out = random.uniform(amplitude[0], amplitude[1])
        prewait_out = random.randint(prewait[0], prewait[1])
        postwait_out = random.randint(postwait[0], postwait[1])
        mils_out = random.randint(mils_range[0], mils_range[1])
        freq_out = mils_to_freq(mils_out)

        if shape == 'any':
            shape_out = possible_shapes[random.randint(0,len(possible_shapes)-1)]
        else:
            shape_out = shape
        if operation == 'any':
            operation_out = possible_operations[random.randint(0,len(possible_operations)-1)]
        else:
            operation_out = operation
    
        constituent_waves.append(Wave(freq_out,wave_length_out,amplitude_out,
                                      prewait=prewait_out,
                                      postwait=postwait_out,
                                      shape=shape_out))

    active_waves = activate(constituent_waves, no_of_active_waves_out)
    active_waves = [w for w in active_waves if w.active]
    final_product = merge(active_waves)
    final_product.waves = constituent_waves
    return final_product

def make_generation(age=0,
                    no_of_voices=10, 
                    waves_per_voice=30, 
                    wav_length=5):
    
        print "Building voice", i
        sample_root = os.path.abspath("./samples")
        generation_folder = "Generation " + str(age)
        full_root = os.path.join(sample_root,generation_folder)
        if not os.path.exists(full_root):
            os.mkdir(full_root)

        out_path = os.path.join(full_root,"Voice "+ str(i)+".wav")
        shpl=possible_shapes.append("any")
        shp=[random.randint(0,len(possible_shapes))]
        opl=possible_operations.append("any")
        op=[random.randint(0,len(possible_operations))]

        out_voice = make_voice(no_of_active_waves=(3,20),
                               wave_length=(0.1,15),
                               prewait=(0,66000), 
                               postwait=(0,66000),
                               operation=op,
                               freq_range=(32,3000),)
        out_voice.write_to_wav(out_path,length=wav_length)


def main():
    make_generation(13,3,20,10)

if __name__=="__main__":
    main()

