import re
from collections import Counter


# Count Specific Word
def count_specific_word(text, search_word):
    """
    Counts the number of occurrences of a specific word in the text.
    Case-insensitive.
    """

    if not text or not search_word:
        return 0

    # Extract words only
    words = re.findall(r'\b\w+\b', text.lower())

    return words.count(search_word.lower())


# Identify Most Common Word
def identify_most_common_word(text):
    """
    Identifies the most common word in the text.
    Returns None for an empty string.
    """

    if not text.strip():
        return None

    words = re.findall(r'\b\w+\b', text.lower())

    if not words:
        return None

    word_counts = Counter(words)

    return word_counts.most_common(1)[0][0]


# Calculate Average Word Length
def calculate_average_word_length(text):
    """
    Calculates the average length of words in the text.
    Excludes punctuation and special characters.
    Returns 0 for an empty string.
    """

    words = re.findall(r'\b\w+\b', text)

    if not words:
        return 0

    total_length = sum(len(word) for word in words)

    return total_length / len(words)


# Count Number of Paragraphs
def count_paragraphs(text):
    """
    Counts the number of paragraphs in the text.
    Paragraphs are separated by empty lines.
    Returns 1 for an empty string.
    """

    if not text.strip():
        return 1

    paragraphs = [p for p in text.split('\n\n') if p.strip()]

    return len(paragraphs)


# Count Number of Sentences
def count_sentences(text):
    """
    Counts the number of sentences in the text.
    Sentences end with ., !, or ?
    Returns 1 for an empty string.
    """

    if not text.strip():
        return 1

    sentences = re.findall(r'[^.!?]+[.!?]', text)

    return len(sentences)


# -------------------------
# Example Usage
# -------------------------

sample_text = """
Artificial Intelligence is transforming the world.
AI is used in healthcare, finance, and education!

Many companies are investing heavily in AI technologies.
AI helps automate tasks and improve efficiency.
"""

search_word = "AI"

print("Specific Word Count:", count_specific_word(sample_text, search_word))

print("Most Common Word:", identify_most_common_word(sample_text))

print("Average Word Length:", calculate_average_word_length(sample_text))

print("Number of Paragraphs:", count_paragraphs(sample_text))

print("Number of Sentences:", count_sentences(sample_text))