#!/usr/bin/env python

"""Used to generate waves, merge these into more complex voices, plot them and
write them to .wav files."""

#import freqTools
import wavebender as wb
import sys
import matplotlib.pyplot as plot
from itertools import *
from numpy import absolute
from random import randrange

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

def calculate(i,j,operation):
    """Merge i and j according to operation, return a float.

    operation: string
        The operation to je performed on i and j. Determines the 
        +   -- Sum i and j
        *   -- Multiply i and j
        avg -- Find the average of i and j
    """

    if operation == "+":
        return i+j
    if operation == "*":
        return i*j   
    if operation == "avg":
        return (i+j)/2.0

def merge(voices,operation="+",norm=False):
    """Merge a list  of voices or waves together. Outputs a new voice.
    
    operation: string
        Determines how the sample values for the waves will be combined.
        +   -- Return waves[0] + waves[1] + ...
        *   -- Return  waves[0] * waves[1] * ...
        avg -- Return the average of waves[0], waves[1]

    norm: bool
        If true, normalise each wave after calculating it
    """ 
     
    def points_generator():
        """Returns a generator repesenting voices combined using operation.
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
            print "At least two waves merged have differeng sample rates," + \
                  "making a merge impossible. Please correct this."
            sys.exit(1)
        else:
            out_voice.waves.append(voice)

    out_voice.points=points_generator

    return out_voice

class Voice:
    """A collection of waves and other points which make a noise. 
    
    Can be written to file.
   
    sample_rate: int (Hz) - default: 44000
        Determines how many times per second the wave will be sampled to
        produce sound. 

    channels: int - default 2
        No of channels. Still not sure what this means but it's in wavebender.
    
    generation: int - default 0
        Which generation of creatures this voice belongs to.

    """
    def __init__(self,
                 sample_rate=44000, 
                 channels=2, 
                 generation=0):

        self.sample_rate = sample_rate
        self.points=zeroes()
        self.channels = channels
        self.waves = []
        self.generation = generation 

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
        #Generate a finite list of samples from our points generator
        no_of_samples = length * self.sample_rate
        self.samples = []
        for tick in range(no_of_samples):
            self.samples.append(self.points().next())

        self.normalise()
        channels = ((self.samples,) for i in range(self.channels))
        computed_samples = wb.compute_samples(channels, no_of_samples)

        wb.write_wavefile(name, samples=computed_samples, 
                         nframes=no_of_samples, nchannels=self.channels, 
                         sampwidth=2, framerate=self.sample_rate)

class Wave(Voice):    

    def __init__(self,frequency,time,
                 amplitude=0.5, 
                 sample_rate=44000,
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
        self.time = time
        self.sample_rate = sample_rate
        self.total_ticks = (sample_rate * time) + prewait + postwait
        self.amplitude = amplitude
        self.shape = shape
        self.phase = phase
        self.norm = norm
        self.active = active        
        self.waves = [self] #This may seem ludicrous but is needed when defining voices.
        self.points = self.construct()
 
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

