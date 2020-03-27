from flask import Flask, jsonify, request
import mysql.connector
import re
import calcCarJourneyCost
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
        try:
            # accesses dictionary containing all journey types and executes related function
            return journeyTypeSwitcher(request.json["journeyType"])
        except:
            print("journeyType not recognised")
            return jsonify({"error": "journeyType not recognised"})
    else:
        print("not a journeyTask")
        return jsonify({"error": "taskType not recognised"})


def taskTypeSwitcher(taskType):
    # execute function in dictionary based on taskType given
    try:
        return taskTypeDictionary[taskType]()
    except:
        print("taskType not defined")


def journeyTypeSwitcher(journeyType):
    # execute function in dictionary based on journeyType given
    try:
        return journeyTypeDictionary[journeyType]()
    except:
        print("journeyType not defined")


def carJourneyHandler():
    # extract json request, calculate carbon cost and post to firestore
    try:
        userId, taskId, taskType, journeyType, origin, destination, distance = journeyTaskVariables(request)
        emissionsPerMile = float(request.json['emissionsPerMile'])
        passengers = request.json['passengers']
        carMake = request.json['carMake']
        carModel = request.json['carModel']
        carbonCost = calcCarJourneyCost(distance, emissionsPerMile, passengers)
        return jsonify({"received": "carJourney"})
    except:
        print("something went wrong")
        return jsonify({"error": "something went wrong"})

def bikeJourneyHandler():
    # extract json request, calculate carbon cost and post to firestore
    try:
        userId, taskId, taskType, journeyType, origin, destination, distance = journeyTaskVariables(request)

        if request.json["isElectric"] == "true":
            isElectric = True
        else:
            isElectric = False

        print("origin %s destination %s distance %s isElectric %s" % (origin, destination, distance, isElectric))
        carbonCost = calcBikeJourneyCost(distance, isElectric)
        return jsonify({"recieved": "bikeJourney"})
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
    origin = (float(regex.group(1)), float(regex.group(2)))

    destinationString = request.json["destination"]
    regex = re.search('.*\((.*),(.*)\)', destinationString)
    destination = (float(regex.group(1)), float(regex.group(2)))

    distance = float(request.json["distance"])

    return userId, taskId, taskType, journeyType, origin, destination, distance

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

