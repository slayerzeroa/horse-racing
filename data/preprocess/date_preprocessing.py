import re

def date_preprocessing(file_names):
    # change \n to \t
    file_names = re.sub('\n', ' ', file_names)

    # change many \t to one \t
    file_names = re.sub('\t', ' ', file_names)
    file_names = re.sub(' +', ' ', file_names)

    # split by ' '
    file_names = file_names.split(' ')

    file_list = []
    for idx, i in enumerate(file_names):
        if idx % 2 == 0:
            file_list.append(i[:8])

    return file_list

