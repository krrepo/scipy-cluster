/**
 * cluster.c
 *
 * Author: Damian Eads
 * Date:   September 22, 2007
 *
 * Copyright (c) 2007, Damian Eads
 *
 * All rights reserved.
 *
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions
 * are met:
 *   - Redistributions of source code must retain the above
 *     copyright notice, this list of conditions and the
 *     following disclaimer.
 *   - Redistributions in binary form must reproduce the above copyright
 *     notice, this list of conditions and the following disclaimer
 *     in the documentation and/or other materials provided with the
 *     distribution.
 *   - Neither the name of the author nor the names of its
 *     contributors may be used to endorse or promote products derived
 *     from this software without specific prior written permission.
 *
 * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
 * "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
 * LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
 * A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
 * OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
 * SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
 * LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
 * DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
 * THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
 * (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
 * OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
 */

#define NCHOOSE2(_n) ((_n)*(_n-1)/2)
#define ISCLUSTER(_nd) ((_nd)->id >= n)
#define GETCLUSTER(_id) ((lists + _id - n))

#define CPY_MAX(_x, _y) ((_x > _y) ? (_x) : (_y))
#define CPY_MIN(_x, _y) ((_x < _y) ? (_x) : (_y))


#include <malloc.h>
#include <string.h>
#include <stdio.h>
#include <math.h>

#include "cluster.h"

double euclidean_distance(const double *u, const double *v, int n) {
  int i = 0;
  double s = 0.0, d;
  for (i = 0; i < n; i++) {
    d = u[i] - v[i];
    s = s + d * d;
  }
  return sqrt(s);
}

double city_block_distance(const double *u, const double *v, int n) {
  int i = 0;
  double s = 0.0, d;
  for (i = 0; i < n; i++) {
    d = fabs(u[i] - v[i]);
    s = s + d;
  }
  return s;
}

double minkowski_distance(const double *u, const double *v, int n, double p) {
  int i = 0;
  double s = 0.0, d;
  for (i = 0; i < n; i++) {
    d = fabs(u[i] - v[i]);
    s = s + pow(d, p);
  }
  return pow(s, 1.0 / p);
}

void compute_mean_vector(double *res, const double *X, int m, int n) {
  int i, j;
  const double *v;
  for (i = 0; i < n; i++) {
    res[i] = 0.0;
  }
  for (j = 0; j < m; j++) {

    v = X + (j * n);
    for (i = 0; i < n; i++) {
      res[i] += v[i];
    }
  }
  for (i = 0; i < n; i++) {
    res[i] /= (double)m;
  }
}

void vector_subtract(double *result, const double *u, const double *v, int n) {
  int i;
  for (i = 0; i < n; i++) {
    result[i] = u[i] - v[i];
  }
}

void pdist_euclidean(const double *X, double *dm, int m, int n) {
  int i, j;
  const double *u, *v;
  double *it = dm;
  for (i = 0; i < m; i++) {
    for (j = i + 1; j < m; j++, it++) {
      u = X + (n * i);
      v = X + (n * j);
      *it = euclidean_distance(u, v, n);
    }
  }
}

void pdist_city_block(const double *X, double *dm, int m, int n) {
  int i, j;
  const double *u, *v;
  double *it = dm;
  for (i = 0; i < m; i++) {
    for (j = i + 1; j < m; j++, it++) {
      u = X + (n * i);
      v = X + (n * j);
      *it = city_block_distance(u, v, n);
    }
  }
}

void pdist_minkowski(const double *X, double *dm, int m, int n, double p) {
  int i, j;
  const double *u, *v;
  double *it = dm;
  for (i = 0; i < m; i++) {
    for (j = i + 1; j < m; j++, it++) {
      u = X + (n * i);
      v = X + (n * j);
      *it = minkowski_distance(u, v, n, p);
    }
  }
}


void chopmins(int *ind, int mini, int minj, int np) {
  int i;
  /**  if (mini < np - 2) {**/
  for (i = mini; i < minj - 1; i++) {
    ind[i] = ind[i + 1];
  }
  /**}**/
  /**  if (minj < np - 2) {**/
  for (i = minj - 1; i < np - 2; i++) {
    ind[i] = ind[i + 2];
  }
  /**  }**/
  /**  if (np > 0) {
    ind[np - 1] = HUGE_VALF;
  }
  if (np > 1) {
    ind[np - 2] = INFINITY;
    }***/
  /**  fprintf(stderr, "[Remove mini=%d minj=%d]\n", mini, minj);**/
}

