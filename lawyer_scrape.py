"""Justia_Scrape.py

Takes a directory of URLs and scrapes their information, writes to a single .csv
Scrapes the Real Estate Law Portion of Justia: Ask a Lawyer
"""

import pandas as pd
import numpy as np
import os
import requests
import json
import urllib.request
from bs4 import BeautifulSoup
import csv


def question_lookup(url_list:list, sub_url:str):
  '''Util Function: Iterates through the list of raw URLs and returns a list of URLs that only contain the 
  desired sub-url
  '''
  return_list = []
  for url in url_list:
      if url.startswith(sub_url):
          return_list.append(url)
  return return_list



def directory_to_cleaned_list(dir:str):
  '''Iterates through all files of a dictionary and returns a list of URLs 
  matching the sub url.
  '''
  cleaned_URLs = []

  for fname in os.listdir(dir):
    f = f = os.path.join(dir, fname)
    print('reading file: ' + str(fname))
    df = pd.read_csv(f)

    all_urls = df['Unnamed: 1'].tolist()
    all_urls = all_urls[1:]
    question_urls = question_lookup(all_urls, "https://answers.justia.com/question/")
  
    for url in question_urls:
      cleaned_URLs.append(url)

  #Drop duplicate URLs in cleaned list
  unique_URLs = []
  for url in cleaned_URLs:
      if url not in unique_URLs:
          unique_URLs.append(url)
  
  return unique_URLs

  #print('length of cleaned URL list: ' + str(len(unique_URLs)))

def scrape(url:str, filename: str):
  ''' Takes a url from the Question page of Lawyers.com and writes to a .csv
  in a 2-column format Question, Answer(s)
  '''
  print('scraping ' + str(url))
  #Scrapes Data
  rows = []
  header = ['Question', 'Answer(s)']

  response = requests.get(
  url='https://proxy.scrapeops.io/v1/',
  params={
      'api_key': 'd02ca450-7b42-4789-8528-ecf96ea1a150',
      'url': url, 
      'residential': 'true', 
  },
)

  soup = BeautifulSoup(response.content, 'html.parser')
  data_q = soup.find_all('div', {'class': "qaDetailsContent"})
  data_a = soup.find_all('div', {'class': "small-12 columns qaDetailsContent"})
  
  rows.append([data_q, data_a])

  #Wrtie to .csv
  file_exists = os.path.isfile(filename)

  with open(filename, 'a', newline='') as csv_file:
        writer = csv.writer(csv_file)
        
        if not file_exists:
            writer.writerow(header)

        writer.writerows(rows)

def save_to_csv(data, filename):
    header = ['question_title', 'question_description', 'answer', 'upvote_count']

    rows = []
    for key, value in data.items():
        if key.startswith('answer'):
            answer, upvote_count = value
            question_title = data['question_title']
            question_description = data['question_description']
            rows.append([question_title, question_description, answer, upvote_count])

    #Check if file exists --> append header if not
    file_exists = os.path.isfile(filename)

    with open(filename, 'a', newline='') as csv_file:
        writer = csv.writer(csv_file)
        
        if not file_exists:
            writer.writerow(header)

        writer.writerows(rows)

#__Main__
directory = 'Justia_rawURLs'
sub_url = "https://answers.justia.com/question/"




'''
url = "https://www.lawyers.com/ask-a-lawyer/real-estate/as-a-seller-can-i-cancel-the-sale-if-i-am-not-able-get-the-liens-removed-before-closing--will-there-be-a-penalty-1537928.html"

response = requests.get(
  url='https://proxy.scrapeops.io/v1/',
  params={
      'api_key': 'd02ca450-7b42-4789-8528-ecf96ea1a150',
      'url': url, 
      'residential': 'true', 
  },
)

soup = BeautifulSoup(response.content, 'html.parser')
data_q = soup.find_all('div', {'class': "qaDetailsContent"})
print(data_q)

data_a = soup.find_all('div', {'class': "small-12 columns qaDetailsContent"})
print(data_a)'''


