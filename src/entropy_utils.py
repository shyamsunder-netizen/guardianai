import math
from collections import Counter


def calculate_entropy(text):
    if not text:
        return 0

    counter = Counter(text)
    length = len(text)
    entropy = 0

    for count in counter.values():
        probability = count / length
        entropy -= probability * math.log2(probability)

    return entropy