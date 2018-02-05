#!/usr/bin/env python2.7
import houndify
import sys



CLIENT_ID = sys.argv[1]
CLIENT_KEY = sys.argv[2]
QUERY = sys.argv[3]

requestInfo = {
  ## Pretend we're at SoundHound HQ.  Set other fields as appropriate
  'Latitude': 37.388309, 
  'Longitude': -121.973968
}

client = houndify.TextHoundClient(CLIENT_ID, CLIENT_KEY, "test_user", requestInfo)

## Uncomment the lines below to see an example of using a custom
## grammar for matching.  Use the file 'turnthelightson.wav' to try it.
# clientMatches = [ {
#   "Expression" : '([1/100 ("can"|"could"|"will"|"would")."you"].[1/10 "please"].("turn"|"switch"|(1/100 "flip"))."on".["the"].("light"|"lights").[1/20 "for"."me"].[1/20 "please"])|([1/100 ("can"|"could"|"will"|"would")."you"].[1/10 "please"].[100 ("turn"|"switch"|(1/100 "flip"))].["the"].("light"|"lights")."on".[1/20 "for"."me"].[1/20 "please"])|((("i".("want"|"like"))|((("i".["would"])|("i\'d")).("like"|"want"))).["the"].("light"|"lights").["turned"|"switched"|("to"."go")|(1/100"flipped")]."on".[1/20"please"])"',
#   "Result" : { "Intent" : "TURN_LIGHT_ON" },
#   "SpokenResponse" : "Ok, I\'m turning the lights on.",
#   "SpokenResponseLong" : "Ok, I\'m turning the lights on.",
#   "WrittenResponse" : "Ok, I\'m turning the lights on.",
#   "WrittenResponseLong" : "Ok, I\'m turning the lights on."
# } ]
# client.setHoundRequestInfo('ClientMatches', clientMatches)

response = client.query(QUERY)
print response
