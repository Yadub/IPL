import urllib.request
from urllib.error import HTTPError
import pandas as pd
import socket


# Load file with Picture URLs for IPL photos
data_file_path = 'output.csv'
df = pd.read_csv(data_file_path)
# If downloading in parts then change start and max index for downloading images
start_index = 0
max_index = 10000
# Set dir where to save the photos
save_path_dir = './images/'
# Set timeout (seconds) incase there is a websocket timeout
webpage_timeout = 20
socket.setdefaulttimeout(webpage_timeout)
# Iterate
for i in df.index:
    if i < start_index: continue
    if i > max_index: break
    try:
        image_file_name = save_path_dir + 'img_' + str(i + 1) + '.jpg'
        urllib.request.urlretrieve(df['Picture URL'].loc[i], image_file_name)
        print("Downloaded img at index: " + str(i))
    except HTTPError as err:
        print("Failed for img at index " + str(i) + ". Due to HTTP error code: " + str(err.code))
    except Exception as e:
        print("Failed for img at index " + str(i) + ".")
        print(e)
