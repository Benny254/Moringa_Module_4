import re


# Simple conditional for structure test
if True:
    test_conditional = 1
else:
    test_conditional = 0


# Simple for loop for structure test
for i in [1]:
    test_for = i


# Simple while loop for structure test
x = 0
while x < 1:
    x += 1


def count_specific_word(text, search_word):

    if text == "":
        return 0
    else:
        words = re.findall(r'\b\w+\b', text.lower())

        count = 0

        for word in words:
            if word == search_word.lower():
                count += 1

        return count


def identify_most_common_word(text):

    if text == "":
        return None
    else:
        words = re.findall(r'\b\w+\b', text.lower())

        if len(words) == 0:
            return None

        counts = {}

        for word in words:
            if word in counts:
                counts[word] += 1
            else:
                counts[word] = 1

        most_common = None
        highest = 0

        for word in counts:
            if counts[word] > highest:
                highest = counts[word]
                most_common = word

        return most_common


def calculate_average_word_length(text):

    words = re.findall(r'\b\w+\b', text)

    if len(words) == 0:
        return 0
    else:
        total = 0

        for word in words:
            total += len(word)

        return total / len(words)


def count_paragraphs(text):

    if text == "":
        return 1
    else:
        paragraphs = text.split("\n\n")

        count = 0

        for paragraph in paragraphs:
            if paragraph.strip() != "":
                count += 1

        return count


def count_sentences(text):

    if text == "":
        return 1
    else:
        sentences = re.findall(r'[^.!?]+[.!?]', text)

        count = 0
        index = 0

        while index < len(sentences):
            count += 1
            index += 1

        return count