import scipy.signal as signal
import matplotlib.pyplot as plt
import numpy as np
import RPi.GPIO as GPIO
import time
import math
import Adafruit_ADS1x15
import numpy as np

def hanningw(N):
    x=[]
    res=[]
    for n in range(N):
        x.append(.5-.5*(math.cos(2*math.pi*(n/(N-1)))))
    return(x)

def hammingw(N):
    x=[]
    res=[]
    for n in range(N):
        x.append(.5-(.46*(math.cos(2*math.pi*(n/(N-1))))))
    return(x)

def flattopw(N):
    x=[]
    res=[]
    for n in range(N):
        f1=math.cos(2*math.pi*(n/(N-1)))
        f2=math.cos(4*math.pi*(n/(N-1)))
        f3=math.cos(6*math.pi*(n/(N-1)))
        f4=math.cos(8*math.pi*(n/(N-1)))
        x.append(1-(1.93*f1)+(1.29*f2)-(.338*f3)+(0.028*f4))
    return(x)



def hamming(a):
    zero_crossings = np.where(np.diff(np.sign(a)))[0]
    inp=[]
    peak=0
    valley=0
    for i in a:
        inp.append(round(i,3))
    for i in inp:
        if max(inp)==i:
            peak=peak+1
        elif min(inp)==i:
            valley=valley+1
    #print(peak,valley,inp)
    if (peak==(valley+1) or peak==(valley-1) or peak==valley) and ((a[zero_crossings[0]]<0 and a[zero_crossings[1]]<0 and a[zero_crossings[2]]<0 and a[zero_crossings[3]]<0) or (a[zero_crossings[0]]>0 and a[zero_crossings[1]]>0 and a[zero_crossings[2]]>0 and a[zero_crossings[3]]>0)):
        return True
    else:
        return False

def hanning(a):
    if hamming(a)==False:
        return True
    else:
        return False



adc = Adafruit_ADS1x15.ADS1115()
GPIO.setmode(GPIO.BCM)
GPIO.setup(16, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(20, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GAIN = 1
inp=[]
for i in range((256)):
    value=adc.read_adc(3, gain=GAIN)
    inp.append((value-12984)/3750)



if hamming(inp)==True:
    l1=hammingw(N)
    l2=inp
    res=[]
    for i in range(N):
        res.append(l1[i]*l2[i])
        
    print("closely space sine wave detected")
    print("window selected: hamming")
    print("\n")
    b = signal.firwin(256, cutoff = [.3], window = "hamming")
    plt.plot(inp,label="input")
    plt.plot(res,label="Windowed")
    plt.legend(bbox_to_anchor=(0.,1.02,1.,.102),loc=3,ncol=2,mode="expand",borderaxespad=0.)
    plt.savefig('/home/pi/Pictures/out.png')
    plt.show()

    print("Amplitude accuracy is important: press button 1")
    while True:
        input1 = GPIO.input(16)
        if input1==False:
            l1=flattopw(N)
            l2=inp
            res=[]
            for i in range(N):
                res.append(l1[i]*l2[i])
            print("button 1 pressed")
            print('window selected: flattop')
            print("\n")
            b = signal.firwin(256, cutoff = [.3], window = "flattop")
            plt.plot(inp,label="input")
            plt.plot(res,label="Windowed")
            plt.legend(bbox_to_anchor=(0.,1.02,1.,.102),loc=3,ncol=2,mode="expand",borderaxespad=0.)
            plt.savefig('/home/pi/Pictures/out.png')
            plt.show()
            break
    

if hanning(inp)==True:
    l1=hanningw(N)
    l2=inp
    res=[]
    for i in range(N):
        res.append(l1[i]*l2[i])
    print("sine wave is detected")
    print("window selected: hanning")
    print("\n")
    b = signal.firwin(256, cutoff = [.3], window = "hanning")
    plt.plot(inp,label="input")
    plt.plot(res,label="Windowed")
    plt.legend(bbox_to_anchor=(0.,1.02,1.,.102),loc=3,ncol=2,mode="expand",borderaxespad=0.)
    plt.savefig('/home/pi/Pictures/out.png')
    plt.show()

    print("Amplitude accuracy is important: press button 1")
    while True:
        input1 = GPIO.input(16)
        if input1==False:
            l1=hammingw(N)
            l2=inp
            res=[]
            for i in range(N):
                res.append(l1[i]*l2[i])
            print("button 1 pressed")
            print('window selected: flattop')
            print("\n")
            b = signal.firwin(256, cutoff = [.3], window = "flattop")
            plt.plot(inp,label="input")
            plt.plot(res,label="Windowed")
            plt.legend(bbox_to_anchor=(0.,1.02,1.,.102),loc=3,ncol=2,mode="expand",borderaxespad=0.)
            plt.savefig('/home/pi/Pictures/out.png')
            plt.show()
            break
    



