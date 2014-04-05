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

    def make_creature(self,
                      max_no_of_partners = (1,30)
                      no_of_x_points = None        
                      ):
        """Constructs a creature with attributes randomly chosen from 
        the ranges passed"""

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

class Generation:
    def __init__(self,creatures, era, no_of_creatures=30):
        self.era = era
        self.creatures = []
        self.no_of_creatures = no_of_creatures
    
    def make_generation(self,
                        waves_per_voice=30,
                        wav_length=5):

        """Returns a list of creatures, each with its own voice."""
        out_creatures = []
        out_creature = Creature()

        for i in range(no_of_creatures):
            out_creature = Creature()
            print "Building creature", i

            #To be removed - operations to become attributes of waves. 
            opl=possible_operations.append("any")
            op=[random.randint(0,len(possible_operations))]

            out_creature.voice.make_voice()
            out_creatures.append(out_creature)
        
        return out_creatures


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
