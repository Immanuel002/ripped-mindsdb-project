import asyncio
from flask import render_template, request, json, jsonify
import requests

from app import app


async def fetch_recipe():
    session = requests.Session()
    session.post('https://cloud.mindsdb.com/cloud/login', json={
        'email': 'zubeenqadry@gmail.com',
        'password': 'Asdf@1234'
    })

    query = "SELECT answer FROM mindsdb.recipemaster6 WHERE question = 'Start your response with the sentence Hola Amigo !  Do not add salutations or anything else to your response. Behave like a chef who knows a ton of different recipes. You are responding to an audience that is looking to loose weight. Now suggest me just one new recipe each time I ask you, in the form of bullet points, that is healthy and easy to cook?';"
    resp = session.post('https://cloud.mindsdb.com/api/sql/query', json={'query': query})

    #query_calories = "answer in exactly this format: It has xx calories. This is the question: What are the number of calories in an average sized turnip"
    #resp_calories = session.post('https://cloud.mindsdb.com/api/sql/query', json={'query': query})
    
    json_response = resp.json()
    #json_response2 = resp_calories.json()
    # Assuming there's only one element in the inner list
    data_value = json_response['data'][0][0]  
    #data_value2 = json_response['data'][0][0] 
    
    # Remove special characters from start and end
    data_value = data_value.strip('[\n]').strip()
    #data_value2 = data_value2.strip('[\n]').strip()

    #Debug and print value
    #print(data_value2)

    if resp.status_code == 200:
        return data_value
    else:
        return 'Error fetching recipe'
    
async def fetch_calories():
    session = requests.Session()
    session.post('https://cloud.mindsdb.com/cloud/login', json={
        'email': 'zubeenqadry@gmail.com',
        'password': 'Asdf@1234'
    })
    food_item_to_check = request.form['food_item']
    custom_query = "SELECT answer FROM mindsdb.recipemaster6 WHERE question = 'answer in exactly this format: It has xx calories. This is the question: What are the number of calories in an average sized" + food_item_to_check +"?';"
    
    query_calories = custom_query
    resp_calories = session.post('https://cloud.mindsdb.com/api/sql/query', json={'query': query_calories})

    json_response_calories = resp_calories.json()

    #if 'data' in json_response_calories and json_response_calories['data']:
    data_value_calories = json_response_calories['data'][0][0]

        # Remove special characters from start and end
    data_value_calories = data_value_calories.strip('[\n]').strip()

        # Debug and print value
    print(data_value_calories)

    if resp_calories.status_code == 200:
        return data_value_calories
    else:
        return 'Error fetching calories'


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        # Fetch recipe asynchronously
        recipe_response = loop.run_until_complete(fetch_recipe())

        # Fetch calories asynchronously
        calories_response = loop.run_until_complete(fetch_calories())

        loop.close()

        return render_template('index.html', recipe_response=recipe_response, calories_response=calories_response)

    return render_template('index.html', recipe_response=None, calories_response=None)

