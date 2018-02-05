# bot.py

# speechrecognition, pyaudio, brew install portaudio
import sys
sys.path.append("./")

import requests
import datetime
import time
import dateutil.parser
import json
import traceback
from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.tools import argparser
from uber_rides.client import UberRidesClient
from uber_rides.session import OAuth2Credential
from uber_rides.session import Session
import houndify


from nlg import NLG
from speech import Speech
from knowledge import Knowledge
from vision import Vision

my_name = "Raghav"
launch_phrase = "ok mirror"
use_launch_phrase = True
weather_api_token = ""
wit_ai_token = ""
debugger_enabled = True
camera = 0


class Bot(object):
    def __init__(self):
        self.nlg = NLG(user_name=my_name)
        self.speech = Speech(launch_phrase=launch_phrase, debugger_enabled=debugger_enabled)
        self.knowledge = Knowledge(weather_api_token)
        self.vision = Vision(camera=camera)

    def start(self):
        """
        Main loop. Waits for the launch phrase, then decides an action.
        :return:
        """
        while True:
            requests.get("http://localhost:8080/clear")
            if self.vision.recognize_face():
                print "Found face"
                if use_launch_phrase:
                    recognizer, audio = self.speech.listen_for_audio()
                    if self.speech.is_call_to_action(recognizer, audio):
                        self.__acknowledge_action()
                        self.decide_action()

                            
                else:

                    self.decide_action()

                        

    def decide_action(self):
        """
        Recursively decides an action based on the intent.
        :return:
        """
        recognizer, audio = self.speech.listen_for_audio()

        # received audio data, now we'll recognize it using Google Speech Recognition
        speech = self.speech.google_speech_recognition(recognizer, audio)
        #speech = "can you show me a map of Pune"
        #print speech

        if speech is not None:
            try:
                r = requests.get('https://api.wit.ai/message?v=20160918&q=%s' % speech,
                                 headers={"Authorization": wit_ai_token})
                print r.text
                json_resp = json.loads(r.text)
                entities = None
                intent = None
                Status_Type = None
                if 'entities' in json_resp and 'Intent' in json_resp['entities']:
                    entities = json_resp['entities']
                    intent = json_resp['entities']['Intent'][0]["value"]

                print intent
                if 'Status_Type' in json_resp['entities'] :
                    entities = json_resp['entities']
                    Status_Type = json_resp['entities']['Status_Type'][0]["value"]
                    

                #print Status_Type
                if Status_Type is not None:
                   self.__module_action(entities)
                   return 

               

                if intent == 'greeting':
                    self.__text_action(self.nlg.greet())
                elif intent == 'snow white':
                    self.__text_action(self.nlg.snow_white())
                elif intent == 'weather':
                    self.__weather_action(entities)
                elif intent == 'news':
                    self.__news_action()
                elif intent == 'maps':
                    self.__maps_action(entities)
                elif intent == 'youtube':
                    self.__youtube_action(entities)
                    #if self.vision.recognize_face():
                       # print "Found face"
                elif intent == 'zomato':
                    self.__zomato_action(entities)
                elif intent == 'uber':
                    self.__uber_action(entities)        
                elif intent == 'holidays':
                    self.__holidays_action()
                elif intent == 'appearance':
                    self.__appearance_action()
                elif intent == 'user status':
                    self.__user_status_action(entities)
                elif intent == 'user name':
                    self.__user_name_action()
                elif intent == 'personal status':
                    self.__personal_status_action()
                elif intent == 'joke':
                    self.__joke_action()
                elif intent == 'insult':
                    self.__insult_action()
                    return
                elif intent == 'appreciation':
                    self.__appreciation_action()
                    return
                  
                
                elif intent is None:
                    self.__hound_action(speech)
                    return
 

                else:
                     self.__text_action("I'm sorry, I don't know about that yet.")
                     return

                #time.sleep(20)
                

            except Exception as e:
                print "Failed wit!"
                print(e)
                traceback.print_exc()
                self.__text_action("I'm sorry, I couldn't understand what you meant by that")
                return

            self.decide_action()

    def __joke_action(self):
        joke = self.nlg.joke()

        if joke is not None:
            self.__text_action(joke)
        else:
            self.__text_action("I couldn't find any jokes")

    def __user_status_action(self, nlu_entities=None):
        attribute = None

        if (nlu_entities is not None) and ("Status_Type" in nlu_entities):
            attribute = nlu_entities['Status_Type'][0]['value']

        self.__text_action(self.nlg.user_status(attribute=attribute))

    def __user_name_action(self):
        if self.nlg.user_name is None:
            self.__text_action("I don't know your name. You can configure it in bot.py")

        self.__text_action(self.nlg.user_name)

    def __appearance_action(self):
        requests.get("http://localhost:8080/face")

    def __appreciation_action(self):
        self.__text_action(self.nlg.appreciation())

    def __acknowledge_action(self):
        self.__text_action(self.nlg.acknowledge())

    def __insult_action(self):
        self.__text_action(self.nlg.insult())

    def __personal_status_action(self):
        self.__text_action(self.nlg.personal_status())

    def __text_action(self, text=None):
        if text is not None:
            requests.get("http://localhost:8080/statement?text=%s" % text)
            self.speech.synthesize_text(text)

    def __news_action(self):
        headlines = self.knowledge.get_news()

        if headlines:
            requests.post("http://localhost:8080/news", data=json.dumps({"articles":headlines}))
            self.speech.synthesize_text(self.nlg.news("past"))
            interest = self.nlg.article_interest(headlines)
            if interest is not None:
                self.speech.synthesize_text(interest)
        else:
            self.__text_action("I had some trouble finding news for you")

    def __weather_action(self, nlu_entities=None):

        current_dtime = datetime.datetime.now()
        skip_weather = False # used if we decide that current weather is not important

        weather_obj = self.knowledge.find_weather()
        temperature = weather_obj['temperature']
        icon = weather_obj['icon']
        wind_speed = weather_obj['windSpeed']

        weather_speech = self.nlg.weather(temperature, current_dtime, "present")
        forecast_speech = None

        if nlu_entities is not None:
            if 'datetime' in nlu_entities:
                if 'grain' in nlu_entities['datetime'][0] and nlu_entities['datetime'][0]['grain'] == 'day':
                    dtime_str = nlu_entities['datetime'][0]['value'] # 2016-09-26T00:00:00.000-07:00
                    dtime = dateutil.parser.parse(dtime_str)
                    if current_dtime.date() == dtime.date(): # hourly weather
                        forecast_obj = {'forecast_type': 'hourly', 'forecast': weather_obj['daily_forecast']}
                        forecast_speech = self.nlg.forecast(forecast_obj)
                    elif current_dtime.date() < dtime.date(): # sometime in the future ... get the weekly forecast/ handle specific days
                        forecast_obj = {'forecast_type': 'daily', 'forecast': weather_obj['weekly_forecast']}
                        forecast_speech = self.nlg.forecast(forecast_obj)
                        skip_weather = True
            if 'Weather_Type' in nlu_entities:
                weather_type = nlu_entities['Weather_Type'][0]['value']
                print weather_type
                if weather_type == "current":
                    forecast_obj = {'forecast_type': 'current', 'forecast': weather_obj['current_forecast']}
                    forecast_speech = self.nlg.forecast(forecast_obj)
                elif weather_type == 'today':
                    forecast_obj = {'forecast_type': 'hourly', 'forecast': weather_obj['daily_forecast']}
                    forecast_speech = self.nlg.forecast(forecast_obj)
                elif weather_type == 'tomorrow' or weather_type == '3 day' or weather_type == '7 day':
                    forecast_obj = {'forecast_type': 'daily', 'forecast': weather_obj['weekly_forecast']}
                    forecast_speech = self.nlg.forecast(forecast_obj)
                    skip_weather = True


        weather_data = {"temperature": temperature, "icon": icon, 'windSpeed': wind_speed, "hour": datetime.datetime.now().hour}
        requests.post("http://localhost:8080/weather", data=json.dumps(weather_data))

        if not skip_weather:
            self.speech.synthesize_text(weather_speech)

        if forecast_speech is not None:
            self.speech.synthesize_text(forecast_speech)

    def __maps_action(self, nlu_entities=None):

        location = None
        map_type = None
        if nlu_entities is not None:
            if 'location' in nlu_entities:
                location = nlu_entities['location'][0]["value"]
                #location = nlu_entities['search_query'][0]["value"]
            else:
                location = nlu_entities['search_query'][0]["value"]
            if "Map_Type" in nlu_entities:
                map_type = nlu_entities['Map_Type'][0]["value"]

        if location is not None:
            maps_url = self.knowledge.get_map_url(location, map_type)
            maps_action = "Sure. Here's a map of %s." % location
            body = {'url': maps_url}
            requests.post("http://localhost:8080/image", data=json.dumps(body))
            self.speech.synthesize_text(maps_action)
        else:
            self.__text_action("I'm sorry, I couldn't understand what location you wanted.")

    def __youtube_action(self, nlu_entities=None):
        video = None
        DEVELOPER_KEY = ""  #add developer key 
        YOUTUBE_API_SERVICE_NAME = "youtube"
        YOUTUBE_API_VERSION = "v3"
        

        
        if nlu_entities is not None:
            if 'search_query' in nlu_entities:
                video = nlu_entities['search_query'][0]["value"]

        if video is not None:
            youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
            developerKey=DEVELOPER_KEY)
            search_response = youtube.search().list(
            q=video,
            part="id,snippet",
            ).execute()

            
            for search_result in search_response.get("items"):


                if search_result["id"]["kind"] == "youtube#video":
                    id= search_result["id"]["videoId"]
                    ch_title =  search_result["snippet"]["channelTitle"]
                   
                    title =  search_result["snippet"]["title"]
                    break;
                thumb = search_result["snippet"]["thumbnails"]["medium"]    

                


            for search_result in search_response.get("items"):


                thumb = search_result["snippet"]["thumbnails"]["medium"] 
                   
                break;
                   
           
            print id
            #print thumb
            videou = "https://www.youtube.com/embed/" + id + "?autoplay=1&controls=1"
            #print videou
           
            youtube_action = "Sure. Here's a video of %s." % video
            body = {'url': videou, 'channel': ch_title, 'thumb':thumb, 'titles':title}
            requests.post("http://localhost:8080/video", data=json.dumps(body))
            self.speech.synthesize_text(youtube_action)
            time.sleep(8)
            
           
           
        else:
            self.__text_action("I'm sorry, I couldn't understand what video you wanted.")  

    def __zomato_action(self, nlu_entities=None):
        if nlu_entities is not None:
            if 'location' in nlu_entities:
                entities=nlu_entities['location'][0]["value"]
                print entities
                response= requests.get('https://maps.googleapis.com/maps/api/geocode/json?address=%s&key=' %entities) #inset google maps key here
                resp_json_payload = response.json()
                lat=(resp_json_payload['results'][0]['geometry']['location']['lat'])
                lng=(resp_json_payload['results'][0]['geometry']['location']['lng'])

                print lat
                print lng
                locationUrlFromLatLong = "https://developers.zomato.com/api/v2.1/geocode?lat=%s&lon=%s" %(lat,lng)
                header = {"Accept": "application/json", "user_key": ""}  #add user key

                response = requests.get(locationUrlFromLatLong, headers=header)

                restaurants=(response.json().get("nearby_restaurants"))
                name = []
                rating = []
                avgcost = []
                for restaurant in restaurants:
                    name.append(restaurant['restaurant']['name'])
                    avgcost.append(restaurant['restaurant']['average_cost_for_two'])
                    rating.append(restaurant['restaurant']['user_rating']['aggregate_rating'])
                    
                    

                    #print name    

                

                zomato_data = {"cabtype": name, 'maxfare': avgcost, "minfare": rating}
                uber_action = "Sure. Here are some results"
                
                

                requests.post("http://localhost:8080/zomato", data=json.dumps(zomato_data))
                #self.speech.synthesize_text(uber_action)


               

                self.speech.synthesize_text(uber_action)
            
           
           
        else:
            self.__text_action("I'm sorry, I couldn't understand what restaurant you wanted.")  

    
    def __uber_action(self, nlu_entities=None):
        uber = None
        
                
        if nlu_entities is not None:
            if 'location' in nlu_entities:
                 entities3=nlu_entities['search_query'][0]["value"]
                 entities1=nlu_entities['location'][0]["value"]
                 entities2=nlu_entities['location'][1]["value"]
                 print entities3
                 print entities1
                 print entities2

        if entities1 and entities2  is not None:
            response= requests.get('https://maps.googleapis.com/maps/api/geocode/json?address=%s&key=' %entities1) #add key
            resp_json_payload = response.json()

            lat1=(resp_json_payload['results'][0]['geometry']['location']['lat'])
            lng1=(resp_json_payload['results'][0]['geometry']['location']['lng'])

            response = requests.get('https://maps.googleapis.com/maps/api/geocode/json?address=%s&key=' %entities2)  #add key

            resp_json_payload = response.json()
            
            lat2=(resp_json_payload['results'][0]['geometry']['location']['lat'])
            lng2=(resp_json_payload['results'][0]['geometry']['location']['lng'])

            oauth2credential = OAuth2Credential(
            client_id='', #add client id
            access_token='', #get access token
            expires_in_seconds= '2592000',
            scopes='all_trips delivery history history_lite places profile request request_receipt ride_widgets',
            grant_type='authorization_code',
            redirect_url='', #add redirect_url
            client_secret='', #add client secret
            refresh_token='', # add refresh token
        )

            session = Session(oauth2credential=oauth2credential)
            client = UberRidesClient(session, sandbox_mode=True)

            print (client)

            response = client.get_products(lat1, lng1)
            credentials = session.oauth2credential
            #print (response)
            response = client.get_user_profile()
            profile = response.json
            
            # response_uber = client.get_price_estimates(
            #     start_latitude=lat1,
            #     start_longitude=lng1,
            #     end_latitude=lat2,
            #     end_longitude=lng2,
            #     seat_count=1
            # )

            # estimate = response_uber.json.get('prices')

            # print estimate[0]['high_estimate']
            # print estimate[0]['low_estimate']
            # print estimate[0]['localized_display_name']
            # print estimate[0]['currency_code']
            # currency = estimate[0]['currency_code']
            # hi_est =  str(estimate[0]['high_estimate']) + str(estimate[0]['currency_code'])
            # low_est =  str(estimate[0]['low_estimate']) + str(estimate[0]['currency_code'])
            # type_cab =  estimate[0]['localized_display_name']
             

            # print estimate[0]

            response = client.get_products(lat1, lng1)
            products = response.json.get('products')
            #print(products)
            if entities3 == 'Uber go':
                for i in range(1,5):
                    if products[i]['display_name']=='uberGO':
                        product_id = products[i].get('product_id')
                        type_cab = products[i].get('display_name')
            elif entities3 == 'Uber pool':
                for i in range(1,5):
                    if products[i]['display_name']=='POOL':
                        product_id = products[i].get('product_id')
                        type_cab = products[i].get('display_name')
            else:
                product_id = products[0].get('product_id')
                type_cab = products[0].get('display_name')

            

            estimate = client.estimate_ride(
                product_id=product_id,
                start_latitude=lat1,
                start_longitude=lng1,
                end_latitude=lat2,
                end_longitude=lng2,
                seat_count=1
            )
            fare = estimate.json.get('fare') 
            bas = fare['display'] 
            client.cancel_current_ride()
            response = client.request_ride(
             product_id=product_id,
             start_latitude=lat1,
             start_longitude=lng1,
             end_latitude=lat2,
             end_longitude=lng2,
             seat_count=1,
             fare_id=fare['fare_id']
            )  

            request = response.json
            print request
            request_id = request.get('request_id')
            url = 'https://sandbox-api.uber.com/v1.2/sandbox/requests/' + request_id
            ur = 'https://sandbox-api.uber.com/v1.2/requests/' + request_id + '/map'

            token = "" #insert token

            data = {
                "status": "accepted"

                }

            headers = {'Authorization': 'Bearer ' + token, "Content-Type": "application/json"}

