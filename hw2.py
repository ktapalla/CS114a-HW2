import math
import random
from collections import defaultdict, Counter
from math import log
from typing import Sequence, Iterable, Generator, TypeVar

# hw2.py
# Version 1.1
# 9/26/2022

############################################################
# The following constants and function are provided as helpers.
# Do not modify them! The stubs for what you need to implement are later in the file.

# DO NOT MODIFY
random.seed(0)

# DO NOT MODIFY
START_TOKEN = "<start>"
# DO NOT MODIFY
END_TOKEN = "<end>"
# DO NOT MODIFY
NEG_INF = float("-inf")
# DO NOT MODIFY (needed if you copy code from HW 1)
T = TypeVar("T")


# DO NOT MODIFY
def load_tokenized_file(path: str) -> Generator[Sequence[str], None, None]:
    """Yield sentences as sequences of tokens."""
    with open(path, encoding="utf8") as file:
        for line in file:
            line = line.rstrip("\n")
            tokens = line.split(" ")
            yield tuple(tokens)


# DO NOT MODIFY
def sample(probs: dict[str, float]) -> str:
    """Return a sample from a distribution."""
    # To avoid relying on the dictionary iteration order, sort items
    # This is very slow and should be avoided in general, but we do
    # it in order to get predictable results
    items = sorted(probs.items())
    # Now split them back up into keys and values
    keys, vals = zip(*items)
    # Choose using the weights in the values
    return random.choices(keys, weights=vals)[0]


############################################################
# The stubs below this are the ones that you should fill in.
# Do not modify anything above this line other than to add any needed imports.


# HELPER CODE FROM HW1
# converts a sentence/sequence to bigrams with start and end padding
def bigrams(sentence: Sequence[str]) -> list[tuple[str, str]]:
    """Return the bigrams contained in a sequence."""
    tpl_list = list()
    sentence = list(sentence)
    sentence.insert(0, START_TOKEN)
    sentence.insert(len(sentence), END_TOKEN)
    for ind in range(len(sentence) - 1):
        tpl_list.append(tuple([sentence[ind], sentence[ind + 1]]))
    return tpl_list


# HELPER CODE FROM HW1
# converts a sentence/sequence to trigrams with start and end padding
def trigrams(sentence: Sequence[str]) -> list[tuple[str, str, str]]:
    """Return the trigrams contained in a sequence."""
    tpl_list = list()
    sentence = list(sentence)
    sentence.insert(0, START_TOKEN)
    sentence.insert(0, START_TOKEN)
    sentence.insert(len(sentence), END_TOKEN)
    sentence.insert(len(sentence), END_TOKEN)
    for ind in range(len(sentence) - 2):
        tpl_list.append(tuple([sentence[ind], sentence[ind + 1], sentence[ind + 2]]))
    return tpl_list


# calculates probabilities of keys
def counts_to_probs(counts: Counter[T]) -> dict[T, float]:
    """Return a defaultdict with the input counts converted to probabilities."""
    prob_dict = dict()
    reverse_sort = counts.most_common()
    # generates total sum of all keys/tokens
    total = sum(counts.values())
    # calculates probability of each and enters it into the dictionary
    for key, val in counts.items():
        prob = val / total
        prob_dict[key] = prob
    return prob_dict


def bigram_probs(sentences: Iterable[Sequence[str]], ) -> dict[str, dict[str, float]]:
    """Return bigram probabilities computed from the provided sequences."""
    final_dict = dict()
    bgrms_list = list()
    keys = set()
    # creates bigrams from sentences
    for sentence in sentences:
        bgrms_list.append(bigrams(sentence))
    # creates a set of possible keys
        for word in sentence:
            keys.add(word)
    keys.add(START_TOKEN)
    # goes through keys to calculate probabilities of next word
    for key in keys:
        poss_dict = dict()
        # creates a counter for next possible words and num of times they appear
        counter = Counter()
        for bigram_sent in bgrms_list:
            for tpl in bigram_sent:
                if tpl[0] == key:
                    next_pos_word = tpl[1]
                    counter[next_pos_word] += 1
            # calculates probabilities
            poss_dict = counts_to_probs(counter)
        # puts probabilities of next word for specific keys
        final_dict[key] = poss_dict
    return final_dict


