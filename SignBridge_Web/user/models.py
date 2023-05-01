from flask import  jsonify, redirect, request, session
from passlib.hash import pbkdf2_sha256
import uuid
import pymongo

client = pymongo.MongoClient("localhost", 27017)
db = client.user_login_system

class User:
    def start_session(self, user):
        del user['password']
        session['logged_in'] = True
        session['user'] = user
        return jsonify(user), 200


    def signup(self):

        user = {
            "_id" : uuid.uuid4().hex,
            "name" : request.form.get('name'),
            "email" : request.form.get('email'),
            "password" : request.form.get('password'),
        }

        if db.users.find_one({"email" : user["email"]}):
            return jsonify({"error" : "Email already exists"}), 400

        user["password"] = pbkdf2_sha256.encrypt(user["password"])

        if db.users.insert_one(user):
            return self.start_session(user)

        return jsonify({"error" : "Signup failed"}), 400

    def signout(self):
        session.clear()
        return redirect('/')

    def login(self):
        user = db.users.find_one({
            "email" : request.form.get('email')
        })

        if user:
            if pbkdf2_sha256.verify(request.form.get("password"), user["password"]):
                return self.start_session(user)
            else:
                return jsonify({"error" : "Invalid credentials"}), 401
        else:
            return jsonify({"error" : "Unknown email address"}), 404
        # return redirect('/home')
