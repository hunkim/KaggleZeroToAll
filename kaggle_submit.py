"""
Kaggle Submission Dataset Wrapper

Examples
----------
$ python kaggle_submit.py {competition-name} {submission-file} -m {message}
$ python kaggle_submit.py digit-recognizer k0-01-mnist/submission.csv -m "First Submission"

"""
import configparser
import bs4
import requests
import argparse
import os

from urllib.parse import urljoin


def login(username, password):
    session = requests.session()
    login_info = {"UserName": username, "Password": password}
    session.post("https://www.kaggle.com/account/login?ReturnUrl=kaggle.com", login_info)

    return session


def read_config(file='kaggle.ini'):
    parser = configparser.ConfigParser()
    parser.read(file)
    username = parser.get('account', 'username')
    password = parser.get('account', 'password')

    return username, password


def read_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("competition",
                        help="name of competition. For example, if the URL is http://www.kaggle.com/c/digit-recognizer then enter digit-recognizer")
    parser.add_argument("submission",
                        help="submission file")

    parser.add_argument("-m", "--message", help="submission message")
    args = parser.parse_args()

    competition = args.competition
    submission = args.submission
    message = args.message
    return competition, submission, message


def upload(competition, session, file, message=None):
    upload_URL = "https://www.kaggle.com/c/{}/submissions/attach".format(competition)
    submit_URL = urljoin(upload_URL, "/competitions/submissions/accept")

    bs = bs4.BeautifulSoup(session.get(upload_URL).text, "html.parser")
    token = bs.find('input', attrs={"name": "__RequestVerificationToken"})['value']
    competition_id = bs.find('input', attrs={"id": "CompetitionId"})['value']

    input_data = {
        "__RequestVerificationToken": token,
        "CompetitionId": competition_id,
        "SubmissionDescription": message,
        "IsScriptVersionSubmission": False,
    }

    with open(file, 'rb') as f:
        files = {"SubmissionUpload": f}
        return session.post(submit_URL, files=files, data=input_data)


if __name__ == '__main__':
    kaggle_int = 'kaggle.ini'

    if not os.path.exists(kaggle_int):
        print("Please create kaggle.ini first. See kaggle.ini.sample.")
        exit()

    username, password = read_config(kaggle_int)

    if username == "KAGGLE@KAGGLE.COM" or password == "KAGGLE_PASSWORD":
        print("Please setup kaggle.ini first")

    else:
        session = login(username, password)
        competition_name, submission_file, message = read_args()
        res = upload(competition_name, session, submission_file, message)
        print("Uploaded: https://www.kaggle.com/c/{}/submissions".format(competition_name))