void chopmins_ns_ij(double *ind, int mini, int minj, int np) {
  int i;
  /**if (mini < np - 2) {**/
  for (i = mini; i < minj - 1; i++) {
    ind[i] = ind[i + 1];
  }
  /**}**/
  /**if (minj < np - 2) {**/
  for (i = minj - 1; i < np - 2; i++) {
    ind[i] = ind[i + 2];
  }
  /**}**/
  /**  if (np > 0) {
    ind[np - 1] = INFINITY;
  }
  if (np > 1) {
    ind[np - 2] = INFINITY;
    }**/
}

void chopmins_ns_i(double *ind, int mini, int np) {
  int i;
    for (i = mini; i < np - 1; i++) {
      ind[i] = ind[i + 1];
    }
    /**  if (np > 0) {
    ind[np - 1] = INFINITY;
    }**/
}

void dist_single(cinfo *info, int mini, int minj, int np, int n) {
  double **rows = info->rows;
  double *buf = info->buf;
  double *bit;
  int i;
  bit = buf;
  for (i = 0; i < mini; i++, bit++) {
    *bit = CPY_MIN(*(rows[i] + mini - i - 1), *(rows[i] + minj - i - 1));
  }
  for (i = mini + 1; i < minj; i++, bit++) {
    *bit = CPY_MIN(*(rows[mini] + i - mini - 1), *(rows[i] + minj - i - 1));
  }
  for (i = minj + 1; i < np; i++, bit++) {
    *bit = CPY_MIN(*(rows[mini] + i - mini - 1), *(rows[minj] + i - minj - 1));
  }
  /**  fprintf(stderr, "[");
  for (i = 0; i < np - 2; i++) {
    fprintf(stderr, "%5.5f ", buf[i]);
  }
  fprintf(stderr, "]");**/
}

void dist_complete(cinfo *info, int mini, int minj, int np, int n) {
  double **rows = info->rows;
  double *buf = info->buf;
  double *bit;
  int i;
  bit = buf;
  for (i = 0; i < mini; i++, bit++) {
    *bit = CPY_MAX(*(rows[i] + mini - i - 1), *(rows[i] + minj - i - 1));
  }
  for (i = mini + 1; i < minj; i++, bit++) {
    *bit = CPY_MAX(*(rows[mini] + i - mini - 1), *(rows[i] + minj - i - 1));
  }
  for (i = minj + 1; i < np; i++, bit++) {
    *bit = CPY_MAX(*(rows[mini] + i - mini - 1), *(rows[minj] + i - minj - 1));
  }
}

/** BROKEN **/
void dist_average(cinfo *info, int mini, int minj, int np, int n) {
  double **rows = info->rows;
  double *buf = info->buf;
  double *bit;
  int i;
  bit = buf;
  /**  double ni = (double)info->nodes[info->ind[mini]].n;
       double nj = (double)info->nodes[info->ind[minj]].n;**/

  for (i = 0; i < mini; i++, bit++) {
    *bit = CPY_MAX(*(rows[i] + mini - i - 1), *(rows[i] + minj - i - 1));
  }
  for (i = mini + 1; i < minj; i++, bit++) {
    *bit = CPY_MAX(*(rows[mini] + i - mini - 1), *(rows[i] + minj - i - 1));
  }
  for (i = minj + 1; i < np; i++, bit++) {
    *bit = CPY_MAX(*(rows[mini] + i - mini - 1), *(rows[minj] + i - minj - 1));
  }
}

void recompute_centroid(const cnode *lnode, const cnode *rnode,
			const double *lv, const double *rv,
			double *result, int n) {
  int i;
  for (i = 0; i < n;  i++) {
    result[i] = (lv[i] * (double)lnode->n) + (rv[i] * (double)rnode->n);
    result[i] = result[i] * 1 / ((double)(lnode->n + rnode->n));
  }
}

void print_dm(const double **rows, int np) {
  int i, j, k;
  const double *row;
  fprintf(stderr, "[DM, np=%d\n", np);
  for (i = 0; i < np - 1; i++) {
    row = rows[i];
    for (j = 0; j <= i; j++) {
      fprintf(stderr, "%5.5f ", 0.0);
    }

    for (k = 0, j = i + 1; j < np; j++, k++) {
      fprintf(stderr, "%5.5f ", *(row + k)/1000000.0);
    }
    fprintf(stderr, "|j=%d|\n", i + 1);
  }
}

