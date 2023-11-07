"""Justia_Scrape.py

Takes a directory of URLs and scrapes their information, writes to a single .csv
Scrapes the Real Estate Law Portion of Justia: Ask a Lawyer
"""

import pandas as pd
import os
import requests
from bs4 import BeautifulSoup
import csv


def file_lookup(url_list:list, sub_url:str):
  '''Util Function: Iterates through the list of raw URLs and returns a list of URLs that only contain the 
  desired sub-url
  '''
  sub_urls = []
  for url in url_list:
      if url.startswith(sub_url):
          sub_urls.append(url)
  
  return sub_urls



def directory_to_cleaned_list(dir:str):
  '''Iterates through all files of a dictionary and returns a list of URLs 
  matching the sub url.
  '''

  for fname in os.listdir(dir):
    f = f = os.path.join(dir, fname)
    print('reading file: ' + str(fname))
    df = pd.read_csv(f)

    all_urls = df['Unnamed: 1'].tolist()
    all_urls = all_urls[1:]
    question_urls = file_lookup(all_urls, "https://www.lawyers.com/ask-a-lawyer/real-estate")
  
  #Drop duplicate URLs in cleaned list
  unique_URLs = []
  for url in question_urls:
      if url not in unique_URLs:
          unique_URLs.append(url)
  
  return unique_URLs

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


#__Main__

all_urls = directory_to_cleaned_list("lawyers_rawData")
for url in all_urls:
  scrape(url, 'scraped_lawyer.csv')


