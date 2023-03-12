import urllib.request
import nltk
import bs4
import requests
from nltk.corpus import stopwords
import pickle
import re
import math


def main():
    # First we need to find a list of applicable URLs, we will start with our first,
    # url, and follow save all the that seem applicable. We will then start going through
    # them, and keep a list of relevant URLs
    start = "https://www.google.com/search?q=john+f+kennedy&sxsrf=AJOqlzWp2txuZjlenR6DIlgJ01JtiDCZgQ%3A1678596718002&ei=bVoNZL7vPKmnqtsPleu8sA0&ved=0ahUKEwj-2eOIzNX9AhWpk2oFHZU1D9YQ4dUDCA8&uact=5&oq=john+f+kennedy&gs_lcp=Cgxnd3Mtd2l6LXNlcnAQAzIGCC4QJxBDMgQILhBDMg4ILhCABBCxAxDHARCvATIECAAQQzILCC4QrwEQxwEQgAQyBAgAEEMyBAgAEEMyCAgAEIAEELEDMgQIABBDMgQIABBDOgcIIxCwAxAnOgoIABBHENYEELADOgQILhAnOgQIIxAnOgsILhCABBCxAxCDAToQCAAQgAQQFBCHAhCxAxCDAToLCC4QsQMQxwEQrwE6CAguEIAEELEDOg4ILhCABBCxAxCDARDUAjoLCC4QgAQQxwEQrwFKBAhBGABQpAtY0xhguxloA3ABeAGAAZYBiAGSCpIBAzguNZgBAKABAcgBCsABAQ&sclient=gws-wiz-serp"
    r = requests.get(start)

    data = r.text
    soup = bs4.BeautifulSoup(data, features="html.parser")
    urlqueue = []
    goodurls = []
    counter = 0

    # Loop that will keep going through the URLs until we have enough relevant ones. This is a modified version of the
    # code from the examples.
    while len(goodurls) < 15:
        for link in soup.findAll('a'):
            link_str = str(link.get('href'))
            # print(link_str)
            if 'kennedy' in link_str or 'Kennedy' in link_str \
                    or 'jfk' in link_str or 'JFK' in link_str:  # or 'cold' in link_str or 'Cold' in link_str:
                if link_str.startswith('/url?q='):
                    link_str = link_str[7:]
                    # print('MOD:', link_str)
                if '&' in link_str:
                    i = link_str.find('&')
                    link_str = link_str[:i]
                if '%' in link_str:
                    i = link_str.find('%')
                    link_str = link_str[:i]
                if 'additional-info' in link_str:
                    i = link_str.find('additional-info')
                    link_str = link_str[:i]
                if link_str.startswith('http') and 'google' not in link_str and 'images' not in link_str and 'jpg' not \
                        in link_str and "britannica" not in link_str and "facebook" not in link_str and "twitter" not in \
                        link_str: # "Jr" not in link_str and "Caroline" not in link_str:
                    # Add the values to the applicable lists
                    if urlqueue.count(link_str) == 0:
                        urlqueue.append(link_str)
                    if goodurls.count(link_str) == 0:
                        goodurls.append(link_str)

        # Get the next url from the queue and start again
        r = requests.get(urlqueue.pop(0))
        data = r.text
        soup = bs4.BeautifulSoup(data, features="html.parser")

    print("Urls:")
    print(len(goodurls))
    for i in range(len(goodurls)):
        print(goodurls[i])

    goodpage_count = 0
    # Now that we have our web crawler and enough relevant web pages, we need to scrape the text off of each one
    # and store in a file
    for i in range(len(goodurls)):
        url = goodurls[i]
        try:
            html = urllib.request.urlopen(url).read().decode('utf8')
            soup = bs4.BeautifulSoup(html, features="html.parser")
            for script in soup(["script", "style"]):
                script.extract()
            text = soup.get_text()

            goodpage_count = goodpage_count + 1
            filename = str(goodpage_count) + ".txt"

            # Write the text to a file
            with open(filename, "w") as f:
                f.write(text)
            print(goodurls[i], " Success \n")

        except:
            print(goodurls[i], "Fail \n")

    print("Good Pages:", goodpage_count)

    # Now that we have our raw text files, we can go through each one
    # clean up the text, and save it to another file. Since this main function is already massive
    # this will be another file
    for i in range(15):
        textcleanup(i)

    # Call the function that determines the most important keywords from each file
    # I'm too sick to do this a smarter way
    vocab = set()
    tf1 = tf(1)
    tf2 = tf(2)
    tf3 = tf(3)
    tf4 = tf(4)
    tf5 = tf(5)
    tf6 = tf(6)
    tf7 = tf(7)
    tf8 = tf(8)
    tf9 = tf(9)
    tf10 = tf(10)
    tf11 = tf(11)
    tf12 = tf(12)
    tf13 = tf(13)
    tf14 = tf(14)
    tf15 = tf(15)
    print("TFs completed\n")

    # Create the vocab set
    vocab = set(tf1.keys())
    vocab = vocab.union(set(tf2.keys()))
    vocab = vocab.union(set(tf3.keys()))
    vocab = vocab.union(set(tf4.keys()))
    vocab = vocab.union(set(tf5.keys()))
    vocab = vocab.union(set(tf6.keys()))
    vocab = vocab.union(set(tf7.keys()))
    vocab = vocab.union(set(tf8.keys()))
    vocab = vocab.union(set(tf9.keys()))
    vocab = vocab.union(set(tf10.keys()))
    vocab = vocab.union(set(tf11.keys()))
    vocab = vocab.union(set(tf12.keys()))
    vocab = vocab.union(set(tf13.keys()))
    vocab = vocab.union(set(tf14.keys()))
    vocab = vocab.union(set(tf15.keys()))

    # Create the IDF
    idf_dict = {}

    vocab_by_topic = [tf1.keys(), tf2.keys(), tf3.keys(), tf4.keys(), tf5.keys(), tf6.keys(), tf7.keys(), tf8.keys(),
                      tf9.keys(), tf10.keys(), tf11.keys(), tf12.keys(), tf13.keys(), tf14.keys(), tf15.keys()]

    for term in vocab:
        temp = ['x' for voc in vocab_by_topic if term in voc]
        idf_dict[term] = math.log(16) / (1 + len(temp))

    print("IDF complete\n")

    # Call the function to calculate and display the 5 highest tf idf terms for each
    # page
    tfidf1 = tfidf(1, tf1, idf_dict)
    tfidf2 = tfidf(2, tf2, idf_dict)
    tfidf3 = tfidf(3, tf3, idf_dict)
    tfidf4 = tfidf(4, tf4, idf_dict)
    tfidf5 = tfidf(5, tf5, idf_dict)
    tfidf6 = tfidf(6, tf6, idf_dict)
    tfidf7 = tfidf(7, tf7, idf_dict)
    tfidf8 = tfidf(8, tf8, idf_dict)
    tfidf9 = tfidf(9, tf9, idf_dict)
    tfidf10 = tfidf(10, tf10, idf_dict)
    tfidf11 = tfidf(11, tf11, idf_dict)
    tfidf12 = tfidf(12, tf12, idf_dict)
    tfidf13 = tfidf(13, tf13, idf_dict)
    tfidf14 = tfidf(14, tf14, idf_dict)
    tfidf15 = tfidf(15, tf15, idf_dict)

    # Create the knowledge base. The 10 terms we are using are
    # Kennedy, Oswald, War, Russians, Assassination, Presidency, Senator, Commission, 1960, Museum
    knowledge_dict = {}
    keywords = ['kennedy', 'oswald', 'war', 'russians', 'assassination', 'presidency', 'senator', 'commission', '1960', 'museum']
    for word in range(len(keywords)):
        occurrences = []

        # Go through each file picking up occurrences
        for i in range(15):
            filename = "new" + str(i + 1) + ".txt"
            with open(filename, "r") as f:
                filetext = f.read()
            filetext = filetext.lower()
            sentences = nltk.sent_tokenize(filetext)

            # Add each occurrence of the word to the list
            for j in sentences:
                if keywords[word] in j:
                    occurrences.append(j)

            # Add the key and list to the dict
            knowledge_dict[word] = occurrences

    print(knowledge_dict)

    # save the pickle file
    pickle.dump(knowledge_dict, open('kb.p', 'wb'))



