from flask import Flask, request, make_response
import mysql.connector


app = Flask(__name__)
