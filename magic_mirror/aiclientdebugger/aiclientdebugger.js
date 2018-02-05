//aiclientdebugger.js

Module.register("aiclientdebugger",{

	// Default module config.
	defaults: {
		animationSpeed: 0.2 * 1000
	},

	// Define required translations.
	getTranslations: function() {
		// The translations for the defaut modules are defined in the core translation files.
		// Therefor we can just return false. Otherwise we should have returned a dictionairy.
		// If you're trying to build your own module including translations, check out the documentation.
		return false;
	},

	// Define start sequence.
	start: function() {
		Log.log("Starting module: " + this.name);

		this.sendSocketNotification("INITIALIZE", {})
		
	},

	// Override dom generator.
	getDom: function() {
		var wrapper = document.createElement("div");
		wrapper.innerHTML = "<ul><li><img src=\"" + this.file("yout.png") + "\" style=\"width:4.3%;height:4.3%;margin-right:21px;\"></li><li><img src=\"" + this.file("zomato.png") + "\" style=\"width:4%;height:4%;margin-right:19px;margin-top:24px;\"></li><li><img src=\"" + this.file("maps.png") + "\" style=\"width:5%;height:5%;margin-right:12px;margin-top:18px;\"></li><li><img src=\"" + this.file("ube.png") + "\" style=\"width:8%;height:8%;margin-right:-9px;\"></li></ul>";
		var listen = document.createElement("div");
		if (this.microphoneEnabled) {
			listen.innerHTML = "<img src=\"" + this.file("siri.gif") + "\" style=\"width:10%;height:10%;margin-bottom:-50px;\"><p style=\"margin-right:32px;margin-bottom:-85px;\">Listening</p>";
			
			listen.className = "small bright";
			wrapper.append(listen)
		}
		return wrapper
	},

	// Override socket notification handler.
	socketNotificationReceived: function(notification, payload) {
		console.log("module received: " + notification)
		var self = this

		if (notification == "MICROPHONE"){
			this.microphoneEnabled = payload.enabled
			this.updateDom(this.config.animationSpeed);
		}
	}
});
