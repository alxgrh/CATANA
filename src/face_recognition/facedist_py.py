import numpy as np
from scipy.spatial.distance import cdist
from scipy.sparse import dok_matrix


def mean_dist(A):

    print(A.shape)
    
    nrow = A.shape[0]
    ncol = A.shape[1]

    # this line is particularly expensive, since creating a numpy array
    # involves unavoidable Python API overhead
    D = np.zeros( (nrow*(nrow-1)/2), np.float64)

    for ii in range(nrow):
        for jj in range(ii + 1, nrow):
            rd = np.mean(cdist(A[ii], A[jj], metric='euclidean'))
            nn = ii+jj*(jj-1)/2
            D[nn] = rd

    return D
