import numpy as np


def mean_reciprocal_rank(rs):
    rs = (np.asarray(r).nonzero()[0] for r in rs)
    return np.mean([1. / (r[0] + 1) if r.size else 0. for r in rs])


# rr
def imp2_rr(ss):
    for i, s in enumerate(ss):
        i += 1
        if s == True:
            return 1.0 / float(i)
        else:
            pass


# mrr
def imp2_mrr(scores):
    result = 0.0
    for i, score in enumerate(scores):
        i += 1
        result += imp2_rr(score)
    return result / i


def r_precision(r):
    r = np.asarray(r) != 0
    z = r.nonzero()[0]
    if not z.size:
        return 0.
    return np.mean(r[:z[-1] + 1])


def precision_at_k(r, k):
    if len(r) < k:
        for i in range(len(r), k):
            r.append(0)
    r = np.asarray(r)[:k] != 0
    if r.size != k:
        raise ValueError('Relevance score length < k')
    return np.mean(r)


def average_precision(r):
    r = np.asarray(r) != 0
    out = [precision_at_k(r, k + 1) for k in range(r.size) if r[k]]
    if not out:
        return 0.
    return np.mean(out)
    # return np.sum(out) / len(r) # another implementation


def mean_average_precision(rs):
    return np.mean([average_precision(r) for r in rs])

# https://en.wikipedia.org/wiki/Evaluation_measures_(information_retrieval)#Precision
# https://en.wikipedia.org/wiki/Mean_reciprocal_rank
# print("mean_reciprocal_rank:", mean_reciprocal_rank([[1, 1, 1], [0, 0, 1]]))
# print("r_precision:", r_precision([0, 0, 1, 1]))
# print("precision_at_1:", precision_at_k([0, 1, 1], 1))
# print("precision_at_2:", precision_at_k([0, 1, 1], 2))
# print("precision_at_3:", precision_at_k([0, 1, 1], 3))
# print("average_precision:", average_precision([0, 1, 1]))
# print("mean_average_precision:", mean_average_precision([[1, 1, 1], [0, 0, 0]]))
# print(imp2_rr([1, 1, 1]))
# print(imp2_rr([0, 0, 1]))
# print(imp2_mrr([[1, 1, 1], [0, 0, 1]]))
