from flask import Flask, jsonify, request
import mysql.connector

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


@app.route("carbonCost", methods=['POST'])
def calculateCarbonCost():
    # calculate carbon cost of task, return json with carbonCost
    if request.json["taskType"] == "journeyTask":
        try:
            journeyTypeSwitcher(request.json["journeyType"])
        except:
            print("journeyType not recognised")
    else:
        print("not a journeyTask")







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
    print("carJourney")

def bikeJourneyHandler():
    print("bikeJourney")

def transitJourneyHandler():
    print("transitJourney")

def walkingJourneyHandler():
    print("walkingJourney")

taskTypeDictionary = {
    "journeyTask" : journeyTypeSwitcher
}

journeyTypeDictionary = {
    "carJourney": carJourneyHandler,
    "bikeJourney": bikeJourneyHandler,
    "transitJourney": transitJourneyHandler,
    "walkingJourney": walkingJourneyHandler
}


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port="5001")

