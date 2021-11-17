import os
import string
from utility import all_img_captions


def cleaning_text(captions):
    # Data cleaning- lower casing, removing puntuations and words containing numbers
    table = str.maketrans('', '', string.punctuation)
    for img, caps in captions.items():
        for i, img_caption in enumerate(caps):
            img_caption.replace("-", " ")
            desc = img_caption.split()
            # converts to lowercase
            desc = [word.lower() for word in desc]
            # remove punctuation from each token
            desc = [word.translate(table) for word in desc]
            # remove hanging 's and a
            desc = [word for word in desc if(len(word) > 1)]
            # remove tokens with numbers in them
            desc = [word for word in desc if(word.isalpha())]
            # convert back to string
            img_caption = ' '.join(desc)
            captions[img][i] = img_caption
    return captions


def text_vocabulary(descriptions):
    # build vocabulary of all unique words
    vocab = set()
    for key in descriptions.keys():
        [vocab.update(d.split()) for d in descriptions[key]]
    return vocab


def save_descriptions(descriptions, filename):
    # All descriptions in one file
    lines = list()
    for key, desc_list in descriptions.items():
        for desc in desc_list:
            lines.append(key + '\t' + desc)
    data = "\n".join(lines)
    file = open(filename, "w")
    file.write(data)
    file.close()


dataset_path = os.getcwd() + '\\dataset\\'
dataset_text = dataset_path + 'Text'
dataset_images = dataset_path + 'Images'

filename = dataset_text + "\\" + "Flickr8k.token.txt"
descriptions = all_img_captions(filename)
clean_descriptions = cleaning_text(descriptions)
vocabulary = text_vocabulary(clean_descriptions)

print("Length of descriptions =", len(descriptions))
print("Length of vocabulary = ", len(vocabulary))

save_descriptions(clean_descriptions, "descriptions.txt")
