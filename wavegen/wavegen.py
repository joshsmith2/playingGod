#!/usr/bin/env python

import freqTools
import wavebender as wb
import sys
import matplotlib.pyplot as plot
from itertools import *
from numpy import absolute

def zeroes():
    """A generator which will return only zeroes.
    
    Used to create an empty voice
    """
    while True: 
        yield 0

class Voice:
    """A collection of waves and other points which make a noise. 
    
    Can be written to file.
    """
    points=zeroes() #Points is a generator, always.

    def __init__(self, sample_rate=44000, time=1):

        try:
            self.time 
        except:
            self.time = time

        try:
            self.sample_rate
        except:
            self.sample_rate = sample_rate

        no_of_samples = int(round(self.sample_rate * self.time))
        self.samples = [next(self.points) for i in range(no_of_samples)] 

    def plot_wave(self, num_points=None, style='k.'):
        """Use matplotlib to plot a graph of the wave

        num_points: int
            Number of samples to be plotted.
        style: str
            Point style - from http://matplotlib.org/api/pyplot_api.html
        """
        graph = plot.subplot(111)
        
        for i in range(num_points):
            graph.plot(i, self.samples[i], style)
        plot.show()

    def normalise(self):
        """Bring values of self.samples back between 1 and -1"""
        factor = max(absolute(self.samples))
        if factor != 1:
            for i in range(len(self.samples)):
                self.samples[i] = self.samples[i] / factor

    def write_to_wav(self, name="wavegen-voice.wav", location="." ):
        """Write the voice to a .wav file

        name: str
            The name of the file to be written
        location: path
            Where the file should be written to. Default is current working dir.
        """
        self.normalise()
        channels = ((self.samples,) for i in range(self.channels))
        samples = wb.compute_samples(channels, 
                                         self.sample_rate * self.time)

        wb.write_wavefile(name, samples=samples, 
                         nframes=self.sample_rate*self.time, nchannels=self.channels, 
                         sampwidth=2, framerate=self.sample_rate)

    def merge(waves,operation="+", norm=False):
        """Merge wave objects self and other.

        This will add, for each sample, a value to the current value.
        
        operation: string
            Determines how the sample values for self aand other will be combined.
            +   -- Sum the values
            *   -- Multiply the values
            avg -- Find the average of the values
            %   -- Returns self % other

        norm: bool
            If true, normalise each wave after calculating it
        """ 

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
                return (i+j)/2
        
        def merged_points(waves, operation, norm=False):
            """Given a list of wave objects, return a points generator

            waves: List of Waves
                The objects to be combined

            e.g wave.points=merged_points([wave1,wave2],"+")
            """
            seed = waves[0].points.next()
            for wave in waves[1:]:
                end_sample = wave.points.next()
            yield end_sample
    
    out_wave=Wave(0,0)

    #Check waves are all of the same sample rate:
    model_sample_rate = waves[0].sample_rate
    for wave in waves:
        if wave.sample_wave != model_sample_rate:
            print "At least two waves merged have differeng sample rates," + \
                  "making a merge impossible. Please correct this."
            sys.exit(1)

    out_wave.points=merged_points(waves, operation, norm)

#        if other.sample_rate != self.sample_rate:
#            print "Cannot merge two waves of different sample rates."
#            print "Current rate: ", self.sample_rate
#            print "New rate: ", other.sample_rate
#            sys.exit(1)
#
#
#        #Print prewait
#        for i in range( host_no_of_samples ):
#            if i > other.prewait:
#                self.samples[i] = calculate(self.samples[i],other.points.next(),operation)
#        for j in range(host_no_of_samples, other_no_of_samples):
#            if j > other.prewait:
#                self.samples.append(other.points.next())
#
#        if norm:
#            self.normalise()
#
#        if other_total_time > self.time:
#            self.time = other_total_time    

class Wave(Voice):    

    def __init__(self,frequency,time,
                 amplitude=0.5, 
                 channels=2,
                 sample_rate=44000,
                 prewait=0, 
                 postwait=0,
                 shape='sine', 
                 phase=0,
                 norm=False):
        """Initialise properties of wave objects"""

        self.frequency = frequency
        self.prewait = prewait
        self.postwait = postwait
        self.time = time
        self.sample_rate = sample_rate
        self.total_ticks = (self.sample_rate * time) + prewait + postwait
        self.amplitude = amplitude
        self.channels = channels
        self.shape = shape
        self.points = self.construct()
        self.phase = phase
        self.norm = norm
        
        Voice.__init__(self) #Call __init__ of parent class so attributes get loaded
 
    def construct(self):
        """Given a Wave object, produces a soundwave which can be written to file.

        Internal vars:
            waveform - the 'meat' of the wave, containing the sound rather than 0s for pre/postwait.
        """

        print "self.total_ticks: ", self.total_ticks

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
