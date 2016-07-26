# imports of both spynnaker and external device plugin.
import spynnaker.pyNN as Frontend
import spynnaker_external_devices_plugin.pyNN as ExternalDevices

#######################
# import to allow prefix type for the prefix eieio protocol
######################
from spynnaker_external_devices_plugin.pyNN.connections\
    .spynnaker_live_spikes_connection import SpynnakerLiveSpikesConnection

# plotter in python
import pylab
import time
import random
import threading

import time
import rospy
from std_msgs.msg import Int8
from spinn_wrapper.msg import Spike



#pub = rospy.Publisher('/output_spikes', Int8, queue_size = 10)
pub = rospy.Publisher('/output_spikes', Spike, queue_size = 10)

def spike_received_ros_callback(msg):
    #id = msg.data
    id = msg.id
    label = msg.label
    print "Received spike from external device: " + str(id) + " with population label " + str(label)
    #live_spikes_connection_send.send_spike("spike_injector",id)
    live_spikes_connection_send.send_spike(label,id)

#subscriber = rospy.Subscriber('/input_spikes', Int8, spike_received_ros_callback)
subscriber = rospy.Subscriber('/input_spikes', Spike, spike_received_ros_callback)


# Create an initialisation method
def init_pop(label, n_neurons, run_time_ms, machine_timestep_ms):
    print "{} has {} neurons".format(label, n_neurons)
    print "Simulation will run for {}ms at {}ms timesteps".format(
        run_time_ms, machine_timestep_ms)

# Create a receiver of live spikes
def receive_spikes(label, time, neuron_ids):
    global pub
    for neuron_id in neuron_ids:
        #pub.publish(neuron_id)
        msg = Spike()
        msg.id = neuron_id
        msg.label = label
        pub.publish(msg)


# initial call to set up the front end (pynn requirement)
Frontend.setup(timestep=1.0, min_delay=1.0, max_delay=144.0)

# neurons per population and the length of runtime in ms for the simulation,
# as well as the expected weight each spike will contain
n_neurons = 15000
run_time = 800000
weight_to_spike = 2.0

# neural parameters of the ifcur model used to respond to injected spikes.
# (cell params for a synfire chain)
cell_params_lif = {'cm': 0.25,
		  'i_offset': 0.0,
		  'tau_m': 20.0,
		  'tau_refrac': 2.0,
		  'tau_syn_E': 5.0,
		  'tau_syn_I': 5.0,
		  'v_reset': -70.0,
		  'v_rest': -65.0,
		  'v_thresh': -50.0
		  }

##################################
# Parameters for the injector population.  This is the minimal set of
# parameters required, which is for a set of spikes where the key is not
# important.  Note that a virtual key *will* be assigned to the population,
# and that spikes sent which do not match this virtual key will be dropped;
# however, if spikes are sent using 16-bit keys, they will automatically be
# made to match the virtual key.  The virtual key assigned can be obtained
# from the database.
##################################
cell_params_spike_injector = {

    # The port on which the spiNNaker machine should listen for packets.
    # Packets to be injected should be sent to this port on the spiNNaker
    # machine
    'port': 12345,
}


##################################
# Parameters for the injector population.  Note that each injector needs to
# be given a different port.  The virtual key is assigned here, rather than
# being allocated later.  As with the above, spikes injected need to match
# this key, and this will be done automatically with 16-bit keys.
##################################
cell_params_spike_injector_with_key = {

    # The port on which the spiNNaker machine should listen for packets.
    # Packets to be injected should be sent to this port on the spiNNaker
    # machine
    'port': 12346,

    # This is the base key to be used for the injection, which is used to
    # allow the keys to be routed around the spiNNaker machine.  This
    # assignment means that 32-bit keys must have the high-order 16-bit
    # set to 0x7; This will automatically be prepended to 16-bit keys.
    'virtual_key': 0x70000,
}

# create synfire populations (if cur exp)
#pop = Frontend.Population(n_neurons, Frontend.IF_curr_exp,
				  #cell_params_lif, label='pop')
				  
pop_one = Frontend.Population(n_neurons, Frontend.IF_curr_exp,
				  cell_params_lif, label='pop_one')




# Create injection populations
#injector = Frontend.Population(
    #n_neurons, ExternalDevices.SpikeInjector,
    #cell_params_spike_injector_with_key, label='spike_injector')

injector_one = Frontend.Population(
    n_neurons, ExternalDevices.SpikeInjector,
    cell_params_spike_injector_with_key, label='spike_injector_one')



# Create a connection from the injector into the populations
#Frontend.Projection(injector, pop,
		    #Frontend.OneToOneConnector(weights=weight_to_spike))

Frontend.Projection(injector_one, pop_one,
		    Frontend.OneToOneConnector(weights=weight_to_spike))




# Activate the sending of live spikes
#ExternalDevices.activate_live_output_for(
    #pop, database_notify_host="localhost",
    #database_notify_port_num=19996)

ExternalDevices.activate_live_output_for(
    pop_one, database_notify_host="localhost",
    database_notify_port_num=19996)




# Set up the live connection for sending spikes
#live_spikes_connection_send = SpynnakerLiveSpikesConnection(
    #receive_labels=None, local_port=19999,
    #send_labels=["spike_injector"])
 

live_spikes_connection_send = SpynnakerLiveSpikesConnection(
    receive_labels=None, local_port=19999,
    send_labels=["spike_injector_one"])



# Set up callbacks to occur at initialisation
#live_spikes_connection_send.add_init_callback(
    #"spike_injector", init_pop)
    
    
live_spikes_connection_send.add_init_callback(
    "spike_injector_one", init_pop)





#live_spikes_connection_receive = SpynnakerLiveSpikesConnection(
	#receive_labels=["pop"],
	#local_port=19996, send_labels=None)
	
live_spikes_connection_receive = SpynnakerLiveSpikesConnection(
	receive_labels=["pop_one"],
	local_port=19996, send_labels=None)





# Set up callbacks to occur when spikes are received
#live_spikes_connection_receive.add_receive_callback(
	#"pop", receive_spikes)
	
	
live_spikes_connection_receive.add_receive_callback(
	"pop_one", receive_spikes)






def run():

  Frontend.run(run_time)

  Frontend.end()
