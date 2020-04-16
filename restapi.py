from flask import Flask, jsonify, request
import mysql.connector
import re
import firebase_admin
import requests
from firebase_admin import credentials
from firebase_admin import firestore
from calcCarJourneyCost import calcCarJourneyCost
from calcBikeJourneyCost import calcBikeJourneyCost

app = Flask(__name__)

mydb = mysql.connector.connect(
    host="mysql.netsoc.co",
    user="olanmccarthy",
    passwd="asdf",
    database="olanmccarthy_test"
)
mycursor = mydb.cursor()

cred = credentials.Certificate('final-year-project-35cae-firebase-adminsdk-v5e77-c6b170ddd6.json')
firebase_admin.initialize_app(cred)

db = firestore.client()


@app.route("/test", methods=['GET'])
def hello():
    return jsonify({"about": "Hello World!"})


@app.route("/car_makes", methods=['GET'])
def carMakes():
    # return json of all car makes
    mycursor.execute("SELECT * FROM carMakes")
    myresult = mycursor.fetchall()
    return jsonify({"makes": [make[0] for make in myresult]})


@app.route("/car_models/<string:make>", methods=['GET'])
def carModels(make):
    # return json of all car models of a certain make
    sql = "SELECT model, id FROM cars WHERE make = '%s'" % make
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    return jsonify({"models": [{"id": model[1], "model": model[0]} for model in myresult]})


@app.route("/carbonCost", methods=['POST'])
def calculateCarbonCost():
    # calculate carbon cost of task, return json with carbonCost
    if request.json["taskType"] == "journeyTask":
        return journeyTypeSwitcher(request.json["journeyType"])

    else:
        print("not a journeyTask")
        return jsonify({"error": "taskType not recognised"})


def taskTypeSwitcher(taskType):
    # execute function in dictionary based on taskType given
    return taskTypeDictionary[taskType]()



def journeyTypeSwitcher(journeyType):
    # execute function in dictionary based on journeyType given
    return journeyTypeDictionary[journeyType]()



def carJourneyHandler():
    # extract json request, calculate carbon cost and post to firestore
    try:
        userId, taskId, taskType, journeyType, origin, destination, distance = journeyTaskVariables(request)
        carId = request.json['carId']
        passengers = int(request.json['passengers'])
        carMake = request.json['carMake']
        carModel = request.json['carModel']

        sql = "SELECT emissionsPerMile FROM cars WHERE id = '%s'" % carId
        mycursor.execute(sql)
        myresult = mycursor.fetchone()
        emissionsPerMile = myresult[0]

        carbonCost = calcCarJourneyCost(distance, emissionsPerMile, passengers)

        data = {
            "journeyType": journeyType,
            "taskType": taskType,
            "userId": userId,
            "taskId": taskId,
            "carId": carId,
            "origin": origin,
            "destination": destination,
            "distance": distance,
            "passengers": passengers,
            "carMake": carMake,
            "carModel": carModel,
            "carbonCost": carbonCost
        }

        db.collection(u'users').document(userId).collection('currentPlan').document(taskId).set(data)
        data["origin"] = (data["origin"].latitude, data['origin'].longitude)
        data["destination"] = (data["destination"].latitude, data['destination'].longitude)

        return jsonify(data)
    except:
        print("something went wrong")
        return jsonify({"ERROR": "Something went wrong"})

def bikeJourneyHandler():
    # extract json request, calculate carbon cost and post to firestore
    try:
        userId, taskId, taskType, journeyType, origin, destination, distance = journeyTaskVariables(request)

        if request.json["isElectric"] == "true":
            isElectric = True
        else:
            isElectric = False

        carbonCost = calcBikeJourneyCost(distance, isElectric)

        data = {
            "journeyType": journeyType,
            "taskType": taskType,
            "userId": userId,
            "taskId": taskId,
            "origin": origin,
            "destination": destination,
            "distance": distance,
            "isElectric": isElectric,
            "carbonCost": carbonCost
        }

        db.collection(u'users').document(userId).collection('currentPlan').document(taskId).set(data)
        data["origin"] = (data["origin"].latitude, data['origin'].longitude)
        data["destination"] = (data["destination"].latitude, data['destination'].longitude)

        return jsonify(data)
    except:
        print("something went wrong")
        return jsonify({"error": "something went wrong"})

def transitJourneyHandler():
    print("transitJourney")

def walkingJourneyHandler():
    print("walkingJourney")


def journeyTaskVariables(request):
    # get variables common to all journey tasks from json request
    userId = request.json["userId"]
    taskType = request.json["taskType"]
    journeyType = request.json["journeyType"]
    taskId = request.json["taskId"]

    originString = request.json["origin"]
    regex = re.search('.*\((.*),(.*)\)', originString)
    origin = firestore.GeoPoint(float(regex.group(1)), float(regex.group(2)))

    destinationString = request.json["destination"]
    regex = re.search('.*\((.*),(.*)\)', destinationString)
    destination = firestore.GeoPoint(float(regex.group(1)), float(regex.group(2)))

    distance = float(request.json["distance"])

    return userId, taskId, taskType, journeyType, origin, destination, distance

def addToCurrentPlan(userId, task):
    # add plan with carbon cost to firebase
    return

taskTypeDictionary = {
    "journeyTask": journeyTypeSwitcher
}

# dict key is a journey type, value is a function to handle that type
journeyTypeDictionary = {
    "carJourney": carJourneyHandler,
    "bikeJourney": bikeJourneyHandler,
    "transitJourney": transitJourneyHandler,
    "walkingJourney": walkingJourneyHandler
}

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5001)

