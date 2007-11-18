"""
-----------------------------------------
Hierarchical Clustering Library for Scipy
    Copyright (C) Damian Eads, 2007.
          All Rights Reserved.
             New BSD License
-----------------------------------------

Flat cluster formation

 fcluster           forms flat clusters from hierarchical clusters.
 fclusterdata       forms flat clusters directly from data.
 leaders            singleton root nodes for flat cluster.

Agglomorative cluster formation

 linkage            agglomoratively clusters original observations.
 single             the single/min/nearest algorithm. (alias)
 complete           the complete/max/farthest algorithm. (alias)
 average            the average/UPGMA algorithm. (alias)
 weighted           the weighted/WPGMA algorithm. (alias)
 centroid           the centroid/UPGMC algorithm. (alias)
 median             the median/WPGMC algorithm. (alias)
 ward               the Ward/incremental algorithm. (alias)

Distance matrix computation from a collection of raw observation vectors

 pdist              computes distances between each observation pair.
 squareform         converts a sq. D.M. to a condensed one and vice versa.

Statistic computations on hierarchies

 cophenet           computes the cophenetic distance between leaves.
 from_mlab_linkage  converts a linkage produced by MATLAB(TM).
 inconsistent       the inconsistency coefficients for cluster.
 maxinconsts        the maximum inconsistency coefficient for each cluster.
 maxdists           the maximum distance for each cluster.
 maxRstat           the maximum specific statistic for each cluster.
 to_mlab_linkage    converts a linkage to one MATLAB(TM) can understand.

Visualization

 dendrogram         visualizes linkages (requires matplotlib).

Tree representations of hierarchies

 cnode              represents cluster nodes in a cluster hierarchy.
 lvlist             a left-to-right traversal of the leaves.
 totree             represents a linkage matrix as a tree object.

Distance functions between two vectors u and v

 braycurtis         the Bray-Curtis distance.
 canberra           the Canberra distance.
 chebyshev          the Chebyshev distance.
 cityblock          the Manhattan distance.
 correlation        the Correlation distance.
 cosine             the Cosine distance.
 dice               the Dice dissimilarity (boolean).
 euclidean          the Euclidean distance.
 hamming            the Hamming distance (boolean).
 jaccard            the Jaccard distance (boolean).
 kulsinski          the Kulsinski distance (boolean).
 mahalanobis        the Mahalanobis distance.
 matching           the matching dissimilarity (boolean).
 minkowski          the Minkowski distance.
 rogerstanimoto     the Rogers-Tanimoto dissimilarity (boolean).
 russellrao         the Russell-Rao dissimilarity (boolean).
 seuclidean         the normalized Euclidean distance.
 sokalmichener      the Sokal-Michener dissimilarity (boolean).
 sokalsneath        the Sokal-Sneath dissimilarity (boolean).
 sqeuclidean        the squared Euclidean distance.
 yule               the Yule dissimilarity (boolean).

Predicates

 is_valid_dm        checks for a valid distance matrix.
 is_valid_im        checks for a valid an inconsistency matrix.
 is_valid_linkage   checks for a valid hierarchical clustering.
 is_valid_y         checks for a valid condensed distance matrix.
 is_isomorphic      checks if two flat clusterings are isomorphic.
 is_monotonic       checks if a linkage is monotonic.
 Z_y_correspond     checks for validity of distance matrix given a linkage.

Utility Functions

 numobs_dm          # of observations in a distance matrix.
 numobs_linkage     # of observations in a linkage.
 numobs_y           # of observations in a condensed distance matrix.

Legal stuff

 copying            Displays the license for this package.


  MATLAB and MathWorks are registered trademarks of The MathWorks, Inc.
  Mathematica is a registered trademark of The Wolfram Research, Inc.

References:

 [1] "Statistics toolbox." API Reference Documentation. The MathWorks.
     http://www.mathworks.com/access/helpdesk/help/toolbox/stats/.
     Accessed October 1, 2007.

 [2] "Hierarchical clustering." API Reference Documentation.
     The Wolfram Research, Inc. http://reference.wolfram.com/...
     ...mathematica/HierarchicalClustering/tutorial/...
     HierarchicalClustering.html. Accessed October 1, 2007.
     
 [3] Gower, JC and Ross, GJS. "Minimum Spanning Trees and Single Linkage
     Cluster Analysis." Applied Statistics. 18(1): pp. 54--64. 1969.

 [4] Ward Jr, JH. "Hierarchical grouping to optimize an objective
     function." Journal of the American Statistical Association. 58(301):
     pp. 236--44. 1963.

 [5] Johnson, SC. "Hierarchical clustering schemes." Psychometrika.
     32(2): pp. 241--54. 1966.

 [6] Sneath, PH and Sokal, RR. "Numerical taxonomy." Nature. 193: pp.
     855--60. 1962.

 [7] Batagelj, V. "Comparing resemblance measures." Journal of
     Classification. 12: pp. 73--90. 1995.

 [8] Sokal, RR and Michener, CD. "A statistical method for evaluating
     systematic relationships." Scientific Bulletins. 38(22):
     pp. 1409--38. 1958.

 [9] Edelbrock, C. "Mixture model tests of hierarchical clustering
     algorithms: the problem of classifying everybody." Multivariate
     Behavioral Research. 14: pp. 367--84. 1979.

[10] Jain, A., and Dubes, R., "Algorithms for Clustering Data."
     Prentice-Hall. Englewood Cliffs, NJ. 1988.
"""

