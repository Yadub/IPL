import requests
from bs4 import BeautifulSoup
import pandas as pd


# Set file name for the data output
save_file_name = 'output' + '.csv'
# Load IPL photos page
ipl_URL = "https://www.iplt20.com"
url = ipl_URL + "/photos"
r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
if r.status_code != 404:
    soup = BeautifulSoup(r.content, features="html.parser")
else:
    soup = None
# Get all the hrefs to event pages on the webpage of the form "/photos/*"
event_hrefs = []
for a in soup.find_all('a', href=True):
    if a['href'].startswith('/photos/'):
        event_hrefs.append(a['href'])
# Array to store the output
output = []
# Load each event webpage
for href in event_hrefs:
    event_url = ipl_URL + href
    r = requests.get(event_url, headers={'User-Agent': 'Mozilla/5.0'})
    if r.status_code != 404:
        soup = BeautifulSoup(r.content, features="html.parser")
    else:
        soup = None
    # Get all the hrefs to photo pages on the eventpage of the form "/photos/*"
    photo_hrefs = []
    for a in soup.find_all('a', href=True):
        if a['href'].startswith('/photos/'):
            photo_hrefs.append(a['href'])
    # Load each photo webpage
    for photo_href in photo_hrefs:
        photo_url = ipl_URL + photo_href
        r = requests.get(photo_url, headers={'User-Agent': 'Mozilla/5.0'})
        if r.status_code != 404:
            soup = BeautifulSoup(r.content, features="html.parser")
        else:
            soup = None
        # Save desired data if avaialable
        try:
            pic_url = soup.find_all('picture', attrs={'class': 'main-photo__picture'})[0].img['src']
            description_str = soup.find_all('meta', attrs={'name': 'description'})[0]['content']
            output.append([photo_url, pic_url, description_str])
            print("Saved from url: " + photo_url)
        except:
            print("Failed for url: " + photo_url)
    # Save data after photos of every event have been loaded
    print("Completed url: " + event_url)
    df = pd.DataFrame(output, columns = ['Webpage URL', 'Picture URL', 'Description'])
    df.to_csv('output.csv', index=False)
