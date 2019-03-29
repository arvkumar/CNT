import nest
import matplotlib.pyplot as plt
import numpy as np

# Visualize recordings
def visualSS(sdin, sdout):
    """Visualize spiking activities recorded from two spike detectors.

    Parameters
    ----------
    sdin : NEST spike_detector
        Activities of input neurons.
    sdout : NEST spike_detector
        Activities of output neurons.

    Returns
    -------
    figure, axes handler
        Handlers of visualized figure.

    """
    # Render
    plt.figure();
    f,arr = plt.subplots(2,1,figsize = [15,10],sharex=True)

    # Input
    inputs = nest.GetStatus(sdin, 'events')
    spikeIn = [event['times'] for event in inputs]
    arr[0].eventplot(spikeIn)
    arr[0].set_ylabel('input neuron')

    # Output
    outputs = nest.GetStatus(sdout, 'events')
    spikeOut = [event['times'] for event in outputs]
    arr[1].eventplot(spikeOut)
    arr[1].set_xlabel('time(ms)')
    arr[1].set_ylabel('output neuron')

    return f, arr

def visualVS(vm, sd):
    """Visualize vm recording together with spiking activities.

    Parameters
    ----------
    vm : NEST voltmeter
        Vm recording device.
    sd : NEST spike_detector
        Spike detecting device.

    Returns
    -------
    figure, axes handler
        Handlers of visualized figure.

    """
    # Render
    plt.figure();
    f,arr = plt.subplots(2,1,figsize = [15,10],sharex=True);

    times = nest.GetStatus(vm, "events")[0]["times"]

    # Recording
    potentials = nest.GetStatus(vm, "events")[0]["V_m"]
    arr[0].plot(times, potentials)
    arr[0].set_ylabel("V_m (mV)")

    # Events
    spikes = nest.GetStatus(sd, 'events')[0]["times"]
    arr[1].eventplot(spikes)
    arr[1].set_xlabel("time (ms)")
    arr[1].set_ylabel("Spikes")

    return f, arr

def visualVV(vmG, vmS, restV=-70):
    """Visualize vm recordings and one trial.

    Parameters
    ----------
    vmG : NEST voltmeter
        Vm recording devices.
    vmS : NEST voltmeter
        Vm recording device.

    Returns
    -------
    figure, axes handler
        Handlers of visualized figure.

    """
    # Render
    plt.figure();
    f,arr = plt.subplots(2,1,figsize = [15,10],sharex=True);

    times = nest.GetStatus(vmS, "events")[0]["times"]

    # Recording
    events = nest.GetStatus(vmG, "events")
    groupVs = [event["V_m"] for event in events]
    for potentials in groupVs:
        arr[0].plot(times, potentials)
    arr[0].set_ylabel("V_m (mV)")

    # Events
    potentials = nest.GetStatus(vmS, 'events')[0]["V_m"]
    potentialsum = np.sum(np.array(groupVs)-restV, axis=0)
    arr[1].plot(times, potentials)
    arr[1].plot(times, potentialsum+restV)
    arr[1].set_xlabel("time (ms)")
    arr[1].set_ylabel("V_m (mV)")

    return f, arr

# Visualize networks
def visualWM(I_neurons, O_neurons):
    """Extract and plot connection weight matrix of two neuron populations.

    Parameters
    ----------
    I_neurons : NEST neurons
        Input neuron populatoin.
    I_neurons : NEST neurons
        Output neuron populatoin.

    Returns
    -------
    Numpy array
        Connection matrix.

    """
    M = len(I_neurons)
    N = len(O_neurons)
    W = np.zeros([M, N])

    a = nest.GetConnections(I_neurons, O_neurons)
    c = nest.GetStatus(a, keys='weight')

    for idx, n in enumerate(a):
        W[n[0] - min(I_neurons), n[1] - min(O_neurons)] += c[idx]

    plt.imshow(W, extent=[0,M,0,N], aspect='auto')
    plt.xlabel('Input Neuron ID')
    plt.ylabel('Output Neuron ID')

    return W
