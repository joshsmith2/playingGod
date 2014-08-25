#!/usr/bin/env python

debug = True

"""generation_game.py

The tools to create and manipulate generations of Voices - soon, creatures."""

from wavegen import *
from freqtools import *
import random
import os
import pprint

global mutation_types_and_limits
"""A dictionary containing the names and values for all possible
types of mutation,"""
mutation_types_and_limits = {'+': (-100, 100),
                             '*': (2, 16),
                             '/': (2, 16),
                             'inherit_north': (1,1),
                             'inherit_south': (1,1),
}


class UndefinedOperation(Exception):
    def __init__(self, input, possible_values):
        self.input = input
        self.possible_values = possible_values


#####NOT CURRENTLY USED#######

#def set_parameters(object):
#    if isinstance(object, Creature):
#        out_dict = {
#            no_of_partners=None
##            no_of_x_points=None #Both set at copulate
##
#
#        }


def choose_partners(all_creatures, no_of_partners):
    """Select no_of_partners partners from all_creatures to mate with. 
    Returns a list of creatures.
    
    all_creatures: list of Creatures
        The creatures to pick from. Usually every creature in the
        current generation.
    no_of_partners: int
    """
    partners = []
    creatures_sorted = sorted(all_creatures, key=lambda x: x.fitness,
                              reverse=True)
    gene_pool = creatures_sorted  #The list from which our partners will be chosen

    if no_of_partners > len(all_creatures):
        print "Attempted to mate with ", no_of_partners, " creatures."
        print "Only", len(all_creatures), " exist"
        no_of_partners = random.randint(1, len(all_creatures))
        print "Rerolling. New no. of partners = " + str(no_of_partners)

    for n in range(no_of_partners):
        fitness_list = [c.fitness for c in gene_pool]
        chosen_index = weighted_choice(fitness_list)
        chosen_creature = gene_pool[chosen_index]
        partners.append(chosen_creature)
        gene_pool.remove(chosen_creature)

    return partners


def weighted_choice(weights):
    """Return an index given a sorted list of weights. 
    Thanks go to Eli Bendersky for this function.
    http://eli.thegreenplace.net/2010/01/22/weighted-rand m-generation-in-python/
    """
    rnd = random.random() * sum(weights)
    for i, w in enumerate(weights):
        rnd -= w
        if rnd < 0:
            return i



