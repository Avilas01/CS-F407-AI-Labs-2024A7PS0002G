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
    tokens = ["<START>"] + tokens + ["<END>"]
    tokenised_sentences.append(tokens)


# -------------------------------------------------
# Count transitions
# -------------------------------------------------

transition_counts = defaultdict(Counter)

for sentence in tokenised_sentences:
    for i in range(len(sentence) - 1):
        current_word = sentence[i]
        next_word = sentence[i + 1]

        transition_counts[current_word][next_word] += 1


# -------------------------------------------------
# Construct conditional probabilities
# P(next word | current word)
# -------------------------------------------------

probabilities = {}

for current_word, next_words in transition_counts.items():

    total = sum(next_words.values())

    probabilities[current_word] = {}

    for next_word, count in next_words.items():
        probabilities[current_word][next_word] = count / total


# -------------------------------------------------
# Display probability distribution
# -------------------------------------------------

def display_distribution(word):

    if word not in probabilities:
        print(f"No transitions found for '{word}'")
        return

    print(f"\nP(next word | {word})")

    for next_word, probability in probabilities[word].items():
        print(f"{next_word}: {probability:.3f}")


# -------------------------------------------------
# Greedy next-word selection
# Always choose the highest probability word
# -------------------------------------------------

def greedy_next_word(word):

    if word not in probabilities:
        return None

    return max(
        probabilities[word],
        key=probabilities[word].get
    )


# -------------------------------------------------
# Sampling next-word selection
# Randomly choose according to probabilities
# -------------------------------------------------

def sample_next_word(word):

    if word not in probabilities:
        return None

    words = list(probabilities[word].keys())
    probs = list(probabilities[word].values())

    return random.choices(
        words,
        weights=probs,
        k=1
    )[0]


# -------------------------------------------------
# Generate sentence
# mode = "greedy" or "sampling"
# -------------------------------------------------

def generate_sentence(mode="sampling", max_length=30):

    current_word = "<START>"
    generated = []

    for _ in range(max_length):

        if mode == "greedy":
            next_word = greedy_next_word(current_word)

        elif mode == "sampling":
            next_word = sample_next_word(current_word)

        else:
            print("Invalid mode")
            return ""

        if next_word is None:
            break

        if next_word == "<END>":
            break

        generated.append(next_word)
        current_word = next_word

    return " ".join(generated)


# -------------------------------------------------
# Probability normalisation test
# -------------------------------------------------

def test_probabilities():

    print("\nProbability normalisation test:")

    for word in probabilities:

        total = sum(probabilities[word].values())

        print(f"{word}: {total:.3f}")


# -------------------------------------------------
# Selected conditional probability tables
# -------------------------------------------------

words_to_test = ["the", "cat", "dog", "sat", "ran"]

for word in words_to_test:
    display_distribution(word)


# -------------------------------------------------
# Most probable predictions
# -------------------------------------------------

print("\nMost probable next words:")

for word in words_to_test:

    prediction = greedy_next_word(word)

    print(f"{word} -> {prediction}")


# -------------------------------------------------
# Probability test
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
# Part X: Greedy vs Sampling
# -------------------------------------------------

print("\n5 Greedy-generated sentences:")

for i in range(5):

    sentence = generate_sentence("greedy")

    print(f"{i + 1}. {sentence}")


print("\n5 Sampling-generated sentences:")

for i in range(5):

    sentence = generate_sentence("sampling")

    print(f"{i + 1}. {sentence}")