import os

from preprocessing import text_vocabulary, save_descriptions, cleaning_text
from predict import predict
from utility import all_img_captions

if __name__ == '__main__':
    # dataset_path = os.getcwd() + '\\dataset\\'
    # dataset_text = dataset_path + 'Text'
    # dataset_images = dataset_path + 'Images'

    # filename = dataset_text + "\\" + "Flickr8k.token.txt"
    # descriptions = all_img_captions(filename)
    # clean_descriptions = cleaning_text(descriptions)
    # vocabulary = text_vocabulary(clean_descriptions)

    # print("Length of descriptions =", len(descriptions))
    # print("Length of vocabulary = ", len(vocabulary))

    # save_descriptions(clean_descriptions, "descriptions.txt")
    img_path = 'test/img.png'
    max_length = 32
    predict(img_path)
