# README - COSI 114a HW2

The code provided in this repository contains the solutions to HW2 for COSI 114a - Fundamentals of Natural Language Processing I. The assignment asked us to do the following for both bigrams and trigrams: 

1. Compute bigram and trigram probabilities given input sequences 
2. Use those probabilities to generate new sequences and compute the probability of sequences 

Students were allowed to reuse code from previous homework assignments. As this assignment was done for a class, some helper files and testing files were provided. All student-written solutions to the assignment were written in the ``` hw2.py ``` file. 

## Installation and Execution 

Get the files from GitHub and in your terminal/console move into the project folder. To run the test file included with the files given to students, run the following: 

``` bash 
python test_hw2.py 
```

Doing this will run the set of tests in the test file that was provided to students to test their code. Running the test file will print a score to the user's console indicating the success of the program for each given test case. 

Note: The test file provided only made up a portion of the final grade for the assignment. More extensive tests were done during final grading, but students weren't given access to those tests. Furthermore, these instructions assume that the user has python downloaded and is able to run the ``` python ``` command in their terminal. 


## Assignment Description 

### Bigram and Trigram Probabilities

The following two functions were written to compute bigram and trigram probabilities from an iterable of sequences: 

1. ``` bigram_probs(sentences: Iterable[Sequence[str]], ) -> dict[str, dict[str, float]] ``` 
2. ``` trigram_probs(sentences: Iterable[Sequence[str]], ) -> dict[tuple[str, str], dict[str, float]] ```

Each function returns nested dictionaries that represent the bigram or trigram probabilities of the n-grams input provided. The input is an iterable of sequences (Ex: lists or tuples), where each sequences contains the tokens to be used in n-grams. Since the input is an ``` Iterable ```, it is only accessed by a for loop once. Each sequence should be considered as a sentence, and tokens are used without any modification. 

The top-level dictionaries have keys for the contexts (the first word of a bigram or the first two of a trigram), represented as strings (bigrams) or two-item tuples of strings (trigrams). The inner dictionary has string keys and float values, where the values represent the probability of each string given the context. Each inner dictionary forms a probability distribution, so its float values are the counts divided by the total count for the context. Like previous assignments, the start and end of each sequence is padded with their appropriate tokens when computing the n-grams. The function returns a dictionary of type ``` dict ``` where the values themselves are dictionaries. It is assumed that the input iterable contains at least one sequence and that every sequence contains at least one token. 

### Bigram and Trigram Generators  

The following two functions have been written to generate a sentence from a bigram or trigram distribution: 

1. ``` sample_bigrams(probs: dict[str, dict[str, float]]) -> list[str] ``` 
2. ``` sample_trigrams(probs: dict[tuple[str, str], dict[str, float]]) -> list[str] ```

To generate a sentence, a variable is used to represent the current context and is constantly updated as each token is generated. The following is the logic behind how it works: 

1. The context is set to the ``` START_TOKEN ``` and an empty list is created for the output sentence 
2. The distribution is sampled for the context using a helper method provided, which is then added to the output sentence and set as the new context 
3. This continues until the ``` END_TOKEN ``` is reached, as this would indicate the end of a sentence 

### Bigram and Trigram Sequence Probability  

The following two functions have been implemented to compute the log probability of a bigram or trigram model: 

1. ``` bigram_sequence_prob(sequence: Sequence[str], probs: dict[str, dict[str, float]]) -> float ``` 
2. ``` trigram_sequence_prob(sequence: Sequence[str], probs: dict[tuple[str, str], dict[str, float]]) -> float ``` 

The log probability is computed by adding the logs of probabilities using ``` math.log ```. The logs of the probabilities are added up by taking the probability of the lof and then adding them to each other. The input sentences of the function contain tokens that represent a sentence, and the input is not padded with the start and end tokens. 

If an n-gram sequence is not possible given the specified ``` probs ```, a pre-provided constant, ``` NEG_INF ```, is returned instead. N-gram sequences can be impossible either because the context isn't in the distribution, or the context is in the distribution but it doesn't assign any probability to the token that follows it in the sequence. 

