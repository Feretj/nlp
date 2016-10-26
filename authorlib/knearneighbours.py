"""K Near Neighbours

    This module conteins realization of K Near Neighbours model
"""
from collections import Counter


def dot(a, b):
    """Dot of two dict vectors"""
    keys = a.keys() & b.keys()
    dot_product = 0
    for i in keys:
        dot_product += a[i]*b[i]
    return dot_product


def lenght2(v):
    """Square of lenght of dict vector"""
    return (sum(i[1]*i[1] for i in v.items()))


def _text_dot(a_len_uni, a_len_bi, a_len_tri, a, b, uni, bi, tri):
    """Dot of two classes text_vector
       a_len_uni, a_len_bi, a_len_tri - squares of lenghts of first text_vector
       a - first text_vector
       b - second text_vector
       uni, bi, tri - coefs of gramms
    """
    b_len_uni = lenght2(b.unigramms)
    b_len_bi = lenght2(b.bigramms)
    b_len_tri = lenght2(b.trigramms)
    uni_dot = dot(a.unigramms, b.unigramms)
    uni_dot = uni_dot*uni_dot/(a_len_uni*b_len_uni)
    bi_dot = dot(a.bigramms, b.bigramms)
    bi_dot = bi_dot*bi_dot/(a_len_bi*b_len_bi)
    tri_dot = dot(a.trigramms, b.trigramms)
    tri_dot = tri_dot*tri_dot/(a_len_tri*b_len_tri)
    return uni*(uni_dot)**0.5 + bi*(bi_dot)**0.5 + tri*(tri_dot)**0.5


def knn(vectors, vector, k=1, uni=2.002183406113537, bi=1.2890829694323145, tri=0.1890829694323144):
    """Determinate author of text_vector using model knn
        vectors - text_vectors, which author is known
        vector - text_vector of text
        uni, bi, tri - coefs of gramms
    """
    v_len_uni = lenght2(vector.unigramms)
    v_len_bi = lenght2(vector.bigramms)
    v_len_tri = lenght2(vector.trigramms)
    if k == 1:
        return max(vectors, key=lambda x:
                   _text_dot(v_len_uni, v_len_bi,
                             v_len_tri, vector, x, uni, bi, tri)).author

    knvectors = sorted(vectors, key=lambda x:
                       _text_dot(v_len_uni, v_len_bi,
                                 v_len_tri, vector, x, uni, bi, tri),
                       reverse=True)[:k]
    nauthors = Counter([i.author for i in knvectors])
    author = max(nauthors.items(), key=lambda x: x[1])[0]
    return author
