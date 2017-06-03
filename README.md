# KaggleZeroToAll

After knowing basics of machine learning, deep learning, and TensorFlow/Keras, what's the next?

Kaggle provides many interesting problems for machine learning experts. 
This repository hosts interesting Kaggle problems and show how to solve these problems using decent deep learning models.

## Kaggle problem directory naming 
k0-00-short-title

* Difficulty (k0, k1, ... k9): 
    - 0: easy
    - 5: normal
    - 9: very difficult
* k0-XX: 00 serial number
* short-title: title for the Kaggle data
* put `.py`, `.ipynb`, and data files in the directory
    - If data files are large, you can create a script. Please check [this](k0-01-titanic/data_download.sh)

## Content of each file
Please see k0-00-template.ipynb

* Kaggle name
* dataset/problem description
* loading data
* model to solve the problem
* results
* future work and exercises

## Dependencies for Kaggle Utils (optional)
```
requests==2.13.0
beautifulsoup4==4.6.0
```
or 
```bash
pip install -r requirements.txt
```

## Kaggle Utils (optional)
* `kaggle_download.py`: Kaggle download script
    1. Create **kaggle.ini**
        - Copy `kaggle.ini.sample` and name it `kaggle.ini`
        - Fill out your `username` and `password` in kaggle.ini
    2. **Accept the agreement term** in Kaggle website
        - Click the download button on the competition main site
    3. Find a **competition name**
        * Competition name can be found in the URL
        * For example, if the url is https://www.kaggle.com/c/digit-recognizer,  
          then the competition name is **digit-recognizer**
    3. In terminal,
    ```bash
    # python kaggle_download.py competition-name --destination path/to/save/dataset
    # Example:
    $ python kaggle_download.py digit-recognizer --destination k0-01-mnist/input
    ```

* `kaggle_submit.py`: Kaggle submission script
    1. You can also submit your submission
    2. In terminal,
    ```bash 
    # python kaggle_submit.py competition-name /path/to/submission.csv -m "Submission message"
    # Example:
    python kaggle_submit.py digit-recognizer k0-01-mnist/submission.csv -m "First Submission"
    ```

## Tests

```bash
py.test
```

 ## Contributions
 We welcome any contributions including writing issues and sending pull requests.
 
 ## References (Thanks to the TF-KR user group)
 * https://www.quora.com/What-Kaggle-competitions-should-a-beginner-start-with-1
 * http://ndres.me/kaggle-past-solutions/
 * http://www.chioka.in/kaggle-competition-solutions/
 * http://analyticscosm.com/learning-predictive-analytics-kaggle-competition-solutions/
