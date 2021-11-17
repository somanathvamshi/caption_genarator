import os
import numpy as np
from PIL import Image

from pickle import dump, load

from keras.applications.xception import Xception
from keras.preprocessing.text import Tokenizer

from tqdm.notebook import tqdm

from utility import load_doc, all_img_captions

tqdm().pandas()


def extract_features(directory):
    model = Xception(include_top=False, pooling='avg')
    features = {}
    for img in tqdm(os.listdir(directory)):
        filename = directory + "/" + img
        image = Image.open(filename)
        image = image.resize((299, 299))
        image = np.expand_dims(image, axis=0)
        #image = preprocess_input(image)
        image = image/127.5
        image = image - 1.0

        feature = model.predict(image)
        features[img] = feature
    return features


def load_photos(filename):
    # load the data
    file = load_doc(filename)
    photos = file.split("\n")[:-1]
    return photos


def load_clean_descriptions(filename, photos):
    # loading clean_descriptions
    file = load_doc(filename)
    descriptions = {}
    for line in file.split("\n"):

        words = line.split()
        if len(words) < 1:
            continue

        image, image_caption = words[0], words[1:]

        if image in photos:
            if image not in descriptions:
                descriptions[image] = []
            desc = '<start> ' + " ".join(image_caption) + ' <end>'
            descriptions[image].append(desc)

    return descriptions


def load_features(photos):
    # loading all features
    all_features = load(open("features.p", "rb"))
    # selecting only needed features
    features = {k: all_features[k] for k in photos}
    return features

# converting dictionary to clean list of descriptions


def dict_to_list(descriptions):
    all_desc = []
    for key in descriptions.keys():
        [all_desc.append(d) for d in descriptions[key]]
    return all_desc


def create_tokenizer(descriptions):
    # creating tokenizer class
    # this will vectorise text corpus
    # each integer will represent token in dictionary

    desc_list = dict_to_list(descriptions)
    tokenizer = Tokenizer()
    tokenizer.fit_on_texts(desc_list)
    return tokenizer


def max_length(descriptions):
    # calculate maximum length of descriptions
    desc_list = dict_to_list(descriptions)
    return max(len(d.split()) for d in desc_list)


# ** features = extract_features(dataset_images)
# ** dump(features, open("features.p", "wb"))
# features = load(open("features.p", "rb"))


# dataset_path = os.getcwd() + '\\dataset\\'
# dataset_text = dataset_path + 'Text'
# filename = dataset_text + "/" + "Flickr_8k.trainImages.txt"

# descriptions = all_img_captions(filename)

# #train = loading_data(filename)
# train_imgs = load_photos(filename)
# train_descriptions = load_clean_descriptions("descriptions.txt", train_imgs)
# train_features = load_features(train_imgs)


# tokenizer = create_tokenizer(train_descriptions)
# dump(tokenizer, open('tokenizer.p', 'wb'))
# vocab_size = len(tokenizer.word_index) + 1
# print('Vocab Size:', vocab_size)

# max_length = max_length(descriptions)
