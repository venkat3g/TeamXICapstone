import numpy as np


def srrc(D, alpha, P):
    """
    Generates a root raised cosine (RRC) filter (FIR) impulse response.
    Parameters
    ----------
    D : int
        Half-length of the pulse
    alpha : float
        Roll off factor (Valid values are [0, 1]).
    P : int
        Oversampling factor (how many samples in-between - 1)
    Returns
    ---------
    1-D ndarray of floats
    """

    k = np.arange(-D, D, 1.0/P)
    N = D*P*2+1
    h_rrc = np.zeros(N, dtype=float)
    
    g = [(np.sin(np.pi * (1 - alpha) * v) + (4 * alpha * v) * np.cos(np.pi * (1+alpha) * v)) \
        / ((np.pi * v) * (1-(4*alpha*v)**2))/np.sqrt(P) \
        for v in k]

    for x in range(N - 1):
        if k[x] == 0:
            h_rrc[x] = 1.0 - alpha + (4*alpha/np.pi)
        else:
            h_rrc[x] = g[x]

    return h_rrc
    

    