from flask import Blueprint, render_template, Flask, request, url_for, flash, send_from_directory, redirect, jsonify, make_response, session
from flask_wtf import FlaskForm
from flask_login import login_required, logout_user
from flask_session import Session
import base64, random
import json
from src import app
from src import log
from src import prepResponse
import paho.mqtt.client as mqttClient
import paho.mqtt.publish as mqttPublish


core_bp = Blueprint("core", __name__)

app.config["SESSION_COOKIE_NAME"] = "svCookie"
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

########################
#### RIO STUFF #########
########################

# RIO Answers
flags = [
    "TBD1",
    "TBD2"
]

## Configure RIO Tokens, not super secret, change range to 0 - # of flags
challengeTokens = [f"sVision{i}" for i in range(0, 2)] # creates ["sVision0, ... "sVision1']

## RIO Stuff - This function allows pushing completion directly to RIO so players don't have to copy/pasta the flags
def RioApi(PlayerId, challengeToken, flag):
    url = "https://ranges.io/api/v1/try-flag"
    jsonData = {
        "challenge_token":challengeToken, #Value passed from objective met 
        "player_token":PlayerId, #RIO Player token RIO_PLAYER_TOKEN
        "flag":flag #This is called 'answer' in RIO"
        }
    response = request.post(url, json=jsonData)
    # Log RioApi response text
    log_msg = f"RioApi response: {response.text}"
    app.logger.info(log_msg)
    return response.text

################
#### Routes ####
################

@login_required
def deleteBrokerClients(name): #Delete Player Broker Clients
    try:
        mqttPublish.single("$CONTROL/dynamic-security/v1","{\"commands\":[{\"command\": \"deleteClient\",\"username\": \""+name+"\"}]}",hostname="localhost",port=1883,auth={'username':"SantaBrokerAdmin", 'password':"8r0k3R4d1mp455wD"})
    except:
        pass
        

@login_required
def deleteBrokerRoleAcl(PlyrRole,PlyrTopic): #Delete Player Broker Role ACL from Player Topic
    try:
        mqttPublish.single("$CONTROL/dynamic-security/v1","{\"commands\":[{\"command\": \"removeRoleACL\",\"rolename\": \""+PlyrRole+"\",\"acltype\": \"subscribeLiteral\",\"topic\": \""+PlyrTopic+"\"}]}",hostname="localhost",port=1883,auth={'username':"SantaBrokerAdmin", 'password':"8r0k3R4d1mp455wD"})
    except:
        pass

@login_required
def deleteBrokerRole(PlyrRole): #Delete Player Broker Role
    try:
        mqttPublish.single("$CONTROL/dynamic-security/v1","{\"commands\":[{\"command\": \"deleteRole\",\"rolename\": \""+PlyrRole+"\"}]}",hostname="localhost",port=1883,auth={'username':"SantaBrokerAdmin", 'password':"8r0k3R4d1mp455wD"})        
    except:
        pass

def pubDefaultImgs(usr,pwd,tpc,imgs,pCid):
    try:
        mqttPublish.single(tpc, imgs, 0, True, hostname="localhost", port=1883, client_id=pCid, auth={'username':usr, 'password':pwd})
    except:
        print("PubFalied")
        
def pubSantaImgs(usr,pwd,tpc,imgs,pCid):
    try:
        mqttPublish.single(tpc, imgs, 0, True, hostname="localhost", port=1883, client_id=pCid, auth={'username':usr, 'password':pwd})
    except:
        print("PubFalied")
    
