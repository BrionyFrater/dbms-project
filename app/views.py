from flask import render_template, request, make_response
from app import app
import mysql.connector

@app.route('/', methods=['GET'])
def hello_world():
    return "Hello World👋"

