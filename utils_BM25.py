from math import log

k1 = 1.2
k2 = 100
b = 0.75
R = 0.0


class InvertedIndex:
    def __init__(self):
        self.index = dict()

    def __contains__(self, item):
        return item in self.index

    def __getitem__(self, item):
        return self.index[item]

    def add(self, word, docid):
        if word in self.index:
            if docid in self.index[word]:
                self.index[word][docid] += 1
            else:
                self.index[word][docid] = 1
        else:
            d = dict()
            d[docid] = 1
            self.index[word] = d


class DocumentLengthTable:
    def __init__(self):
        self.table = dict()

    def __len__(self):
        return len(self.table)

    def add(self, docid, length):
        self.table[docid] = length

    def get_length(self, docid):
        if docid in self.table:
            return self.table[docid]
        else:
            raise LookupError('%s not found in table' % str(docid))

    def get_average_length(self):
        sum = 0
        for length in self.table.values():
            sum += length
        return float(sum) / float(len(self.table))


def score_BM25(n, f, qf, r, N, dl, avdl):
    K = compute_K(dl, avdl)
    first = log(((r + 0.5) / (R - r + 0.5)) / ((n - r + 0.5) / (N - n - R + r + 0.5)))
    second = ((k1 + 1) * f) / (K + f)
    third = ((k2 + 1) * qf) / (k2 + qf)
    return first * second * third


def compute_K(dl, avdl):
    return k1 * ((1 - b) + b * (float(dl) / float(avdl)))


def get_query_result(inverted_index, document_lengths, query):
    query_result = dict()
    for term in query:
        if term in inverted_index:
            doc_dict = inverted_index[term]  # retrieve index entry
            for docid, freq in doc_dict.items():  # for each document and its word frequency
                score = score_BM25(n=len(doc_dict), f=freq, qf=1, r=0, N=len(document_lengths), dl=document_lengths.get_length(docid), avdl=document_lengths.get_average_length())  # calculate score
                if docid in query_result:  # this document has already been scored once
                    query_result[docid] += score
                else:
                    query_result[docid] = score
    return query_result
