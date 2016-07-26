__author__ = 'mateev'

#TODO: Deal with resource sharing
# How many?

import threading
import rospy
from std_msgs.msg import Int8
import time
import random
from collections import deque
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import cv2
from spinn_wrapper.msg import Spike
import rwlock as lck



cap = cv2.VideoCapture("/fzi/ids/mateev/catkin_ws/src/spinn_wrapper/src/spinn_wrapper/360x240.mp4")
#Do this to make sure roscore starts before the script starts executing
failed = True
while failed == True:
  try:
    failed = False
    rospy.get_master().getPid()
  except:
    failed = True
    

start_time = time.time()
sources = []

#import a random grayscale image for testing purposes, extract 5 different values
#img = cv2.imread('/fzi/ids/mateev/catkin_ws/src/spinn_wrapper/src/spinn_wrapper/img.jpg',0)
#scaled_img = cv2.resize(img,(100,100))
pos_frame = cap.get(cv2.cv.CV_CAP_PROP_POS_FRAMES)
fnumber = cap.get(cv2.cv.CV_CAP_PROP_FRAME_COUNT)

while not cap.isOpened():
    cap = cv2.VideoCapture("/fzi/ids/mateev/catkin_ws/src/spinn_wrapper/src/spinn_wrapper/360x240.mp4")
    cv2.waitKey(1000)
    print "Wait for the header"
  
frame = cap.read()
frame_gray = cv2.cvtColor(frame[1],cv2.COLOR_RGB2GRAY)
#frame_gray.resize(np.shape(frame_gray)[0]/2,np.shape(frame_gray)[1]/2)
print "Frame size: "  + str(np.shape(frame_gray)) + "\n"
print "Frame number: " + str(pos_frame) +"\n"

#print np.shape(img)


pub = rospy.Publisher('/input_spikes', Spike, queue_size = 100)
container_lock = threading.Lock()

#An uniform spike source with an adjustable spiking rate, able to encode values in rates given a min and a max
class UniformSource:
    min_value = None
    max_value = None
    publisher = None
    rate = None
    neuron_id = None
    pop_label = None
    def publish_spike(self):
            i = np.random.uniform()
            if i <= self.rate:
		msg = Spike()
		msg.id = self.neuron_id
		msg.label = self.pop_label
                self.publisher.publish(msg)
                #print "published a spike! Neuron ID: " + str(self.neuron_id) + " of population " + str(self.pop_label)
                print str(self.neuron_id) + "!\n"
            else:
                #print "Nope\n"
                pass

    def __init__(self,publish,id,label,minimum,maximum,spikerate=0):
        self.rate = spikerate
        self.publisher = publish
        self.neuron_id = id
        self.pop_label = label
        self.min_value = minimum
        self.max_value = maximum

    def encode_value(self,value):
        self.rate = float((value-self.min_value))/float((self.max_value - self.min_value))
	#print "Value: " + str(value) + "\n"


#lists of ids of the spiked neurons and their respective spike times
times = deque([0]*10000,10000)
ids = deque([0]*10000,10000)
labels = deque([0]*10000,10000)

#set up an interactive plot
fig = plt.figure()
ax = fig.add_subplot(111)
ax.set_xlim([0,1000])
ax.set_ylim([0,10000])
ax.set_xlabel("Time")
ax.set_ylabel("Neuron ID")
ax.set_title("Spiking activity of SpiNNaker population")
scat = ax.scatter(times, ids, c = labels, s = 1)

#Create a legend with the different neuron populations in different colours
use_colours = {0: 'red', 1: 'green'}
recs = []
classes = ['Population one', 'Population two'] 
for i in range(0,len(use_colours)):
    recs.append(mpatches.Rectangle((0,0),1,1,fc=use_colours[i]))  
plt.legend(recs,classes,loc=4)

manager = plt.get_current_fig_manager()
manager.show()


#create spike sources for each value (could be a pixel) we want to represent
#scaled_img = scaled_img.flatten()
frame_gray = frame_gray.flatten()
#value_buf = list(frame_gray)
#print value_buf

for i in range(len(frame_gray)):
      src = UniformSource(pub,i,"spike_injector_one",0,255)
      sources.append(src)


#function to update plot at runtime
def RealtimePlotter(arg):
  global times, ids,labels,scat
  #container_lock.acquire()
  data = zip(times,ids)
  scat.set_offsets(data)
  c = [use_colours[x] for x in labels]
  #container_lock.release()
  scat.set_color(c)
  manager.canvas.draw()
  