void print_ind(const int *inds, int np) {
  int i;
  fprintf(stderr, "[IND, np=%d || ", np);
  for (i = 0; i < np; i++) {
    fprintf(stderr, "%d ", inds[i]);
  }
  fprintf(stderr, "]\n");
}

/**
 *
 * dm:    The distance matrix
 * Z:     The result of the linkage, a (n-1) x 3 matrix
 * n:     The number of objects
 * ml:    A boolean indicating whether a list of objects in the forest
 *        clusters should be maintained.
 * euc:   Euclidean space distances.
 */
void linkage(double *dm, double *Z, int n, int ml, distfunc dfunc) {
  int i, j, k, np, nid, mini, minj;
  double min;
  int *ind;
  /** An iterator through the distance matrix. */
  double *dmit, *buf;

  int *rowsize;

  /** Temporary array to store modified distance matrix. */
  double *dmt, **rows;
  clist *lists, *listL, *listR, *listC;
  clnode *lnodes;
  cnode *nodes, *node;

  cinfo info;


  /** The next two are only necessary for euclidean distance methods. */
  if (ml) {
    lists = (clist*)malloc(sizeof(clist) * (n-1));
    lnodes = (clnode*)malloc(sizeof(clnode) * n);
  }
  else {
    lists = 0;
    lnodes = 0;
  }
  nodes = (cnode*)malloc(sizeof(cnode) * (n * 2) - 1);
  ind = (int*)malloc(sizeof(int) * n);
  dmt = (double*)malloc(sizeof(double) * NCHOOSE2(n));
  buf = (double*)malloc(sizeof(double) * n);
  rows = (double**)malloc(sizeof(double*) * n);
  rowsize = (int*)malloc(sizeof(int) * n);
  memcpy(dmt, dm, sizeof(double) * NCHOOSE2(n));

  info.nodes = nodes;
  info.ind = ind;
  info.dmt = dmt;
  info.buf = buf;
  info.rows = rows;
  info.rowsize = rowsize;
  info.dm = dm;

  for (i = 0; i < n; i++) {
    ind[i] = i;
    node = nodes + i;
    node->left = 0;
    node->right = 0;
    node->id = i;
    node->n = 1;
    node->d = 0.0;
    rowsize[i] = n - 1 - i;
  }
  rows[0] = dmt;
  for (i = 1; i < n; i++) {
    rows[i] = rows[i-1] + n - i;
  }
  
  if (ml) {
    for (i = 0; i < n; i++) {
      (lnodes + i)->val = nodes + i;
      (lnodes + i)->next = 0;
    }
  }

  for (k = 0, nid = n; k < n - 1; k++, nid++) {
    np = n - k;
    /**    fprintf(stderr, "k=%d, nid=%d, n=%d np=%d\n", k, nid, n, np);**/
    min = dmt[0];
    mini = 0;
    minj = 1;
    /** Note that mini < minj since j > i is always true. */
    for (i = 0; i < np - 1; i++) {
      dmit = rows[i];
      for (j = i + 1; j < np; j++, dmit++) {
	if (*dmit < min) {
	  min = *dmit;
	  mini = i;
	  minj = j;
	}
      }
    }

    node = nodes + nid;
    node->left = nodes + ind[mini];
    node->right = nodes + ind[minj];
    node->n = node->left->n + node->right->n;
    node->d = min;
    node->id = nid;

    *(Z + (k * 3)) = node->left->id;
    *(Z + (k * 3) + 1) = node->right->id;
    *(Z + (k * 3) + 2) = min;

    /**    fprintf(stderr,
	    "[lid=%d, rid=%d, llid=%d, rrid=%d m=%5.8f]",
	    node->left->id, node->right->id, ind[mini], ind[minj], min);**/

    if (ml) {
      listC = GETCLUSTER(nid);
      if (ISCLUSTER(node->left) != 0) {
	listL = GETCLUSTER(node->left->id);
	if (ISCLUSTER(node->right) != 0) {
	  listR = GETCLUSTER(node->right->id);
	  listL->tail->next = listR->head;
	  listC->tail = listR->tail;
	  listR->tail->next = 0;
	}
	else {
	  listC->tail = lnodes + node->right->id;
	  listL->tail->next = listC->tail;
	  listC->tail->next = 0;
	}
	listC->head = listL->head;
      }
      else {
	listC->head = lnodes + node->left->id;
	if (ISCLUSTER(node->right)) {
	  listR = GETCLUSTER(node->right->id);
	  listC->head->next = listR->head;
	  listC->tail = listR->tail;
	  listC->tail->next = 0;
	}
	else {
	  listC->tail = lnodes + node->right->id;
	  listC->tail->next = 0;
	  listC->head->next = listC->tail;
	}
      }
    }
    /**    print_dm(rows, np);**/
    /**    dfunc(buf, rows, mini, minj, np, dm, n, ind, nodes);**/
    dfunc(&info, mini, minj, np, n);

    /** For these rows, we must remove, i and j but leave all unused space
        at the end. This reduces their size by two.*/
    for (i = 0; i < mini; i++) {
      chopmins_ns_ij(rows[i], mini - i - 1, minj - i - 1, rowsize[i]);
    }

    /** We skip the i'th row. For rows i+1 up to j-1, we just remove j. */
    for (i = mini + 1; i < minj; i++) {
      chopmins_ns_i(rows[i], minj - i - 1, rowsize[i]);
    }

    /** For rows 0 to mini - 1, we move them down the matrix, leaving the
	first row free. */
    /**    for (i = mini; i > 0; i--) {
      memcpy(rows[i], rows[i-1], sizeof(double) * rowsize[i]-k);
      }**/

    for (i = mini; i < minj - 1; i++) {
      memcpy(rows[i], rows[i+1], sizeof(double) * (rowsize[i+1]));
    }

    /** For rows mini+1 to minj-1, we do nothing since they are in the
	right place for the next iteration. For rows minj+1 onward,
	we move them to the right. */
	
    for (i = minj - 1; i < np - 2; i++) {
      memcpy(rows[i], rows[i+2], sizeof(double) * (rowsize[i+2]));
    }

    /** Rows i+1 to j-1 lose one unit of space, so we move them up. */
    /** Rows j to np-1 lose no space. We do nothing to them. */

    /**    memcpy(rows[0], buf, sizeof(double) * rowsize[0] - k);*/

    for (i = 0; i < np - 2; i++) {
      *(rows[i] + np - 3 - i) = buf[i];
    }
    /**    print_dm(rows, np - 1);
	   print_ind(ind, np);**/
    chopmins(ind, mini, minj, np);
    ind[np - 2] = nid;
    /**    print_ind(ind, np - 1);**/
  }
  free(lists);
  free(lnodes);
  free(nodes);
  free(ind);
  free(dmt);
  free(buf);
  free(rows);
  free(rowsize);
}

