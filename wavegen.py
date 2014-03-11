#!/usr/bin/env python

import freqtools
import wavebender as wb
import sys
import matplotlib.pyplot as plot
from itertools import *
from numpy import absolute

debug = None

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

        Plots num_points points
    
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

    def write_to_wav(self, name="Wavefile", location="." ):
        """Write the voice to a .wav file"""
        self.normalise()
        channels = ((self.samples,) for i in range(self.channels))
        samples = wb.compute_samples(channels, 
                                         self.sample_rate * self.time)

        wb.write_wavefile(name, samples=samples, 
                         nframes=self.sample_rate*self.time, nchannels=self.channels, 
                         sampwidth=2, framerate=self.sample_rate)

    def merge(self,other):
        """Add a generator to this voice. 

        This will add, for each sample, a value to the current value.

        """
        if other.sample_rate != self.sample_rate:
            print "Cannot merge two waves of different sample rates."
            print "Current rate: ", self.sample_rate
            print "New rate: ", other.sample_rate
            sys.exit(1)


        other_total_time = other.time + other.prewait

        host_no_of_samples = int(round(self.time * self.sample_rate))
        other_no_of_samples = int(round(other_total_time * other.sample_rate))
        other_no_of_pw_samples = int(round(other.prewait * other.sample_rate))

        #Print prewait
        for i in range( host_no_of_samples ):
            if i > other_no_of_pw_samples:
                self.samples[i] = self.samples[i] + other.points.next()
        for j in range(host_no_of_samples, other_no_of_samples):
            if j > other_no_of_pw_samples:
                self.samples.append(other.points.next())

        if other_total_time > self.time:
            self.time = other_total_time    

class Wave(Voice):
    
    def __init__(self, frequency, time, amplitude=0.5, channels=2, sample_rate=44000, prewait=0, postwait=0, shape='sine', phase=0):
        """Initialise properties of wave objects"""

        self.frequency = frequency
        self.prewait = prewait
        self.postwait = postwait
        self.time = time
        self.total_time = time + prewait + postwait
        self.amplitude = amplitude
        self.channels = channels
        self.sample_rate = sample_rate
        self.shape = shape
        self.points = self.construct()
        self.phase = phase
        
        Voice.__init__(self) #Call __init__ of parent class so attributes get loaded
    
    def construct(self):
        if self.shape == 'sine':
            return wb.sine_wave(self.frequency, 
                                self.sample_rate, self.amplitude)
        if self.shape == 'square':
            return wb.square_wave(self.frequency,
                                  self.sample_rate, self.amplitude)
        if self.shape == 'damped':
            return wb.damped_wave(self.frequency,
                                  self.sample_rate, self.amplitude)
        if self.shape == 'white_noise':
            return wb.white_noise(self.amplitude)

#General functions
def freq_at_octave(freq_at_zero, target_octave):
    """Used to facilitate frquency calculations at different octaves
    
    Given the frequency at octave 0, returns the frequency at 
    target_octave.
    """
    target_frequency = 0

    if target_octave<0:
        b = (target_octave*-2)/2
    else:
        b = target_octave


    for a in range(0,b):
        if target_octave>0:
           target_frequency *=2
        else:
           target_frequency /=2
    target_frequency = freq_at_zero
    return target_frequency;

out=Wave(410,17)
A=Wave(415,6, prewait=1.3)
B=Wave(412,7,prewait=4)
C=Wave(400,7,prewait=0.52)
D=Wave(2,4, prewait=9)
E=Wave(807,5, prewait=10)

outList=[A,B,C,D,E]

for p in outList:
    out.merge(p)

out.write_to_wav('wills.wav')