#Call REST API
            respons = requests.put(url, data=json.dumps(data), headers=headers)
            respon = requests.get(ur, headers=headers)
            response = client.get_ride_details(request_id)
            ride = response.json
            print ride

            status = ride.get('status')
            dri_name = ride.get('driver').get('name')
            dri_pic = ride.get('driver').get('picture_url')

            eta = ride.get('destination').get('eta')   
            car_pix = ride.get('vehicle').get('picture_url')

            
            # product_name1 = products[3]['display_name'] #GO
            # product_nam2 = products[2]['display_name'] #POOL

            uber_action = "Sure. Booking your uber from %s to %s. Your cab type is %s and estimated time of arrival is %s and fare will be approx %s" % (entities1, entities2, type_cab, eta, bas)
            cab_data = {"cabtype": type_cab, 'maxfare': bas, "minfare": eta, 'to': entities2, 'from': entities1, 'status':status, 'driver': dri_name, 'pic': dri_pic, 'car': car_pix, 'map':ur}
            #print cab_data

            requests.post("http://localhost:8080/cab", data=json.dumps(cab_data))
            self.speech.synthesize_text(uber_action)
            
           
        else:
            self.__text_action("I'm sorry, I don't think that their is any cab available between these two locations.")                

    def __holidays_action(self):
        holidays = self.knowledge.get_holidays()
        next_holiday = self.__find_next_holiday(holidays)
        requests.post("http://localhost:8080/holidays", json.dumps({"holiday": next_holiday}))
        self.speech.synthesize_text(self.nlg.holiday(next_holiday['localName']))

    def __find_next_holiday(self, holidays):
        today = datetime.datetime.now()
        for holiday in holidays:
            date = holiday['date']
            if (date['day'] > today.day) and (date['month'] > today.month):
                return holiday

        # next year
        return holidays[0]


    

    def __module_action(self, nlu_entities=None):
        
        if nlu_entities is not None:
 
            Status_Type = nlu_entities['Status_Type'][0]["value"]
            if 'search_query' in nlu_entities:
                
                video = nlu_entities['search_query'][0]["value"]
                print video
                body = {'url': video, 'sta': Status_Type}
                print body

                requests.post("http://localhost:8080/module", data=json.dumps(body)) 
                print 'Raghav'
                self.speech.synthesize_text("sure")


        
  
    def __hound_action(self, speech=None):
         if speech is not None:
            clientId = "" #get client id from houndify
            clientKey = "" #insert client key
            userId = "test_user"
            requestInfo = {
              "Latitude": 18.5679, 
              "Longitude": 73.9143
            }

            client = houndify.TextHoundClient(clientId, clientKey, userId, requestInfo)
            response = client.query(speech)
            #conversationState = response["AllResults"][0]["ConversationState"]
            #client.setConversationState(conversationState)
            command = response["AllResults"][0]["WrittenResponseLong"]
            
           
            spoken = response["AllResults"][0]["SpokenResponseLong"]
             
            name = []
            rating = []
            avgcost = []    
            url = []  
            print 
            if "Template" in response["AllResults"][0]["ViewType"]:
                if len(response["AllResults"][0]["TemplateData"]["Items"]) > 8:
                    for item in range(0,10):
                        if 'Title' in response["AllResults"][0]["TemplateData"]["Items"][item]["TemplateData"]:
                            name.append(response["AllResults"][0]["TemplateData"]["Items"][item]["TemplateData"]["Title"])
                        if 'Subtitle' in response["AllResults"][0]["TemplateData"]["Items"][item]["TemplateData"]:
                            rating.append(response["AllResults"][0]["TemplateData"]["Items"][item]["TemplateData"]["Subtitle"])
                        if 'BodyText' in response["AllResults"][0]["TemplateData"]["Items"][item]["TemplateData"]:    
                            avgcost.append(response["AllResults"][0]["TemplateData"]["Items"][item]["TemplateData"]["BodyText"])
                        if 'URL' in response["AllResults"][0]["TemplateData"]["Items"][item]["TemplateData"]["Image"]:    
                            url.append(response["AllResults"][0]["TemplateData"]["Items"][item]["TemplateData"]["Image"][ "URL"])


                    hound_data = {"title": name, 'subtitle': rating, "details": avgcost, "url": url, "command": command}
                    requests.post("http://localhost:8080/other", data=json.dumps(hound_data))
                else:   
                    requests.post("http://localhost:8080/other", data=json.dumps(command))
                    

            #requests.get("http://localhost:8080/statement?text=%s" % text)
            #self.speech.synthesize_text(text)
            
            else:
                requests.post("http://localhost:8080/other", data=json.dumps(command))

            self.speech.synthesize_text(spoken)
            self.decide_action()
        #     if conversationState is not None:
        #         recognizer, audio = self.speech.listen_for_audio()

        # # received audio data, now we'll recognize it using Google Speech Recognition                            ## SOUNHOUND Converstaion state
        #         speech = self.speech.google_speech_recognition(recognizer, audio)
        #         response = client.query(speech)
                
        #         if response["AllResults"][0]["WrittenResponseLong"] == "Didn't get that!" :
        #             self.decide_action()


            


            
            

            # command = response["AllResults"][0]["WrittenResponseLong"]
            
           
            # spoken = response["AllResults"][0]["SpokenResponseLong"]

           

            # #requests.get("http://localhost:8080/statement?text=%s" % text)
            # #self.speech.synthesize_text(text)
            
            
            # requests.post("http://localhost:8080/other", data=json.dumps(command))
            # #self.speech.synthesize_text(spoken)
          
    

     


if __name__ == "__main__":
    bot = Bot()
    bot.start()
