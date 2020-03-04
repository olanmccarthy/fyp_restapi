from flask import Flask, jsonify
import mysql.connector
app = Flask(__name__)

mydb = mysql.connector.connect(
    host = "mysql.netsoc.co",
    user = "olanmccarthy",
    passwd = "asdf",
    database = "olanmccarthy_test"
)
mycursor = mydb.cursor()

#testing git pulls

@app.route("/test")
def hello():
   return jsonify({"about": "Hello World!"})

@app.route("/car_makes")
def carMakes():
    mycursor.execute("SELECT * FROM carMakes")
    myresult = mycursor.fetchall()
    return jsonify({"makes": [make[0] for make in myresult]})

@app.route("/car_models/<string:make>")
def carModels(make):
    sql = "SELECT model FROM carModels WHERE make = '%s'" % make
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    return jsonify({"models": [model[0] for model in myresult]})

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port="5001")