@core_bp.route("/auth", methods=["GET"])
@login_required
def home():
    ###############################################
    #### Check that RIO PLAYER TOKEN IS PRESENT####
    ###############################################
    session.clear
    if "RIO_PLAYER_TOKEN" in request.args:  # should get "RIO_PLAYER_TOKEN" from the game    
            RIO_PLAYER_TOKEN = request.args.get("RIO_PLAYER_TOKEN")
            if 'userid' not in session.keys(): #First time requesting /auth with submitted RIO_PLAYER_TOKEN value
                session["userid"] = RIO_PLAYER_TOKEN            
                playerClientId = RIO_PLAYER_TOKEN
                session["PlayerWomblyBrokerClientCreated"] = 0
                session["PlayerAlabasterBrokerClientCreated"] = 0
                session["PlayerBrokerClientCreated"] = 0
                session["PlayerWomblyFixed"] = 0
                session["PlayerAlabasterFixed"] = 0
                session["PlayerSantaImagesRestored"] = 0
                session["PlayerBrokerUserName"] =""
                session["PlayerBrokerUserPwd"] = ""
                session["PlayerBrokerClientId"] = ""
                session["PlayerBrokerTopic"] = ""
                session["PlayerBrokerImages"] = ""    
            else:
                playerClientId = session["userid"] #Set playerClientId to existing session userId value for setup check
    else:
        log.warning(
            f"   *** Whoever's watching log output, you should know someone came in without 'RIO_PLAYER_TOKEN'"
         )
        noTokenResp = prepResponse("core/no-token.html")
        return noTokenResp
        
    ################################    
    ####Setup Player environment####
    ################################        
    if (playerClientId == RIO_PLAYER_TOKEN): #Check that player hasn't tried refreshing the /auth page with a different RIO_PLAYER_TOKEN
        #Player Broker Client String
        plyrRandomPwdNum = (random.randint(1000000000,9999999999))
        plyrBrkrUsrNm = "Elf-"+playerClientId #Broker User Name for authenticated player
        plyrBrkrUsrPwd = "playerElfPass"+str(plyrRandomPwdNum) #Broker User Pwd for authenticated player
        plyrBrkrClientId = "Elf-ClientId-"+playerClientId #Player Broker ClientId for authenticated player
        createPlayer = "\"username\":\""+plyrBrkrUsrNm+"\",\"password\":\""+plyrBrkrUsrPwd+"\",\"clientid\":\""+plyrBrkrClientId+"\""
        playerAdminRole = "NorthPoleFeedsAdminRole-"+playerClientId
        playerElfRole = "NorthPoleFeedsElfRole-"+playerClientId
        playerBrokerTopic = "northpolefeeds-"+playerClientId 
        
        #WomblyC Broker Client String for publishing
        plyrWomblyBrkrUsrNm = "WomblyC-"+playerClientId #WomblyC Broker User Name for authenticated player
        plyrWomblyRandomPwdNum = (random.randint(1000000000,9999999999))
        plyrWomblyBrkrUsrPwd = "playerWomblyPass"+str(plyrWomblyRandomPwdNum) #Players should not see or receive this at anytime. Just requirement for creating client
        plyrWomblyBrkrClientId = "WomblyC-ClientId-"+playerClientId #WomblyC Broker ClientId for authenticated player
        createWombly = "\"username\":\""+plyrWomblyBrkrUsrNm+"\",\"password\":\""+plyrWomblyBrkrUsrPwd+"\",\"clientid\":\""+plyrWomblyBrkrClientId+"\""
        
        #AlabasterS Broker Client Strings for publishing
        plyrAlabasterBrkrUsrNm = "AlabasterS-"+playerClientId #AlabasterS Broker User Name for authenticated player
        plyrAlabasterRandomPwdNum = (random.randint(1000000000,9999999999))
        plyrAlabasterBrkrUsrPwd = "playerAlabasterPass"+str(plyrAlabasterRandomPwdNum) #Players should not see or receive this at anytime. Just requirement for creating client
        plyrAlabasterBrkrClientId = "AlabasterS-ClientId-"+playerClientId #AlabasterS Broker ClientId for authenticated player
        createAlabaster = "\"username\":\""+plyrAlabasterBrkrUsrNm+"\",\"password\":\""+plyrAlabasterBrkrUsrPwd+"\",\"clientid\":\""+plyrAlabasterBrkrClientId+"\""
        
        #Delete Existing if exist
        deleteBrokerClients(plyrBrkrUsrNm)
        deleteBrokerClients(plyrWomblyBrkrUsrNm)
        deleteBrokerClients(plyrAlabasterBrkrUsrNm)
        deleteBrokerRoleAcl(playerAdminRole,playerBrokerTopic)
        deleteBrokerRoleAcl(playerElfRole,playerBrokerTopic)
        deleteBrokerRole(playerAdminRole)
        deleteBrokerRole(playerElfRole)
        
        #Create Wombly, Alabaster, and Player Broker Clients for Player if not already present
        try: 

            CreatePlayerClients = [{'topic':"$CONTROL/dynamic-security/v1", 'payload':"{\"commands\": [{\"command\": \"listClients\"}]}"},("$CONTROL/dynamic-security/v1", "{\"commands\": [{\"command\": \"createRole\",\"rolename\":\""+playerAdminRole+"\"}]}", 0, False),("$CONTROL/dynamic-security/v1", "{\"commands\": [{\"command\": \"createRole\",\"rolename\":\""+playerElfRole+"\"}]}", 0, False),("$CONTROL/dynamic-security/v1", "{\"commands\": [{\"command\": \"createClient\","+createWombly+",\"roles\":[{\"rolename\":\""+playerAdminRole+"\",\"priority\":-1}]}]}", 0, False),("$CONTROL/dynamic-security/v1", "{\"commands\": [{\"command\": \"createClient\","+createAlabaster+",\"roles\":[{\"rolename\":\""+playerAdminRole+"\",\"priority\":-1}]}]}", 0, False),("$CONTROL/dynamic-security/v1", "{\"commands\": [{\"command\": \"createClient\","+createPlayer+",\"roles\":[{\"rolename\":\""+playerAdminRole+"\",\"priority\":-1},{\"rolename\":\"SiteStatusElfRole\",\"priority\":-1}]}]}", 0, False),("$CONTROL/dynamic-security/v1", "{\"commands\":[{\"command\": \"addRoleACL\",\"rolename\": \""+playerAdminRole+"\",\"acltype\": \"subscribeLiteral\",\"topic\": \""+playerBrokerTopic+"\",\"priority\": 5,\"allow\": true}]}", 0, False),("$CONTROL/dynamic-security/v1", "{\"commands\":[{\"command\": \"addRoleACL\",\"rolename\": \""+playerAdminRole+"\",\"acltype\": \"publishClientSend\",\"topic\": \""+playerBrokerTopic+"\",\"priority\": 5,\"allow\": true}]}", 0, False), ("$CONTROL/dynamic-security/v1", "{\"commands\":[{\"command\": \"addRoleACL\",\"rolename\": \""+playerAdminRole+"\",\"acltype\": \"publishClientReceive\",\"topic\": \""+playerBrokerTopic+"\",\"priority\": 5,\"allow\": true}]}", 0, False), ("$CONTROL/dynamic-security/v1", "{\"commands\":[{\"command\": \"addRoleACL\",\"rolename\": \""+playerElfRole+"\",\"acltype\": \"subscribeLiteral\",\"topic\": \""+playerBrokerTopic+"\",\"priority\": 5,\"allow\": true}]}", 0, False), ("$CONTROL/dynamic-security/v1", "{\"commands\":[{\"command\": \"addRoleACL\",\"rolename\": \""+playerElfRole+"\",\"acltype\": \"publishClientReceive\",\"topic\": \""+playerBrokerTopic+"\",\"priority\": 5,\"allow\": true}]}", 0, False), ("$CONTROL/dynamic-security/v1", "{\"commands\":[{\"command\": \"enableClient\",\"username\": \""+plyrBrkrUsrNm+"\"}]}", 0, False)]

            #Publish Messages to Broker to Create Player Broker Clients
            mqttPublish.multiple(CreatePlayerClients,hostname="localhost",port=1883,auth={'username':"SantaBrokerAdmin", 'password':"8r0k3R4d1mp455wD"})
            
            #Set session flags for this part of the challenge
            session["PlayerWomblyBrokerClientCreated"] = 1
            session["PlayerAlabasterBrokerClientCreated"] = 1
            session["PlayerBrokerClientCreated"] = 1
            session["PlayerWomblyBrokerUserName"] = plyrWomblyBrkrUsrNm
            session["PlayerAlabasterBrokerUserName"] = plyrAlabasterBrkrUsrNm
            session["PlayerBrokerUserName"] = plyrBrkrUsrNm
            session["PlayerBrokerUserPwd"] = plyrBrkrUsrPwd
            session["PlayerBrokerClientId"] = plyrBrkrClientId
            session["PlayerAdminRole"] = playerAdminRole
            session["PlayerBrokerTopic"] = playerBrokerTopic
            session["PlayerElfRole"] = playerElfRole
            plyrImgs = "./static/images/monitor1.png,./static/images/monitor2.png,./static/images/monitor3.png,./static/images/monitor4.png,./static/images/monitor5.png,./static/images/monitor6.png,./static/images/monitor7.png,./static/images/monitor8.png"
            session["PlayerBrokerImages"] = plyrImgs
            
            #Return the monitor page   
            challengeHome = prepResponse("core/index.html")
            challengeHome.headers["BrkrTopic"] = "northpolefeeds"
            challengeHome.headers["BrkrUser"] = "Elf"
            challengeHome.headers["BrkrPswd"] = plyrBrkrUsrPwd    
            return challengeHome
        except:
            pass
    else:
        invalidResponse = prepResponse("core/invalid-token.html")
        return invalidResponse

