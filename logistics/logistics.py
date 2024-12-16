import requests
import os
from dotenv import find_dotenv, load_dotenv
import uuid

load_dotenv(find_dotenv())



def process_weather(query):

    url = f"{os.getenv('URL')}?q={query}&key={os.getenv('LOGISTICS_KEY')}"

    r = requests.get(url)

    if r.status_code == 200:


        return r.json(), True
    else:

        return {"message": "An error occured"}, False




def generate_tracking_id():

    return str(uuid.uuid4())[:8]