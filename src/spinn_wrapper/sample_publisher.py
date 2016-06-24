__author__ = 'mateev'
import threading
import rospy
from std_msgs.msg import Int8
import time
import random
from collections import deque
import matplotlib.pyplot as plt
import numpy as np

start_time = time.time()
sources = []
import cv2
from spinn_wrapper.msg import Spike

#import a random grayscale image for testing purposes, extract 5 different values
img = cv2.imread('/fzi/ids/mateev/catkin_ws/src/spinn_wrapper/src/spinn_wrapper/image.png',0)
print np.shape(img)
img_values = np.array([img[0,0], img[0,220], img[0,440],img[0,660],img[0,880]])
print np.shape(img_values)
print img_values

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
                print "published a spike! Neuron ID: " + str(self.neuron_id) + " of population " + str(self.pop_label)
                time.sleep(0.1)
            else:
                print "No spike! Neuron ID: " + str(self.neuron_id) + " of population " + str(self.pop_label)
                time.sleep(0.1)

    def __init__(self,publish,id,label,minimum,maximum,spikerate=0):
        self.rate = spikerate
        self.publisher = publish
        self.neuron_id = id
        self.pop_label = label
        self.min_value = minimum
        self.max_value = maximum

    def encode_value(self,value):
        print "Value to encode: " + str(value)
        self.rate = float((value-self.min_value))/float((self.max_value - self.min_value))

use_colours = {0: 'red', 1: 'green'}
#lists of ids of the spiked neurons and their respective spike times
times = deque([0]*1000,1000)
ids = deque([0]*1000,1000)
labels = deque([0]*1000,1000)

#set up an interactive plot
fig = plt.figure()
ax = fig.add_subplot(111)
ax.set_xlim([0,200])
ax.set_ylim([0,100])
ax.set_xlabel("Time")
ax.set_ylabel("Neuron ID")
ax.set_title("Spiking activity of SpiNNaker population")
scat = ax.scatter(times, ids, c = labels, s = 15)
manager = plt.get_current_fig_manager()
manager.show()


#create spike sources for each value (could be a pixel) we want to represent
for i in range(len(img_values)):
    if i < 2:
      src = UniformSource(pub,(i+1)*10,"spike_injector_one",0,255)
    else:
      src = UniformSource(pub,(i+1)*10,"spike_injector_two",0,255)
    sources.append(src)

#function to update plot at runtime
def RealtimePlotter(arg):
  global times, ids,labels,scat
  container_lock.acquire()
  data = zip(times,ids)
  scat.set_offsets(data)
  c = [use_colours[x] for x in labels]
  container_lock.release()
  scat.set_color(c)
  manager.canvas.draw()

#publish spikes at a rate according to the encoded value
def publish_uniform():
    global pub, sources
    #sources[index].encode_value(rate)
    while not rospy.is_shutdown():
        for l in range(len(sources)):
            sources[l].publish_spike()
            print "Invoked publish_spike for source " + str(l)

#encode the given values in the created sources
def encode_values():
    global sources
    for i in range(len(sources)):
        sources[i].encode_value(img_values[i])
        print "Encoded value " + str(img_values[i]) + " for source " + str(i)
        time.sleep(1)

#callback for spikes received from the spinnaker network, saves them in a queue-type container
def spike_received_from_spinnaker(msg):
    global times, ids, start_time, labels
    t = time.time() -start_time
    id = msg.id
    label = msg.label
    #print "Received spike: " + str(id)
    container_lock.acquire()
    times.appendleft(t)
    ids.appendleft(id)
    if label == "pop_one":
      labels.appendleft(1)
    elif label == "pop_two":
      labels.appendleft(0)
    else:
      print "EEEERRRORRRR"
    container_lock.release()

#subscriber used to receive spikes from spinnaker
subscriber = rospy.Subscriber('/output_spikes', Spike, spike_received_from_spinnaker)

#set everything up and start threads
def run():
  start = time.time()
  encode_values()
  timer = fig.canvas.new_timer(interval=1)
  timer.add_callback(RealtimePlotter, ())
  thread_publisher = threading.Thread(target = publish_uniform)
  timer.daemon = True
  thread_publisher.daemon = True
  thread_publisher.start()  
  timer.start()


  plt.show()

  









