#!/usr/bin/env python
from time import sleep
import requests
from bs4 import BeautifulSoup
import getpass


def dork_list(dork_file):
    dorks = []
    with open(dork_file, 'r') as file:
        for line in file:
            dorks.append(line.rstrip().replace(" ", "+"))
    return dorks


def keyword_search(keyword, dorks: list, session):
    s = session
    for dork in dorks:
        sleep(1)
        print(f'Checking for {keyword}+{dork}')
        page = 1
        url = f'https://github.com/search?o=asc&p={str(page)}&q={keyword}+{dork}&s=indexed&type=Code'

        r = s.get(url, timeout=300)
        soup = BeautifulSoup(r.content, 'html5lib')
        menu_items = soup.find_all("a", class_="menu-item")
        total_results = 0
        for menu in menu_items:
            spans = menu.find(
                "span", class_="ml-1 js-codesearch-count Counter Counter--primary")
            if spans:
                for span in spans:
                    total_results = int(span)
        repos = soup.find_all("div", class_="f4 text-normal")
        if total_results >= 1:
            if total_results < 10:
                total_pages = 1
            else:
                total_pages = total_results // 10
                if total_pages % total_results != 0:
                    total_pages += 1
            print(f'Total results: {total_results}')
            print(f'Total Pages: {total_pages}')
            for i in range(1, total_pages+1):
                sleep(1)
                page = i
                url = f'https://github.com/search?o=asc&p={str(page)}&q={keyword}+{dork}&s=indexed&type=Code'
                print(f'url: {url}')
                r = s.get(url, timeout=300)
                soup = BeautifulSoup(r.content, 'html5lib')
                repos = soup.find_all("div", class_="f4 text-normal")
                for repo in repos:
                    data = repo.find_all("a")
                    for item in data:
                        url = 'https://github.com' + item.get('href')
                        print(url)
        else:
            print('No results')


def github_login(base_url, username, password):
    with requests.Session() as s:
        headers = {
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36',
        }
        s.headers.update(headers)
        res = s.get(base_url + 'login')
        soup = BeautifulSoup(res.text, 'html5lib')
        auth_token = soup.find(
            'input', {'name': 'authenticity_token'}).attrs['value']
        commit = soup.find('input', {'name': 'commit'}).attrs['value']

        data = {
            'login': username,
            'password': password,
            'commit': commit,
            'authenticity_token': auth_token
        }
        res = s.post(base_url + 'session', data=data)
        return s


def main():
    base_url = 'https://github.com/'
    dork_file = 'github-dorks.txt'
    username = input('Username:')
    password = getpass.getpass('Password:')
    keyword = input('Keyword to search:')
    s = github_login(base_url, username, password)
    print(f'Logged in: {s.cookies["logged_in"]}')
    dorks = dork_list(dork_file)
    keyword_search(keyword, dorks, s)


if __name__ == '__main__':
    main()
