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
    """Returns a logged in session

    Parameters
    ----------
    username : str
        Usually, it's your email

    password : str

    Returns
    ----------
    session : `requests.session`
    """
    session = requests.session()
    login_info = {"UserName": username, "Password": password}
    session.post("https://www.kaggle.com/account/login?ReturnUrl=kaggle.com", login_info)

    return session


def download(url, session, destination):
    """Downloads the file(URL) to the destination

    Parameters
    ----------
    url : str
        URL to a datafile
        http://..../data.csv or data.zip

    session : `requests.session`
        From `login(username, password)`

    destination : str
        Path for a downloaded data
        It's a directory name.
        The filename will be same as in the URL's filename
    """
    r = session.post(url)
    local_filename = os.path.join(destination, url.split('/')[-1])

    total_length = r.headers.get('content-length')
    content_type = r.headers.get('Content-Type', '')
    content_disp = r.headers.get('Content-Disposition', '')

    if 'text/html' in content_type and 'attachment' not in content_disp:
        print("Please accept the agreement terms by going to {}".format(url))
        return False

    # Writes the data to a local file one chunk at a time.
    with open(local_filename, 'wb') as f:
        if total_length is None:  # no content length header
            f.write(r.content)

        else:

            dl = 0
            total_length = int(total_length)

            for data in r.iter_content(chunk_size=4096):
                f.write(data)

                dl += len(data)
                done = int(50 * dl / total_length)

                msg = "[{}{}] {}".format("=" * done, ' ' * (50 - done), local_filename)
                print(msg, flush=True, end='\r')

            print()


def get_data_url_by_name(competition):
    """Returns downloadable URLs from a competition name

    Parameters
    ----------
    competition : str
        Competition name can be found in the URL

    Returns
    ----------
    filenames : list
        Each file is the url to a datafile
        Something like http://kaggle.com/asdfaf/train.csv
    """
    base_url = "http://www.kaggle.com/"
    url = urljoin(base_url, "c/{}/data".format(competition))
    r = requests.get(url)
    bs = bs4.BeautifulSoup(r.text, 'html.parser')
    filenames = re.findall('"url":"(/c/{}/download/[^"]+)"'.format(competition), bs.text)
    filenames = [urljoin(base_url, f) for f in filenames]
    return filenames


def read_config(file):
    """Reads a config(kaggle.ini) and returns username/password

    Parameters
    ----------
    file : str
        /Path/to/kaggle.ini

    Returns
    ----------
    username : str
    password : str
    """
    parser = configparser.ConfigParser()
    parser.read(file)
    username = parser.get('account', 'username')
    password = parser.get('account', 'password')

    return username, password


def read_args():
    """Returns a competition name and destination

    ``ArgumentParser`` helper
    And it will create a destination directory if it's not available

    Returns
    ----------
    competition : str
    destination : str
    """

    def check_destination(path):
        """Makes a directory if not exists"""
        os.makedirs(path, exist_ok=True)

    parser = argparse.ArgumentParser(description="Kaggle Download Script. Please set up ``kaggle.ini`` before using")

    parser.add_argument("competition",
                        help="name of competition. For example, if the URL is http://www.kaggle.com/c/digit-recognizer then enter digit-recognizer")
    parser.add_argument("--destination",
                        default='.',
                        help="local path for datasets to be downloaded (default: ./)")
    args = parser.parse_args()

    competition = args.competition
    destination = args.destination
    check_destination(destination)

    return competition, destination


if __name__ == '__main__':
    kaggle_ini = 'kaggle.ini'

    if not os.path.exists(kaggle_ini):
        print("Please create kaggle.ini first. See kaggle.ini.sample.")
        exit()

    competition, destination = read_args()
    username, password = read_config(kaggle_ini)

    if username == "KAGGLE@KAGGLE.COM" or password == "KAGGLE_PASSWORD":
        print("Please setup kaggle.ini using your kaggle username and password.")

    else:
        session = login(username, password)
        data_url_list = get_data_url_by_name(competition)

        pool = pool.Pool()
        tasks = [(url, session, destination) for url in data_url_list]
        results = pool.starmap_async(download, tasks)
        results.wait()
