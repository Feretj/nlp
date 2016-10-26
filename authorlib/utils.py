import itertools

def data_to_vectors(data):
    return list(itertools.chain(*(data.values())))
