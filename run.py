from scholarly import scholarly, ProxyGenerator
import urllib.parse as urlparse
from urllib.parse import parse_qs
import pandas as pd
import itertools


pg = ProxyGenerator()
pg.Tor_External(tor_sock_port=9050, tor_control_port=9051, tor_password="scholarly_password")
scholarly.use_proxy(pg)

# fetch & store latest data.xlsx file - from GDrive, etc.
data = pd.read_excel('data.xlsx')

def peek(iterable):
    try:
        first = next(iterable)
    except StopIteration:
        return None
    return first, itertools.chain([first], iterable)
    
for index, row in data.iterrows():
    # Retrieve the author's data, fill-in, and print
    # search_query = scholarly.search_author('Steven A Cholewiak')
    # do not use generators coz we'll always get a single profile
    name = row['Last name'].strip()+" "+row['First name'].strip()
    url = row['Google scholar']
    
    print("Author: ", name)
        
    if not pd.isna(url):
        print("Research Profile: ", url)
        parsed = urlparse.urlparse(url)
        search_query = scholarly.search_author_id(parse_qs(parsed.query)['user'][0])
        author = search_query.fill()
        
        print(search_query)    
        print(author)
        # break
        # Print the titles of the author's publications
        # print([pub.bib['title'] for pub in author.publications])

        # Take a closer look at the first publication
        # pub = author.publications[0].fill()
        # print(pub)

        # Which papers cited that publication?
        # print([citation.bib['title'] for citation in pub.citedby])
        # break
    else:
        print("Google Scholar Research Profile not found. Searching using Author name")
        search_query = scholarly.search_author(name)
        if peek(search_query) is not None:
            author = next(search_query).fill()
            print(search_query)    
            print(author)        
        else: 
            print("Couldn't find any research profiles matching input parameter")
        
    print()