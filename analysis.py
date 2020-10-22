import json

from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import stopwords
from nltk.tag import pos_tag
from nltk.tokenize import word_tokenize
from nltk import FreqDist, classify, NaiveBayesClassifier

import re, string, random

def remove_noise(article_tokens, stop_words = ()):

    cleaned_tokens = []

    for token, tag in pos_tag(article_tokens):
        # remove special characters, @'s, numbers --> data still needs to be cleaned more
        token = re.sub('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+#]|[!*\(\),]|'\
                       '(?:%[0-9a-fA-F][0-9a-fA-F]))+','', token)
        token = re.sub("(@[A-Za-z0-9_]+)","", token)
        token = re.sub(r"[0-9]+[a-z]+","", token)
        token = re.sub(r'\d+', '', token)

        if tag.startswith("NN"):
            pos = 'n'
        elif tag.startswith('VB'):
            pos = 'v'
        else:
            pos = 'a'

        # normalize verbs, nouns, etc.
        lemmatizer = WordNetLemmatizer()
        token = lemmatizer.lemmatize(token, pos)

        if len(token) > 0 and token not in string.punctuation and token.lower() not in stop_words:
            cleaned_tokens.append(token.lower())
    return cleaned_tokens

def get_all_words(cleaned_tokens_list):
    for tokens in cleaned_tokens_list:
        for token in tokens:
            yield token

def get_tokens_for_model(cleaned_tokens_list):
    for tokens in cleaned_tokens_list:
        yield dict([token, True] for token in tokens)

if __name__ == "__main__":

    # loading organized data
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

    far_right_file_path = '/Users/madelineholt/Downloads/NewsQRanking/data/farright.json'
    with open(far_right_file_path, 'r') as json_obj:
        far_right = json.loads(json_obj.read())

    stop_words = stopwords.words('english')

    # tokenize
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

    far_right_tokens_for_model = get_tokens_for_model(far_right_cleaned_tokens_list)
    right_tokens_for_model = get_tokens_for_model(right_cleaned_tokens_list)
    neutral_tokens_for_model = get_tokens_for_model(neutral_cleaned_tokens_list)
    left_tokens_for_model = get_tokens_for_model(left_cleaned_tokens_list)
    far_left_tokens_for_model = get_tokens_for_model(far_left_cleaned_tokens_list)

    # classifier.classify(dict([token, True] for token in custom_tokens))
    far_right_dataset = [(token_dict, "Far Right")
                         for token_dict in far_right_tokens_for_model]

    right_dataset = [(token_dict, "Right")
                     for token_dict in right_tokens_for_model]

    neutral_dataset = [(token_dict, "Neutral")
                       for token_dict in neutral_tokens_for_model]

    left_dataset = [(token_dict, "Left")
                    for token_dict in left_tokens_for_model]

    far_left_dataset = [(token_dict, "Far Left")
                        for token_dict in far_left_tokens_for_model]

    dataset = far_right_dataset + right_dataset + neutral_dataset + far_left_dataset + left_dataset
    random.shuffle(dataset)

    train_data = dataset[:7000]
    test_data = dataset[7000:]


    classifier = NaiveBayesClassifier.train(train_data)

    print("Accuracy is:", classify.accuracy(classifier, test_data))

    print(classifier.show_most_informative_features(10))

    custom_article = ""
    custom_tokens = remove_noise(word_tokenize(custom_article))

    sentimentAnalysis = classifier.classify(dict([token, True] for token in custom_tokens))
    print(sentimentAnalysis)

