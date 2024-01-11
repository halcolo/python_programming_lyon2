# Overview
This project is consibed to be a search engine for articles of Reddit and Arxiv platform, the main purpose is  aims to create a search engine for articles from the Reddit and Arxiv platforms. The main purpose of this project is to improve the usage and accessibility of these platforms.

## Setiting up project
### credentials
To get started with the project, you need to follow the steps outlined in the "Usage" section:

Install the required dependencies by running `pip install -r requirements.txt`. This command will install all the necessary Python packages specified in the requirements.txt file.

Configure your own credentials in the ENV vars settings of the project in the `config.py` file. You need to set the following environment variables (to get credentials go to reddit [docs](https://praw.readthedocs.io/en/stable/getting_started/authentication.html)):

- CLIENT_SECRET: This is the client secret for authentication.
- USER_AGENT: This is the user agent for making API requests.
- CLIENT_ID: This is the client ID for authentication.

### Running project
- Run the main script `main.py` to start the project. This script is responsible for executing the web interface of the search engine, this will gives you  functionality and retrieving data using a table to select subject to search and a key word (*two inputs are required*).

![ScreenRecording2024-01-11at01 11 12-ezgif com-video-to-gif-converter](https://github.com/jdalfons/search_engine/assets/25759070/d7659ca9-f062-4bef-8cb6-3851405b6e8b)

You will see the data outputs in the output zone (follow images at the top), inside each article you can see a recomendation of a recommended articles due it's similarity, and a table with the evolution of each keyword sended. These outputs will display the results of the search queries made to the Reddit and Arxiv platforms.

> Note: Jupyter notebook is not currently available check version 2.0

---

## Make Docs
run following command to make documentation
```
pydoctor \          
    --project-name=search-engine \
    --project-version=3.0.1 \
    --project-url=https://github.com/jdalfons/search_engine \
    --html-viewsource-base=https://github.com/jdalfons/search_engine/tree/main \
    --make-html \
    --html-output=docs/ \
    --project-base-dir="." \
    --docformat=epytext \
    --intersphinx=https://docs.python.org/3/objects.inv \
    ./modules ./utils

```

## Common issues
After configure the application you may have some of the most common failures, here are some possible solutions:

1. We use nltk exactly the module called stopwords, this module requires special installation, we have implemented a solution to check if the module is installed but does not work in all cases, for this reason we recommend running the following command after the installing the requirements file.
```
from nltk.corpus import stopwords
nltk.download('stopwords')
from nltk.corpus import stopwords
```
 2. In some cases, in Windows environments, the watchdogs library which is a dependency of the flask used by Dash have an error like the following.
```
from watchdog.events import EVENT_TYPE_OPENED
ImportError: cannot import name 'EVENT_TYPE_OPENED' from 'watchdog.events'
(C:\*********\Python\Python310\lib\site-packages\watchdog\events.py)
```

- This issue is caused by the fact that in some cases the library cannot be installed or was not installed correctly for several reasons:
The default version required for a few libraries on Windows is not supported and you must install version watchdog~=2.3 or watchdog~=3.0.
- Sometimes Jedi is another reason for this error and it is because the jedi library is used by another library and is installed the latest version (jedi==0.19.1) which is not necessary, use a version instead earlier like jedi==0.19.0.