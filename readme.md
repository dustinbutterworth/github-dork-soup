# github-dork-soup
I grew tired of dealing with Github API and its endless api limits and caveats, so I thought I'd see what a web scraping process could look like
with dorking github.

# Prerequisites
A github account with MFA not enabled. I recommend creating a throwaway account for this, never use it for anything important or sensitive. 


# Steps to Run
Set up your python virtual environment then install dependencies
```
pip install -r requirements.txt
```

Then just run `python github_dork_soup.py`  
When prompted, provide username, then passsword, then the keyword you want to search for alongside with your dorks.

Github dorks should all be placed in [github-dorks.txt](./github-dorks.txt), which I found on the [github-dorks](https://github.com/techgaun/github-dorks) project from techgaun. You can cater this file to your needs.

# Notes
I threw this together pretty quickly, so there is lots more that could be added and improved on. This project is more of a POC than anything.
