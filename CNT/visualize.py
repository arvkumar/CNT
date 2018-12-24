import nest
import matplotlib.pyplot as plt

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
