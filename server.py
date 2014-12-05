import sys
import requests
from flask import request, Flask
import json
import logging


logging.basicConfig(stream=sys.stdout, level=logging.INFO,
                    format='%(asctime)s %(levelname)s: %(message)s')

# Geo Name API user id: http://www.geonames.org/
GEO_NAMES_USER_ID = ''
# Yo API Token: http://dev.justyo.co
YO_API_TOKEN = ''

LAT_LONG_URL = 'http://ws.geonames.org/findNearbyJSON?lat=%s&lng=%s&username=%s'

URL_SPOTITY_INDIA = 'spotify:user:filtrindia:playlist:4nNVfQ9eWidZXkBKZN5li4'
URL_SPOTITY_US = 'spotify:user:spotify:playlist:6LBZwjKY0VZLoe79qeGcCF'



app = Flask(__name__)

@app.route("/yo/")
def yo():

    # extract and parse query parameters
    username = request.args.get('username')
    location = request.args.get('location')

    logging.info('We got a Yo from : ' + username)

    country = ''

    if location is not None:
        splitted = location.split(';')
        latitude = splitted[0]
        longitude = splitted[1]
        lat_log_tmp = LAT_LONG_URL % (latitude, longitude,GEO_NAMES_USER_ID)
        response = requests.get(lat_log_tmp).json()
        logging.info('We got Lat Long : %s , %s' %
                     (str(latitude), str(longitude)))

    country = repsonse['geonames'][0]['countryName']

    logging.info('Country decoded to : ' + str(country))

    spotify_url = ''

    if country is 'India':
        spotify_url = URL_SPOTITY_INDIA
    else:
        spotify_url = URL_SPOTITY_US

    # Yo the result back to the user
    requests.post("http://api.justyo.co/yo/",
                  data={'api_token': YO_API_TOKEN, 'username': username, 'link': spotify_url})

    # OK!
    return 'OK'


if __name__ == "__main__":
    app.debug = True
    app.run(host="0.0.0.0", port=5050)
