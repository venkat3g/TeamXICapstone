import numpy as np


def srrc_old(D, alpha, P):
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

    k = np.arange(-D, D, 1.0 / P)
    N = D * P * 2 + 1
    h_rrc = np.zeros(N, dtype=float)

    g = [(np.sin(np.pi * (1 - alpha) * v) + (4 * alpha * v) * np.cos(np.pi * (1+alpha) * v)) \
        / ((np.pi * v) * (1-(4*alpha*v)**2))/np.sqrt(P) \
        for v in k]

    for x in range(N - 1):
        if k[x] == 0:
            h_rrc[x] = 1.0 - alpha + (4 * alpha / np.pi)
        else:
            h_rrc[x] = g[x]

    return h_rrc


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

    N = D * P * 2 + 1
    k = np.linspace(-D, D, N)

    g = (np.sin(np.pi * (1 - alpha) * k) +
         (4 * alpha * k) * np.cos(np.pi * (1 + alpha) * k)) / (
             (np.pi * k) * (1 - (4 * alpha * k)**2)) / np.sqrt(P)

    # fill in for denominator zeros
    g[k == 0] = (1 + (4 / np.pi - 1) * alpha) / np.sqrt(P)
    g[abs(abs(4 * alpha * k) -
          1) < np.sqrt(np.finfo(float).eps)] = alpha / np.sqrt(2 * P) * (
              (1 + 2 / np.pi) * np.sin(np.pi / 4 / alpha) +
              (1 - 2 / np.pi) * np.cos(np.pi / 4 / alpha))

    return g
