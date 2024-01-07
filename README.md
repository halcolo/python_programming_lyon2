# Overview
This project is consibed to be a search engine for articles of Reddit and Arxiv platform, the main purpose is  aims to create a search engine for articles from the Reddit and Arxiv platforms. The main purpose of this project is to improve the usage and accessibility of these platforms.

## Setiting up project
### credentials
To get started with the project, you need to follow the steps outlined in the "Usage" section:

Install the required dependencies by running `pip install -r requirements.txt`. This command will install all the necessary Python packages specified in the requirements.txt file.

Configure your own credentials in the ENV vars settings of the project in the `config.py` file. You need to set the following environment variables (to get credentials go to reddit [docs](https://praw.readthedocs.io/en/stable/getting_started/authentication.html)):

CLIENT_SECRET: This is the client secret for authentication.
USER_AGENT: This is the user agent for making API requests.
CLIENT_ID: This is the client ID for authentication.

### Running project
You have two ways to run project:
- Run the main script `main.py` to start the project. This script is responsible for executing the web interface of the search engine, this will gives you  functionality and retrieving data using a table to select subject to search and a key word (*two inputs are required*).



![ScreenRecording2024-01-07at17 15 49online-video-cutter com-ezgif com-video-to-gif-converter(1)](https://github.com/jdalfons/search_engine/assets/25759070/fafd475b-5529-4494-af12-86f317ac5869)


- Second way is using jupyter notebook interface, you can open Jupyter normaly and open file `main.ipynb` after set up the credentials and run full notebook, this will gives you a little interface with three inputs and a button.

![ScreenRecording2024-01-07at17 31 01-ezgif com-video-to-gif-converter(3)](https://github.com/jdalfons/search_engine/assets/25759070/121f8dcf-696f-4172-a47e-e6cb2d707bda)

In both cases once the button is clicked the script will running, you will see the data outputs in the output zone (follow images at the top). These outputs will display the results of the search queries made to the Reddit and Arxiv platforms.