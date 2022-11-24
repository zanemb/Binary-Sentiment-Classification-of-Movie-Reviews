import os

# list of positive descriptor words - mostly derived from a thesaurus
pos_words = ["good", "exciting", "interesting", "excellent", "superb", 
             "outstanding", "magnificent", "exceptional", "marvelous",
             "wonderful", "splendid", "admirable", "awesome", "upstanding",
             "worthy", "praiseworthy", "commendable", "enjoyable", "pleasant",
             "agreeable", "pleasing", "pleasurable", "delightful", "great", 
             "nice", "lovely", "amusing", "cheerful", "fantastic", "fabulous",
             "terrific", "glorious", "magic", "magical", "cool", "brilliant",
             "beautiful", "fitting", "happy", "wholesome", "genuine", 
             "authentic", "powerful", "best", "riveting", "intriguing", 
             "clever", "dazzling", "imaginative", "charming", "original", 
             "brilliant", "expertly", "liked", "convincing"]
# list of negative descriptor words - mostly derived from a thesaurus
neg_words = ["bad", "terrible", "boring", "awful", "negative", "poor", 
             "inferior", "unacceptable", "amateurish", "dreadful", "atrocious",
             "disgraceful", "hopeless", "laughable", "miserable", "sorry", 
             "incompetent", "inept", "pathetic", "usesless", "bummed", 
             "appalling", "abysmal", "pitiful", "godawful", "dire", "rubbish",
             "crap", "shit", "egregious", "undesirable", "unpleasant", 
             "unfortunate", "waste", "disappointing", "moronic", "juvenile",
             "flawed", "distasteful", "disgusting", "confusing", "predictable",
             "weak", "cliché", "bland", "uneven", "outdated", "crummy",
             "stupid", "ordinary", "trite", "nasty", "static", "tragic", 
             "horrific", "horrifying", "horrible", "horendous", "abhorrent",
             "shocking", "hideous", "unspeakable", "ghastly", "intolerable",
             "nauseating", "offensive", "obnoxious", "hellacious", "lousy",
             "unbearable", "agonizing", "hate", "hated", "disliked", "cryptic",
             "avoid", "worthless", "bummer", "failed", "failure", "badly"]

# store directory locations for ease of use
pos_dir = "/Users/zanemazorbrown/Desktop/BUS 498 - Zhan/aclImdb/train/pos"
neg_dir = "/Users/zanemazorbrown/Desktop/BUS 498 - Zhan/aclImdb/train/neg"

# function to open a file in read mode given directory and file name
def read_text(file_name, dir):
    file_location = dir + "/" + file_name
    file = open(file_location, "r")
    return file

# Preprocessing

# funcion to remove punctuation from each word in a file and add to list as LC
def preprocess(file_name, dir):
    file = read_text(file_name, dir)
    # create empty list to append words to
    word_list = []
    for line in file:
        line = line.split()
        for word in line:
            word = word.strip(" .,!?()/<>")
            # all words in pos/neg lists are lower case
            word_list.append(word.lower())
    # close file to free up resources
    file.close()
    return word_list

# function to count the number of positive and negative words in a text file
def pos_neg_freq(pos_words, neg_words, file_name, dir):
    word_list = preprocess(file_name, dir)
    pos_count = 0
    neg_count = 0
    # use range(len()) to get previous list index - check if modified by "not"
    for word in range(len(word_list)):
        if word_list[word] in pos_words and word_list[word-1] == "not":
            neg_count += 1
        # uncomment the following lines if "not {negative}" = positive.
        # elif word_list[word] in neg_words and word_list[word-1] == "not":
        #     pos_count += 1
        elif word_list[word] in pos_words:
            pos_count += 1
        elif word_list[word] in neg_words:
            neg_count += 1
    return pos_count, neg_count

# function to label a file as positive or negative given pos/neg frequencies
def label_review(pos_words, neg_words, file_name, dir):
    pos_freq, neg_freq = pos_neg_freq(pos_words, neg_words, file_name, dir)
    # went with simple rule: pos>neg=pos, neg>pos=neg
    # positive label is 1
    if pos_freq > neg_freq:
        label = 1
    # negative label is -1
    else:
        label = -1
    # return label as a string -> can add "\n" when writing to file
    return str(label)

# create an empty list to append label outcomes to when iterating
rev_labels = []

# create list of file names from the pos directory
pos_file_list = os.listdir(pos_dir)
# iterate through each pos file and append file label to the review labels list
for file in pos_file_list:
    label = label_review(pos_words, neg_words, file, pos_dir)
    rev_labels.append(label)

# create list of file names from the pos directory
neg_file_list = os.listdir(neg_dir)
# iterate through each neg file and append file label to the review labels list
for file in neg_file_list:
    label = label_review(pos_words, neg_words, file, neg_dir)
    rev_labels.append(label)

# try opening with "x" mode - creates a text file if file name doesn't exist
label_file_name = "BUS 498 - Assignment #1 Labels"
try:
    label_file = open(label_file_name, "x")
# if the file does exist, open it in write mode.
except:
    label_file = open(label_file_name, "w")

# iterate through the review labels list and write to file with a line break
for label in rev_labels:
    label_file.write(label + "\n")

# close label file
label_file.close()

# Report your labeling accuracy.

# function to count the number of pos/neg reviews in the label list
def count_labels(lst):
    # QA to make sure total labels = 25,000
    total_labels = 0
    pos_labels = 0
    neg_labels = 0
    for label in lst:
        # return label to integer (after turning to string for step #9)
        label = int(label)
        total_labels += 1
        if label == 1:
            pos_labels += 1
        elif label == -1:
            neg_labels += 1
    return total_labels, pos_labels, neg_labels

# function to count total number of files in a given directory
def count_files(dir_lst):
    num_files = 0
    for file in dir_lst:
        num_files += 1
    return num_files

# retrieve total number of labels, positive and negative.
total_labels, num_pos_labels, num_neg_labels = count_labels(rev_labels)
# retrieve number of files in a directory (should be 12,500)
num_pos_files = count_files(pos_file_list)
num_neg_files = count_files(neg_file_list)
# calculate number of labels correctly classified with my specified criteria
pos_correct = num_pos_files - abs(num_pos_labels - num_pos_files)
neg_correct = num_neg_files - abs(num_neg_labels - num_neg_files)
# calculate the ratio of correctly labeled reviews to total number of reviews
accuracy = ((pos_correct + neg_correct)/(num_pos_files + num_neg_files)) * 100
# display findings and contrast with correct data
print(f"Total number of reviews labeled: {total_labels:,}\n")
print(f"Number of total positive reviews: {num_pos_files:,}")
print(f"Number of total positive labels: {num_pos_labels:,}\n")
print(f"Number of total negative reviews: {num_neg_files:,}")
print(f"Number of total negative labels: {num_neg_labels:,}\n")
print(f"Total Accuracy: {accuracy:,.2f}%")

# as of last run:
# Total number of reviews labeled: 25,000

# Number of total positive reviews: 12,500
# Number of total positive labels: 13,933

# Number of total negative reviews: 12,500
# Number of total negative labels: 11,067

# Total Accuracy: 88.54%
