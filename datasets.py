import requests, os

FOLDER = 'datasets'

def download_datasets():
    urls = {
        'breast.csv': 'http://raullgdev.es/code/se_intro/breast_cancer_short.csv',
    }
    create_folder_if_needed()

    for file_name, url in urls.items():
        if os.path.exists(os.path.join(FOLDER, file_name)):
            continue

        print('Downloading {}...'.format(url))
        r = requests.get(url)
        with open(os.path.join(FOLDER, file_name), 'wb') as f:
            f.write(r.content)

def create_folder_if_needed():
    if os.path.exists(FOLDER):
        return
    
    os.mkdir(FOLDER)