@core_bp.route("/static/js/mqttJS.js", methods=["GET"])
@login_required
def mqttJS(): 
    return send_from_directory("static", "js/mqttJS.js", mimetype="text/javascript", as_attachment=False)

@core_bp.route("/mqtt", methods=["GET"])
@login_required
def playerMqttConnect(): #The true purpose of this route is to get the players default images published to the broker when they subscribe to 'northpolefeeds'
    usr = session["PlayerBrokerUserName"]
    pwd = session["PlayerBrokerUserPwd"]
    tpc = session["PlayerBrokerTopic"]
    imgs = session["PlayerBrokerImages"]
    pCid = session["PlayerBrokerClientId"]
    pubDefaultImgs(usr,pwd,tpc,imgs,pCid)
    Connected = "Connected"
    return make_response(jsonify(connect=Connected), 200)

#TEMPORARY ROUTE/FUNCTION FOR GETTING SANTA IMAGES.     
@core_bp.route("/getSantaImages", methods=["GET"])
@login_required
def getSantaImages(): #The true purpose of this route is to get Santa images published to the broker
    plyrImgs = "./static/images/santa1.png,./static/images/santa2.png,./static/images/santa3.png,./static/images/santa4.png"
    session["PlayerBrokerImages"] = plyrImgs
    usr = session["PlayerBrokerUserName"]
    pwd = session["PlayerBrokerUserPwd"]
    tpc = session["PlayerBrokerTopic"]
    imgs = session["PlayerBrokerImages"]
    pCid = session["PlayerBrokerClientId"]
    pubSantaImgs(usr,pwd,tpc,imgs,pCid)
    SI = "Santa's Images Published"
    return make_response(jsonify(gsi=SI), 200)

