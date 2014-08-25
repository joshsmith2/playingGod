#!/usr/bin/env python

"""Used to generate waves, merge these into more complex voices, plot them and
write them to .wav files."""

#import freqTools
import wavebender as wb
import sys
import matplotlib.pyplot as plot
import inspect
from numpy import absolute
import random
from pprint import pprint
from freqtools import *

"""Globals"""
global possible_operations #See calculate()
possible_operations = ["+","*","avg"]

global possible_shapes #See construct()
possible_shapes = ['sine', 'square', 'damped', 'white_noise']


def zeroes():
    """A generator which will return only zeroes.

    Used to create an empty voice
    """
    while True:
        yield 0

def print_vars(obj):
    pprint(variables(obj))

def variables(self):
    """Returns the defined variables of an selfect wave as a dictionary

    Particularly designed for waves / voices."""
    members = inspect.getmembers(self)
    out_dict = {}

    for member in members:
        m_name = member[0]
        m_value = member[1]
        if not '__' in m_name:
            if not inspect.ismethod(m_value) and not inspect.isgenerator(m_value):
                if m_name != 'waves' and m_name != 'samples':
                    out_dict[m_name] = m_value
    return out_dict

def calculate(i,j,operation):
    """Merge i and j according to operation, return a float.

    operation: string
        The operation to be performed on i and j. Determines the
        +   -- Sum i and j
        *   -- Multiply i and j
        avg -- Find the average of i and j
    """

    if operation == "+":
        return i+j
    elif operation == "*":
        if i == 0:
            out = j
        elif j == 0:
            out = i
        else:
            out = i*j
        return out

    elif operation == "avg":
        return (i+j)/2.0

def merge(voices,operation="+",norm=False):
    """Merge a list  of voices or waves together. Outputs a generator used for voice.points

    operation: string
        Determines how the sample values for the waves will be combined.
        +   -- Return waves[0] + waves[1] + ...
        *   -- Return  waves[0] * waves[1] * ...
        avg -- Return the average of waves[0], waves[1]

    norm: bool
        If true, normalise each wave after calculating it
    """

    def points_generator():
        """Returns a generator representing voices combined using operation.
        """

        sample = voices[0].points.next()
        for voice in voices[1:]:
            sample = calculate(sample,voice.points.next(),operation)
        yield sample

    out_voice=Voice()

    #Check voices are all of the same sample rate:
    model_sample_rate = voices[0].sample_rate
    for voice in voices:
        if voice.sample_rate != model_sample_rate:
            print "At least two waves merged have differing sample rates," + \
                  "making a merge impossible. Please correct this."
            sys.exit(1)
        else:
            out_voice.waves.append(voice)

    return points_generator