_copyingtxt="""
cluster.py

Author: Damian Eads
Date:   September 22, 2007

Copyright (c) 2007, Damian Eads

All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions
are met:
  - Redistributions of source code must retain the above
    copyright notice, this list of conditions and the
    following disclaimer.
  - Redistributions in binary form must reproduce the above copyright
    notice, this list of conditions and the following disclaimer
    in the documentation and/or other materials provided with the
    distribution.
  - Neither the name of the author nor the names of its
    contributors may be used to endorse or promote products derived
    from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
"AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""

import _cluster_wrap, scipy, scipy.stats, numpy, types, math, sys

_cpy_non_euclid_methods = {'single': 0, 'complete': 1, 'average': 2, 'weighted': 6}
_cpy_euclid_methods = {'centroid': 3, 'median': 4, 'ward': 5}
_cpy_linkage_methods = set(_cpy_non_euclid_methods.keys()).union(set(_cpy_euclid_methods.keys()))
_array_type = type(numpy.array([]))

try:
    import warnings
    def _warning(s):
        warnings.warn('scipy-cluster: %s' % s, stacklevel=3)
except:
    def _warning(s):
        print ('[WARNING] scipy-cluster: %s' % s)

def _copy_array_if_base_present(a):
    """
    Copies the array if its base points to a parent array.
    """
    if a.base is not None:
        return a.copy()
    else:
        return a
    
def _copy_arrays_if_base_present(T):
    """
    Accepts a tuple of arrays T. Copies the array T[i] if its base array
    points to an actual array. Otherwise, the reference is just copied.
    This is useful if the arrays are being passed to a C function that
    does not do proper striding.
    """
    l = [_copy_array_if_base_present(a) for a in T]
    return l
            

def copying():
    """ Displays the license for this package."""
    print _copyingtxt
    return None

def _randdm(pnts):
    """ Generates a random distance matrix stored in condensed form. A
        pnts * (pnts - 1) / 2 sized vector is returned.
    """
    if pnts >= 2:
        D = numpy.random.rand(pnts * (pnts - 1) / 2)
    else:
        raise ValueError("The number of points in the distance matrix must be at least 2.")
    return D

def single(y):
    """
    Z = single(y)

    Performs single/min/nearest linkage on the condensed distance
    matrix Z. See linkage for more information on the return structure
    and algorithm.

          (a condensed alias for linkage)
    """
    return linkage(y, method='single', metric='euclidean')

def complete(y):
    """
    Z = complete(y)

    Performs complete complete/max/farthest point linkage on the
    condensed distance matrix Z. See linkage for more information
    on the return structure and algorithm.

      (a condensed alias for linkage)
    """
    return linkage(y, method='complete', metric='euclidean')

def average(y):
    """
    Z = average(y)

    Performs average/UPGMA linkage on the condensed distance matrix Z. See
    linkage for more information on the return structure and algorithm.

      (a condensed alias for linkage)
    """
    return linkage(y, method='average', metric='euclidean')

def weighted(y):
    """
    Z = weighted(y)

    Performs weighted/WPGMA linkage on the condensed distance matrix Z.
    See linkage for more information on the return structure and
    algorithm.

      (a condensed alias for linkage)
    """
    return linkage(y, method='weighted', metric='euclidean')

def centroid(y):
    """
    Z = centroid(y)
    
    Performs centroid/UPGMC linkage on the condensed distance matrix Z.
    See linkage for more information on the return structure and
    algorithm.

      (a condensed alias for linkage)

    Z = centroid(X)

    Performs centroid/UPGMC linkage on the observation matrix X using
    Euclidean distance as the distance metric. See linkage for more
    information on the return structure and algorithm.    

    """
    return linkage(y, method='centroid', metric='euclidean')

def median(y):
    """
    Z = median(y)

    Performs median/WPGMC linkage on the condensed distance matrix Z.
    See linkage for more information on the return structure and
    algorithm.

    Z = median(X)

    Performs median/WPGMC linkage on the observation matrix X using
    Euclidean distance as the distance metric. See linkage for more
    information on the return structure and algorithm.    

      (a condensed alias for linkage)
    """
    return linkage(y, method='median', metric='euclidean')

def ward(y):
    """
    Z = ward(y)
    
    Performs Ward's linkage on the condensed distance matrix Z. See
    linkage for more information on the return structure and algorithm.

    Z = ward(X)

    Performs Ward's linkage on the observation matrix X using Euclidean
    distance as the distance metric. See linkage for more information
    on the return structure and algorithm.    

      (a condensed alias for linkage)
    """
    return linkage(y, method='ward', metric='euclidean')

      
def linkage(y, method='single', metric='euclidean'):
    """ Z = linkage(y, method)

          Performs hierarchical/agglomorative clustering on the
          condensed distance matrix y. y must be a {n \choose 2} sized
          vector where n is the number of original observations paired
          in the distance matrix. The behavior of this function is very
          similar to the MATLAB(TM) linkage function.

          A (n - 1) * 4 matrix Z is returned. At the i'th iteration,
          clusters with indices Z[i, 0] and Z[i, 1] are combined to
          form cluster n + i. A cluster with an index less than n
          corresponds to one of the n original observations. The
          distance between clusters Z[i, 0] and Z[i, 1] is given by
          Z[i, 2]. The fourth value Z[i, 3] represents the number of
          original observations in the newly formed cluster.

          The following linkage methods are used to compute the
          distance dist(s, t) between two clusters s and t. The
          algorithm begins with a forest of clusters that have yet
          to be used in the hierarchy being formed. When two clusters
          s and t from this forest are combined into a single cluster u,
          s and t are removed from the forest, and u is added to
          the forest. When only one cluster remains in the forest,
          the algorithm stops, and this cluster becomes the root.

          A distance matrix is maintained at each iteration. The
          d[i,j] entry corresponds to the distance between cluster
          i and j in the original forest.
          
          At each iteration, the algorithm must update the distance
          matrix to reflect the distance of the newly formed cluster
          u with the remaining clusters in the forest.
          
          Suppose there are |u| original observations u[0], ..., u[|u|-1]
          in cluster u and |v| original objects v[0], ..., v[|v|-1]
          in cluster v. Recall s and t are combined to form cluster
          u. Let v be any remaining cluster in the forest that is not
          u.

          The following are methods for calculating the distance between
          the newly formed cluster u and each v.
        
            * method='single' assigns dist(u,v) = MIN(dist(u[i],v[j])
              for all points i in cluster u and j in cluster v.

                (also called Nearest Point Algorithm)

            * method='complete' assigns dist(u,v) = MAX(dist(u[i],v[j])
              for all points i in cluster u and j in cluster v.

                (also called Farthest Point Algorithm
                      or the Voor Hees Algorithm)

           * method='average' assigns dist(u,v) =
                \sum_{ij} { dist(u[i], v[j]) } / (|u|*|v|)
             for all points i and j where |u| and |v| are the
             cardinalities of clusters u and v, respectively.

                (also called UPGMA)

           * method='weighted' assigns

               dist(u,v) = (dist(s,v) + dist(t,v))/2
               
             where cluster u was formed with cluster s and t and v
             is a remaining cluster in the forest. (also called WPGMA)

        Z = linkage(X, method, metric='euclidean')

         Performs hierarchical clustering on the objects defined by the
         n by m observation matrix X.

         If the metric is 'euclidean' then the following methods may be
         used:

           * method='centroid' assigns dist(s,t) = euclid(c_s, c_t) where
             c_s and c_t are the centroids of clusters s and t,
             respectively. When two clusters s and t are combined into a new
             cluster u, the new centroid is computed over all the original
             objects in clusters s and t. The distance then becomes
             the Euclidean distance between the centroid of u and the
             centroid of a remaining cluster v in the forest.
             (also called UPGMC)
 
           * method='median' assigns dist(s,t) as above. When two clusters
             s and t are combined into a new cluster u, the average of
             centroids s and t give the new centroid u. (also called WPGMC)
           
           * method='ward' uses the Ward variance minimization algorithm.
             The new entry dist(u, v) is computed as follows,

                 dist(u,v) =

                ----------------------------------------------------
                | |v|+|s|            |v|+|t|            |v|
                | ------- d(v,s)^2 + ------- d(v,t)^2 - --- d(s,t)^2
               \|    T                  T                T

             where u is the newly joined cluster consisting of clusters
             s and t, v is an unused cluster in the forest, T=|v|+|s|+|t|,
             and |*| is the cardinality of its argument.
             (also called incremental)

           Warning to MATLAB(TM) users: when the minimum distance pair in
           the forest is chosen, there may be two or more pairs with the
           same minimum distance. This implementation may chose a
           different minimum than the MATLAB(TM) version.
        """
    if type(y) != _array_type:
        raise TypeError('Incompatible data type. y must be an array.')
    s = y.shape
    if type(method) != types.StringType:
        raise TypeError("Argument 'method' must be a string.")
    if y.dtype != 'double':
        raise TypeError('Incompatible data type. y must be a matrix of doubles.')

    # Since the C code does not support striding using strides.
    [y] = _copy_arrays_if_base_present([y])

    if len(s) == 1:
        d = numpy.ceil(numpy.sqrt(s[0] * 2))
        if d * (d - 1)/2 != s[0]:
            raise ValueError('Incompatible vector size. It must be a binomial coefficient.')
        if method not in _cpy_non_euclid_methods.keys():
            raise ValueError("Valid methods when the raw observations are omitted are 'single', 'complete', 'weighted', and 'average'.")
        Z = numpy.zeros((d - 1, 4))
        _cluster_wrap.linkage_wrap(y, Z, int(d), \
                                   int(_cpy_non_euclid_methods[method]))
    elif len(s) == 2:
        X = y
        n = s[0]
        m = s[1]
        if method not in _cpy_linkage_methods:
            raise ValueError('Invalid method: %s' % method)
        if method in _cpy_non_euclid_methods.keys():
            dm = pdist(X, metric)
            Z = numpy.zeros((n - 1, 4))
            _cluster_wrap.linkage_wrap(dm, Z, n, \
                                       int(_cpy_non_euclid_methods[method]))
        elif method in _cpy_euclid_methods.keys():
            if metric != 'euclidean':
                raise ValueError('Method %s requires the distance metric to be euclidean' % s)
            dm = pdist(X, metric)
            Z = numpy.zeros((n - 1, 4))
            _cluster_wrap.linkage_euclid_wrap(dm, Z, X, m, n,
                                              int(_cpy_euclid_methods[method]))
    return Z

class cnode:
    """
    A tree node class for representing a cluster. Leaf nodes correspond
    to original observations, while non-leaf nodes correspond to
    non-singleton clusters.

    The totree function converts a matrix returned by the linkage
    function into an easy-to-use tree representation.
    """

    def __init__(self, id, left=None, right=None, dist=0, count=1):
        if id < 0:
            raise ValueError('The id must be non-negative.')
        if dist < 0:
            raise ValueError('The distance must be non-negative.')
        if (left is None and right is not None) or \
           (left is not None and right is None):
            raise ValueError('Only full or proper binary trees are permitted. This node has one child.')
        if count < 1:
            raise ValueError('A cluster must contain at least one original observation.')
        self.id = id
        self.left = left
        self.right = right
        self.dist = dist
        if self.left is None:
            self.count = count
        else:
            self.count = left.count + right.count

    def getId(self):
        """
        i = nd.getId()
        
        Returns the id number of the node nd. For 0 <= i < n, i
        corresponds to original observation i. For n <= i < 2n - 1,
        i corresponds to non-singleton cluster formed at iteration i-n.
        """
        return self.id

    def getCount(self):
        """
        c = nd.getCount()

        Returns the number of leaf nodes (original observations)
        belonging to the cluster node nd. If the nd is a leaf, c=1.
        """
        return self.count

    def getLeft(self):
        """
        left = nd.getLeft()

        Returns a reference to the left child. If the node is a
        leaf, None is returned.
        """
        return self.left

    def getRight(self):
        """
        left = nd.getLeft()

        Returns a reference to the right child. If the node is a
        leaf, None is returned.
        """
        return self.right

    def isLeaf(self):
        """
        Returns True if the node is a leaf.
        """
        return self.left is None

    def preOrder(self, func=(lambda x: x.id)):
        """
        vlst = preOrder(func)
    
          Performs preorder traversal without recursive function calls.
          When a leaf node is first encountered, func is called with the
          leaf node as its argument, and its result is appended to the
          list vlst.
    
          For example, the statement
        
            ids = root.preOrder(lambda x: x.id)
    
          returns a list of the node ids corresponding to the leaf
          nodes of the tree as they appear from left to right.
        """
    
        # Do a preorder traversal, caching the result. To avoid having to do
        # recursion, we'll store the previous index we've visited in a vector.
        n = self.count
        
        curNode = [None] * (2 * n)
        lvisited = numpy.zeros((2 * n,), dtype='bool')
        rvisited = numpy.zeros((2 * n,), dtype='bool')
        curNode[0] = self
        k = 0
        preorder = []
        while k >= 0:
            nd = curNode[k]
            ndid = nd.id
            if nd.isLeaf():
                preorder.append(func(nd))
                k = k - 1
            else:
                if not lvisited[ndid]:
                    curNode[k + 1] = nd.left
                    lvisited[ndid] = True
                    k = k + 1
                elif not rvisited[ndid]:
                    curNode[k + 1] = nd.right
                    rvisited[ndid] = True
                    k = k + 1
                # If we've visited the left and right of this non-leaf
                # node already, go up in the tree.
                else:
                    k = k - 1
            
        return preorder

_cnode_bare = cnode(0)
_cnode_type = type(cnode)

def totree(Z, rd=False):
    """
    r = totree(Z)
    
      Converts a hierarchical clustering encoded in the matrix Z
      (by linkage) into an easy-to-use tree object. The reference r
      to the root cnode object is returned.
    
      Each cnode object has a left, right, dist, id, and count
      attribute. The left and right attributes point to cnode
      objects that were combined to generate the cluster. If
      both are None then the cnode object is a leaf node, its
      count must be 1, and its distance is meaningless but set
      to 0.

    (r, d) = totree(Z, rd=True)

      Same as totree(Z) except a tuple is returned where r is
      the reference to the root cnode and d is a reference to a
      dictionary mapping cluster ids to cnodes. If a cluster id
      is less than n, then it corresponds to a singleton cluster
      (leaf node).

    Note: This function is provided for the convenience of the
    library user. cnodes are not used as input to any of the
    functions in this library.
    """

    is_valid_linkage(Z, throw=True, name='Z')
    
    # The number of original objects is equal to the number of rows minus
    # 1.
    n = Z.shape[0] + 1

    # Create a list full of None's to store the node objects
    d = [None] * (n*2-1)

    # If we encounter a cluster being combined more than once, the matrix
    # must be corrupt.
    if len(numpy.unique(Z[:, 0:2].reshape((2 * (n - 1),)))) != 2 * (n - 1):
        raise ValueError('Corrupt matrix Z. Some clusters are more than once.')
    # If a cluster index is out of bounds, report an error.
    if (Z[:, 0:2] >= 2 * n - 1).any():
        raise ValueError('Corrupt matrix Z. Some cluster indices (first and second) are out of bounds.')
    if (Z[:, 0:2] < 0).any():
        raise ValueError('Corrupt matrix Z. Some cluster indices (first and second columns) are negative.')
    if (Z[:, 2] < 0).any():
        raise ValueError('Corrupt matrix Z. Some distances (third column) are negative.')

    if (Z[:, 3] < 0).any():
        raise ValueError('Some counts (fourth column) are negative.')

    # Create the nodes corresponding to the n original objects.
    for i in xrange(0, n):
        d[i] = cnode(i)

    nd = None

    for i in xrange(0, n - 1):
        fi = int(Z[i, 0])
        fj = int(Z[i, 1])
        if fi > i + n:
            raise ValueError('Corrupt matrix Z. Index to derivative cluster is used before it is formed. See row %d, column 0' % fi)
        if fj > i + n:
            raise ValueError('Corrupt matrix Z. Index to derivative cluster is used before it is formed. See row %d, column 1' % fj)
        nd = cnode(i + n, d[fi], d[fj],  Z[i, 2])
        #          ^ id   ^ left ^ right ^ dist
        if Z[i,3] != nd.count:
            raise ValueError('Corrupt matrix Z. The count Z[%d,3] is incorrect.' % i)
        d[n + i] = nd

    if rd:
        return (nd, d)
    else:
        return nd

def squareform(X, force="no", checks=True):
    """
    ... = squareform(...)

    Converts a vector-form distance vector to a square-form distance
    matrix, and vice-versa. 

    v = squareform(X)

      Given a square d by d symmetric distance matrix X, v=squareform(X)
      returns a d*(d-1)/2 (or {n \choose 2}) sized vector v.

      v[{n \choose 2}-{n-i \choose 2} + (j-i-1)] is the distance
      between points i and j. If X is non-square or asymmetric, an error
      is returned.

    X = squareform(v)

      Given a d*d(-1)/2 sized v for some integer d>=2 encoding distances
      as described, X=squareform(v) returns a d by d distance matrix X. The
      X[i, j] and X[j, i] values are set to
      v[{n \choose 2}-{n-i \choose 2} + (j-u-1)] and all
      diagonal elements are zero.

    As with MATLAB(TM), if force is equal to 'tovector' or 'tomatrix',
    the input will be treated as a distance matrix or distance vector
    respectively.

    If checks is set to False, no checks will be made for matrix
    symmetry nor zero diagonals. This is useful if it is known that
    X - X.T is small and diag(X) is close to zero. These values are
    ignored any way so they do not disrupt the squareform
    transformation.
    """
    
    if type(X) is not _array_type:
        raise TypeError('The parameter passed must be an array.')

    if X.dtype != 'double':
        raise TypeError('A double array must be passed.')

    s = X.shape

    # X = squareform(v)
    if len(s) == 1 and force != 'tomatrix':
        # Grab the closest value to the square root of the number
        # of elements times 2 to see if the number of elements
        # is indeed a binomial coefficient.
        d = int(numpy.ceil(numpy.sqrt(X.shape[0] * 2)))

        print d, s[0]
        # Check that v is of valid dimensions.
        if d * (d - 1) / 2 != int(s[0]):
            raise ValueError('Incompatible vector size. It must be a binomial coefficient n choose 2 for some integer n >= 2.')
        
        # Allocate memory for the distance matrix.
        M = numpy.zeros((d, d), 'double')

        # Since the C code does not support striding using strides.
        # The dimensions are used instead.
        [X] = _copy_arrays_if_base_present([X])

        # Fill in the values of the distance matrix.
        _cluster_wrap.to_squareform_from_vector_wrap(M, X)

        # Return the distance matrix.
        M = M + M.transpose()
        return M
    elif len(s) != 1 and force.lower() == 'tomatrix':
        raise ValueError("Forcing 'tomatrix' but input X is not a distance vector.")
    elif len(s) == 2 and force.lower() != 'tovector':
        if s[0] != s[1]:
            raise ValueError('The matrix argument must be square.')
        if checks:
            if numpy.sum(numpy.sum(X == X.transpose())) != numpy.product(X.shape):
                raise ValueError('The distance matrix must be symmetrical.')
            if (X.diagonal() != 0).any():
                raise ValueError('The distance matrix must have zeros along the diagonal.')

        # One-side of the dimensions is set here.
        d = s[0]
        
        # Create a vector.
        v = numpy.zeros(((d * (d - 1) / 2),), 'double')

        # Since the C code does not support striding using strides.
        # The dimensions are used instead.
        [X] = _copy_arrays_if_base_present([X])

        # Convert the vector to squareform.
        _cluster_wrap.to_vector_from_squareform_wrap(X, v)
        return v
    elif len(s) != 2 and force.lower() == 'tomatrix':
        raise ValueError("Forcing 'tomatrix' but input X is not a distance vector.")
    else:
        raise ValueError('The first argument must be a vector or matrix. A %d-dimensional array is not permitted' % len(s))

def minkowski(u, v, p):
    """
    d = minkowski(u, v, p)
    
      Returns the Minkowski distance between two vectors u and v,

        ||u-v||_p = (\sum {|u_i - v_i|^p})^(1/p).
    """
    if p < 1:
        raise ValueError("p must be at least 1")
    return math.pow((abs(u-v)**p).sum(), 1.0/p)

def euclidean(u, v):
    """
    d = euclidean(u, v)
    
      Computes the Euclidean distance between two n-vectors u and v, ||u-v||_2
    """
    q=numpy.matrix(u-v)
    return numpy.sqrt((q*q.T).sum())

def sqeuclidean(u, v):
    """
    d = sqeuclidean(u, v)

      Computes the squared Euclidean distance between two n-vectors u and v,
        (||u-v||_2)^2.
    """
    return ((u-v)*(u-v).T).sum()

def cosine(u, v):
    """
    d = cosine(u, v)

      Computes the Cosine distance between two n-vectors u and v,
        (1-uv^T)/(||u||_2 * ||v||_2).
    """
    return (1.0 - (scipy.dot(u, v.T) / \
                   (math.sqrt(scipy.dot(u, u.T)) * math.sqrt(scipy.dot(v, v.T)))))

def correlation(u, v):
    """
    d = correlation(u, v)
    
      Computes the correlation distance between two n-vectors u and v,

            1 - (u - n|u|_1)(v - n|v|_1)^T
            --------------------------------- ,
            |(u - n|u|_1)|_2 |(v - n|v|_1)|^T

      where |*|_1 is the Manhattan norm and n is the common dimensionality
      of the vectors.
    """
    vmu = v.mean()
    umu = u.mean()
    um = u - umu
    vm = v - vmu
    return 1.0 - (scipy.dot(um, vm.T) / (math.sqrt(scipy.dot(um, vm).T)) \
            * math.sqrt(scipy.dot(vm, vm.T)))

def hamming(u, v):
    """
    d = hamming(u, v)
    
      Computes the Hamming distance between two n-vectors u and v,
      which is simply the proportion of disagreeing components in u
      and v. If u and v are boolean vectors, the hamming distance is

         (c_{01} + c_{10}) / n

      where c_{ij} is the number of occurrences of

         u[k] == i and v[k] == j

      for k < n.
    """
    return (u != v).mean()

def jaccard(u, v):
    """
    d = jaccard(u, v)

      Computes the Jaccard-Needham dissimilarity between two boolean
      n-vectors u and v, which is

              c_{TF} + c_{FT}
         ------------------------
         c_{TT} + c_{FT} + c_{TF}

      where c_{ij} is the number of occurrences of

         u[k] == i and v[k] == j

      for k < n.
    """
    return ((scipy.bitwise_and((u != v), scipy.bitwise_or(u != 0, v != 0))).sum()) / scipy.bitwise_or(u != 0, v != 0).sum()

def kulsinski(u, v):
    """
    d = kulsinski(u, v)

      Computes the Kulsinski dissimilarity between two boolean n-vectors
      u and v, which is

         c_{TF} + c_{FT} - c_{TT} + n
         ----------------------------
              c_{FT} + c_{TF} + n

      where c_{ij} is the number of occurrences of

         u[k] == i and v[k] == j

      for k < n.
    """
    (nff, nft, ntf, ntt) = _nbool_correspond_all(u, v)

    return (ntf + nft - ntt + n) / (ntf + nft + n)

def seuclidean(u, v, V):
    """
    d = seuclidean(u, v, V)
    
      Returns the standardized Euclidean distance between two
      n-vectors u and v. V is a m-dimensional vector of component
      variances. It is usually computed among a larger collection vectors.
    """
    if type(V) is not _array_type or len(V.shape) != 1 or V.shape[0] != u.shape[0] or u.shape[0] != v.shape[0]:
        raise TypeError('V must be a 1-D numpy array of doubles of the same dimension as u and v.')
    return numpy.sqrt(((u-v)**2 / V).sum())

def cityblock(u, v):
    """
    d = cityblock(u, v)

      Computes the Manhattan distance between two n-vectors u and v,
         \sum {u_i-v_i}.
    """
    return abs(u-v).sum()

def mahalanobis(u, v, VI):
    """
    d = mahalanobis(u, v, VI)
    
      Computes the Mahalanobis distance between two n-vectors u and v,
        (u-v)VI(u-v)^T
      where VI is the inverse covariance matrix.
    """
    if type(V) is not _array_type:
        raise TypeError('V must be a 1-D numpy array of doubles of the same dimension as u and v.')
    return numpy.sqrt(scipy.dot(scipy.dot((u-v),VI),(u-v).T).sum())

def chebyshev(u, v):
    """
    d = chebyshev(u, v)
    
      Computes the Chebyshev distance between two n-vectors u and v,
        \max {|u_i-v_i|}.
    """
    return max(abs(u-v))

def braycurtis(u, v):
    """
    d = braycurtis(u, v)
    
      Computes the Bray-Curtis distance between two n-vectors u and v,
        \sum{|u_i-v_i|} / \sum{|u_i+v_i|}.
    """
    return abs(u-v).sum() / abs(u+v).sum()

def canberra(u, v):
    """
    d = canberra(u, v)

      Computes the Canberra distance between two n-vectors u and v,
        \sum{|u_i-v_i|} / \sum{|u_i|+|v_i}.
    """
    return abs(u-v).sum() / (abs(u).sum() + abs(v).sum())

def _nbool_correspond_all(u, v):
    not_u = scipy.bitwise_not(u)
    not_v = scipy.bitwise_not(v)
    nff = scipy.bitwise_and(not_u, not_v).sum()
    nft = scipy.bitwise_and(not_u, v).sum()
    ntf = scipy.bitwise_and(u, not_v).sum()
    ntt = scipy.bitwise_and(u, v).sum()
    return (nff, nft, ntf, ntt)

def _nbool_correspond_ft_tf(u, v):
    not_u = scipy.bitwise_not(u)
    not_v = scipy.bitwise_not(v)
    nft = scipy.bitwise_and(not_u, v).sum()
    ntf = scipy.bitwise_and(u, not_v).sum()
    return (nft, ntf)

def yule(u, v):
    """
    d = yule(u, v)
      Computes the Yule dissimilarity between two boolean n-vectors u and v,

                  R
         ---------------------
         c_{TT} + c_{FF} + R/2

      where c_{ij} is the number of occurrences of

         u[k] == i and v[k] == j

      for k < n, and

         R = 2.0 * (c_{TF} + c_{FT}).
    """
    (nff, nft, ntf, ntt) = _nbool_correspond_all(u, v)
    return float(2.0 * ntf * nft) / float(ntt * nff + ntf * nft)

def matching(u, v):
    """
    d = matching(u, v)

      Computes the Matching dissimilarity between two boolean n-vectors
      u and v, which is

         (c_{TF} + c_{FT}) / n

      where c_{ij} is the number of occurrences of

         u[k] == i and v[k] == j

      for k < n.
    """
    (nft, ntf) = _nbool_correspond_ft_tf(u, v)
    return float(nft + ntf) / float(len(u))

def dice(u, v):
    """
    d = dice(u, v)
    
      Computes the Dice dissimilarity between two boolean n-vectors
      u and v, which is

                c_{TF} + c_{FT}
         ----------------------------
         2 * c_{TT} + c_{FT} + c_{TF}

      where c_{ij} is the number of occurrences of

         u[k] == i and v[k] == j

      for k < n.
    """
    ntt = scipy.bitwise_and(u, v).sum()
    (nft, ntf) = _nbool_correspond_ft_tf(u, v)
    return float(ntf + nft)/float(2.0 * ntt + ntf + nft)

def rogerstanimoto(u, v):
    """
    d = rogerstanimoto(u, v)
    
      Computes the Rogers-Tanimoto dissimilarity between two boolean
      n-vectors u and v,

                  R
         -------------------
         c_{TT} + c_{FF} + R

      where c_{ij} is the number of occurrences of

         u[k] == i and v[k] == j

      for k < n, and

         R = 2.0 * (c_{TF} + c_{FT}).

    """
    (nff, nft, ntf, ntt) = _nbool_correspond_all(u, v)
    return float(2.0 * (ntf + nft)) / float(ntt + nff + (2.0 * (ntf + nft)))

def russellrao(u, v):
    """
    d = russellrao(u, v)
    
      Computes the Russell-Rao dissimilarity between two boolean n-vectors
      u and v, (n - c_{TT}) / n where c_{ij} is the number of occurrences
      of u[k] == i and v[k] == j for k < n.
    """
    ntt = scipy.bitwise_and(u, v).sum()
    return float(len(u) - ntt) / float(len(u))

def sokalmichener(u, v):
    """
    d = sokalmichener(u, v)

      Computes the Sokal-Michener dissimilarity between two boolean vectors
      u and v, 2R / (S + 2R) where c_{ij} is the number of occurrences of
      u[k] == i and v[k] == j for k < n and R = 2 * (c_{TF} + c{FT}) and
      S = c_{FF} + c_{TT}.
    """
    ntt = scipy.bitwise_and(u, v).sum()
    nff = scipy.bitwise_and(scipy.bitwise_not(u), scipy.bitwise_not(v)).sum()
    (nft, ntf) = _nbool_correspond_ft_tf(u, v)
    return float(2.0 * (ntf + nft))/float(ntt + nff + 2.0 * (ntf + nft))

def sokalsneath(u, v):
    """
    d = sokalsneath(u, v)

      Computes the Sokal-Sneath dissimilarity between two boolean vectors
      u and v, 2R / (c_{TT} + 2R) where c_{ij} is the number of occurrences
      of u[k] == i and v[k] == j for k < n and R = 2 * (c_{TF} + c{FT}).
    """
    ntt = scipy.bitwise_and(u, v).sum()
    (nft, ntf) = _nbool_correspond_ft_tf(u, v)
    return float(2.0 * (ntf + nft))/float(ntt + 2.0 * (ntf + nft))

# V means pass covariance
_pdist_metric_info = {'euclidean': ['double'],
                      'seuclidean': ['double'],
                      'sqeuclidean': ['double'],
                      'minkowski': ['double'],
                      'cityblock': ['double'],
                      'cosine': ['double'],
                      'correlation': ['double'],
                      'hamming': ['double','bool'],
                      'jaccard': ['double', 'bool'],
                      'chebyshev': ['double'],
                      'canberra': ['double'],
                      'braycurtis': ['double'],
                      'mahalanobis': ['bool'],
                      'yule': ['bool'],
                      'matching': ['bool'],
                      'dice': ['bool'],
                      'kulsinski': ['bool'],
                      'rogerstanimoto': ['bool'],
                      'russellrao': ['bool'],
                      'sokalmichener': ['bool'],
                      'sokalsneath': ['bool']}

def pdist(X, metric='euclidean', p=2, V=None, VI=None):
    """ Y = pdist(X, method='euclidean', p=2)
    
           Computes the distance between m original observations in
           n-dimensional space. Returns a condensed distance matrix Y.
           For each i and j (i<j), the metric dist(u=X[i], v=X[j]) is
           computed and stored in the ij'th entry. See squareform
           to learn how to retrieve this entry.

        1. Y = pdist(X)

          Computes the distance between m points using Euclidean distance
          (2-norm) as the distance metric between the points. The points
          are arranged as m n-dimensional row vectors in the matrix X.

        2. Y = pdist(X, 'minkowski', p)

          Computes the distances using the Minkowski distance ||u-v||_p
          (p-norm) where p>=1.

        3. Y = pdist(X, 'cityblock')

          Computes the city block or Manhattan distance between the
          points.

        4. Y = pdist(X, 'seuclidean', V=None)

          Computes the standardized Euclidean distance. The standardized
          Euclidean distance between two n-vectors u and v is

            sqrt(\sum {(u_i-v_i)^2 / V[x_i]}).

          V is the variance vector; V[i] is the variance computed over all
          the i'th components of the points. If not passed, it is
          automatically computed.

        5. Y = pdist(X, 'sqeuclidean')

          Computes the squared Euclidean distance ||u-v||_2^2 between
          the vectors.

        6. Y = pdist(X, 'cosine')

          Computes the cosine distance between vectors u and v,
        
               1 - uv^T
             -----------
             |u|_2 |v|_2

          where |*|_2 is the 2 norm of its argument *.

        7. Y = pdist(X, 'correlation')

          Computes the correlation distance between vectors u and v. This is

            1 - (u - n|u|_1)(v - n|v|_1)^T
            --------------------------------- ,
            |(u - n|u|_1)|_2 |(v - n|v|_1)|^T

          where |*|_1 is the Manhattan (or 1-norm) of its argument *,
          and n is the common dimensionality of the vectors.

        8. Y = pdist(X, 'hamming')

          Computes the normalized Hamming distance, or the proportion
          of those vector elements between two n-vectors u and v which
          disagree. To save memory, the matrix X can be of type boolean.

        9. Y = pdist(X, 'jaccard')

          Computes the Jaccard distance between the points. Given two
          vectors, u and v, the Jaccard distance is the proportion of
          those elements u_i and v_i that disagree where at least one
          of them is non-zero.

        10. Y = pdist(X, 'chebyshev')

          Computes the Chebyshev distance between the points. The
          Chebyshev distance between two n-vectors u and v is the maximum
          norm-1 distance between their respective elements. More
          precisely, the distance is given by

            d(u,v) = max {|u_i-v_i|}.

        11. Y = pdist(X, 'canberra')

          Computes the Canberra distance between the points. The
          Canberra distance between two points u and v is

                      |u_1-v_1|     |u_2-v_2|           |u_n-v_n|
            d(u,v) = ----------- + ----------- + ... + -----------
                     |u_1|+|v_1|   |u_2|+|v_2|         |u_n|+|v_n|

        12. Y = pdist(X, 'braycurtis')

          Computes the Bray-Curtis distance between the points. The
          Bray-Curtis distance between two points u and v is

                     |u_1-v_1| + |u_2-v_2| + ... + |u_n-v_n|
            d(u,v) = ---------------------------------------
                     |u_1+v_1| + |u_2+v_2| + ... + |u_n+v_n|

        13. Y = pdist(X, 'mahalanobis', VI=None)

          Computes the Mahalanobis distance between the points. The
          Mahalanobis distance between two points u and v is
                (u-v)(1/V)(u-v)^T
          where (1/V) is the inverse covariance. If VI is not None,
          VI will be used as the inverse covariance matrix.

        14. Y = pdist(X, 'yule')

          Computes the Yule distance between each pair of boolean
          vectors. (see yule function documentation)

        15. Y = pdist(X, 'matching')

          Computes the matching distance between each pair of boolean
          vectors. (see matching function documentation)

        16. Y = pdist(X, 'dice')

          Computes the Dice distance between each pair of boolean
          vectors. (see dice function documentation)

        17. Y = pdist(X, 'kulsinski')

          Computes the Kulsinski distance between each pair of
          boolean vectors. (see kulsinski function documentation)

        17. Y = pdist(X, 'rogerstanimoto')

          Computes the Rogers-Tanimoto distance between each pair of
          boolean vectors. (see rogerstanimoto function documentation)

        18. Y = pdist(X, 'russellrao')

          Computes the Russell-Rao distance between each pair of
          boolean vectors. (see russellrao function documentation)

        19. Y = pdist(X, 'sokalmichener')

          Computes the Sokal-Michener distance between each pair of
          boolean vectors. (see sokalmichener function documentation)

        20. Y = pdist(X, 'sokalsneath')

          Computes the Sokal-Sneath distance between each pair of
          boolean vectors. (see sokalsneath function documentation)

        21. Y = pdist(X, f)
        
          Computes the distance between all pairs of vectors in X
          using the user supplied 2-arity function f. For example,
          Euclidean distance between the vectors could be computed
          as follows,

            dm = pdist(X, (lambda u, v: numpy.sqrt(((u-v)*(u-v).T).sum())))

          Note that you should avoid passing a reference to one of
          the distance functions defined in this library. For example,

            dm = pdist(X, sokalsneath)

          would calculate the pair-wise distances between the vectors
          in X using the Python function sokalsneath. This would result
          in sokalsneath being called {n \choose 2} times, which is
          inefficient. Instead, the optimized C version is more
          efficient, and we call it using the following syntax.

            dm = pdist(X, 'sokalsneath')
       """
#         21. Y = pdist(X, 'test_Y')
#
#           Computes the distance between all pairs of vectors in X
#           using the distance metric Y but with a more succint,
#           verifiable, but less efficient implementation.

    
    if type(X) is not _array_type:
        raise TypeError('The parameter passed must be an array.')

    # The C code doesn't do striding.
    [X] = _copy_arrays_if_base_present([X])

    s = X.shape

    if len(s) != 2:
        raise ValueError('A matrix must be passed.');

    m = s[0]
    n = s[1]
    dm = numpy.zeros((m * (m - 1) / 2,), dtype='double')

    mtype = type(metric)
    if mtype is types.FunctionType:
        k = 0
        for i in xrange(0, m - 1):
            for j in xrange(i+1, m):
                dm[k] = metric(X[i, :], X[j, :])
                k = k + 1
    elif mtype is types.StringType:
        mstr = metric.lower()

        if X.dtype != 'double' and (mstr != 'hamming' and mstr != 'jaccard'):
            TypeError('A double array must be passed.')
        if mstr in set(['euclidean', 'euclid', 'eu', 'e']):
            _cluster_wrap.pdist_euclidean_wrap(X, dm)
        elif mstr in set(['sqeuclidean']):
            _cluster_wrap.pdist_euclidean_wrap(X, dm)
            dm = dm ** 2.0
        elif mstr in set(['cityblock', 'cblock', 'cb', 'c']):
            _cluster_wrap.pdist_city_block_wrap(X, dm)
        elif mstr in set(['hamming', 'hamm', 'ha', 'h']):
            if X.dtype == 'double':
                _cluster_wrap.pdist_hamming_wrap(X, dm)
            elif X.dtype == 'bool':
                _cluster_wrap.pdist_hamming_bool_wrap(X, dm)
            else:
                raise TypeError('Invalid input matrix type %s for hamming.' % str(X.dtype))
        elif mstr in set(['jaccard', 'jacc', 'ja', 'j']):
            if X.dtype == 'double':
                _cluster_wrap.pdist_hamming_wrap(X, dm)
            elif X.dtype == 'bool':
                _cluster_wrap.pdist_hamming_bool_wrap(X, dm)
            else:
                raise TypeError('Invalid input matrix type %s for jaccard.' % str(X.dtype))
        elif mstr in set(['chebyshev', 'cheby', 'cheb', 'ch']):
            _cluster_wrap.pdist_chebyshev_wrap(X, dm)            
        elif mstr in set(['minkowski', 'mi', 'm']):
            _cluster_wrap.pdist_minkowski_wrap(X, dm, p)
        elif mstr in set(['seuclidean', 'se', 's']):
            if V:
                if type(V) is not _array_type:
                    raise TypeError('V must be a numpy array')
                if V.dtype != 'double':
                    raise TypeError('V must contain doubles.')
                if len(V.shape) != 1:
                    raise ValueError('V must be one-dimensional.')
                if V.shape[0] != n:
                    raise ValueError('V must be a vector of the same dimension as the points.')
                # The C code doesn't do striding.
                [VV] = _copy_arrays_if_base_present([V])
            else:
                VV = scipy.stats.var(X, axis=0)
            _cluster_wrap.pdist_seuclidean_wrap(X, VV, dm)
        # Need to test whether vectorized cosine works better.
        # Find out: Is there a dot subtraction operator so I can
        # subtract matrices in a similar way to multiplying them?
        # Need to get rid of as much unnecessary C code as possible.
        elif mstr in set(['cosine_old', 'cos_old']):
            norms = numpy.sqrt(numpy.sum(X * X, axis=1))
            _cluster_wrap.pdist_cosine_wrap(X, dm, norms)
        elif mstr in set(['cosine', 'cos']):
            norms = numpy.sqrt(numpy.sum(X * X, axis=1))
            nV = norms.reshape(m, 1)
            # The numerator u * v
            nm = numpy.dot(X, X.T)
            # The denom. ||u||*||v||
            de = numpy.dot(nV, nV.T);
            dm = 1 - (nm / de)
            dm[xrange(0,m),xrange(0,m)] = 0
            dm = squareform(dm)
        elif mstr in set(['correlation', 'co']):
            X2 = X - numpy.repmat(numpy.mean(X, axis=1).reshape(m, 1), 1, n)
            norms = numpy.sqrt(numpy.sum(X2 * X2, axis=1))
            _cluster_wrap.pdist_cosine_wrap(X2, dm, norms)
        elif mstr in set(['mahalanobis', 'mahal', 'mah']):
            if VI:
                if type(VI) != _array_type:
                    raise TypeError('VI must be a numpy array.')
                if VI.dtype != 'double':
                    raise TypeError('The array must contain doubles.')
                [VI] = _copy_arrays_if_base_present([VI])
            else:
                V = numpy.cov(X.T)
                VI = numpy.linalg.inv(V).T.copy()
            # (u-v)V^(-1)(u-v)^T
            _cluster_wrap.pdist_mahalanobis_wrap(X, VI, dm)
        elif mstr == 'canberra':
            _cluster_wrap.pdist_canberra_wrap(X, dm)
        elif mstr == 'braycurtis':
            _cluster_wrap.pdist_bray_curtis_wrap(X, dm)
        elif mstr == 'yule':
            _cluster_wrap.pdist_yule_bool_wrap(X, dm)
        elif mstr == 'matching':
            _cluster_wrap.pdist_matching_bool_wrap(X, dm)
        elif mstr == 'kulsinski':
            _cluster_wrap.pdist_kulsinski_bool_wrap(X, dm)
        elif mstr == 'dice':
            _cluster_wrap.pdist_dice_bool_wrap(X, dm)
        elif mstr == 'rogerstanimoto':
            _cluster_wrap.pdist_rogerstanimoto_bool_wrap(X, dm)
        elif mstr == 'russellrao':
            _cluster_wrap.pdist_russellrao_bool_wrap(X, dm)
        elif mstr == 'sokalmichener':
            _cluster_wrap.pdist_sokalmichener_bool_wrap(X, dm)
        elif mstr == 'sokalsneath':
            _cluster_wrap.pdist_sokalsneath_bool_wrap(X, dm)
        elif metric == 'test_euclidean':
            dm = pdist(X, euclidean)
        elif metric == 'test_sqeuclidean':
            if V is None:
                V = scipy.stats.var(X, axis=0)
            dm = pdist(X, lambda u, v: seuclidean(u, v, V))
        elif metric == 'test_braycurtis':
            dm = pdist(X, braycurtis)
        elif metric == 'test_mahalanobis':
            if VI is None:
                V = numpy.cov(X.T)
                VI = numpy.linalg.inv(V)
            [VI] = _copy_arrays_if_base_present([VI])
            # (u-v)V^(-1)(u-v)^T
            dm = pdist(X, (lambda u, v: mahalanobis(u, v, VI)))
        elif metric == 'test_cityblock':
            dm = pdist(X, cityblock)
        elif metric == 'test_minkowski':
            dm = pdist(X, minkowski)
        elif metric == 'test_cosine':
            dm = pdist(X, cosine)
        elif metric == 'test_correlation':
            dm = pdist(X, correlation)
        elif metric == 'test_hamming':
            dm = pdist(X, hamming)
        elif metric == 'test_jaccard':
            dm = pdist(X, jaccard)
        elif metric == 'test_chebyshev':
            dm = pdist(X, chebyshev)
        elif metric == 'test_yule':
            dm = pdist(X, yule)
        elif metric == 'test_matching':
            dm = pdist(X, matching)
        elif metric == 'test_dice':
            dm = pdist(X, dice)
        elif metric == 'test_rogerstanimoto':
            dm = pdist(X, rogerstanimoto)
        elif metric == 'test_russellrao':
            dm = pdist(X, russellrao)
        elif metric == 'test_sokalsneath':
            dm = pdist(X, sokalsneath)
        else:
            raise ValueError('Unknown Distance Metric: %s' % mstr)
    else:
        raise TypeError('2nd argument metric must be a string identifier or a function.')
    return dm

def cophenet(*args, **kwargs):
    """
    d = cophenet(Z)

      Calculates the cophenetic distances between each observation in the
      hierarchical clustering defined by the linkage Z.

      Suppose p and q are original observations in disjoint clusters
      s and t, respectively and s and t are joined by a direct parent
      cluster u. The cophenetic distance between observations i and j
      is simply the distance between clusters s and t.

      d is cophenetic distance matrix in condensed form. The ij'th
      entry is the cophenetic distance between original observations
      i and j.

    c = cophenet(Z, Y)

      Calculates the cophenetic correlation coefficient c of a hierarchical
      clustering Z of a set of n observations in m dimensions. Y is the
      condensed distance matrix from which Z was generated.

    (c, d) = cophenet(Z, Y, [])

      Also returns the cophenetic distance matrix in condensed form.
      
    """
    nargs = len(args)

    if nargs < 1:
        raise ValueError('At least one argument must be passed to cophenet.')

    Z = args[0]
    is_valid_linkage(Z, throw=True, name='Z')
    Zs = Z.shape
    n = Zs[0] + 1

    zz = numpy.zeros((n*(n-1)/2,), dtype='double')
    # Since the C code does not support striding using strides.
    # The dimensions are used instead.
    [Z] = _copy_arrays_if_base_present([Z])

    _cluster_wrap.cophenetic_distances_wrap(Z, zz, int(n))
    if nargs == 1:
        return zz

    Y = args[1]
    if (type(Y) is not _array_type) and Y.dtype != 'double':
        raise TypeError('Second argument Y must be an array of doubles.')

    Ys = Y.shape

    if len(Ys) != 1:
        raise ValueError('Second argument Y must be a 1-D array.')

    if Ys[0] != n*(n-1)/2:
        raise ValueError('Incorrect size of Y. It must be a distance vector containing n*(n-1) elements.')
    
    z = zz.mean()
    y = Y.mean()
    Yy = Y - y
    Zz = zz - z
    #print Yy.shape, Zz.shape
    numerator = (Yy * Zz)
    denomA = Yy ** 2
    denomB = Zz ** 2
    c = numerator.sum() / numpy.sqrt((denomA.sum() * denomB.sum()))
    #print c, numerator.sum()
    if nargs == 2:
        return c

    if nargs == 3:
        return (c, zz)

def inconsistent(Z, d=2):
    """
    R = inconsistent(Z, d=2)
    
      Calculates statistics on links up to d levels below each
      non-singleton cluster defined in the (n-1)x4 linkage matrix Z.

      R is a (n-1)x5 matrix where the i'th row contains the link
      statistics for the non-singleton cluster i. The link statistics
      are computed over the link heights for links d levels below the
      cluster i. R[i,0] and R[i,1] are the mean and standard deviation of
      the link heights, respectively; R[i,2] is the number of links
      included in the calculation; and R[i,3] is the inconsistency
      coefficient, (Z[i, 2]-R[i,0])/R[i,2].

      This function behaves similarly to the MATLAB(TM) inconsistent
      function.
    """

    Zs = Z.shape
    is_valid_linkage(Z, throw=True, name='Z')
    if (not d == numpy.floor(d)) or d < 0:
        raise ValueError('The second argument d must be a nonnegative integer value.')
#    if d == 0:
#        d = 1

    # Since the C code does not support striding using strides.
    # The dimensions are used instead.
    [Z] = _copy_arrays_if_base_present([Z])

    n = Zs[0] + 1
    R = numpy.zeros((n - 1, 4), dtype='double')

    _cluster_wrap.inconsistent_wrap(Z, R, int(n), int(d));
    return R
    
def from_mlab_linkage(Z):
    """
    Z2 = from_mlab_linkage(Z)
    
    Converts a linkage matrix Z generated by MATLAB(TM) to a new linkage
    matrix Z2 compatible with this module. The conversion does two
    things:

     * the indices are converted from 1..N to 0..(N-1) form, and
    
     * a fourth column Z[:,3] is added where Z[i,3] is equal to
       the number of original observations (leaves) in the non-singleton
       cluster i.
    """
    is_valid_linkage(Z, throw=True, name='Z')
    Zs = Z.shape
    Zpart = Z[:,0:2]
    Zd = Z[:,2].reshape(Zs[0], 1)
    if Zpart.min() != 1.0 and Zpart.max() != 2 * Zs[0]:
        raise ValueError('The format of the indices is not 1..N');
    CS = numpy.zeros((Zs[0], 1), dtype='double')
    Zpart = Zpart - 1
    _cluster_wrap.calculate_cluster_sizes_wrap(numpy.hstack([Zpart, \
                                                             Zd]).copy(), \
                                               CS, int(Zs[0]) + 1)
    return numpy.hstack([Zpart, Zd, CS]).copy()

def to_mlab_linkage(Z):
    """
    Z2 = to_mlab_linkage(Z)

    Converts a linkage matrix Z generated by the linkage function of this
    module to one compatible with MATLAB(TM). Z2 is the same as Z with the
    last column removed and the cluster indices converted to use
    1..N indexing.
    """
    is_valid_linkage(Z, throw=True, name='Z')
    
    return numpy.hstack([Z[:,0:2] + 1, Z[:,2]])

def is_monotonic(Z):
    """
    is_monotonic(Z)
    
      Returns True if the linkage Z is monotonic. The linkage is monotonic
      if for every cluster s and t joined, the distance between them is
      no less than the distance between any previously joined clusters.
    """
    is_valid_linkage(Z, throw=True, name='Z')

    # We expect the i'th value to be greater than its successor.
    return (Z[:-1,2]>=Z[1:,2]).all()

def is_valid_im(R, warning=False, throw=False, name=None):
    """
    is_valid_im(R)
    
      Returns True if the inconsistency matrix passed is valid. It must
      be a n by 4 numpy array of doubles. The standard deviations R[:,1]
      must be nonnegative. The link counts R[:,2] must be positive and
      no greater than n-1.
    """
    valid = True
    try:
        if type(R) is not _array_type:
            if name:
                raise TypeError('Variable \'%s\' passed as inconsistency matrix is not a numpy array.' % name)
            else:
                raise TypeError('Variable passed as inconsistency matrix is not a numpy array.')
        if R.dtype != 'double':
            if name:
                raise TypeError('Inconsistency matrix \'%s\' must contain doubles (float64).' % name)
            else:
                raise TypeError('Inconsistency matrix must contain doubles (float64).')
        if len(R.shape) != 2:
            if name:
                raise ValueError('Inconsistency matrix \'%s\' must have shape=2 (i.e. be two-dimensional).' % name)
            else:
                raise ValueError('Inconsistency matrix must have shape=2 (i.e. be two-dimensional).')
        if R.shape[1] != 4:
            if name:
                raise ValueError('Inconsistency matrix \'%s\' must have 4 columns.' % name)
            else:
                raise ValueError('Inconsistency matrix must have 4 columns.')
        if R.shape[0] < 1:
            if name:
                raise ValueError('Inconsistency matrix \'%s\' must have at least one row.' % name)
            else:
                raise ValueError('Inconsistency matrix must have at least one row.')
    except Exception, e:
        if throw:
            raise
        if warning:
            _warning(str(e))
        valid = False
    return valid

def is_valid_linkage(Z, warning=False, throw=False, name=None):
    """
    is_valid_linkage(Z, t)

      Returns True if Z is a valid linkage matrix. The variable must
      be a 2-dimensional double numpy array with n rows and 4 columns.
      The first two columns must contain indices between 0 and 2n-1. For a
      given row i, 0 <= Z[i,0] <= i+n-1 and 0 <= Z[i,1] <= i+n-1 (i.e.
      a cluster cannot join another cluster unless the cluster being joined
      has been generated.)
    """
    valid = True
    try:
        if type(Z) is not _array_type:
            if name:
                raise TypeError('\'%s\' passed as a linkage is not a valid array.' % name)
            else:
                raise TypeError('Variable is not a valid array.')
        if Z.dtype != 'double':
            if name:
                raise TypeError('Linkage matrix \'%s\' must contain doubles (float64).' % name)
            else:
                raise TypeError('Linkage matrix must contain doubles (float64).')
        if len(Z.shape) != 2:
            if name:
                raise ValueError('Linkage matrix \'%s\' must have shape=2 (i.e. be two-dimensional).' % name)
            else:
                raise ValueError('Linkage matrix must have shape=2 (i.e. be two-dimensional).')
        if Z.shape[1] != 4:
            if name:
                raise ValueError('Linkage matrix \'%s\' must have 4 columns.' % name)
            else:
                raise ValueError('Linkage matrix must have 4 columns.')
        n = Z.shape[0]
        if not ((Z[:,0]-xrange(n-1, n*2-1) <= 0).any()) or \
           (Z[:,1]-xrange(n-1, n*2-1) <= 0).any():
            if name:
                raise ValueError('Linkage \'%s\' contains negative indices.' % name)
            else:
                raise ValueError('Linkage contains negative indices.')
    except Exception, e:
        if throw:
            raise
        if warning:
            _warning(str(e))
        valid = False
    return valid

def is_valid_y(y):
    """
    is_valid_y(y)

      Returns True if the variable y passed is a valid condensed
      distance matrix. Condensed distance matrices must be
      1-dimensional numpy arrays containing doubles. Their length
      must be a binomial coefficient {n \choose 2} for some positive
      integer n.
    """
    valid = type(y) is _array_type
    valid = valid and y.dtype == 'double'
    if valid:
        s = y.shape
    valid = valid and len(s) == 1
    if valid:
        d = int(numpy.ceil(numpy.sqrt(s[0] * 2)))
        valid = valid and (d*(d-1)/2) == s[0]
    return valid

def is_valid_dm(D, t=0.0):
    """
    is_valid_dm(D)
    
      Returns True if the variable D passed is a valid distance matrix.
      Distance matrices must be 2-dimensional numpy arrays containing
      doubles. They must have a zero-diagonal, and they must be symmetric.

    is_valid_dm(D, t)

      Returns True if the variable D passed is a valid distance matrix.
      Small numerical differences in D and D.T and non-zeroness of the
      diagonal are ignored if they are within the tolerance specified
      by t.
    """
    valid = type(D) is _array_type
    if valid:
        s = D.shape
    valid = valid and len(s) == 2
    valid = valid and s[0] == s[1]
    if t == 0.0:
        valid = valid and (D == D.T).all()
        valid = valid and (D[xrange(0, s[0]), xrange(0, s[0])] == 0).all()
    else:
        valid = valid and (D - D.T <= t).all()
        valid = valid and (D[xrange(0, s[0]), xrange(0, s[0])] <= t).all()
    return valid

def numobs_linkage(Z):
    """
    Returns the number of original observations that correspond to a
    linkage matrix Z.
    """
    is_valid_linkage(Z, throw=True, name='Z')
    return (Z.shape[0] - 1)

def numobs_dm(D):
    """
    numobs_dm(D)
    
      Returns the number of original observations that correspond to a
      square, non-condensed distance matrix D.
    """
    if not is_valid_dm(D, tol=Inf):
        raise ValueError('Z is not a valid linkage.')
    return D.shape[0]

def numobs_y(Y):
    """
    numobs_y(Y)
    
      Returns the number of original observations that correspond to a
      condensed distance matrix Y.
    """
    if not is_valid_y(y):
        raise ValueError('Z is not a valid condensed distance matrix.')
    d = int(numpy.ceil(numpy.sqrt(y.shape[0] * 2)))
    return d

def Z_y_correspond(Z, Y):
    """
    yesno = Z_y_correspond(Z, Y)
    
      Returns True if a linkage matrix Z and condensed distance matrix
      Y could possibly correspond to one another. They must have the same
      number of original observations. This function is useful as a sanity
      check in algorithms that make extensive use of linkage and distance
      matrices that must correspond to the same set of original observations.
    """
    return numobs_y(Y) == numobs_Z(Z)

def fcluster(Z, t, criterion='inconsistent', depth=2, R=None, monocrit=None):
    """

    T = fcluster(Z, t, criterion, depth=2, R=None, monocrit=None):

      Forms flat clusters from the hierarchical clustering defined by
      the linkage matrix Z. The threshold t is a required parameter.

      T is a vector of length n; T[i] is the flat cluster number to which
      original observation i belongs.

      The criterion parameter can be any of the following values,
      
        * 'inconsistent': If a cluster node and all its decendents have an
        inconsistent value less than or equal to c then all its leaf
        descendents belong to the same flat cluster. When no non-singleton
        cluster meets this criterion, every node is assigned to its
        own cluster. The depth parameter is the maximum depth to perform
        the inconsistency calculation; it has no meaning for the other
        criteria.

        * 'distance': Forms flat clusters so that the original
        observations in each flat cluster have no greater a cophenetic
        distance than t.

        * 'maxclust': Finds a minimum threshold r so that the cophenetic
        distance between any two original observations in the same flat
        cluster is no more than r and no more than t flat clusters are
        formed.

        * 'monocrit': Forms a flat cluster from a cluster node c with
        index i when monocrit[j] <= t. monocrit must be monotonic.

        monocrit is a (n-1) numpy vector of doubles; monocrit[i] is
        the criterion upon which non-singleton i is thresholded. The
        monocrit vector must be monotonic, i.e. given a node c with
        index i, for all node indices j corresponding to nodes below c,
        monocrit[i] >= monocrit[j].

        For example, to threshold on the maximum mean distance as computed
        in the inconsistency matrix R with a threshold of 0.8 do

          MR = maxRstat(Z, R, 3)
          cluster(Z, t=0.8, criterion='monocrit', monocrit=MR)

        * 'maxclust_monocrit': Forms a flat cluster from a non-singleton
        cluster node c when monocrit[i] <= r for all cluster indices i below
        and including c. r is minimized such that no more than t flat clusters
        are formed. monocrit must be monotonic.
        
        For example, to minimize the threshold t on maximum inconsistency
        values so that no more than 3 flat clusters are formed, do:

          MI = maxinconsts(Z, R)
          cluster(Z, t=3, criterion='maxclust_monocrit', monocrit=MI)
        
    """
    is_valid_linkage(Z, throw=True, name='Z')

    n = Z.shape[0] + 1
    T = numpy.zeros((n,), dtype='int32')
    
    # Since the C code does not support striding using strides.
    # The dimensions are used instead.
    [Z] = _copy_arrays_if_base_present([Z])

    if criterion == 'inconsistent':
        # Since the C code does not support striding using strides.
        # The dimensions are used instead.
        [R] = _copy_arrays_if_base_present([R])

        if R is None:
            R = inconsistent(Z, depth)
        else:
            is_valid_im(R, throw=True, name='R')
            # Since the C code does not support striding using strides.
            # The dimensions are used instead.
            [R] = _copy_arrays_if_base_present([R])
        _cluster_wrap.cluster_in_wrap(Z, R, T, float(t), int(n), int(0))
    elif criterion == 'distance':
        _cluster_wrap.cluster_dist_wrap(Z, T, float(t), int(n))
    elif criterion == 'maxclust':
        _cluster_wrap.cluster_maxclust_dist_wrap(Z, T, int(n), int(t))
    elif criterion == 'monocrit':
        [monocrit] = _copy_arrays_if_base_present([monocrit])
        _cluster_wrap.cluster_monocrit_wrap(Z, monocrit, T, int(n), int(t))
    elif criterion == 'maxclust_monocrit':
        [monocrit] = _copy_arrays_if_base_present([monocrit])
        _cluster_wrap.cluster_maxclust_monocrit_wrap(Z, monocrit, T,
                                                     float(t), int(n))
    else:
        raise ValueError('Invalid cluster formation criterion: %s' % str(criterion))
    return T

def fclusterdata(X, t, criterion='inconsistent', linkage='single', \
                distance='euclid', d=2):
    """
    T = fclusterdata(X, t)

      Clusters the original observations in the n by m data matrix X
      (n observations in m dimensions), using the euclidean distance
      metric to calculate distances between original observations,
      performs hierarchical clustering using the single linkage
      algorithm, and forms flat clusters using the inconsistency
      method with t as the cut-off threshold.

      A one-dimensional numpy array T of length n is returned. T[i]
      is the index of the flat cluster to which the original
      observation i belongs.

    T = fclusterdata(X, t, criterion='inconsistent', linkage='single',
                    dist='euclid', depth=2, R=None)

      Clusters the original observations in the n by m data matrix X using
      the thresholding criterion, linkage method, and distance metric
      specified.

      Named parameters are described below.
      
        criterion:  specifies the criterion for forming flat clusters.
                    Valid values are 'inconsistent', 'distance', or
                    'maxclust' cluster formation algorithms. See
                    cluster for descriptions.
           
        lmethod:    the linkage method to use. See linkage for
                    descriptions.

        dmethod:    the distance metric for calculating pairwise
                    distances. See pdist for descriptions and
                    linkage to verify compatibility with the linkage
                    method.
                     
        t:          the cut-off threshold for the cluster function.

        depth:      the maximum depth for the inconsistency calculation.
                    See inconsistent for more information.

        R:          the inconsistency matrix. It will be computed if
                    necessary if it is not passed.

    This function is similar to MATLAB(TM) clusterdata function.
    """

    if type(X) is not _array_type or len(X.shape) != 2:
        raise TypeError('X must be an n by m numpy array.')

    Y = pdist(X, method=dmethod)
    Z = linkage(Y, method=lmethod)
    T = fcluster(Z, criterion=criterion, depth=depth, R=R, t=t)
    return T

def lvlist(Z):
    """
    L = lvlist(Z):

      Returns a list of leaf node ids as they appear in the tree from
      left to right. Z is a linkage matrix.
    """
    is_valid_linkage(Z, throw=True, name='Z')
    n = Z.shape[0] + 1
    ML = numpy.zeros((n,), dtype='int32')
    [Z] = _copy_arrays_if_base_present([Z])
    _cluster_wrap.prelist_wrap(Z, ML, int(n))
    return ML

# Let's do a conditional import. If matplotlib is not available, 
try:
    
    import matplotlib
    import matplotlib.pylab
    _mpl = True
    
    # Maps number of leaves to text size.
    #
    # p <= 20, size="12"
    # 20 < p <= 30, size="10"
    # 30 < p <= 50, size="8"
    # 50 < p <= scipy.inf, size="6"

    _dtextsizes = {20: 12, 30: 10, 50: 8, 85: 6, scipy.inf: 5}
    _drotation =  {20: 0,          40: 45,       scipy.inf: 90}
    _dtextsortedkeys = list(_dtextsizes.keys())
    _dtextsortedkeys.sort()
    _drotationsortedkeys = list(_drotation.keys())
    _drotationsortedkeys.sort()

    def _get_tick_text_size(p):
        for k in _dtextsortedkeys:
            if p <= k:
                return _dtextsizes[k]

    def _get_tick_rotation(p):
        for k in _drotationsortedkeys:
            if p <= k:
                return _drotation[k]


    def _plot_dendrogram(icoords, dcoords, ivl, p, n, mh, orientation, no_labels, color_list, leaf_font_size=None, leaf_rotation=None):
        axis = matplotlib.pylab.gca()
        # Independent variable plot width
        ivw = len(ivl) * 10
        # Depenendent variable plot height
        dvw = mh + mh * 0.05
        ivticks = scipy.arange(5, len(ivl)*10+5, 10)
        if orientation == 'top':
            axis.set_ylim([0, dvw])
            axis.set_xlim([0, ivw])
            xlines = icoords
            ylines = dcoords
            if no_labels:
                axis.set_xticks([])
                axis.set_xticklabels([])
            else:
                axis.set_xticks(ivticks)
                axis.set_xticklabels(ivl)
            axis.xaxis.set_ticks_position('bottom')
            lbls=axis.get_xticklabels()
            if leaf_rotation:
                matplotlib.pylab.setp(lbls, 'rotation', leaf_rotation)
            else:
                matplotlib.pylab.setp(lbls, 'rotation', float(_get_tick_rotation(len(ivl))))
            if leaf_font_size:
                matplotlib.pylab.setp(lbls, 'size', leaf_font_size)
            else:
                matplotlib.pylab.setp(lbls, 'size', float(_get_tick_text_size(len(ivl))))
#            txt.set_fontsize()
#            txt.set_rotation(45)
            # Make the tick marks invisible because they cover up the links
            for line in axis.get_xticklines():
                line.set_visible(False)
        elif orientation == 'bottom':
            axis.set_ylim([dvw, 0])
            axis.set_xlim([0, ivw])
            xlines = icoords
            ylines = dcoords
            if no_labels:
                axis.set_xticks([])
                axis.set_xticklabels([])
            else:
                axis.set_xticks(ivticks)
                axis.set_xticklabels(ivl)
            lbls=axis.get_xticklabels()
            if leaf_rotation:
                matplotlib.pylab.setp(lbls, 'rotation', leaf_rotation)
            else:
                matplotlib.pylab.setp(lbls, 'rotation', float(_get_tick_rotation(p)))
            if leaf_font_size:
                matplotlib.pylab.setp(lbls, 'size', leaf_font_size)
            else:
                matplotlib.pylab.setp(lbls, 'size', float(_get_tick_text_size(p)))    
            axis.xaxis.set_ticks_position('top')
            # Make the tick marks invisible because they cover up the links
            for line in axis.get_xticklines():
                line.set_visible(False)
        elif orientation == 'left':
            axis.set_xlim([0, dvw])
            axis.set_ylim([0, ivw])
            xlines = dcoords
            ylines = icoords
            if no_labels:
                axis.set_yticks([])
                axis.set_yticklabels([])
            else:
                axis.set_yticks(ivticks)
                axis.set_yticklabels(ivl)

            lbls=axis.get_yticklabels()
            if leaf_rotation:
                matplotlib.pylab.setp(lbls, 'rotation', leaf_rotation)
            if leaf_font_size:
                matplotlib.pylab.setp(lbls, 'size', leaf_font_size)
            axis.yaxis.set_ticks_position('left')
            # Make the tick marks invisible because they cover up the
            # links
            for line in axis.get_yticklines():
                line.set_visible(False)
        elif orientation == 'right':
            axis.set_xlim([dvw, 0])
            axis.set_ylim([0, ivw])
            xlines = dcoords
            ylines = icoords
            if no_labels:
                axis.set_yticks([])
                axis.set_yticklabels([])
            else:
                axis.set_yticks(ivticks)
                axis.set_yticklabels(ivl)
            lbls=axis.get_yticklabels()
            if leaf_rotation:
                matplotlib.pylab.setp(lbls, 'rotation', leaf_rotation)
            if leaf_font_size:
                matplotlib.pylab.setp(lbls, 'size', leaf_font_size)
            axis.yaxis.set_ticks_position('right')
            # Make the tick marks invisible because they cover up the links
            for line in axis.get_yticklines():
                line.set_visible(False)
        for (xline,yline,color) in zip(xlines, ylines, color_list):
            line = matplotlib.lines.Line2D(xline, yline, color=color)
            axis.add_line(line)
        matplotlib.pylab.draw_if_interactive()
except ImportError:
    _mpl = False
    def _plot_dendrogram(*args, **kwargs):
        raise ImportError('matplotlib not available. Plot request denied.')

_link_line_colors=['g', 'r', 'c', 'm', 'y', 'k']

def dendrogram(Z, p=30, truncate_mode=None, colorthreshold=None,
               get_leaves=True, orientation='top', labels=None,
               count_sort=False, distance_sort=False, show_leaf_counts=True,
               no_plot=False, no_labels=False, color_list=None,
               leaf_font_size=None, leaf_rotation=None, leaf_label_func=None,
               no_leaves=False):
    """
    R = dendrogram(Z)

      Plots the hiearchical clustering defined by the linkage Z as a
      dendrogram. The dendrogram illustrates how each cluster is
      composed by drawing a U-shaped link between a non-singleton
      cluster and its children. The height of the top of the U-link
      is the distance between its children clusters. It is also the
      cophenetic distance between original observations in the
      two children clusters. It is expected that the distances in
      Z[:,2] be monotonic, otherwise crossings appear in the
      dendrogram.

      R is a dictionary of the data structures computed to render the
      dendrogram. Its keys are:

         'icoords': a list of lists [I1, I2, ..., Ip] where Ik is a
         list of 4 independent variable coordinates corresponding to
         the line that represents the k'th link painted.

         'dcoords': a list of lists [I2, I2, ..., Ip] where Ik is a
         list of 4 independent variable coordinates corresponding to
         the line that represents the k'th link painted.

         'ivl': a list of labels corresponding to the leaf nodes

    R = dendrogram(..., truncate_mode, p)

      The dendrogram can be hard to read when the original observation
      matrix from which the linkage is derived is large. Truncation
      is used to condense the dendrogram. There are several modes:

       * None/'none': no truncation is performed

       * 'lastp': the last p non-singleton formed in the linkage are
       the only non-leaf nodes in the linkage; they correspond to
       to rows Z[n-p-2:end] in Z. All other non-singleton clusters
       are contracted into leaf nodes.

       * 'mlab': This corresponds to MATLAB(TM) behavior. (not implemented)

       * 'level'/'mtica': no more than p levels of the dendrogram tree
       are displayed. This corresponds to Mathematica(TM) behavior.

    R = dendrogram(..., colorthreshold=t)

      Colors all the descendent links below a cluster node k the same color
      if k is the first node below the cut threshold t. All links connecting
      nodes with distances greater than or equal to the threshold are
      colored blue. If t is less than or equal to zero, all nodes
      are colored blue. If t is None or 'default', corresponding with
      MATLAB(TM) behavior, the threshold is set to 0.7*max(Z[:,2]).

    R = dendrogram(..., get_leaves=True)

      Includes a list R['leaves']=H in the result dictionary. For each i,
      H[i] == j, cluster node j appears in the i'th position in the
      left-to-right traversal of the leaves, where j < 2n-1 and i < n.

    R = dendrogram(..., get_node_stats=True)

      Includes a list R['node_ids'] in the result dictionary. The i'th
      value is the node index k (where k > n) to which linkage line i
      corresponds.

    R = dendrogram(..., orientation)

      Plots the dendrogram in a particular direction. The orientation
      parameter can be any of:

        * 'top': plots the root at the top, and plot descendent
          links going downwards. (default).
           
        * 'bottom': plots the root at the bottom, and plot descendent
          links going upwards.

        * 'left': plots the root at the left, and plot descendent
          links going right.

        * 'right': plots the root at the right, and plot descendent
          links going left.

    R = dendrogram(..., labels=None)

        The labels parameter is a n-sized list (or tuple). The labels[i]
        value is the text to put under the i'th leaf node only if it
        corresponds to an original observation and not a non-singleton
        cluster.

        When labels=None, the index of the original observation is used
        used.
        
    R = dendrogram(..., count_sort)

        When plotting a cluster node and its directly descendent links,
        the order the two descendent links and their descendents are
        plotted is determined by the count_sort parameter. Valid values
        of count_sort are:

          * False: nothing is done.
          
          * 'ascending'/True: the child with the minimum number of
          original objects in its cluster is plotted first.

          * 'descendent': the child with the maximum number of
          original objects in its cluster is plotted first.

    R = dendrogram(..., distance_sort)

        When plotting a cluster node and its directly descendent links,
        the order the two descendent links and their descendents are
        plotted is determined by the distance_sort parameter. Valid
        values of count_sort are:

          * False: nothing is done.

          * 'ascending'/True: the child with the minimum distance
          between its direct descendents is plotted first.

          * 'descending': the child with the maximum distance
          between its direct descendents is plotted first.

        Note that either count_sort or distance_sort must be False.

    R = dendrogram(..., show_leaf_counts)

        When show_leaf_counts=True, leaf nodes representing k>1
        original observation are labeled with the number of observations
        they contain in parentheses.

    R = dendrogram(..., no_plot)

        When no_plot=True, the final rendering is not performed. This is
        useful if only the data structures computed for the rendering
        are needed or if matplotlib is not available.

    R = dendrogram(..., no_labels)

        When no_labels=True, no labels appear next to the leaf nodes in
        the rendering of the dendrogram.

    R = dendrogram(..., leaf_label_rotation):

        Specifies the angle to which the leaf labels are rotated. When
        unspecified, the rotation based on the number of nodes in the
        dendrogram.

    R = dendrogram(..., leaf_font_size):

        Specifies the font size in points of the leaf labels. When
        unspecified, the size  based on the number of nodes
        in the dendrogram.


    R = dendrogram(..., leaf_label_func)

        When a callable function is passed, leaf_label_func is passed
        cluster index k, and returns a string with the label for the
        leaf.
        
        Indices k < n correspond to original observations while indices
        k >= n correspond to non-singleton clusters.

        For example, to label singletons with their node id and
        non-singletons with their id, count, and inconsistency coefficient,
        we simply do

          # First define the leaf label function.
          llf = lambda id:
                   if id < n:
                      return str(id)
                   else:
                      return '[%d %d %1.2f]' % (id, count, R[n-id,3])

          # The text for the leaf nodes is going to be big so force
          # a rotation of 90 degrees.
          dendrogram(Z, leaf_label_func=llf, leaf_rotation=90)

        Next, let's cluster Sir Ronald Fisher's flower data set,
        originally published in his 1936 paper on discriminant analysis.
        We will use some defaults: single linkage and Euclidean distance.
        In this example, the leaves correspond to one of two different
        flower types, I. setosa or I. virginica. The leaf labels are
        too long to be displayed horizontally, side-by-side due to the
        length of the label strings and the number of flowers being
        clustered. Therefore, we rotate the labels 90 degrees, and use
        a leaf label function to label the leaves according to flower
        type and number.

          iris_labels = ('I. virginica', 'I. setosa')
          iris_Y=load('irisY.txt')
          iris_X=load('irisX.txt')
          Y = pdist(iris_X)
          Z = linkage(Y)
          llf = lambda id:
                   if id < n:
                      return "%s (%d)" % (iris_labels[Y[id]], id)
                   else:
                      return ""
          dendrogram(Z, p=0, leaf_label_func=llf, leaf_rotation=90)

    R = dendrogram(..., show_contracted=False)

        The heights of non-singleton nodes contracted into a leaf node
        are plotted as crosses along the link connecting that leaf node.
        This feature is only useful when truncation is used.
    """

    # Features under consideration.
    #
    #         ... = dendrogram(..., leaves_order=None)
    #
    #         Plots the leaves in the order specified by a vector of
    #         original observation indices. If the vector contains duplicates
    #         or results in a crossing, an exception will be thrown. Passing
    #         None orders leaf nodes based on the order they appear in the
    #         pre-order traversal.

    if not is_valid_linkage(Z):
        raise TypeError('If the first argument is an array, it must be a valid linkage.')
    Zs = Z.shape
    n = Zs[0] + 1
    if type(p) in (types.IntType, types.FloatType):
        p = int(p)
    else:
        raise TypeError('The second argument must be a number')

    if truncate_mode == 'lastp' or truncate_mode == 'mlab':
        if p > n or p == 0:
            p = n

    if truncate_mode == 'mtica' or truncate_mode == 'level':
        if p < 0:
            p = scipy.inf


    if get_leaves:
        lvs = []
    else:
        lvs = None
    icoord_list=[]
    dcoord_list=[]
    color_list=[]
    current_color=[0]
    currently_below_threshold=[False]
    if no_leaves:
        ivl=None
    else:
        ivl=[]
    if colorthreshold is None or \
       (type(colorthreshold) == types.StringType and colorthreshold=='default'):
        colorthreshold = max(Z[:,2])*0.7
    R={'icoord':icoord_list, 'dcoord':dcoord_list, 'ivl':ivl, 'leaves':lvs,
       'color_list':color_list}
    props = {'cbt': False, 'cc':0}
    _dendrogram_calculate_info(Z=Z, p=p,
                               truncate_mode='none', \
                               colorthreshold=colorthreshold, \
                               get_leaves=get_leaves, \
                               orientation=orientation, \
                               labels=labels, \
                               count_sort=count_sort, \
                               distance_sort=distance_sort, \
                               show_leaf_counts=show_leaf_counts, \
                               i=2*n-2, iv=0.0, ivl=ivl, n=n, \
                               icoord_list=icoord_list, \
                               dcoord_list=dcoord_list, lvs=lvs, \
                               current_color=current_color, \
                               color_list=color_list, \
                               currently_below_threshold=currently_below_threshold, \
                               leaf_label_func=leaf_label_func)
    if not no_plot:
        mh = max(Z[:,2])
        _plot_dendrogram(icoord_list, dcoord_list, ivl, p, n, mh, orientation, no_labels, color_list, leaf_font_size=leaf_font_size, leaf_rotation=leaf_rotation)

    return R

def _append_singleton_leaf_node(Z, p, n, level, lvs, ivl, leaf_label_func, i, labels):
    # If the leaf id structure is not None and is a list then the caller
    # to dendrogram has indicated that cluster id's corresponding to the
    # leaf nodes should be recorded.

    if lvs is not None:
        lvs.append(int(i))

    # If leaf node labels are to be displayed...
    if ivl is not None:
        # If a leaf_label_func has been provided, the label comes from the
        # string returned from the leaf_label_func, which is a function
        # passed to dendrogram.
        if leaf_label_func:
            ivl.append(leaf_label_func(i))
        else:
            # Otherwise, if the dendrogram caller has passed a labels list
            # for the leaf nodes, use it.
            if labels is not None:
                ivl.append(labels[i-n])
            else:
                # Otherwise, use the id as the label for the leaf.x
                ivl.append(str(int(i)))

def _append_nonsingleton_leaf_node(Z, p, n, level, lvs, ivl, leaf_label_func, i):
    # If the leaf id structure is not None and is a list then the caller
    # to dendrogram has indicated that cluster id's corresponding to the
    # leaf nodes should be recorded.

    if lvs is not None:
        lvs.append(int(i))
    if ivl is not None:
        if leaf_label_func:
            ivl.append(leaf_label_func(i))
        else:
            if show_leaf_counts:
                ivl.append("(" + str(int(Z[i-n, 3])) + ")")
            else:
                ivl.append("")   


def _dendrogram_calculate_info(Z, p, truncate_mode, \
                               colorthreshold=scipy.inf, get_leaves=True, \
                               orientation='top', labels=None, \
                               count_sort=False, distance_sort=False, \
                               show_leaf_counts=False, i=-1, iv=0.0, \
                               ivl=[], n=0, icoord_list=[], dcoord_list=[], \
                               lvs=None, mhr=False, \
                               current_color=[], color_list=[], \
                               currently_below_threshold=[], \
                               leaf_label_func=None, level=0):
    """
    Calculates the endpoints of the links as well as the labels for the
    the dendrogram rooted at the node with index i. iv is the independent
    variable value to plot the left-most leaf node below the root node i
    (if orientation='top', this would be the left-most x value where the
    plotting of this root node i and its descendents should begin).
    
    ivl is a list to store the labels of the leaf nodes. The leaf_label_func
    is called whenever ivl != None, labels == None, and
    leaf_label_func != None. When ivl != None and labels != None, the
    labels list is used only for labeling the the leaf nodes. When
    ivl == None, no labels are generated for leaf nodes.

    When get_leaves==True, a list of leaves is built as they are visited
    in the dendrogram.

    Returns a tuple with l being the independent variable coordinate that
    corresponds to the midpoint of cluster to the left of cluster i if
    i is non-singleton, otherwise the independent coordinate of the leaf
    node if i is a leaf node.

    Returns a tuple (left, w, h, md)

      * left is the independent variable coordinate of the center of the
        the U of the subtree
        
      * w is the amount of space used for the subtree (in independent
        variable units)

      * h is the height of the subtree in dependent variable units

      * is the max(Z[*,2]) for all nodes * below and including
        the target node.
    
    """
    if n == 0:
        raise ValueError("Invalid singleton cluster count n.")

    if i == -1:
        raise ValueError("Invalid root cluster index i.")


    if truncate_mode == 'lastp':
        # If the node is a leaf node but corresponds to a non-single cluster,
        # it's label is either the empty string or the number of original
        # observations belonging to cluster i.
        if i < 2*n-p and i >= n:
            d = Z[i-n, 2]
            _append_nonsingleton_leaf_node(Z, p, n, level, lvs, ivl, leaf_label_func, i, labels)
            return (iv + 5.0, 10.0, 0.0, d)
        elif i < n:
            _append_singleton_leaf_node(Z, p, n, level, lvs, ivl, leaf_label_func, i, labels)
            return (iv + 5.0, 10.0, 0.0, 0.0)
    elif truncate_mode in ('mtica', 'level'):
        if i > n and level > p:
            d = Z[i-n, 2]
            _append_nonsingleton_leaf_node(Z, p, n, level, lvs, ivl, leaf_label_func, i, labels)
            return (iv + 5.0, 10.0, 0.0, d)
        elif i < n:
            _append_singleton_leaf_node(Z, p, n, level, lvs, ivl, leaf_label_func, i, labels)
            return (iv + 5.0, 10.0, 0.0, 0.0)
    elif truncate_mode in ('mlab'):
        pass

    
    # Otherwise, only truncate if we have a leaf node.
    #
    # If the truncate_mode is mlab, the linkage has been modified
    # with the truncated tree.
    #
    # Only place leaves if they correspond to original observations.
    if i < n:
        _append_singleton_leaf_node(Z, p, n, level, lvs, ivl, leaf_label_func, i, labels)
        return (iv + 5.0, 10.0, 0.0, 0.0)

    # !!! Otherwise, we don't have a leaf node, so work on plotting a
    # non-leaf node.
    # Actual indices of a and b
    aa = Z[i-n, 0]
    ab = Z[i-n, 1]
    if aa > n:
        # The number of singletons below cluster a
        na = Z[aa-n, 3]
        # The distance between a's two direct children.
        da = Z[aa-n, 2]
    else:
        na = 1
        da = 0.0
    if ab > n:
        nb = Z[ab-n, 3]
        db = Z[ab-n, 2]
    else:
        nb = 1
        db = 0.0

    if count_sort == 'ascending' or count_sort == True:
        # If a has a count greater than b, it and its descendents should
        # be drawn to the right. Otherwise, to the left.
        if na > nb:
            # The cluster index to draw to the left (ua) will be ab
            # and the one to draw to the right (ub) will be aa
            ua = ab
            ub = aa
        else:
            ua = aa
            ub = ab
    elif count_sort == 'descending':
        # If a has a count less than or equal to b, it and its
        # descendents should be drawn to the left. Otherwise, to
        # the right.
        if na > nb:
            ua = aa
            ub = ab
        else:
            ua = ab
            ub = aa
    elif distance_sort == 'ascending' or distance_sort == True:
        # If a has a distance greater than b, it and its descendents should
        # be drawn to the right. Otherwise, to the left.
        if da > db:
            ua = ab
            ub = aa
        else:
            ua = aa
            ub = ab
    elif distance_sort == 'descending':
        # If a has a distance less than or equal to b, it and its
        # descendents should be drawn to the left. Otherwise, to
        # the right.
        if da > db:
            ua = aa
            ub = ab
        else:
            ua = ab
            ub = aa
    else:
        ua = aa
        ub = ab

    # The distance of the cluster to draw to the left (ua) is uad
    # and its count is uan. Likewise, the cluster to draw to the
    # right has distance ubd and count ubn.
    if ua < n:
        uad = 0.0
        uan = 1
    else:
        uad = Z[ua-n, 2]
        uan = Z[ua-n, 3]
    if ub < n:
        ubd = 0.0
        ubn = 1
    else:
        ubd = Z[ub-n, 2]
        ubn = Z[ub-n, 3]

    # Updated iv variable and the amount of space used.
    (uiva, uwa, uah, uamd) = \
          _dendrogram_calculate_info(Z=Z, p=p, \
                                     truncate_mode=truncate_mode, \
                                     colorthreshold=colorthreshold, \
                                     get_leaves=get_leaves, \
                                     orientation=orientation, \
                                     labels=labels, \
                                     count_sort=count_sort, \
                                     distance_sort=distance_sort, \
                                     show_leaf_counts=show_leaf_counts, \
                                     i=ua, iv=iv, ivl=ivl, n=n, \
                                     icoord_list=icoord_list, \
                                     dcoord_list=dcoord_list, lvs=lvs, \
                                     current_color=current_color, \
                                     color_list=color_list, \
                                     currently_below_threshold=currently_below_threshold, \
                                     leaf_label_func=leaf_label_func, \
                                     level=level+1)

    h = Z[i-n, 2]
    if h >= colorthreshold or colorthreshold <= 0:
        c = 'b'

        if currently_below_threshold[0]:
            current_color[0] = (current_color[0] + 1) % len(_link_line_colors)
        currently_below_threshold[0] = False
    else:
        currently_below_threshold[0] = True
        c = _link_line_colors[current_color[0]]

    (uivb, uwb, ubh, ubmd) = \
          _dendrogram_calculate_info(Z=Z, p=p, \
                                     truncate_mode=truncate_mode, \
                                     colorthreshold=colorthreshold, \
                                     get_leaves=get_leaves, \
                                     orientation=orientation, \
                                     labels=labels, \
                                     count_sort=count_sort, \
                                     distance_sort=distance_sort, \
                                     show_leaf_counts=show_leaf_counts, \
                                     i=ub, iv=iv+uwa, ivl=ivl, n=n, \
                                     icoord_list=icoord_list, \
                                     dcoord_list=dcoord_list, lvs=lvs, \
                                     current_color=current_color, \
                                     color_list=color_list, \
                                     currently_below_threshold=currently_below_threshold,
                                     leaf_label_func=leaf_label_func, \
                                     level=level+1)
    # The height of clusters a and b
    ah = uad
    bh = ubd

    max_dist = max(uamd, ubmd, h)

    icoord_list.append([uiva, uiva, uivb, uivb])
    dcoord_list.append([uah, h, h, ubh])
    color_list.append(c)
    return ( ((uiva + uivb) / 2), uwa+uwb, h, max_dist)

def is_isomorphic(T1, T2):
    """
      Returns True iff two different cluster assignments T1 and T2 are
      equivalent. T1 and T2 must be arrays of the same size.
    """
    if type(T1) is not _array_type:
        raise TypeError('T1 must be a numpy array.')
    if type(T2) is not _array_type:
        raise TypeError('T2 must be a numpy array.')

    T1S = T1.shape
    T2S = T2.shape

    if len(T1S) != 1:
        raise ValueError('T1 must be one-dimensional.')
    if len(T2S) != 1:
        raise ValueError('T2 must be one-dimensional.')
    if T1S[0] != T2S[0]:
        raise ValueError('T1 and T2 must have the same number of elements.')
    n = T1S[0]
    d = {}
    for i in xrange(0,n):
        if T1[i] in d.keys():
            if d[T1[i]] != T2[i]:
                return False
        else:
            d[T1[i]] = T2[i]
    return True
    
def maxdists(Z):
    """
    MD = maxdists(Z)

      MD is a (n-1)-sized numpy array of doubles; MD[i] represents the
      maximum distance between any cluster (including singletons) below
      and including the node with index i. More specifically,
      MD[i] = Z[Q(i)-n, 2].max() where Q(i) is the set of all node indices
      below and including node i.
      
      Note that when Z[:,2] is monotonic, Z[:,2] and MD should not differ.
      See linkage for more information on this issue.
    """
    is_valid_linkage(Z, throw=True, name='Z')
    
    n = Z.shape[0] + 1
    MD = numpy.zeros((n-1,))
    [Z] = _copy_arrays_if_base_present([Z])
    _cluster_wrap.get_max_dist_for_each_cluster_wrap(Z, MD, int(n))
    return MD

def maxinconsts(Z, R):
    """
    MI = maxinconsts(Z, R)

      Calculates the maximum inconsistency coefficient for each node
      and its descendents. Z is a valid linkage matrix and R is a valid
      inconsistency matrix. MI is a monotonic (n-1)-sized numpy array of
      doubles.
    """
    is_valid_linkage(Z, throw=True, name='Z')
    is_valid_im(R, throw=True, name='R')
    
    n = Z.shape[0] + 1
    MI = numpy.zeros((n-1,))
    [Z, R] = _copy_arrays_if_base_present([Z, R])
    _cluster_wrap.get_max_Rfield_for_each_cluster_wrap(Z, R, MI, int(n), 3)
    return MI

def maxRstat(Z, R, i):
    """
    MR = maxRstat(Z, R, i)

    Calculates the maximum statistic for the i'th column of the
    inconsistency matrix R for each non-singleton cluster node. MR[j]
    is the maximum over R[Q(j)-n, i] where Q(j) the set of all node ids
    corresponding to nodes below and including j.
    """
    is_valid_linkage(Z, throw=True, name='Z')
    is_valid_im(R, throw=True, name='R')
    if type(i) is not type.IntType:
        raise TypeError('The third argument must be an integer.')
    if i < 0 or i > 3:
        return ValueError('i must be an integer between 0 and 3 inclusive.')

    n = Z.shape[0] + 1
    MR = numpy.zeros((n-1,))
    [Z, R] = _copy_arrays_if_base_present([Z, R])
    _cluster_wrap.get_max_Rfield_for_each_cluster_wrap(Z, R, MR, int(n), i)
    return MR

def leaders(Z, T):
    """
    (L, M) = leaders(Z, T):

    For each flat cluster j of the k flat clusters represented in the
    n-sized flat cluster assignment vector T, this function finds the
    lowest cluster node i in the linkage tree Z such that:

      * leaf descendents belong only to flat cluster j (i.e. T[p]==j
        for all p in S(i) where S(i) is the set of leaf ids of leaf
        nodes descendent with cluster node i)

      * there does not exist a leaf that is not descendent with i
        that also belongs to cluster j (i.e. T[q]!=j for all q not in S(i)).
        If this condition is violated, T is not a valid cluster assignment
        vector, and an exception will be thrown.

    Two k-sized numpy vectors are returned, L and M. L[j]=i is the linkage
    cluster node id that is the leader of flat cluster with id M[j]. If
    i < n, i corresponds to an original observation, otherwise it
    corresponds to a non-singleton cluster.
    """
    if type(T) != _array_type or T.dtype != 'int':
        raise TypeError('T must be a one-dimensional numpy array of integers.')
    is_valid_linkage(Z, throw=True, name='Z')
    if len(T) != Z.shape[0] + 1:
        raise ValueError('Mismatch: len(T)!=Z.shape[0] + 1.')
    
    Cl = numpy.unique(T)
    k = len(Cl)
    L = numpy.zeros((k,), dtype='int32')
    M = numpy.zeros((k,), dtype='int32')
    n = Z.shape[0]
    [Z, T] = _copy_arrays_if_base_present([Z, T])
    s = _cluster_wrap.leaders_wrap(Z, T, L, M, int(n))
    if s >= 0:
        raise ValueError('T is not a valid assignment vector. Error found when examining linkage node %d (< 2n-1).' % i)
    return (L, M)
