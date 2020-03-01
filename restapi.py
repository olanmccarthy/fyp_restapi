from flask import Flask, jsonify
import mysql.connector
app = Flask(__name__)

mydb = mysql.connector.connect(
    host = "localhost",
    user = "olan",
    passwd = "Ibanez260sql!",
    database = "test"
)
mycursor = mydb.cursor()
#test push

@app.route("/test")
def hello():
   return jsonify({"about": "Hello World!"})

@app.route("/car_makes")
def carMakes():
    mycursor.execute("SELECT * FROM carMakes")
    myresult = mycursor.fetchall()
    return jsonify({"Car Makes": [make[0] for make in myresult]})

@app.route("/car_models/<string:make>")
def carModels(make):
    sql = "SELECT model FROM carModels WHERE make = '%s'" % make
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    return jsonify({"Car Model": [model[0] for model in myresult]})

if __name__ == "__main__":
    app.run(debug=True)