def trigram_probs(sentences: Iterable[Sequence[str]], ) -> dict[tuple[str, str], dict[str, float]]:
    """Return trigram probabilities computed from the provided sequences."""
    tgrms_list = list()
    final_dict = dict()
    counter = Counter()
    keys = set()
    # creates trigrams from sentences
    for sentence in sentences:
        tgrms_list.append(trigrams(sentence))
    # creates a set of possible keys
        for word_ind in range(len(sentence)):
            if word_ind+1 < len(sentence):
                keys.add((sentence[word_ind], sentence[word_ind+1]))
            else:
                keys.add((sentence[word_ind], END_TOKEN))
        keys.add((START_TOKEN, START_TOKEN))
        keys.add((START_TOKEN, sentence[0]))
    # goes through keys to calculate probabilities of next word
    for key in keys:
        poss_dict = dict()
        # creates a counter for next possible words and num of times they appear
        counter = Counter()
        for trigram_sent in tgrms_list:
            for tpl in trigram_sent:
                if tpl[0] == key[0] and tpl[1] == key[1]:
                    next_pos_word = tpl[2]
                    counter[next_pos_word] += 1
            # calculates probabilities
            poss_dict = counts_to_probs(counter)
        # puts probabilities of next word for specific keys
        final_dict[key] = poss_dict
    return final_dict


def sample_bigrams(probs: dict[str, dict[str, float]]) -> list[str]:
    """Generate a sequence by sampling from the provided bigram probabilities."""
    poss_out = list()
    context = START_TOKEN
    # continues to generate samples while the END_TOKEN isn't seen
    while context != END_TOKEN:
        context = sample(probs[context])
        # adds sample to possible outputs as long as it's not the END_TOKEN
        if context != END_TOKEN:
            poss_out.append(context)
    return poss_out


def sample_trigrams(probs: dict[tuple[str, str], dict[str, float]]) -> list[str]:
    """Generate a sequence by sampling from the provided trigram probabilities."""
    poss_out = list()
    context1 = START_TOKEN
    context2 = START_TOKEN
    # continues to generate samples while the END_TOKEN isn't seen
    while context2 != END_TOKEN:
        context_tpl = (context1, context2)
        next_out = sample(probs[context_tpl])
        # adds sample to possible outputs as long as it's not the END_TOKEN
        if next_out != END_TOKEN:
            poss_out.append(next_out)
        # shifts context over by 1, removing first and inserting next output for second
        context1 = context2
        context2 = next_out
    return poss_out


def bigram_sequence_prob(sequence: Sequence[str], probs: dict[str, dict[str, float]]) -> float:
    """Compute the probability of a sequence using bigram probabilities."""
    key = START_TOKEN
    seq_prob = 0.0
    print(sequence)
    # goes through strings in sequence
    for st in sequence:
        print("st: " + st)
        # gets next possible values from key
        poss_next = probs.get(key)
        # calculates log/probability of getting string in sequence, returning NEG_INF immediately if not possible
        if key in probs and st in poss_next:
            seq_prob += math.log(poss_next.get(st))
            # changes key to appropriate values in sequence
            key = st
        else:
            return NEG_INF
        print("key: " + key)
    return seq_prob


def trigram_sequence_prob(sequence: Sequence[str], probs: dict[tuple[str, str], dict[str, float]]) -> float:
    """Compute the probability of a sequence using trigram probabilities."""
    key1 = START_TOKEN
    key2 = START_TOKEN
    seq_prob = 0.0
    # goes through strings in sequence
    for str in sequence:
        # creates a tuple key with appropriate tokens
        key_tpl = (key1, key2)
        # gets next possible values from key
        poss_next = probs.get(key_tpl)
        if key_tpl in probs and str in poss_next:
            seq_prob += math.log(poss_next.get(str))
            # shifts keys over by 1, removing first and inserting appropriate values from sequence for second
            key1 = key2
            key2 = str
        else:
            return NEG_INF
    return seq_prob
