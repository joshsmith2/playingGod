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

    def __init__(self, voice=None, no_of_partners=1, x_points=1):
        self.no_of_partners = no_of_partners
        if voice:
            self.voice = voice
        else:
            self.voice = Voice()
        self.no_of_x_points = x_points

    def make_creature(self,
                      max_no_of_partners = (1,30),
                      no_of_x_points = None,
                      ):
        """Constructs a creature with attributes randomly chosen from
        the ranges passed"""
        self.max_no_of_partners = random.randint(max_no_of_partners[0],
                                                 max_no_of_partners[1])

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

class Generation:
    def __init__(self, era, creatures=[], no_of_creatures=30):
        self.era = era
        self.creatures = []
        self.no_of_creatures = no_of_creatures

    def make_generation(self):
        """Returns a list of creatures, each with its own voice."""
        out_creatures = []

        for i in range(self.no_of_creatures):
            out_creature = Creature()
            out_creature.make_creature()
            
            #To be removed - operations to become attributes of waves.
            opl=possible_operations.append("any")
            op=[random.randint(0,len(possible_operations))]

            out_creature.voice.make_voice()
            out_creatures.append(out_creature)

        self.creatures = out_creatures
