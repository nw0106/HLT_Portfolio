# Import needed libraries to make use of their functions and objects
import sys
import pickle
import re
import pathlib


# Person class, this contains values for first/middle/last name, id, and phone alongside
# a display method to write these fields
class Person:
    def __init__(self, first, middle, last, idnum, phonenum):
        self.first = first
        self.middle = middle
        self.last = last
        self.idnum = idnum
        self.phonenum = phonenum

    def display(self):
        print("ID: ", self.idnum)
        print("Name: ", self.first, self.middle, self.last)
        print("Phone Number: ", self.phonenum)


# Main function, mostly serves to call other functions
def main():
    # Now that we are in main, we need to actually get the csv file we are working with. We will use method 2
    # from the provided GitHub to read the csv file as a text file and print it as raw data
    csv_file = open_file(sys.argv[1])
    print("Raw CSV data:")
    print(csv_file, "\n")

    # print("Split lines:\n")
    # print(csv_file.splitlines(), "\n")
    # Create the empty dict and call text processing function to create it
    person_dict = text_process(csv_file)

    # Save the dict to a pickle file
    pickle.dump(person_dict, open('people.p', 'wb'))

    # Open and read pickle file
    pickle_in = pickle.load(open('people.p', 'rb'))
    # Print the pickle file
    print("Employee list:\n")
    for instance in pickle_in:
        pickle_in[instance].display()

# This function goes through each element of each line, and makes sure they
# conform to the standards of the organization system, allowing for user edits
# if they do not. Returns a dictionary of people to main
def text_process(input_file):
    # Set up the working dictionary, the line counter, and the list of individual
    # lines in the text
    # print("\nSplit on comma:\n")
    working_dict = {}
    line_num = 0
    working_text = input_file.splitlines()

    # Go through each line in the text, ignoring the first line
    for lines in working_text:
        if line_num == 0:
            line_num += 1

        # If this is not the first line, take the current line and split it
        # on the commas. This splits the current string into a list where each
        # element can be worked with.
        else:
            # element_index = 0
            current_line = lines.split(",")
            # DEBUG CODE
            # current_line[0] = "Noah"
            # working_text[line_num] = current_line
            # line_num += 1
            # print(working_text)
            # print(current_line, "\n")

            # We could use a loop for this. But given that we are not doing the
            # same thing to each element, I felt that it would be simpler and cleaner
            # to go through the list of elements "manually". We will go through
            # each element and call a function that will determine if it conforms and
            # calls a function to alter it if not, saving it back to the list of elements.
            # When we are done with a line, we will overwrite the line in working_text with our
            # current line, so that at the end our working_text will be updated as well. This is
            # so we can make use of the "current state" data if we need to, such as checking for
            # repeat keys. When we are finished, working_text will be completely in line and correct.

            # First 3 elements of the list, call the name_edit function
            # to capitalize them and add an X in their place if they are empty
            current_line[0] = name_edit(current_line[0])
            current_line[1] = name_edit(current_line[1])
            current_line[2] = name_edit(current_line[2])

            # For the 4th element, the ID number, call the id_edit function to make sure that it is in the form
            # of 2 letters followed by 4 digits. If not, ask for input. Keep asking for input
            # until the ID number is unique and also in the correct format
            current_line[3] = id_edit(current_line[3], working_text, line_num)

            # The last element we are working on is the phone number, this uses a very similar
            # regex system as the ID number, just with a different format and less restrictive
            # (phone numbers aren't always unique)
            current_line[4] = phonenum_edit([current_line[4]], line_num)

            # Finally, create an instance of the person class and assign the appropriate attributes
            # add this person to the working_dict

            working_dict[str(current_line[3])] = Person(current_line[1], current_line[2], current_line[0],
                                                        current_line[3], current_line[4])

            # Join and save the current line to working_text
            # and increment the line_num counter. End of this iteration of the loop
            # DEBUG: Print the corrected current_line
            # print(current_line)
            working_text[line_num] = ",".join(current_line)
            line_num += 1
    # Print corrected working_text
    # print("\nCorrected split lines:\n", working_text, "\n")
    return working_dict


# Function to take in the phone number, check to make sure it conforms with the format
# and prompts the user to input a new phone number. This will recursively call
# the function again to make sure the new input is valid.
def phonenum_edit(phonenum_input, curr_line_num):

    # Check if the phone number conforms, return the input if so
    if re.match("[0-9][0-9][0-9]-[0-9][0-9][0-9]-[0-9][0-9][0-9][0-9]", str(phonenum_input)):
        return phonenum_input

    # If not, prompt for a new phone number, recursively call with the new input
    else:
        print("Phone number invalid for line:", curr_line_num,
              "\nPhone numbers should be in the form ###-###-####\nEnter a new number:")
        new_input = input()
        return phonenum_edit(new_input,  curr_line_num)


# Function to take in the ID number and check to see that it conforms to the standards
# with regex. Asks for input if not. Keep doing so until the input is unique and matches
def id_edit(id_input, full_text, curr_line_num):
    # Check to see if the input matches the regex and is unique, if so just return the input
    if re.match("[A-Z][A-Z][0-9][0-9][0-9][0-9]", id_input) and (len(re.findall(id_input, ",".join(full_text))) <= 1):
        # print("ID match\n")
        return id_input

    # If the ID does not match, ask them to input a new ID number and recursively call the function again
    else:
        print("ID invalid for line:", curr_line_num,
              "\nIDs should be 2 capital letters followed by 4 digits.\nEnter a new ID:")
        # print(len(re.findall(id_input, ",".join(full_text))), "\n")
        new_input = input()
        # While loop to ask for a new input if the ID is already used
        while len(re.findall(new_input, ",".join(full_text))) > 0:
            print("ID Values must be unique.")
            new_input = input()
        # Recursively call the function with our new value
        return id_edit(new_input, full_text, curr_line_num)


# Function that takes the input string and properly capitalizes it. If the string is
# blank, replace it with an X. Return the corrected string
def name_edit(name_input):
    if name_input == '':
        return "X"
    else:
        return name_input.capitalize()


# This function takes the file path and opens the csv document as a text file
def open_file(path):
    print("\nOpening file at", sys.argv[1], "...\n")

    # Use method 2 from the example GitHub to open the file, read the text, and return the text to main
    with open(pathlib.Path.cwd().joinpath(path), 'r') as f:
        # print("Lines:\n")
        return f.read()


# This checks if the args are appropriate. More specifically, if arg1 is data/data.csv. This is also how we
# run this file as a script
if __name__ == "__main__":
    # Check if there are 2 args
    if len(sys.argv) == 2:
        # Now check to see if the provided arg is data/data.csv, go into main if so
        if sys.argv[1] == "data/data.csv":
            main()
        # If the arg file path does not match, error
        else:
            print("Incorrect relative path. The correct path is data/data.csv")
    # Error if an incorrect number of args
    else:
        print("Incorrect number of arguments. Only include file path")
