import sys
import pathlib
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from random import randint


# Our main function, mostly used to call other functions

def main():
    raw_text = open_file(sys.argv[1])

    # Tokenize the raw text, making each token lowercase and removing punctuation
    lower_char_tokens = [t.lower() for t in nltk.word_tokenize(raw_text) if t.isalpha()]

    # Pass this list of tokens to the lex_diverse function to calculate and print lexical diversity
    print("Lexical Diversity: %.2f" % lex_diverse(lower_char_tokens))

    # Pass our tokenized text to the preprocess function
    processed_list = preprocess(lower_char_tokens)
    all_tokens = processed_list[0]
    nouns = processed_list[1]

    # Create a dict of nouns
    nouns_dict = create_dict(all_tokens, nouns)

    sorted_list = []
    # Create a sorted list and print the values of the dicts, and their counts
    list_count = 0
    for k, v in sorted(nouns_dict.items(), key=lambda x: x[1]):
        if list_count > len(nouns_dict) - 51:
            print(k, ":", v)
            sorted_list.append(k)
        list_count += 1

    # Past the sorted list to the game function to run the game, we will not return to main after this
    starting_points = 5
    final_data = guessing_game(sorted_list, starting_points)

    # When the game ends, print a message with the score and word
    if final_data[0] < 0:
        print("Out of score. Game over.")

    else:
        print("Game over! Final score is:", final_data[0])

    print("The final word was:", final_data[1])


# Function that will be used to serve as the word guessing game. It generates a word, and creates an array out of it
# An equal sized array will be created that consists only of underscores. It prompts the user for a letter,
# and upon receiving a correct letter, it replaces the appropriate place in the "blank" array with the letter and
# gives the user a point incorrect guesses result in a point being deducted. Game ends when ! is input or the points
# goes below 0. If the word is completed, the function is called again recursively
def guessing_game(word_list, current_points):
    player_points = current_points

    # Generate a random number from 0 to 49 and retrieve a word, create the arrays
    rand_num = randint(0, 49)
    # print(rand_num)
    current_word = word_list[rand_num]
    # print(current_word)
    current_word_array = [char for char in current_word]
    player_word_array = ["_" for char in current_word]

    # An array used to store the letter already played
    played_letters = []

    # Until the player word array is full, prompt the player for a letter, if the letter matches, add it and
    # give a point, remove a player otherwise. Game ends when the player enters ! or gets negative points
    while "_" in player_word_array:
        for i in player_word_array:
            print(i, end=" ")
        player_input = input("\nInput a letter: ")

        # If the input is already played make the user pick again
        if player_input in played_letters:
            print("Letter already used. Input a new one: ")

        # If not, then check to see whether the guess is correct or not
        else:

            # If the input is a !, exit the game
            if player_input == "!":
                return [player_points, current_word]

            # If the letter is correct, increase the player_points by 1 and add the letter to the player
            # word array
            if player_input in current_word_array:
                player_points += 1
                print("Correct! Score:", player_points)

                # Add the letter to the played_letters array
                played_letters.append(player_input)

                # Full in the player's guess
                for i in range(len(current_word_array)):
                    if current_word_array[i - 1] == player_input:
                        player_word_array[i - 1] = player_input

            # If it's not any of these, then it must not be a correct input
            else:
                player_points -= 1
                print("Incorrect. Score: ", player_points)

                # Add the letter to the played_letters array
                played_letters.append(player_input)

                # If the new point value is negative, return to main to end the game, return the point value and word
                if player_points < 0:
                    return [player_points, current_word]

    # The word has been solved. Print a message and call the function again recursively
    print("Word solved!\nWord was:", current_word)
    return guessing_game(word_list, player_points)


# Function that takes the list of tokens and the list of nouns to
# create a dict of them both
def create_dict(tokens, nouns):
    # For loop to go through the list of nouns and for each one
    # calculate the amount of times it appears in the text
    # add these values to the dict
    working_dict = {}

    for i in nouns:
        working_dict[i] = tokens.count(i)

    return working_dict


# Function that preprocesses the tokenized text
def preprocess(input_tokens):
    # Removes tokens that are on the stoplist and who's lengths are not > 5
    processed_tokens = [t for t in input_tokens if len(t) > 5 and t not in stopwords.words('english')]

    # Lemmatize the tokens
    lemmatizer = WordNetLemmatizer()
    lemmatized_tokens = [lemmatizer.lemmatize(t) for t in processed_tokens]

    # Get a list of unique lemmas
    unique_lemmas = list(set(lemmatized_tokens))

    # Do POS tagging on the unique lemmas and print the first 20
    tagged = nltk.pos_tag(unique_lemmas)
    print(tagged[:20])

    # Create the list of nouns
    nouns_list = [t[0] for t in tagged if t[1].startswith("N")]

    # Print the number of tokens and nouns
    print("Number of tokens:", len(processed_tokens))
    print("Number of nouns:", len(nouns_list))

    # Create a list to be returned with the processed tokens and nouns
    return_list = [processed_tokens, nouns_list]

    return return_list


# Function that takes the tokenized text and calculates the lexical diversity. We will tokenize the txt
def lex_diverse(input_text):
    unique_chars = set(input_text)
    return len(unique_chars) / len(input_text)


def open_file(path):
    print("\nOpening file at", sys.argv[1], "...\n")

    # Use method 2 from the example GitHub to open the file, read the text, and return the text to main
    with open(pathlib.Path.cwd().joinpath(path), 'r') as f:
        # print("Lines:\n")
        return f.read()


# This checks if the args are appropriate. More specifically, if arg1 is anat19.txt. This is also how we
# run this file as a script
if __name__ == "__main__":
    # Check if there are 2 args
    if len(sys.argv) == 2:
        # Now check to see if the provided arg is anat19.txt, go into main if so
        if sys.argv[1] == "anat19.txt":
            main()
        # If the arg file path does not match, error
        else:
            print("Incorrect filename. The correct name is anat19.txt")
    # Error if an incorrect number of args
    else:
        print("Incorrect number of arguments. Only include filename.")
