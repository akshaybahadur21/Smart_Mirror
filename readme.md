# Smart_Mirror
Smart Mirror with AI as well as home automation.

## Open Source

1) [MichMich MagicMirror](https://magicmirror.builders/)

### Code Requirements
The example code is in Python ([version 2.7](https://www.python.org/download/releases/2.7/) or higher will work). 

1) import speechrecognition
2) import gtts
3) import py4j
4) import python-dateutil
5) import pydub
6) import feedparser
7) import numpy

# Setup Guide

## Magic Mirror
Download the stable version of Node.js: 
https://nodejs.org/en/

Clone the latest MagicMirror code from:
https://github.com/MichMich/MagicMirror

Navigate inside the MagicMirror folder
```shell
cd MagicMirror
```

Install MagicMirror dependencies
```shell
sudo npm install
```
 
Verify it starts
```shell
npm start
```
 
 
Clone this repository (AI Smart Mirror)
```shell
git clone git@github.com:akshaybahadur21/Smart_Mirror.git
```

Copy the folders in `Smart_Mirror/magic_mirror` to `MagicMirror/modules`

Copy the `config.js` file in `Smart_Mirror/magic_mirror` to `MagicMirror/config`
 
## AI
 
We are using [wit.ai](https://wit.ai/) for generating intents out of the text.
You need to generate an access id using which, you can send GET requests to get intents.

## Weather

For weather we are using [darksky.net](https://darksky.net/).
You have to create your own developer account and get the API key.
### What's the weather forecast?

## Youtube
For enabling youTube, you need to get the youTube secret Key from the Google's developer Console.
Add the key in the code.
### Can you play me a video of Eminem?

## Maps

For map, we are using Google maps. Types of map we support right now are :
1) Normal
2) Hybrid
3) Satellite
4) Terrain
### Can you show me map of India?

## News

For news, we use Google news and the location has been set to IN (INDIA).
You can change it according o your country to get the latest news.
### Can you show me the latest news?

## Uber

You can directly book an uber and get the arrival map using this module.
You need to get the API Key, Client Secret, Oauth Key and paste it in the code.
### Can you book me an uber pool/go from Vimaan Nagar to Baner?

## Zomato

For zomato, you need to get the API key from zomato's dev site.
And paste it in the code. 
You can view the list of available restaurants in a region.
### Can you show me restaurants in Pune?

## SoundHound

For various other tasks, we have used soundhound's api. The soundhound service is quite effective and fast. Operations that could be done using soundhound:
1) Solving Mathematical equations
2) Stock Market
3) Hotel Enquiries.

### What are the roots for x^2-x+1
### What are the stock prices and market cap of Google, Apple and Microsoft.
### Can you show me hotels in New York that have a swimming pool for next Monday?
### Who's Sachine Tendulkar?

# Commands that you could use on the mirror

1) Can you play me a video of Eminem?
2) Can you book me an uber pool/go from Vimaan Nagar to Baner?
3) Can you show me restaurants in Pune?
4) Can you show me the latest news?
5) Can you show me the weather forecast?
6) Can you show me map of India?
7) Can you tell me a joke?
8) How do I look?
9) Show me your face.
10) What are the roots for x^2-x+1
11) What are the stock prices and market cap of Google, Apple and Microsoft.
12) Can you show me hotels in New York that have a swimming pool for next Monday?
13) Who's Sachine Tendulkar?

## API

Different APIs have been used for different services. You are required to create an account and get the respective keys from the providers.
You have to place the keys in the code.
The instructions for the same are given in the code.

### There are some easter eggs which you guys can find out and let us know in the forum.

# Starting Up
 
Navigate to the AI-Smart-Mirror folder
```shell
cd AI-Smart-Mirror
```

Make sure MagicMirror is running, then start the AI
```shell
python bot.py
```

## Setup Facial Recognition
[Refer to this guide](http://opencv-python-tutroals.readthedocs.io/en/latest/)

Install openCV with 
```shell
pip install cv2
```

Start the app
```shell
python bot.py
```

## Working Example

<img src="https://github.com/akshaybahadur21/Smart_Mirror/blob/master/smart_mirror.gif">


 
