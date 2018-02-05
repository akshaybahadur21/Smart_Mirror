//node_helper.js

var NodeHelper = require("node_helper");
const ModuleNames = require('./ModuleNames.json')

module.exports = NodeHelper.create({
	// Subclass start method.
	start: function() {
		var self = this;
		var events = [];

		this.fetchers = [];

		console.log("Starting node helper for: " + this.name);

	    this.expressApp.get('/statement', function (req, res) {
	        text = req.query.text
	        self.sendSocketNotification("STATEMENT", {"text":text})
	        res.sendStatus(200);
	    });

	    this.expressApp.post('/image', function (req, res) {
	    	var data = "";
   			req.on('data', function(chunk){ data += chunk})
   			req.on('end', function(){
       			req.rawBody = data;
       			req.jsonBody = JSON.parse(data);
       			url = req.jsonBody.url
       			console.log(url)

	        	self.sendSocketNotification("IMAGE", {"imageurl":url})
	        	res.sendStatus(200);
   			})
	    });

	      this.expressApp.post('/video', function (req, res) {
	    	var data = "";
   			req.on('data', function(chunk){ data += chunk})
   			req.on('end', function(){
       			req.rawBody = data;
       			req.jsonBody = JSON.parse(data);
       			url = req.jsonBody.url
            channel = req.jsonBody.channel
            thumb = req.jsonBody.thumb.url                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              
            title = req.jsonBody.titles
       			console.log(url)
              console.log(thumb)
                
             
        

	        	self.sendSocketNotification("VIDEO", {"videourl":url, "videotitle":title, "chtitle":channel, "videothumb":thumb})
	        	res.sendStatus(200);
   			})
	    });

	   this.expressApp.post('/module', function (req, res) {
	    	var data = "";
   			req.on('data', function(chunk){ data += chunk})
   			req.on('end', function(){
       			req.rawBody = data;
       			req.jsonBody = JSON.parse(data);
       			url = req.jsonBody.url
            var sta = req.jsonBody.sta
       			var turnOn = false
          
            var open = "open ";
            console.log('turnOn = '+turnOn);
            if (sta == open)
              {
                  turnOn = true;
    //console.log(sta);
               }
          console.log(turnOn)
       	
           
       			moduleName = url
       			
       			console.log(moduleName)
       			  
                  if (moduleName in ModuleNames) {
                   moduleName = ModuleNames[moduleName]
                   console.log(moduleName)
               }
       			
       			self.sendSocketNotification("MODULE", {
          moduleName: moduleName,
          turnOn: turnOn
        });
	        	
	        	res.sendStatus(200);
   			})
	    });  


	    this.expressApp.post('/cab', function (req, res) {
	    	var data = "";
   			req.on('data', function(chunk){ data += chunk})
   			req.on('end', function(){
       			req.rawBody = data;
       			req.jsonBody = JSON.parse(data);
       			cabt = req.jsonBody.cabtype
       			ma = req.jsonBody.maxfare
       			mi = req.jsonBody.minfare
       			console.log(req.jsonBody)
	        	self.sendSocketNotification("CAB", req.jsonBody)
	        	res.sendStatus(200);
   			})
	    });  

        this.expressApp.post('/other', function (req, res) {
	    	var data = "";
   			req.on('data', function(chunk){ data += chunk})
   			req.on('end', function(){
       			req.rawBody = data;
       			req.jsonBody = JSON.parse(data);
       			
       			console.log(req.jsonBody)
	        	self.sendSocketNotification("OTHER", req.jsonBody)
	        	res.sendStatus(200);
   			})
	    });

	    this.expressApp.post('/zomato', function (req, res) {
	    	var data = "";
   			req.on('data', function(chunk){ data += chunk})
   			req.on('end', function(){
       			req.rawBody = data;
       			req.jsonBody = JSON.parse(data);
       			zomato = req.jsonBody
       			console.log(zomato)
       			
	        	self.sendSocketNotification("ZOMATO", req.jsonBody)
	        	res.sendStatus(200);
   			})
	    });

	    this.expressApp.post('/weather', function (req, res) {
	        var data = "";
   			req.on('data', function(chunk){ data += chunk})
   			req.on('end', function(){
       			req.rawBody = data;
       			req.jsonBody = JSON.parse(data);
	        	self.sendSocketNotification("WEATHER", req.jsonBody)
	        	res.sendStatus(200);
   			})
	    });

	    this.expressApp.get('/face', function (req, res) {
	        self.sendSocketNotification("FACE", {})
	        res.sendStatus(200);
	    });

	    this.expressApp.post('/holidays', function (req, res) {
	        var data = "";
   			req.on('data', function(chunk){ data += chunk})
   			req.on('end', function(){
       			req.rawBody = data;
       			req.jsonBody = JSON.parse(data);
       			holiday = req.jsonBody.holiday
	        	self.sendSocketNotification("HOLIDAYS", {"holiday": holiday})
	        	res.sendStatus(200);
   			})
	    });

	    this.expressApp.post('/news', function (req, res) {
	       var data = "";
   			req.on('data', function(chunk){ data += chunk})
   			req.on('end', function(){
       			req.rawBody = data;
       			req.jsonBody = JSON.parse(data);
       			articles = req.jsonBody.articles
	        	self.sendSocketNotification("NEWS", {"articles":articles})
	        	res.sendStatus(200);
   			})
	    });

	    this.expressApp.get('/clear', function (req, res) {
	        text = req.query.text
	        self.sendSocketNotification("CLEAR", {})
	        res.sendStatus(200);
	    });




	},

	// Subclass socketNotificationReceived received.
	socketNotificationReceived: function(notification, payload) {
		console.log("helper received: " + notification)
	}
})