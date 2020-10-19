import json_obj as json_obj
from nltk.tokenize import word_tokenize
import json

from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import twitter_samples, stopwords
from nltk.tag import pos_tag
from nltk.tokenize import word_tokenize
from nltk import FreqDist, classify, NaiveBayesClassifier

import re, string, random

def remove_noise(tweet_tokens, stop_words = ()):

    cleaned_tokens = []

    for token, tag in pos_tag(tweet_tokens):
        token = re.sub('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+#]|[!*\(\),]|'\
                       '(?:%[0-9a-fA-F][0-9a-fA-F]))+','', token)
        token = re.sub("(@[A-Za-z0-9_]+)","", token)
        token = re.sub(r"[0-9]+[a-z]+","", token)

        if tag.startswith("NN"):
            pos = 'n'
        elif tag.startswith('VB'):
            pos = 'v'
        else:
            pos = 'a'

        lemmatizer = WordNetLemmatizer()
        token = lemmatizer.lemmatize(token, pos)

        if len(token) > 0 and token not in string.punctuation and token.lower() not in stop_words:
            cleaned_tokens.append(token.lower())
    return cleaned_tokens

def get_all_words(cleaned_tokens_list):
    for tokens in cleaned_tokens_list:
        for token in tokens:
            yield token

def get_tweets_for_model(cleaned_tokens_list):
    for tweet_tokens in cleaned_tokens_list:
        yield dict([token, True] for token in tweet_tokens)

if __name__ == "__main__":

    #loading organized data
    far_left_file_path = '/Users/madelineholt/Downloads/NewsQRanking/data/farleft.json'
    with open(far_left_file_path, 'r') as json_obj:
        far_left = json.loads(json_obj.read())

    left_file_path = '/Users/madelineholt/Downloads/NewsQRanking/data/left.json'
    with open(left_file_path, 'r') as json_obj:
        left = json.loads(json_obj.read())

    neut_file_path = '/Users/madelineholt/Downloads/NewsQRanking/data/neutral.json'
    with open(neut_file_path, 'r') as json_obj:
        neutral = json.loads(json_obj.read())

    right_file_path = '/Users/madelineholt/Downloads/NewsQRanking/data/right.json'
    with open(right_file_path, 'r') as json_obj:
        right = json.loads(json_obj.read())

    far_right_file_path = '/Users/madelineholt/Downloads/NewsQRanking/data/far_right.json'
    with open(far_right_file_path, 'r') as json_obj:
        far_right = json.loads(json_obj.read())

    stop_words = stopwords.words('english')

    #tokenize
    far_left_tokens = word_tokenize(far_left)
    left_tokens = word_tokenize(left)
    neutral_tokens = word_tokenize(neutral)
    right_tokens = word_tokenize(right)
    far_right_tokens = word_tokenize(far_right)

    far_left_cleaned_tokens_list = []
    left_cleaned_tokens_list = []
    neutral_cleaned_tokens_list = []
    right_cleaned_tokens_list = []
    far_right_cleaned_tokens_list = []

    for tokens in far_right_tokens:
        far_right_cleaned_tokens_list.append(remove_noise(tokens, stop_words))

    for tokens in right_tokens:
        right_cleaned_tokens_list.append(remove_noise(tokens, stop_words))

    for tokens in neutral_tokens:
        neutral_cleaned_tokens_list.append(remove_noise(tokens, stop_words))

    for tokens in left_tokens:
        left_cleaned_tokens_list.append(remove_noise(tokens, stop_words))

    for tokens in far_left_tokens:
        far_left_cleaned_tokens_list.append(remove_noise(tokens, stop_words))

    all_right_words = get_all_words(far_right)

    freq_dist_pos = FreqDist(all_right_words)
    # print(freq_dist_pos.most_common(10))

    far_right_tokens_for_model = get_tweets_for_model(far_right_cleaned_tokens_list)
    right_tokens_for_model = get_tweets_for_model(right_cleaned_tokens_list)
    neutral_tokens_for_model = get_tweets_for_model(neutral_cleaned_tokens_list)
    left_tokens_for_model = get_tweets_for_model(left_cleaned_tokens_list)
    far_left_tokens_for_model = get_tweets_for_model(far_left_cleaned_tokens_list)

    # classifier.classify(dict([token, True] for token in custom_tokens))
    far_right_dataset = [(tweet_dict, "Far Right")
                         for tweet_dict in far_right_tokens_for_model]

    right_dataset = [(tweet_dict, "Right")
                     for tweet_dict in right_tokens_for_model]

    neutral_dataset = [(tweet_dict, "Neutral")
                       for tweet_dict in neutral_tokens_for_model]

    left_dataset = [(tweet_dict, "Left")
                    for tweet_dict in left_tokens_for_model]

    far_left_dataset = [(tweet_dict, "Far Left")
                        for tweet_dict in far_left_tokens_for_model]

    # dataset = list(far_left_dataset.items()) + list(far_right_dataset.items()) + list(right_dataset.items()) + list(neutral_dataset.items()) + list(left_dataset.items())
    # dataset = list(dataset)

    dataset = far_right_dataset + right_dataset + neutral_dataset + far_left_dataset + left_dataset
    random.shuffle(dataset)

    train_data = dataset[:7000]
    test_data = dataset[3000:]
    print(type(train_data))

    classifier = NaiveBayesClassifier.train(train_data)

    print("Accuracy is:", classify.accuracy(classifier, test_data))

    print(classifier.show_most_informative_features(10))

    custom_article = "Andy Burnham said in a letter to the PM and other party leaders that Parliament should hold an urgent debate to end the deadlock. " \
                     "Later the mayor said he had a with Mr Johnson's chief strategic adviser. Earlier, minister Michael Gove said:" \
                     "We hope to agree a new approach. Mr Gove said the government wanted the best for Greater Manchester and that he hoped " \
                     "we can find a way through together But he criticised what he described as the  of politicians in that region and warned that if an agreement could not be reached the government would  having to impose restrictions. " \
                     "Manchester, including Mr Burnham, have rejected a move to England's tier three alert level without better financial support.is not just a Greater Manchester issue"
    custom_tokens = remove_noise(word_tokenize(custom_article))

    sentimentAnalysis = classifier.classify(dict([token, True] for token in custom_tokens))
    print(sentimentAnalysis)

    # adjust rank based on output
    rank = None
    weight = None
