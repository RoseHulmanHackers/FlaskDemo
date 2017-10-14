from flask import Flask, request, jsonify
import os
import pyrebase

app = Flask(__name__)
config = {
  "apiKey": "apiKey",
  "authDomain": "projectID.firebaseapp.com",
  "databaseURL": 'https://projectID.firebaseio.com',
  "storageBucket": "projectID.appspot.com"
}

firebase = pyrebase.initialize_app(config)

@app.route('/')
def main():
    return 'Hello, world!'

@app.route('/addMovie', methods=['POST'])
def addMovie():
    name = request.headers['name']
    year = request.headers['year']
    rating = request.headers['rating']
    data = {
        'name': name,
        'year': year,
        'rating': rating
    }
    db = firebase.database()
    db.child('movies').child(name).update(data)
    response = jsonify(data)
    response.status_code = 201
    return response

@app.route('/getMovies', methods=['GET'])
def getMovies():
    db = firebase.database()
    resp = db.child('movies').get().val()
    return jsonify(resp)

@app.route('/search', methods=['GET'])
def search():
    name = request.headers['name']
    db = firebase.database()
    data = None
    for movie in db.child('movies').get().each():
        if movie.val()['name'] == name:
            data = movie.val()
            print(data)
    if data == None:
        return "This movie could not be found"
    return jsonify(data)

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0',port=port)