class Voice:
    """A collection of waves and other points which make a noise.

    Can be written to file.

    sample_rate: int (Hz) - default: 44100
        Determines how many lengths per second the wave will be sampled to
        produce sound.

    channels: int - default 1
        No of channels. Still not sure what this means but it's in wavebender.

    generation: int - default 0
        Which generation of creatures this voice belongs to.

    no_of_waves: int
         The number of waves to be merged into the voice. Should be the same
         across all voices in a generation.

    """
    def __init__(self,
                 sample_rate=44100,
                 channels=1,
                 generation=0,
                 no_of_waves=30,
                 no_of_active_waves=10):

        self.sample_rate = sample_rate
        self.points=zeroes()
        self.channels = channels
        self.waves = []
        self.generation = generation
        self.no_of_waves = no_of_waves
        self.no_of_active_waves = no_of_active_waves


    def activate_waves(self):
        """Change the 'active' attribute of a random selection of waves in
        self.waves, so that no_active are active."""
        try:
            activate_these = random.sample(self.waves, self.no_of_active_waves)

        except ValueError as e:
            print "Error: " + str(e) + "\n" +\
                  "Waves activated: " + str(self.no_of_active_waves) + "\n" +\
                  "Waves in voices: " + str(len(self.waves)) + "\n" +\
                  "Activating them all"
            activate_these = self.waves

        for wave in self.waves:
            if wave in activate_these:
                wave.active = True
            else:
                wave.active = False

    def make_voice(self,
                   active_waves_range=None,
                   length_range=(0,60),
                   freq_range=(2,6000),
                   amp_range=(0.01,0.99),
                   prewait_range=(0,88000),
                   postwait_range=(0,88000),
                   shape='sine',
                   operation='+'):
        """

        Construct a Voice from a random number of waves, with various shapes,
        frequencies and amplitudes, all within predefined boundaries, and return a
        creature with this voice.

        Each argument is a tuple of minumum and maximum values. The resulting
        voice's attributes will be a random value from this range.

        active_waves_range: tuple of ints
             The number of waves you will actually hear.

        length_range(min,max): tuple of floats
             The duration of the audible portion of each wave

        freq_range(min,max): tuple of ints
             The minimum and maximum possible frequencies, in Hz, for each wave.

        amp_range(min,max):
             The amplitude of each wave

        prewait_range(min,max):
             The number of ticks to wait before writing the audible part of the
             wave.

        postwait_range(min,max):
             The number of ticks to wait after writing the audible part of the
             wave.

        shape: str
             The shape of each wave. A value from possible_shapes, or any
             to have a random shape rolled for each wave.

        operation: str
             The operation (e.g addition) with which to merge the waves together
        """

        if not active_waves_range:
            active_waves_range = (1, self.no_of_waves)

        #Convert freq values to mils
        mils_range = (freq_to_mils(freq_range[0]),freq_to_mils(freq_range[1]))

        #Start to generate values from the supplied ranges.
        self.no_of_active_waves = random.randint(active_waves_range[0],
                                                 active_waves_range[1])

        constituent_waves=[]

        for n in range(self.no_of_waves):

            #Generate definitive values for wave attributes
            length = random.uniform(length_range[0], length_range[1])
            amplitude = random.uniform(amp_range[0], amp_range[1])
            prewait = random.randint(prewait_range[0], prewait_range[1])
            postwait = random.randint(postwait_range[0], postwait_range[1])
            mils = random.randint(mils_range[0], mils_range[1])
            frequency = mils_to_freq(mils)

            if operation == 'any':
                operation = random.sample(possible_operations,1)[0]

            constituent_waves.append(Wave(frequency,
                                          length,
                                          amplitude,
                                          prewait=prewait,
                                          postwait=postwait,
                                          shape=shape,)
                                     )

        self.waves = constituent_waves
        self.activate_waves()
        active_waves = [w for w in self.waves if w.active]
        self.points = merge(active_waves, operation)

    def plot_wave(self, num_points=1000, style='k.'):
        """Use matplotlib to plot a graph of the wave

        num_points: int
            Number of samples to be plotted.
        style: str
            Point style - from http://matplotlib.org/api/pyplot_api.html
        """
        graph = plot.subplot(111)

        for i in range(num_points):
            graph.plot(i, self.points().next(), style)
        plot.show()

    def normalise(self):
        """Bring values of self.samples back between 1 and -1"""

        factor = max(absolute(self.samples))

        if factor != 1:
            for i in range(len(self.samples)):
                self.samples[i] = self.samples[i] / factor

    def write_to_wav(self, name="wavegen-voice.wav", length=1, location="."):
        """Write the voice to a .wav file

        name: str
            The name of the file to be written
        location: path
            Where the file should be written to. Default is current working dir.
        """

        ext = ".wav"
        if name[:-len(ext)] != ext:
            name = str(name) + ".wav"

        #Generate a finite list of samples from our points generator
        no_of_samples = length * self.sample_rate
        self.samples = []

        for tick in range(no_of_samples):
            self.samples.append(self.points().next())


        self.normalise()
        channels = ((self.samples,) for i in range(self.channels))
        computed_samples = wb.compute_samples(channels, no_of_samples)

        wb.write_wavefile(name,
                          samples=computed_samples,
                          nframes=no_of_samples,
                          nchannels=self.channels,
                          sampwidth=2,
                          framerate=self.sample_rate)



class Wave(Voice):

    def __init__(self,frequency,length,
                 amplitude=0.5,
                 sample_rate=44100,
                 prewait=0,
                 postwait=0,
                 shape='sine',
                 phase=0,
                 norm=False,
                 active=True):
        """Initialise properties of wave objects"""
        Voice.__init__(self, sample_rate = sample_rate)
        #Call __init__ of parent class so attributes get loaded

        self.frequency = frequency
        self.prewait = prewait
        self.postwait = postwait
        self.length = length
        self.sample_rate = sample_rate
        self.total_ticks = (sample_rate * length) + prewait + postwait
        self.amplitude = amplitude
        self.phase = phase
        self.norm = norm
        self.active = active
        self.waves = [self] #This may seem ludicrous but is needed when defining voices.
        self.points = self.construct()
        if shape == 'any':
            self.shape = random.sample(possible_shapes, 1)[0]
        else:
            self.shape = shape

    def construct(self):
        """Given a Wave object, produces a soundwave which can be written to
           file.

        Global vars:

        possible_shapes: List of strings
            used to keep track of what kinds of waves can be constructed in a
            way which can be queried by other modules.

        Internal vars:
        waveform:
            The audible protion of the wave.

        """

        if self.shape == 'sine':
            waveform =  wb.sine_wave(self.frequency,
                                self.sample_rate, self.amplitude)
        if self.shape == 'square':
            waveform = wb.square_wave(self.frequency,
                                  self.sample_rate, self.amplitude)
        if self.shape == 'damped':
            waveform = wb.damped_wave(self.frequency,
                                  self.sample_rate, self.amplitude)
        if self.shape == 'white_noise':
            waveform  = wb.white_noise(self.amplitude)

        i=-1 #A counter to keep position in the waveform.
        before_postwait = self.total_ticks - self.postwait

        while True:

            i+=1
            cursor = i % self.total_ticks
            #Cursor here represents the position in the waveform

            if cursor <= self.prewait:
                yield 0
            elif self.prewait < cursor <= before_postwait:
                yield waveform.next()
            else:
                yield 0
