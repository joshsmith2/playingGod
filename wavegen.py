#!/usr/bin/env python

import wavebender as wb
import sys
import matplotlib.pyplot as plot
from itertools import *
from numpy import absolute

debug = None

#if sys.argv[1] == 'debug':
 ##   debug = "yes"


def zeroes():
    """A generator which will return only zeroes.
    
    Used to create an empty voice
    """
    while True: 
        yield 0

class Voice:
    """A collection of waves and other points to be written to file. 
    
    Starts life as a 0 length collection of zeroes.  
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
        This might need to be adjusted first in future.
        Also, let's see if we can pass a wave object rather than its attributes.

        """
        if other.sample_rate != self.sample_rate:
            print "Cannot merge two waves of different sample rates."
            print "Current rate: ", self.sample_rate
            print "New rate: ", other.sample_rate
            sys.exit(1)


        other_total_time = other.time + other.prewait

        host_no_of_samples = int(round(self.time * self.sample_rate))
        other_no_of_samples = int(round(other_total_time * other.sample_rate))
        other_no_of_prewait_samples = int(round(other.prewait * other.sample_rate))

        #Print prewait
        for i in range( host_no_of_samples ):
            if i > other_no_of_prewait_samples:
                self.samples[i] = self.samples[i] + other.points.next()
        for j in range(host_no_of_samples, other_no_of_samples):
            if j > other_no_of_prewait_samples:
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

#teste=Voice()

out=Wave(41,17)
A=Wave(9,3, prewait=1.3)
B=Wave(38,3.7,prewait=1.9,shape='square')
C=Wave(7,7,prewait=0.52, shape='white_noise')
D=Wave(5663, 0.7, prewait=2.89, shape='square')

outList=[A,B,C,D]

#teste.plot()
for p in outList:
    out.merge(p)

out.write_to_wav('wills.wav')
out.plot_wave(2000)

def oldWay():
    sRate = 44000
    sChannels = 2 
    sAmp = 0.5 
   
    tune=[]
    times=[0.6,0.2,0.4,0.4,0.4,0.4,1.2]
    pitches=[440, 420, 440, 660, 550, 660, 880]
    tune.append(times)
    tune.append(pitches)
    
    totalTime=sum(times)
 
    for t in range(len(tune[0])):
    
        if t==0:
            first_wave = Wave(tune[1][0], tune[0][0])
            out = first_wave.samples
        else:
            next_wave = Wave(tune[1][t], tune[0][t])
            out = chain(out, next_wave.samples)
    
    print out   

    for o in out:
        print o

    #first_wave.plot()
    
    wb.write_wavefile("./2by440TestOut.wav", samples=out, nframes=sRate * totalTime, nchannels=sChannels, sampwidth=2, framerate=sRate)


#oldWay()
