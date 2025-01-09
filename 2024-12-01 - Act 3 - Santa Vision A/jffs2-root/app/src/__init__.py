from decouple import config
from flask import Flask, render_template, make_response, session
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
import sys, json, time, random, base64, threading
import paho.mqtt.client as mqtt
from jsonschema import validate
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
import logging

log = logging.getLogger(__name__)
log.setLevel(logging.INFO)

app = Flask(__name__)
app.config.from_object(config("APP_SETTINGS"))
    
#################################
#### Standard Response Headers ##
#################################
def prepResponse(Resp):    
    response = make_response(render_template(Resp), 200)
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    response.headers["Cache-Control"] = "public, max-age=0"
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "SAMEORIGIN"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    return response

########################
#### MQTT Client #######
########################

# Create client for sitestatus topic
client = mqtt.Client()
#client.username_pw_set({BROKERUSER}, {BROKERPASSWORD})

# On connect to MQTT server subscribe to {TOPIC}
#def on_connect(client, userdata, flags, rc):
    #client.subscribe({TOPIC})

# Start MQTT client
client.on_connect = on_connect
client.connect_async("localhost", 1883, 120)
client.loop_start()
clientstarted = 1 #Set to permit odd, unresolved issues with docker-compose build process

########################
#### DB and APP setup ##
########################

login_manager = LoginManager()
login_manager.init_app(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Registering blueprints
from src.accounts.views import accounts_bp
from src.core.views import core_bp

app.register_blueprint(accounts_bp)
app.register_blueprint(core_bp)

from src.accounts.models import User

login_manager.login_view = "accounts.login"
login_manager.login_message_category = "danger"

@login_manager.user_loader
def load_user(user_id):
    return User.query.filter(User.id == int(user_id)).first()

########################
#### error handlers ####
########################

@app.errorhandler(401)
def unauthorized_page(error):
    return render_template("errors/401.html"), 401


@app.errorhandler(404)
def page_not_found(error):
    return render_template("errors/404.html"), 404


@app.errorhandler(500)
def server_error_page(error):
    return render_template("errors/500.html"), 500

#########################################
#### Schedule Publish sitestatus Items ##
#########################################

def appPub():        
    Msgs = ["MSG1", "MSG2", "MSG3", "MSG4", "MSG5", "MSG6"]
    randSiteStatus = (random.randint(0,5))
    #client.publish({TOPIC}, Msgs[randSiteStatus])

if clientstarted == 1:
    scheduler = BackgroundScheduler()
    scheduler.add_job(appPub, 'interval', seconds=5)
    scheduler.start()