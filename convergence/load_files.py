import os
import numpy as np
import requests

def download(url, mode="rb", folder="data"):
    """Downloads the specified file if it isn't already downloaded."""
    filename = os.path.basename(url)
    pathname = os.path.join(folder, filename)
    if not os.path.exists(pathname):
        response = requests.get(url)
        with open(pathname, "wb") as f:
            return f.write(response.content)

def download_and_open(url, mode="rb", folder="data"):
    """Downloads the specified file if it isn't already downloaded, then opens it."""
    filename = os.path.basename(url)
    pathname = os.path.join(folder, filename)
    if not os.path.exists(pathname):
        response = requests.get(url)
        with open(pathname, "wb") as f:
            f.write(response.content)
    return open(pathname, mode)

def load_vectors(url):
    """Loads the vector files from the url."""
    print("Loading...")
    f = download_and_open(url, mode='r')
    model = {}
    for line in f:
        whole_line = line.split()
        words = whole_line[0]
        embedding = np.array([float(val) for val in whole_line[1:]])
        model[words] = embedding
    print("Done.",len(model)," words loaded!")
    return model