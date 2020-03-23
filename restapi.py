from flask import Flask, jsonify, request
import mysql.connector
import re

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
    sql = "SELECT model FROM carModels WHERE make = '%s'" % make
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    return jsonify({"models": [model[0] for model in myresult]})


@app.route("/carbonCost", methods=['POST'])
def calculateCarbonCost():
    # calculate carbon cost of task, return json with carbonCost
    if request.json["taskType"] == "journeyTask":
        try:
            # accesses dictionary containing all journey types and executes related function
            journeyTypeSwitcher(request.json["journeyType"])
        except:
            print("journeyType not recognised")
    else:
        print("not a journeyTask")
    # todo remove this return statement, each handler should have it's own return statement
    return jsonify({"test": "test"})


def taskTypeSwitcher(taskType):
    try:
        return taskTypeDictionary[taskType]()
    except:
        print("taskType not defined")


def journeyTypeSwitcher(journeyType):
    try:
        return journeyTypeDictionary[journeyType]()
    except:
        print("journeyType not defined")


def carJourneyHandler():
    try:
        origin = request.json["origin"]
        destination = request.json["destination"]
        distance = request.json["distance"]
        carMake = request.json["carMake"]
        carModel = request.json["carModel"]
        print("origin %s destination %s distance %s" % (origin, destination, distance))
        return jsonify({"recieved": "carJourney"})
    except:
        print("something went wrong")
        return jsonify({"error": "something went wrong"})

def bikeJourneyHandler():
    try:
        originString = request.json["origin"]  # 'lat/lng: (51.89987654029901,-8.459693938493727)'
        regex = re.search('.*\((.*),(.*)\)', originString)
        origin = (float(regex.group(1)), float(regex.group(2)))

        destinationString = request.json["destination"]
        regex = re.search('.*\((.*),(.*)\)', destinationString)
        destination = (float(regex.group(1)), float(regex.group(2)))

        distance = float(request.json["distance"])
        isElectric = request.json["isElectric"]

        print("origin %s destination %s distance %s" % (origin, destination, distance))
        return jsonify({"recieved": "carJourney"})
    except:
        print("something went wrong")
        return jsonify({"error": "something went wrong"})

def transitJourneyHandler():
    print("transitJourney")

def walkingJourneyHandler():
    print("walkingJourney")

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

