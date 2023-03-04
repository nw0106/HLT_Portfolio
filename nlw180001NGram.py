import nltk
import pickle


# NOTE: Please have the dictionary files be in the same folder as this file

# This main function exists mostly to call the function that creates the ngrams and bigrams
# for each language. It then creates pickle files out of the ngrams
def main():
    print("Starting...\n")

    eng_list = createngrams("LangId.train.English")
    print("English done...\n")

    print("Creating pickles...\n")
    pickle.dump(eng_list[0], open("eng_uni.p", "wb"))
    print("English unigrams complete...\n")
    pickle.dump(eng_list[1], open("eng_bi.p", "wb"))
    print("English bigrams complete...\n")

    fre_list = createngrams("LangId.train.French")
    print("French done...\n")

    print("Creating pickles...\n")
    pickle.dump(fre_list[0], open("fre_uni.p", "wb"))
    print("French unigrams complete...\n")
    pickle.dump(fre_list[1], open("fre_bi.p", "wb"))
    print("French bigrams complete...\n")

    ita_list = createngrams("LangId.train.Italian")
    print("Italian done...\n")

    print("Creating pickles...\n")
    pickle.dump(ita_list[0], open("ita_uni.p", "wb"))
    print("Italian unigrams complete...\n")
    pickle.dump(ita_list[1], open("ita_bi.p", "wb"))
    print("Italian bigrams complete...\n")

    print("Done.\n")


# This function takes the filename, reads in the text and removes the newlines.
# After this, the text is encoded into a string and turned into uni/bigrams. Dicts
# are created and returned
def createngrams(filename):
    # Open and read the file
    with open(filename, "r") as f:
        rawtext = f.read().encode("utf8")

    # Turn the raw text into a string and remove newlines
    rawstring = str(rawtext, encoding='utf-8')
    fixedtext = " ".join(rawstring.splitlines())
    # print(fixedtext)

    # Now that we have a string, of our text, we need to tokenize and create uni/bigrams
    unigrams = nltk.word_tokenize(fixedtext)
    bigrams = list(nltk.ngrams(unigrams, 2))
    # print(bigrams)

    # Create and return the dicts
    unigram_dict = {t: unigrams.count(t) for t in set(unigrams)}
    bigram_dict = {b: bigrams.count(b) for b in set(bigrams)}

    dict_list = [unigram_dict, bigram_dict]

    return dict_list


if __name__ == "__main__":
    main()
