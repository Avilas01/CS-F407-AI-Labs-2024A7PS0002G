import random
from collections import defaultdict, Counter

# -------------------------------------------------
# Dataset
# -------------------------------------------------

sentences = [
    "the cat sat on the mat",
    "the cat sat on the rug",
    "the dog sat on the mat",
    "the dog ran to the park",
    "the cat ran to the park",
    "the dog sat on the rug"
]

tokenised_sentences = []

for sentence in sentences:
    tokens = sentence.lower().split()

    # Two START tokens because the model uses
    # the previous two tokens as context
    tokens = ["<START>", "<START>"] + tokens + ["<END>"]

    tokenised_sentences.append(tokens)


# -------------------------------------------------
# Count second-order transitions
#
# (word1, word2) -> next_word
# -------------------------------------------------

transition_counts = defaultdict(Counter)

for sentence in tokenised_sentences:

    for i in range(len(sentence) - 2):

        word1 = sentence[i]
        word2 = sentence[i + 1]
        next_word = sentence[i + 2]

        context = (word1, word2)

        transition_counts[context][next_word] += 1


# -------------------------------------------------
# Construct conditional probabilities
#
# P(next word | previous two words)
# -------------------------------------------------

probabilities = {}

for context, next_words in transition_counts.items():

    total = sum(next_words.values())

    probabilities[context] = {}

    for next_word, count in next_words.items():

        probabilities[context][next_word] = count / total


# -------------------------------------------------
# Display probability distribution
# -------------------------------------------------

def display_distribution(word1, word2):

    context = (word1, word2)

    if context not in probabilities:

        print(f"No transitions found for {context}")
        return

    print(f"\nP(next word | {word1}, {word2})")

    for next_word, probability in probabilities[context].items():

        print(f"{next_word}: {probability:.3f}")


# -------------------------------------------------
# Greedy next-word selection
# -------------------------------------------------

def greedy_next_word(word1, word2):

    context = (word1, word2)

    if context not in probabilities:
        return None

    return max(
        probabilities[context],
        key=probabilities[context].get
    )


# -------------------------------------------------
# Sampling next-word selection
# -------------------------------------------------

def sample_next_word(word1, word2):

    context = (word1, word2)

    if context not in probabilities:
        return None

    words = list(probabilities[context].keys())
    probs = list(probabilities[context].values())

    return random.choices(
        words,
        weights=probs,
        k=1
    )[0]


# -------------------------------------------------
# Generate sentence
#
# mode = "greedy" or "sampling"
# -------------------------------------------------

def generate_sentence(mode="sampling", max_length=30):

    word1 = "<START>"
    word2 = "<START>"

    generated = []

    for _ in range(max_length):

        if mode == "greedy":

            next_word = greedy_next_word(word1, word2)

        elif mode == "sampling":

            next_word = sample_next_word(word1, word2)

        else:

            print("Invalid mode")
            return ""

        if next_word is None:
            break

        if next_word == "<END>":
            break

        generated.append(next_word)

        # Shift the two-word context forward
        word1 = word2
        word2 = next_word

    return " ".join(generated)


# -------------------------------------------------
# Probability normalisation test
# -------------------------------------------------

def test_probabilities():

    print("\nProbability normalisation test:")

    for context in probabilities:

        total = sum(probabilities[context].values())

        print(f"{context}: {total:.3f}")


# -------------------------------------------------
# Display selected conditional distributions
# -------------------------------------------------

contexts_to_test = [
    ("<START>", "<START>"),
    ("<START>", "the"),
    ("the", "cat"),
    ("the", "dog"),
    ("cat", "sat"),
    ("dog", "sat"),
    ("dog", "ran"),
    ("sat", "on"),
    ("ran", "to")
]

for word1, word2 in contexts_to_test:

    display_distribution(word1, word2)


# -------------------------------------------------
# Display most probable next words
# -------------------------------------------------

print("\nMost probable next words:")

for word1, word2 in contexts_to_test:

    prediction = greedy_next_word(word1, word2)

    print(f"({word1}, {word2}) -> {prediction}")


# -------------------------------------------------
# Probability normalisation test
# -------------------------------------------------

test_probabilities()


# -------------------------------------------------
# Generate 20 sentences using sampling
# -------------------------------------------------

print("\n20 Sampling-generated sentences:")

for i in range(20):

    sentence = generate_sentence("sampling")

    print(f"{i + 1}. {sentence}")


# -------------------------------------------------
# Greedy vs Sampling
# -------------------------------------------------

print("\n5 Greedy-generated sentences:")

for i in range(5):

    sentence = generate_sentence("greedy")

    print(f"{i + 1}. {sentence}")


print("\n5 Sampling-generated sentences:")

for i in range(5):

    sentence = generate_sentence("sampling")

    print(f"{i + 1}. {sentence}")


# -------------------------------------------------
# Model statistics
# -------------------------------------------------

number_of_contexts = len(probabilities)

number_of_parameters = sum(
    len(next_words)
    for next_words in probabilities.values()
)

print("\nSecond-order model statistics:")

print("Number of contexts:", number_of_contexts)

print(
    "Number of distinct transition parameters:",
    number_of_parameters
)