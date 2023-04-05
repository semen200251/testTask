import os
import time
import re

import pandas as pd


def fill_data(df, path_to_file, i):
    stat = os.stat(path_to_file)
    df.at[i, 'name'] = os.path.splitext(file)[0]
    df.at[i, 'format'] = os.path.splitext(file)[1]
    df.at[i, 'user id'] = stat.st_uid
    df.at[i, 'size'] = stat.st_size
    df.at[i, 'create'] = time.ctime(stat.st_mtime)
    df.at[i, 'upgrade'] = time.ctime(stat.st_ctime)


if __name__ == '__main__':
    data = pd.DataFrame({
        'name': [],
        'format': [],
        'user id': [],
        'size': [],
        'create': [],
        'upgrade': []
    })

    path = input("Path: ")
    status = input("Get information about all files in a directory? [Yes/No] ")

    error = True

    if status.lower() == "yes":
        i = 0
        for root, dirs, files in os.walk(path):
            for file in files:
                if file.endswith('.pdf') or file.endswith('.xlsx'):
                    path_to_file = os.path.join(root, file)
                    fill_data(data, path_to_file, i)
                    i = i + 1
                    error = False

    elif status.lower() == "no":
        regexes = [re.compile(p) for p in ['.pdf',
                                           '.xlsx',
                                           ]
                   ]
        file = input("File name: ")
        for regex in regexes:
            if regex.search(file):
                path_to_file = path + "\\" + file
                if os.path.isfile(path_to_file):
                    error = False

        if not error:
            fill_data(data, path_to_file, 0)

    if not error:
        print(data)
    else:
        print("Can't find files")
