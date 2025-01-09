var connected_flag = 0
var mqtt;
var reconnectTimeout = 7000;
var stopic = "none";
var currentTopic = "none";
var currentMonitor = 1;
var currentImgMon = 1;
var currentImages = "";
var randImg = 1;
var prevImage = 0;
var imgIntv;
var playerAppend = "-" + parent.window.location.search.split('RIO_PLAYER_TOKEN=')[1];

function onConnectionLost() {
	console.log("connection lost");
	document.getElementById("status").innerHTML = "Broadcast connections lost. Turning off monitors.";
	document.getElementById("messages").innerHTML = "Broadcast connections lost. Turning off monitors.";
	connected_flag = 0;
	currentMonitor = 1;
	currentImages = "";
	clearInterval(imgIntv);
	imgIntv = "";
	stopic = "";
	currentTopic = "none";
	currentMonitor = 1;
	document.getElementById("status").innerHTML = "Monitors off.";
	document.getElementById("messages").innerHTML = "";
	document.getElementById("connectas").value = "";
	document.getElementById("password").value = "";
	document.getElementById("camfeed").value = "";
	document.getElementById("camport").value = "";
	document.getElementById("cambank").value = "";
	connected_flag = 0
	for (let mImg = 1; mImg < 5; mImg++) {
		rImg = "img" + mImg;
		document.getElementById(rImg).setAttribute("src", "/static/images/monitoroff.png")
	}
}

function onFailure(message) {
	console.log("Failed");
	document.getElementById("messages").innerHTML = "Connection Failed";
	document.getElementById("messages").innerHTML = "Connection Failed";
	// setTimeout(MQTTconnect, reconnectTimeout);
}

function onMessageArrived(r_message) {
	var newImg = r_message.payloadString;
	var camBank = r_message.destinationName;
	if (camBank == currentTopic) {
		var out_msg = "Receiving current broadcast for 'northpolefeeds'.....";
		console.log(out_msg);
		document.getElementById("messages").innerHTML = out_msg;
		document.getElementById("status").innerHTML = "Monitors on.<br>Currently viewing the <i>northpolefeeds</i> broadcast";
		var monitorImg = "img" + currentMonitor;
		try {
			if (newImg.includes(".png")) {
				document.getElementById("messages").innerHTML = out_msg;
				currentImages = newImg
				imgIntv = setInterval(ImgLoop, 2000)
			} else {
				document.getElementById(monitorImg).setAttribute("src", "/static/images/noimage.png")
				out_msg = out_msg + "<br>Site status: " + newImg;
				document.getElementById("messages").innerHTML = out_msg;
			}
		} catch (error) {
			document.getElementById(monitorImg).setAttribute("src", "/static/images/noimage.png")
			out_msg = out_msg + "<br>No info.";
			document.getElementById("messages").innerHTML = out_msg;
		}
		currentMonitor = currentMonitor + 1;
		if (currentMonitor > 4) {
			currentMonitor = 1
		}
	}
}

function onConnected(recon, url) {
	console.log(" in onConnected " + reconn);
}

function onConnect() {
	document.getElementById("messages").innerHTML = "Monitors on. Connect to broadcast feed.";
	connected_flag = 1;
	document.getElementById("status").innerHTML = "Monitors on.";
	console.log("on Connect " + connected_flag);
	for (let mImg = 1; mImg < 5; mImg++) {
		rImg = "img" + mImg;
		document.getElementById(rImg).setAttribute("src", "/static/images/nofeed.png");
	}
}

function MQTTconnect() {
	document.getElementById("messages").innerHTML = "";
	var host = document.forms["connform"]["server"].value;
	var port = parseInt(document.forms["connform"]["port"].value); //9001
	var user = document.forms["connform"]["username"].value;
	user = user + playerAppend;
	var pass = document.forms["connform"]["pwd"].value;
	if (host == "" || port == "" || user == "" || pass == "") {
		document.getElementById("messages").innerHTML = "Please provide missing values.";
		return false;
	} else {
		const connectResponse = fetch("/mqtt");
		var svclientId = "Elf-ClientId" + playerAppend;
		console.log("connecting to " + host + " " + port);
		mqtt = new Paho.MQTT.Client(host, port, svclientId);
		var options = {
			invocationContext: { host: host, port: port, clientId: svclientId },
			userName: user,
			password: pass,
			timeout: 10,
			keepAliveInterval: 30,
			onSuccess: onConnect,
			onFailure: onFailure
		};
		mqtt.onConnectionLost = onConnectionLost;
		mqtt.onMessageArrived = onMessageArrived;
		mqtt.connect(options);
		return false;
	}
}

