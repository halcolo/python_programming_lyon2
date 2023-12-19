# Explanation
This project aims to understand connection to Reddit and Arxiv API to scrapping data of posts in case of Reddit and papers meta data in case of Arxiv. It provides a solution by implementing each one of respectives API's solutions.

Usage:
1. Install the required dependencies by running `pip install -r requirements.txt`.
2. Configure your own credentials in ENV vars settings of project in the `config.py` file.
    - CLIENT_SECRET
    - USER_AGENT
    - CLIENT_ID
3. Run the main script `main.py` to start the project.
4. You wil see all data Outputs in the console.

Understanding the project:

In tools folder you will found all tools used in the project. For example.

- `get_data.py` The get_data.py module defines a function that collects data from Reddit and Arxiv based on the provided parameters. Reddit data is obtained through the Reddit API (PRAW) and Arxiv data through its API. The collected data is stored in a dictionary, converted to a pandas DataFrame, and then saved to a CSV file.

- `secrets.py` defines a RedditAuth class to store Reddit authentication credentials. It also defines a set_vars function that runs a shell script to set environment variables, retrieves these variables, and creates a RedditAuth object.

- `tools.py` defines a data_manipulation function that performs various operations on a pandas DataFrame. Prints the length of the DataFrame, the number of words in each text, removes texts with less than 20 characters and creates a single string with all texts.