class Creature:
    """An object which can be evolved."""

    def __init__(self,
                 no_of_partners=None,
                 no_of_x_points=None,
                 fitness=0,
                 generation=0,
                 mutation_values={'+': None, '*': None, '/': None,
                                  'inherit_north':None, 'inherit_south':None},
                 no_of_mutation_functions=4,
                 mutation_functions=[]
                 #mutation_functions={'mf1':None,'mf2':None,
                 #                             'mf3':None, 'mf4':None}
    ):
        """
        :param no_of_partners: int:
            How many other creatures this one mates with when it copulates.
        :param no_of_x_points: int:
            Number of crossover points to be used while copulating
        :param fitness: float:
            The creature's fitness, determining evolutionary strength.
        :param generation:
            Which generation the creature belongs to.
        """
        self.no_of_partners = no_of_partners
        self.voice = Voice()
        self.voice.make_voice()
        self.no_of_x_points = no_of_x_points
        self.fitness = fitness
        self.generation = generation
        self.no_of_x_points = no_of_x_points
        self.no_of_partners = no_of_partners
        self.mutation_values = mutation_values
        self.no_of_mutation_functions = no_of_mutation_functions
        self.mutation_functions = mutation_functions

        #Set up mutation functions; set values...
        for t in mutation_types_and_limits.keys():
            if not mutation_values[t]:
                lower_bound = mutation_types_and_limits[t][0]
                upper_bound = mutation_types_and_limits[t][1]
                value = random.randint(lower_bound, upper_bound)
                mutation_values[t] = value
        self.mutation_values = mutation_values

        #...and choose four possible operations for this creature.
        if not mutation_functions:
            for i in range(no_of_mutation_functions):
                picked_function = random.sample(mutation_values, 1)[0]
                self.mutation_functions.append(picked_function)

    def change_value(self, value, change_type,
                     current_wave_index=None,
                     attribute = None):
        """
        Change an individual value according to the rules in change

        :param value:
            The current value of the attribute
        :param change_type:
            The type of change to make (e.g mult)
        :param current_wave_index:
            The index of the wave being processed in self.voice.waves.
        :param attribute:
            The attribute to be changed.
        """
        if change_type == '+':
            out_value = value + self.mutation_values['+']
            if out_value <= 0:
                out_value = 0
        elif change_type == '*':
            out_value = value * self.mutation_values['*']
        elif change_type == '/':
            out_value = value / self.mutation_values['/']
        elif change_type == 'inherit_north':
            if current_wave_index != 0:
                from_wave = self.voice.waves[current_wave_index - 1]
            else:
                from_wave = self.voice.waves[-1]
            out_value = getattr(from_wave,attribute)
        elif change_type == 'inherit_south':
            if current_wave_index != len(self.voice.waves) - 1:
                from_wave = self.voice.waves[current_wave_index + 1]
            else:
                from_wave = self.voice.waves[0]
            out_value = getattr(from_wave,attribute)
        else:
            print change_type, " is not a possible mutation. Mutation " \
                               "cancelled"
            out_value = value
        return out_value

    def mutate(self,
               creature_params_and_limits,
               wave_params,
               mutation_coefficient=800,
               verbose=False
    ):
        """
        :type self: Creature
        :param creature_params_to_mutate:
            A list of creature parameters changeable through mutation.
        :param voice_params_to_mutate:
            A list of voice attributes changeable through mutation
        :param mutation_coefficient:
            The odds of mutation for any on e value will be
            len(voice_params_to_mutate) / mutation_coefficient
        """

        creature_params = creature_params_and_limits.keys()
        for param in creature_params:
            r = random.randint(0, mutation_coefficient)
            if r <= len(wave_params):
                try:
                    set_value = random.randint(0,creature_params_and_limits[param])
                    if verbose:
                        old = getattr(self, param)
                    setattr(self, param, set_value)
                    if verbose:
                        print "--MUTATING CREATURE--\n\tParameter: " + param +\
                          '\n\tOld value: ' + str(old) +\
                          '\n\tNew value: ' + str(set_value)
                except Exception as e:
                    print e
                    print "Did you forget to set the limits for " + param + "?"
                    continue

        for i, wave in enumerate(self.voice.waves):
            for param in wave_params:
                r = random.randint(0, mutation_coefficient)
                if r <= len(wave_params):
                    change_type = random.sample(self.mutation_functions,1)[0]
                    current = getattr(wave, param)
                    new = self.change_value(current, change_type, i, param)
                    if verbose:
                        print "--MUTATING WAVE--"
                        print '\tWave: ', i
                        print '\tParameter: ', param
                        print '\tChange type: ', change_type
                        print '\tOld value: ', current
                        print '\tNew value: ', new
                    setattr(self, param, new)

    def copulate(self, possible_partners,
                 mut_rate=0.05,
                 attributes=['frequency', 'length', 'prewait', 'postwait'],
                 waves_per_voice=30,
                ):
        """Mixes the attributes of alpha with that of each voice in other.
        Returns a new creature.

        :type possible_partners: object
        :param possible_partners:
        :param mut_rate:
        :param attributes:
        :param waves_per_voice:
        possible_partners: list of Creatures
            The pool from which to pick the partners. Should not contain self.
        mut_rate: float
            The likelihood that a given value will mutate. Not used yet.
        attributes: list of str
            The Voice attributes which can be changed during copulation
        """
        point_index = 0
        out = Creature()
        out.generation = self.generation + 1

        #No self love
        if self in possible_partners:
            possible_partners.remove(self)

        possible_points = waves_per_voice * len(attributes)

        #Define limits for creature attributes:
        x_points_limit = possible_points - 1
        no_of_partners_limit = len(possible_partners)

        #Generate x_points and no_of_partners for self if not already present.
        if not self.no_of_partners:
            self.no_of_partners = random.randint(0, no_of_partners_limit)
        if not self.no_of_x_points:
            self.no_of_x_points = random.randint(0, x_points_limit)

        x_points = random.sample(range(possible_points), self.no_of_x_points)

        #Choose the voices who will pass on their genes this time...
        fertile_creatures = choose_partners(possible_partners,
                                            self.no_of_partners)
        fertile_creatures.append(self)

        #...and the one to be written first.
        dominant_creature = random.sample(fertile_creatures, 1)[0]

        #Inherit wave attributes
        for i, wave in enumerate(out.voice.waves):
            for attr in attributes:
                if point_index in x_points:
                    dominant_creature = random.sample(fertile_creatures, 1)[0]
                set_value = getattr(dominant_creature.voice.waves[i], attr)
                setattr(out.voice.waves[i], attr, set_value)
                point_index += 1

        #And others
        partners_parent = choose_partners(fertile_creatures, 1)[0]
        out.no_of_partners = partners_parent.no_of_partners
        x_points_parent = choose_partners(fertile_creatures, 1)[0]
        out.no_of_x_points = x_points_parent.no_of_x_points

        #Mutate wave
        out.mutate({'no_of_x_points':x_points_limit, 'no_of_partners':no_of_partners_limit}, attributes, verbose=True)

        #Construct wave points
        out.voice.points = merge(out.voice.waves)

        return out


def check_limits(name, value):
    """
    Given a variable and it's defined values in make_voice, will error if these
    values are outside the bounds set here.
    Note: 'None' means no limit."""

    limits = {'no_of_waves': (0, None),
              'wave_length': (0, None),
              'freq_range': (0, None),
              'amplitude': (0, 1),
              'prewait': (0, None),
              'postwait': (0, None), }

    if name == 'shape':
        if value not in possible_shapes:
            print "You have tried to generate a wave with shape " + value + \
                  ". Possible shapes are " + ', '.join(possible_shapes) + "."
            """TURN THIS INTO AN EXCEPTION"""

    elif name == 'operation':
        if value not in possible_operations:
            print "You have tried to merge waves with operation " + \
                  value + ". Possible operations are " + \
                  ', '.join(possible_operations) + "."

    elif value < limits[name][0]:
        print "You have tried to define a voice with a " + name + \
              " of " + str(value) + ". " + \
              name + " has a lower limit of " + str(limits[name][0]) + \
              " and an upper limit of " + str(limits[name][1]) + "."

    elif limits[name][1]:
        if value > limits[name][1]:
            print "You have tried to define a voice with a " + name + " of " + \
                  str(value) + ". " + name + " has a lower limit of " + \
                  str(limits[name][0]) + " and an upper limit of " + \
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
            opl = possible_operations.append("any")
            op = [random.randint(0, len(possible_operations))]

            out_creature.voice.make_voice()
            out_creatures.append(out_creature)

        self.creatures = out_creatures


