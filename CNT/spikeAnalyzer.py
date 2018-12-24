import numpy as np

def spike2bin(signal, template, kernel, dt):
    """Binning spikes from spiking times.

    Parameters
    ----------
    signal : ndarray
        Spiking times.
    template : ndarray
        Binning template.
    kernel : ndarray
        Spike convolution kernel.

    Returns
    -------
    ndarray
        Binned signal from spiking times.

    """
    if signal is []:
        return template
    else:
        for s in signal:
            template[int(s/dt)-1] = 1
        return np.convolve(template, kernel, 'same')

def spikeCoin(spikeMat, type=None):
    """Cout coincidence of several spike trains.

    Parameters
    ----------
    spikeMat : numpy matrix
        A matrix of binned spiking actitivities.
    type : int
        Coincidence normalization type.

    Returns
    -------
    type
        Description of returned object.

    """
    # Get number of trials
    N, _ = spikeMat.shape

    # Calculate coincidence
    coV = np.dot(spikeMat, np.transpose(spikeMat))

    # Normalize
    if type is None:
        # Absolute coincidence count
        pass
    elif type == 1:
        # Normalize to energy
        for i in range(N):
            energy = coV[i,i]
            if energy:
                coV[i] /= energy

    # Correlation
    cor = (np.sum(coV) - np.trace(coV))/N/(N-1)

    return coV, cor
