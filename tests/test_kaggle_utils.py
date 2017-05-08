"""
Test file for kaggle_download.py and kaggle_submit.py

- Needs `py.test`
- Needs `kaggle.ini` 

"""
import os
import kaggle_download as kd
import kaggle_submit as ks


def test_read_config():
    username, password = kd.read_config("kaggle.ini")

    assert type(username) == str
    assert type(password) == str

    assert len(username) > 0
    assert len(password) > 0

    assert "@" in username

    username, password = ks.read_config("kaggle.ini")

    assert type(username) == str
    assert type(password) == str

    assert len(username) > 0
    assert len(password) > 0

    assert "@" in username


def test_session():
    username, password = kd.read_config("kaggle.ini")
    session = kd.login(username, password)
    assert username in session.get("http://www.kaggle.com").text


def test_get_urls():
    urls = kd.get_data_url_by_name("titanic")
    assert urls == ['http://www.kaggle.com/c/titanic/download/train.csv',
                    'http://www.kaggle.com/c/titanic/download/test.csv',
                    'http://www.kaggle.com/c/titanic/download/gender_submission.csv']


def test_download():
    username, password = kd.read_config("kaggle.ini")
    session = kd.login(username, password)
    url = 'http://www.kaggle.com/c/titanic/download/train.csv'

    kd.download(url, session, "tests/")

    assert os.path.isfile("tests/train.csv")
    os.remove("tests/train.csv")
    assert os.path.isfile("tests/train.csv") is False

    assert kd.download("http://www.kaggle.com", session, "tests/") is False