function sub_topics() {
	document.getElementById("messages").innerHTML = "";
	if (connected_flag == 0) {
		out_msg = "<b>Power on monitors first!</b>"
		console.log(out_msg);
		document.getElementById("messages").innerHTML = out_msg;
		return false;
	}
	var stopic = document.forms["subs"]["Stopic"].value;
	if (stopic == "") {
		document.getElementById("messages").innerHTML = "Please provide a broadcast feed."
		return false;
	} else {
		console.log("Unsubscribing to topic 'northpolefeeds'");
		mqtt.unsubscribe(currentTopic);
		clearInterval(imgIntv);
		document.getElementById("status").innerHTML = "Monitors on.";
		for (let mImg = 1; mImg < 5; mImg++) {
			rImg = "img" + mImg;
			document.getElementById(rImg).setAttribute("src", "/static/images/nofeed.png")
		}
		console.log("Subscribing to topic =" + stopic);
		stopic = stopic + playerAppend;
		mqtt.subscribe(stopic);
		currentTopic = stopic;
		currentMonitor = 1;
		return false;
	}
}

async function listClients() {
	const lcResponse = await fetch("/listClients");
	const dataLC = await lcResponse.json();
	document.getElementById("messages").innerHTML = "Available clients: " + dataLC.clients
}

async function listRoles() {
	const lrResponse = await fetch("/listRoles");
	const dataLR = await lrResponse.json();
	document.getElementById("messages").innerHTML = "Available roles: " + dataLR.roles
}

async function tempGetSantaImgs() {
	const gsiResponse = await fetch("/getSantaImages");
	const dataGSI = await gsiResponse.json();
	document.getElementById("messages").innerHTML = "Santa's images have been published. Reconnect/subscribe to view."
}

function powerOff() {
	mqtt.unsubscribe(currentTopic);
	mqtt.disconnect();
	for (let mImg = 1; mImg < 5; mImg++) {
		rImg = "img" + mImg
		document.getElementById(rImg).setAttribute("src", "/static/images/monitoroff.png")
	}
	stopic = "";
	currentTopic = "none";
	currentMonitor = 1;
	document.getElementById("status").innerHTML = "Monitors off.";
	document.getElementById("messages").innerHTML = "";
	document.getElementById("connectas").value = "";
	document.getElementById("password").value = "";
	document.getElementById("camfeed").value = "";
	document.getElementById("camport").value = "";
	document.getElementById("cambank").value = "";
	connected_flag = 0
}

function ImgLoop() {
	randImg = Math.floor(Math.random() * 8);
	if (randImg != prevImage) {
		newImage = currentImages.split(",");
		setMon = "img" + currentImgMon;
		document.getElementById(setMon).setAttribute("src", newImage[randImg]);
		currentImgMon = currentImgMon + 1;
		prevImage = randImg;
		if (currentImgMon > 4) {
			currentImgMon = 1;
		}
	}
}

//TBD HOW/WHEN TO USE/INCORPORATE INTO CHALLENGE
//function send_message(){
//	document.getElementById("messages").innerHTML ="";
//	if (connected_flag==0){
//	out_msg="<b>Not Connected so can't send</b>"
//	console.log(out_msg);
//	document.getElementById("messages").innerHTML = out_msg;
//	return false;
//	}
//	var msg = document.forms["smessage"]["message"].value;
//	console.log(msg);

//	var topic = document.forms["smessage"]["Ptopic"].value;
//	message = new Paho.MQTT.Message(msg);
//	if (topic=="")
//		message.destinationName = "test-topic"
//	else
//		message.destinationName = topic;
//	mqtt.send(message);
//	return false;
//}