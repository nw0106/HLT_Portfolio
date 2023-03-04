import nltk
import pickle


# This function reads the pickle files
def main():
    # Read in the pickle files
    print("Reading pickle files...\n")
    eng_uni = pickle.load(open("eng_uni.p", "rb"))
    eng_bi = pickle.load(open("eng_bi.p", "rb"))
    print("English files read.\n")

    fre_uni = pickle.load(open("fre_uni.p", "rb"))
    fre_bi = pickle.load(open("fre_bi.p", "rb"))
    print("French files read.\n")

    ita_uni = pickle.load(open("ita_uni.p", "rb"))
    ita_bi = pickle.load(open("ita_bi.p", "rb"))
    print("Italian files read.\n")

    # Get the lengths of all the unigram dicts put together
    totallength = len(eng_uni) + len(fre_uni) + len(ita_uni)

    # Open the test file and our result file, for each line, call the function for each language
    # Whichever probability is the highest, add that to our file of results
    testfile = open("LangId.test", "r")
    resultfile = open("ngramresult", "w")

    linecount = 1
    for line in testfile:
        eng_prob = laplace_prob(line, eng_uni, eng_bi, totallength)
        fre_prob = laplace_prob(line, fre_uni, fre_bi, totallength)
        ita_prob = laplace_prob(line, ita_uni, ita_bi, totallength)
        # print(eng_prob, fre_prob, ita_prob, "\n")

        # Create a list of these probs, and reverse sort it, the first value determines
        # which is to be written to the result file
        prob_list = [eng_prob, fre_prob, ita_prob]
        # prob_list.reverse()

        # for i in range(len(prob_list)):
        #    print(prob_list[i])
        # print("\n")

        # Write to the result file
        resultfile.write(str(linecount))

        if max(prob_list) == eng_prob:
            resultfile.write(" English\n")
            # print(prob_list[0], "\n")

        elif max(prob_list) == fre_prob:
            resultfile.write(" French\n")
            # print(prob_list[0], "\n")


        elif max(prob_list) == ita_prob:
            resultfile.write(" Italian\n")
            # print(prob_list[0], "\n")

        linecount = linecount + 1

    print("Result file written.\n")

    # Close the test and result files. Reopen the result file for reading and the
    # correct file
    testfile.close()
    resultfile.close()

    with open("ngramresult", "r") as f:
        resultlist = f.read().splitlines()
    with open("LangId.sol", "r") as g:
        keylist = g.read().splitlines()

    # Go through both the lists, incrementing the numcorrect value whenever they
    # match, and the lines of list elements that do not match up
    numcorrect = 0
    for i in range(len(resultlist)):

        # If they match, increment the numcorrect
        if keylist[i] == resultlist[i]:
            numcorrect = numcorrect + 1

        # If they don't match, print it out
        else:
            print("Line", i + 1, "does not match.")
            print("LangId.sol:", keylist[i])
            print("ngramresult:", resultlist[i], "\n")

    # Calculate and print the accuracy
    accuracy = numcorrect / float(len(resultlist))
    print("Accuracy:", accuracy, "%")


# Function to calculate the laplace probability of the input text being
# a certain language
def laplace_prob(inputtext, lang_unigrams, lang_bigrams, totallength):
    input_unigrams = nltk.word_tokenize(inputtext)
    input_bigrams = list(nltk.ngrams(input_unigrams, 2))
    prob = 1

    # Calculate the laplace prob
    for x in input_bigrams:
        b = lang_bigrams[x] if x in lang_bigrams else 0
        u = lang_unigrams[x[0]] if x[0] in lang_unigrams else 0
        prob = prob * ((b + 1) / (u + totallength))

    # Return the probability
    return prob


if __name__ == "__main__":
    main()
