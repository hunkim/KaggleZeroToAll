"""
Kaggle Download Dataset Wrapper

Examples
----------
$ python kaggle_download.py {competition-name} --destination {destination}
$ python kaggle_download.py digit-recognizer --destination k0-01-mnist/input

"""
import configparser
import bs4
import requests
import re
import os
import argparse
from multiprocessing import pool
from urllib.parse import urljoin


def login(username, password):
    session = requests.session()
    login_info = {"UserName": username, "Password": password}
    session.post("https://www.kaggle.com/account/login?ReturnUrl=kaggle.com", login_info)

    return session


def download(url, session, destination):
    r = session.post(url)
    local_filename = os.path.join(destination, url.split('/')[-1])

    # Writes the data to a local file one chunk at a time.
    with open(local_filename, 'wb') as f:
        total_length = r.headers.get('content-length')
        content_type = r.headers.get('Content-Type', '')
        content_disp = r.headers.get('Content-Disposition', '')

        if 'text/html' in content_type and 'attachment' not in content_disp:
            print(f"Please accept the agreement terms by going to {url}")
            return False
        if total_length is None:  # no content length header
            f.write(r.content)

        else:

            dl = 0
            total_length = int(total_length)

            for data in r.iter_content(chunk_size=4096):
                f.write(data)

                dl += len(data)
                done = int(50 * dl / total_length)

                print(f"[{'=' * done}{' ' * (50 - done)}] {local_filename}", flush=True, end='\r')

            print()


def get_data_url_by_name(competition):
    base_url = "http://www.kaggle.com/"
    url = urljoin(base_url, f"c/{competition}/data")
    r = requests.get(url)
    bs = bs4.BeautifulSoup(r.text, 'html.parser')
    filenames = re.findall('"url":"(/c/{}/download/[^"]+)"'.format(competition), bs.text)
    filenames = [urljoin(base_url, f) for f in filenames]
    return filenames


def read_config(file='kaggle.ini'):
    parser = configparser.ConfigParser()
    parser.read(file)
    username = parser.get('account', 'username')
    password = parser.get('account', 'password')

    return username, password


def read_args():
    def check_destination(path):
        os.makedirs(path, exist_ok=True)
    parser = argparse.ArgumentParser()
    parser.add_argument("competition",
                        help="name of competition. For example, if the URL is http://www.kaggle.com/c/digit-recognizer then enter digit-recognizer")
    parser.add_argument("--destination", default='.',
                        help="local path for datasets to be downloaded (default: ./)")
    args = parser.parse_args()

    competition = args.competition
    destination = args.destination
    check_destination(destination)

    return competition, destination


def run_download(fn, args):
    return fn(*args)


def run_star(args):
    return run_download(*args)


if __name__ == '__main__':

    competition, destination = read_args()
    username, password = read_config()

    if username == "KAGGLE@KAGGLE.COM" or password == "KAGGLE_PASSWORD":
        print("Please setup kaggle.ini first")

    else:
        session = login(username, password)
        data_url_list = get_data_url_by_name(competition)

        pool = pool.Pool()
        tasks = [(download, (url, session, destination)) for url in data_url_list]
        results = pool.map_async(run_star, tasks)
        results.wait()
