#!/usr/bin/env python

"""generation_game.py

The tools to create and manipulate generations of Voices - soon, creatures."""

from wavegen import *
from freqtools import *
import random
import os

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
                 waves_per_voice=30,
                 ):
        """Mixes the attributes of alpha with that of each voice in other.
        Returns a new voice. 

        voices_to_combine: list of Voices
            The pool from which to pick the partners. Should not contain self. 
        mut_rate: float
            The likelihood that a given value will mutate. Not used yet.
        attributes: list of str
            The attributes which can be changed during copulation
        """
        #Pick crossover points
        possible_points = waves_per_voice * len(attributes)
        x_points = random.sample(range(possible_points), self.no_of_x_points)
    
        point_index = 0
        
        out = self    

        #Choose the voices who will pass on their genes this time...
        fertile_list = random.sample(voices_to_combine, self.no_of_partners)
        fertile_list.append(self)
        fertile_voices = [f.voice for f in fertile_list]
        
        #...and the one to be written first.
        dominant_voice = random.sample(fertile_voices, 1)[0]

        waves = self.voice.waves
        for wave in waves:
            wave_index = waves.index(wave)
            for attr in attributes:
                if point_index in x_points:
                    dominant_voice = random.sample(fertile_voices, 1)[0]
                set_value = getattr(dominant_voice.waves[wave_index], attr)
                setattr(out.voice.waves[wave_index], attr, set_value)
        
        return out

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

def make_creature(no_of_waves=30,
                  max_no_of_partners=(0,10),
                  no_of_x_points=(0,100),
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
    frequencies and amplitudes, all within predefined boundaries, and return a 
    creature with this voice. 

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
        max_no_of_partners_out = random.randint(max_no_of_partners[0], max_no_of_partners[1])
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
    final_voice = merge(active_waves)
    final_voice.waves = constituent_waves
    
    return Creature(final_voice, max_no_of_partners_out)

def make_generation(age=0,
                    no_of_creatures=10, 
                    waves_per_voice=30, 
                    wav_length=5):
        
    """Returns a list of creatures, each with its own voice."""
    out_creature = Creature()        
    out_creatures = []

    for i in range(no_of_creatures):
        
        out_creature = Creature()

        print "Building creature", i

        shpl=possible_shapes.append("any")
        shp=[random.randint(0,len(possible_shapes))]
        opl=possible_operations.append("any")
        op=[random.randint(0,len(possible_operations))]

        out_creature = make_creature(max_no_of_partners = (1,2),
                                     no_of_x_points = (5,5),
                                     no_of_active_waves=(1,10),
                                     wave_length=(0.1,15),
                                     prewait=(0,66000), 
                                     postwait=(0,66000),
                                     operation=op,
                                     freq_range=(30,3300),)

        out_creatures.append(out_creature)
    return out_creatures

def pick_a_parent(creature, gene_pool):
    return creature.copulate(gene_pool)

def rubber_stamper(creatures, age=3):

    for c in creatures:
        index = creatures.index(c)
        for w in c.voice.waves:
            print "Attributes for wave ", c.voice.waves.index(w), ":"
            w.print_vars()
            print "\n"
        
        sample_root = os.path.abspath("./samples")
        generation_folder = "Creature generation " + str(age) 
        full_root = os.path.join(sample_root,generation_folder)

        if not os.path.exists(full_root):
            os.mkdir(full_root)

        out_path = os.path.join(full_root,"Voice "+ str(index)+".wav")
        
        print "Writing voice of creature ", index, "\n"
        c.voice.write_to_wav(out_path, length=10)

def main():
    creatures = make_generation(age=2,
                                no_of_creatures=5,
                                waves_per_voice=30,
                                wav_length=10,)

    rubber_stamper(creatures, 3)

    alpha_index = raw_input("Pick a parent: ")
    alpha = creatures[int(alpha_index)]
    other_creatures = creatures
    other_creatures.remove(alpha)
   
    print other_creatures
    print alpha

    child = pick_a_parent(alpha,other_creatures)

    print "No. of parents: ", child.no_of_partners
    for w in child.voice.waves:
        print "vars for wave ", child.voice.waves.index(
        w.print_vars()
        
    print "Writing child..."
    child.voice.write_to_wav("samples/Childred.wav", length=10)

if __name__=="__main__":
    main()