# Calculate the turns with the highest
def tfidf(index, currtf, idf):
    tf_idf = {}
    for t in currtf.keys():
        tf_idf[t] = currtf[t] * idf[t]

    # Print the 5 most important terms per doc
    doc_term_weights = sorted(tf_idf.items(), key=lambda x: x[1], reverse=True)
    print(index, doc_term_weights[:10])

    return tf_idf


# This function determines the term frequency of the document
def tf(index):
    filename = str(index) + ".txt"
    with open(filename, "r") as f:
        filetext = f.read()

    # Preprocess the text, remove stopwords, lowercase everything, and remove punctuation
    content = lower_char_tokens = [t.lower() for t in nltk.word_tokenize(filetext) if
                                   t.isalnum() and t not in stopwords.words('english')]
    tf_dict = {}
    token_set = set(content)
    tf_dict = {t: content.count(t) for t in token_set}

    # Normalize tf
    for t in tf_dict.keys():
        tf_dict[t] = tf_dict[t] / len(content)

    return tf_dict


# Function that opens a file, uses regex to remove all of the whitespaces
def textcleanup(index):
    filename = str(index + 1) + ".txt"
    with open(filename, "r") as f:
        filetext = f.read()

    # Create a new file to store the cleaned up text in
    newfilename = "new" + filename
    g = open(newfilename, "w")

    # Use regex to remove all of the whitespace in the files, write it to a new file
    actual_text = [text for text in filetext.splitlines() if not re.match(r'^\s*$', text)]

    # Combine the list of actual text, so we can, and sentence tokenize it
    wholetext = " ".join(actual_text)
    sentences = nltk.sent_tokenize(wholetext)

    # Print the tokens into the new files
    for i in range(len(sentences)):
        g.write(sentences[i] + " ")
    g.close()


# So we can call from command line
if __name__ == "__main__":
    main()