@core_bp.route("/listClients", methods=["GET"])
@login_required
def listClients():
    clientsForPlayerReview = "'elfanon', 'Elf', 'WomblyC', 'AlabasterS'"
    return make_response(jsonify(clients=clientsForPlayerReview), 200)
    
@core_bp.route("/listRoles", methods=["GET"])
@login_required
def listRoles():
    rolesForPlayerReview = "'SiteStatusElfRole', 'NorthPoleFeedsAdminRole', 'NorthPoleFeedsElfRole'"
    return make_response(jsonify(roles=rolesForPlayerReview), 200)

@core_bp.route("/brokerFeed", methods=["GET"])
@login_required   
def brokerFeed():
    brokerFeedPage = prepResponse("core/brokerFeed.html")
    return brokerFeedPage

@core_bp.route("/logout")
@login_required
def logout():
    #Delete Existing if exist
    deleteBrokerClients(session["PlayerBrokerUserName"])
    deleteBrokerClients(session["PlayerWomblyBrokerUserName"])
    deleteBrokerClients(session["PlayerAlabasterBrokerUserName"])
    deleteBrokerRoleAcl(session["PlayerAdminRole"],session["PlayerBrokerTopic"])
    deleteBrokerRoleAcl(session["PlayerElfRole"],session["PlayerBrokerTopic"])
    deleteBrokerRole(session["PlayerAdminRole"])
    deleteBrokerRole(session["PlayerElfRole"])
    logout_user()
    flash("You were logged out.", "success")
    redirURL = url_for('accounts.login')
    if "RIO_PLAYER_TOKEN" in request.args:
        redirURL = redirURL + "?RIO_PLAYER_TOKEN=" + request.args.get("RIO_PLAYER_TOKEN")
    logoutResp = make_response(redirect(redirURL))
    logoutResp.delete_cookie("svCookie")
    return logoutResp
