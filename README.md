# KaggleZeroToAll

After knowing basics of machine learning, deep learning, and TensorFlow/Keras, what's the next?

Kaggle provides many interesting problems for machine learning experts. 
This repository hosts interesting Kaggle problems and show how to solve these problems using decent deep learning models.

## Kaggle problem directory naming 
k0-00-quick_title

* difficulty(k0, k1, ... k9): 0: easy, 5: normal, 9: very difficult
* k0-XX: 00 serial number
* quick_title: quick title for the Kaggle data
* put py, ipynb, and data files in the directory

## Content of each file
Please see k0-00-template.ipynb

* Kaggle name
* dataset/problem description
* loading data
* model to solve the problem
* results
* future work and exercises

## Install requirements
```bash
pip install -r requirements.txt
```

## Kaggle Utils
* `kaggle_download.py`
    1. Fill out your `username` and `password` in kaggle.ini
    2. Accept the agreement term in Kaggle website by clicking any button like submit predictions or download a dataset
    3. Find out a competition name
        * Competition name can be found in the URL
        * For example, if the url is `https://www.kaggle.com/c/digit-recognizer`,  
          then the competition name is `digit-recognizer`
    3. Run the following command in bash to download a dataset
    ```bash
    # python kaggle_download.py `competition-name` --destination `path/to/save/dataset`
    # Example
    $ python kaggle_download.py digit-recognizer --destination k0-01-mnist/input
    ```
    * `python -h`
    ```bash
    usage: kaggle_download.py [-h] [--destination DESTINATION] competition

    positional arguments:
      competition           name of competition. For example, if the URL is
                            http://www.kaggle.com/c/digit-recognizer then enter
                            digit-recognizer

    optional arguments:
      -h, --help            show this help message and exit
      --destination DESTINATION
                            local path for datasets to be downloaded (default: ./)
    ```

 ## Contributions
 We welcome any contributions including writing issues and sending pull requests.
 
 ## References (Thanks to the TF-KR user group)
 * https://www.quora.com/What-Kaggle-competitions-should-a-beginner-start-with-1
 * http://ndres.me/kaggle-past-solutions/
 * http://www.chioka.in/kaggle-competition-solutions/
 * http://analyticscosm.com/learning-predictive-analytics-kaggle-competition-solutions/