ready_event = threading.Event()
arraylock = lck.RWLock()
#publish spikes at a rate according to the encoded value
def publish_uniform():
    global ready_event
    beg = time.time()
    print "Starting thread creation:\n" 
    global pub, sources
    #sources[index].encode_value(rate)
    #while not rospy.is_shutdown():

    for l in range(0,len(sources),4):
	arraylock.acquire_read()
	for k in range(l, l+3):
	  sources[k].encode_value(frame_gray[k])
	arraylock.release()
        publ = threading.Thread(target = publish_loop, args = (([sources[l],sources[l+1],sources[l+2],sources[l+3]]),l))
        publ.start()
	#sources[l].publish_spike()
        #print "Created thread number  " + str(l)
    end = time.time()
    print "Thread creation finished! Took " + str(end-beg) + " seconds for " + str(len(sources)/4) + " threads!\n"
    ready_event.set()
    
#publlock = threading.Lock()
def publish_loop(*args):
  global ready_event
  ready_event.wait()
  #print "Ready to publish!"
  global frame_gray
  while not rospy.is_shutdown():
    #publlock.acquire()

    for k in range(len(args[0])):
      arraylock.acquire_read()
      args[0][k].encode_value(frame_gray[args[1]+k])
      args[0][k].publish_spike()
      #print "Publishing..."
      arraylock.release()
      #time.sleep(0.03)
    #time.sleep(0.3)

    #publlock.release()
#encode the given values in the created sources


def encode_values():
    global sources
    global frame_gray
    st = time.time()
    for i in range(0,len(sources),4):
	#publlock.acquire()
	#arraylock.acquire()
	for k in range(i,i+3):
	  sources[k].encode_value(frame_gray[k])
        #arraylock.release()
        #publlock.release()
        #print "Encoded value " + str(scaled_img[i]) + " for source " + str(i)
    end = time.time()
    print "Encoding took " + str(end-st) + " seconds to complete!\n"
    
#def change_values():
    #global scaled_img
    #while(True):
      #randoms = random.sample(xrange(10000), 10)
      #sources[randoms] = 0

def get_frame():
    #global arraylock
    global  cap
    
    while(cap.isOpened()):
      start = time.time()
      #print "Entered while loop!"
      #arraylock.acquire()
      arraylock.acquire_write()
      frame = cap.read()
      #value_buf = cv2.cvtColor(frame[1],cv2.COLOR_RGB2GRAY)
      frame_gray = cv2.cvtColor(frame[1],cv2.COLOR_RGB2GRAY)
      pos_frame = cap.get(cv2.cv.CV_CAP_PROP_POS_FRAMES)
      #value_buf.resize(np.shape(value_buf)[0]/2,np.shape(value_buf)[1]/2)
      #print "Frame size: "  + str(np.shape(value_buf))
      #print "Frame number: " + str(pos_frame) + "\n"
      #value_buf= value_buf.flatten()
      frame_gray = frame_gray.flatten()
      arraylock.release()
      end = time.time()
      print "IT TOOK " + str(end - start)
      #input("Press enter!")
      #print value_buf
      #arraylock.release()
      if pos_frame == fnumber:
	print "End of video!\n"
	#break
	exit()
      #time.sleep(0.03)


#def sync_frame():
  #global value_buf, frame_gray, cap, arraylock
  #while (cap.isOpened()):
    #arraylock.acquire_write()
    #frame_gray = list(value_buf)
    #arraylock.release()
    #print "Syncing...\n"
    #time.sleep(0.03)


#callback for spikes received from the spinnaker network, saves them in a queue-type container
def spike_received_from_spinnaker(msg):
    global times, ids, start_time, labels
    t = time.time() -start_time
    id = msg.id
    label = msg.label
    #container_lock.acquire()
    times.appendleft(t)
    ids.appendleft(id)
    if label == "pop_one":
      labels.appendleft(0)
    elif label == "pop_two":
      labels.appendleft(1)
    else:
      print "ERROR!"
    #container_lock.release()

#subscriber used to receive spikes from spinnaker
subscriber = rospy.Subscriber('/output_spikes', Spike, spike_received_from_spinnaker)
#set everything up and start threads
def run():
  frameupdate = threading.Thread(target = get_frame)
  timer = fig.canvas.new_timer(interval=1)
  #framesync = threading.Thread(target = sync_frame)
  #timer = fig.canvas.new_timer()
  timer.add_callback(RealtimePlotter, ())
  #thread_publisher = threading.Thread(target = publish_uniform)
  timer.daemon = True
  #thread_publisher.daemon = True
  #thread_publisher.start() 
  encode_values()
  publish_uniform()
  timer.start()
  frameupdate.start()
  #framesync.start()
  #thread_change = threading.Thread(target = change_values)
  
  

  #thread_change.start()


  


  plt.show()

  





