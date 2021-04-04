import json
import boto3
# from usda import UsdaClient
# import noms
# import requests
# from requests.auth import HTTPBasicAuth
# from flask_cors import CORS
import urllib3

http = urllib3.PoolManager()
API_KEY="e9cl5VngIZPJ3rlP0TjbPfSNatfdGzsxHreADbFR"
NUTRIENTS_NUMBER_LIST = ["203", "204", "205", "606", "269",
"306", "291", "303", "307", "301", "601", "208", "328", "618"]

def recognizeImage():
    client = boto3.client("rekognition")
    s3 = boto3.client("s3")
    response = client.detect_labels(Image = {"S3Object": {"Bucket": "recognize13339-dev", "Name": "public/userUpload.png"}}, MaxLabels=5, MinConfidence=70)
    return response


def nutrientHelper():
    recognizedFoodList=[]
    try:
        imageResult = recognizeImage()
        for i in imageResult["Labels"]:
            nutrientList = []
            recognizedFood ={}
            if i["Name"] == "Food":
                continue
            foodName = i["Name"]
            if('Burger' in foodName):
                url = "https://api.nal.usda.gov/fdc/v1/foods/search?"+ "api_key="+API_KEY+'&query="'+foodName+'" mcdonald'
            else:
                url = "https://api.nal.usda.gov/fdc/v1/foods/search?"+ "api_key="+API_KEY+'&query="'+foodName+'"'
            print(url)
            responseBody = http.request('GET', url)
            response = json.loads(responseBody.data)
            # print(response)
            food = response['foods'][0]
            recognizedFood['description'] = food['description']

            for nutrient in food['foodNutrients']:
                foodNutrients={}
                if nutrient['nutrientNumber'] not in NUTRIENTS_NUMBER_LIST:
                    continue
                elif nutrient['nutrientNumber'] == "618":
                    foodNutrients['nutrientName'] = "Trans Fat"
                elif nutrient['nutrientNumber'] == "208":
                    foodNutrients['nutrientName'] = "Calories"
                else:
                    foodNutrients['nutrientName'] = nutrient['nutrientName']
                foodNutrients['value'] = nutrient['value']
                foodNutrients['unitName'] = nutrient['unitName']
                nutrientList.append(foodNutrients)

            recognizedFood['foodNutrients'] = nutrientList
            recognizedFoodList.append(recognizedFood)

        return recognizedFoodList

    except Exception as e:
        return ("error: {}", e)

def handler(event, context):
    responseObject = nutrientHelper()
    return {
        'statusCode': 200,
        'body': json.dumps(responseObject),
        'headers': {
            'Content-Type' : 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Credentials': True,
            'Access-Control-Allow-Headers' : '*'
        }
    }



# if __name__ == "__main__":
#     print('testing')
#     # response = handler("null", "null")
#     # responseBody = json.loads(response['body'])
#     # foodName = responseBody['Labels'][0]['Name']
#     # foodName = "coffee"
#     responseObject = nutrientHelper()
#     # print(responseObject)
#     print(json.dumps(responseObject, indent=4, sort_keys=True))
#     print(len(responseObject))
#     # print(json.dumps(responseObject))
