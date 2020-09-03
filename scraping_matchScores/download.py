import requests
from bs4 import BeautifulSoup
import pandas as pd
import pickle


def get_innings_data(innings_soup):
    """
        Input bs4 soup data for an innings
        Returns relevant innings data saved as a dictionary
    """
    output = dict()

    # Extract information from i1
    innings_header = innings_soup.find('div', attrs={'class':'cb-scrd-hdr-rw'})
    output['innings_name'] = innings_header.span.text
    output['innings_score'] = innings_header.find('span', attrs={'class': 'pull-right'}).text

    # Split innings into its respective div sections
    innings_array = innings_soup.findChildren(recursive=False)

    # Get data from its first div related to batting information
    innings_batting = innings_array[0]
    div_ = innings_batting.findChildren(recursive=False)
    batting_data = []
    for i, child in enumerate(div_):
        if i == 0:
            innings_name = child.span.text
            innings_score = child.find('span', attrs={'class': 'pull-right'}).text
        else:
            div2_ = child.findChildren(recursive=False)
            row_output = []
            for j, child_2 in enumerate(div2_):
                row_output.append(child_2.text)
            batting_data.append(row_output)
    output['batting_data'] = pd.DataFrame(batting_data[1:], columns=batting_data[0])

    # Get data from its second div related to fall of wickets information
    innings_wickets = innings_array[2]
    fall_of_wickets = innings_wickets.text
    # Get data from its third div related to bowling information
    innings_bowling = innings_array[3]
    div_ = innings_bowling.findChildren(recursive=False)
    bowling_data = []
    for i, child in enumerate(div_):
        div2_ = child.findChildren(recursive=False)
        row_output = []
        for j, child_2 in enumerate(div2_):
            row_output.append(child_2.text)
        bowling_data.append(row_output)
    output['bowling_data'] = pd.DataFrame(bowling_data[1:], columns=bowling_data[0])

    # Get data from its fourth div related to power play information
    innings_power_play = innings_array[4]
    div_ = innings_power_play.findChildren(recursive=False)
    power_play_data = []
    for i, child in enumerate(div_):
        div2_ = child.findChildren(recursive=False)
        row_output = []
        for j, child_2 in enumerate(div2_):
            row_output.append(child_2.text)
        power_play_data.append(row_output)
    output['power_play_data'] = pd.DataFrame(power_play_data[1:], columns=power_play_data[0])

    return output


def download_match_data(url, filename='output', save_path='./', display=True):
    """
        Input url with match website
        Saved a pickle python file (serialized python object as a byte stream)
    """

    save_data = dict() # Initialize
    # Load webpage
    r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
    soup = BeautifulSoup(r.content, features="html.parser")

    # Get match result
    save_data['match_result'] = soup.find('div', attrs={'class':'cb-scrcrd-status'}).text

    # Get innings 1 and innings 2 data
    i1 = soup.find(id='innings_1')
    i2 = soup.find(id='innings_2')
    save_data['innings_1'] = get_innings_data(i1)
    save_data['innings_2'] = get_innings_data(i2)

    # Get match info table (upper columns - upto match umpire)
    match_info = soup.find_all('div', attrs={'class':'cb-mtch-info-itm'})
    match_info_data = []
    for i in range(len(match_info)):
        div_ = match_info[i].findChildren(recursive=False)
        row_output = []
        for i, child in enumerate(div_):
            row_output.append(child.text)
        match_info_data.append(row_output)
    save_data['match_info'] = pd.DataFrame(match_info_data)

    # Get bottom columns of match info table
    further_info = soup.find_all('div', attrs={'class':'cb-minfo-tm-nm'})
    further_info_data = []
    for i in range(len(further_info)):
        div_ = further_info[i].findChildren(recursive=False)
        row_output = []
        for i, child in enumerate(div_):
            row_output.append(child.text)
        further_info_data.append(row_output)
    save_data['further_info'] = pd.DataFrame(further_info_data)

    # Print to console
    if display: print(save_data)

    # Save data as pickle file
    file_path = save_path + filename + '.pkl'
    pickle.dump(save_data, open(file_path, 'wb'))

    return save_data


if __name__ == '__main__':
    # Load IPL photos page
    url = "https://www.cricbuzz.com/live-cricket-scorecard/29793/gaw-vs-bt-22nd-match-caribbean-premier-league-2020"
    download_match_data(url)

    # To load previously downloaded data use the following line of code in python
    # data = pickle.load(open('./data.pkl', 'rb'))