/**
 * endpnts is a (n-1) by 4 by 2 array
 *
 * ctrpnts is a (n-1) by 2 by 2 array
 *
 * edge is a (n-1) by 2 by 2 array
 *
 * sbl: size between leaves
 *
 * Thoughts to self: might be more efficient to compute these bits and
 * pieces when constructing z.
 */
/**
void get_dendrogram_line_endpoints(const double *Z,
				   int n,
				   double *endpnts,
				   double *ctrpnts
				   double *edge,
				   double sbl) {
  const double *Zit;
  double *endpntsit;
  double *ctrpntsit;
  double *edgeit;
  int i, j;
  for (i = 0; i < n - 1; i++) {
    Zit = Z + (4 * i)
  }
  }**/

/** Stub. **/
void compute_inconsistency_coefficient(const double *Z, double *Y, int d) {
  return;
}

void pdist(const double *X, double *dm, int m, int n, int metric, double p) {
  switch (metric) {
  case CPY_PDIST_EUCLIDEAN:
    pdist_euclidean(X, dm, m, n);
    break;
  case CPY_PDIST_CITY_BLOCK:
    pdist_city_block(X, dm, m, n);
    break;
  case CPY_PDIST_MINKOWSKI:
    pdist_minkowski(X, dm, m, n, p);
    break;
  }
}

void dist_to_squareform_from_vector(double *M, const double *v, int n) {
  double *it;
  const double *cit;
  int i, j;
  cit = v;
  for (i = 0; i < n - 1; i++) {
    it = M + (i * n) + i + 1;
    for (j = i + 1; j < n; j++, it++, cit++) {
      *it = *cit;
    }
  }
}

void dist_to_vector_from_squareform(const double *M, double *v, int n) {
  double *it;
  const double *cit;
  int i, j;
  it = v;
  for (i = 0; i < n - 1; i++) {
    cit = M + (i * n) + i + 1;
    for (j = i + 1; j < n; j++, it++, cit++) {
      *it = *cit;
    }
  }
}