//aiclient.js

Module.register("aiclient",{

	// Default module config.
	defaults: {
		animationSpeed: 0.5 * 1000,
		iconTable: {
			"clear-day": "wi-day-sunny",
			"partly-cloudy-day": "wi-day-cloudy",
			"cloudy": "wi-cloudy",
			"wind": "wi-cloudy-windy",
			"rain": "wi-rain",
			"thunderstorm": "wi-thunderstorm",
			"snow": "wi-snow",
			"fog": "wi-fog",
			"clear-night": "wi-night-clear",
			"partly-cloudy-night": "wi-night-cloudy",
			"hail": "wi-rain",
			"tornado": "wi-rain"
		}
	},

	// Define required translations.
	getTranslations: function() {
		// The translations for the defaut modules are defined in the core translation files.
		// Therefor we can just return false. Otherwise we should have returned a dictionairy.
		// If you're trying to build your own module including translations, check out the documentation.
		return false;
	},

	getScripts: function() {
		return ["js/jquery.js"];
	},

	// Define required scripts.
	getStyles: function() {
		return ["weather-icons.css", "currentweather.css"];
	},

	// Define start sequence.
	start: function() {
		Log.log("Starting module: " + this.name);

		this.sendSocketNotification("INITIALIZE", {})
		
	},

	// Override dom generator.
	getDom: function() {
		var wrapper = document.createElement("div");
		/*wrapper.className = "contain";*/
		switch(this.current_selection) {
			case "STATEMENT":
				wrapper.innerHTML = this.text;
				wrapper.className = "medium bright";
				break
			case "IMAGE":
				wrapper.innerHTML = "<img src=\"" + this.imageURL + "\" style=\"border:1px solid black;max-width:100%;\">"
				break

			case "OTHER":
              if (this.other.title) {
			
			var title = document.createElement('div')
				title.innerHTML = this.other.command;
				title.className = "medium bright";
				title.style.marginTop = "-292px";
				title.style.marginLeft = "425px";
				title.style.position = "absolute";
           
                 
				wrapper.appendChild(title)
				

				var keys = ["title", "subtitle", "details", "url"],
    j, k;
var con = document.createElement("div")
con.className = "con";
for (j = 0; j < this.other[keys[0]].length; j++) {
var td = document.createElement("div")
td.className = "hotel";
 var info = document.createElement("div")
         info.className = "subs";
		 var info1 = document.createElement("div")
		 info1.className = "subtitle";
         
		  var img = document.createElement("div")
         img.className = "mainimage";
		  var det = document.createElement("div")
         det.className = "det";
   
    for (k = 0; k < keys.length; k++) {
         if (keys[k] === 'url'){
		 img.innerHTML = '<img src="' + this.other[keys[k]][j] + '"></div>';
		 td.appendChild(img);
		 }
		  if (keys[k] === 'title'){
		 info.innerHTML = '<h1>' + this.other[keys[k]][j] + '</h1>';
		 td.appendChild(info);
		  }
		  if (keys[k] === 'subtitle'){
		 info1.innerHTML = '<h2>' + this.other[keys[k]][j] + '</h2>';
		 td.appendChild(info1);
		  }
		  
		   if (keys[k] === 'details'){
		 det.innerHTML = '<p>' + this.other[keys[k]][j] + '</p>';
		 td.appendChild(det);
		  }
	
		con.appendChild(td);	
    }
	
}
wrapper.appendChild(con);	
			
}
			else{
				console.log(this.other)
				var title = document.createElement('div')
				title.innerHTML = this.other;
				title.className = "medium bright";
				title.style.marginTop = "50px";
				title.style.marginLeft = "155px";
				wrapper.appendChild(title);
			}	
				break

			case "ZOMATO":
			
				var title = document.createElement('div')
				title.innerHTML = "Here are some results"
				title.className = "medium bright";
				title.style.marginTop = "50px";
				title.style.marginLeft = "155px";
           

				wrapper.appendChild(title)
				
               var container = document.createElement("div");
		       container.className = "contain";
		       container.innerHTML = "<img src=\"" + this.file("zomato.png") + "\" style=\"border-radius:50%;top:-24%;left:-21%;position:absolute;transform:scale(.3);\">"
		      
				var table = document.createElement("table");
				table.className = "table";
				var orderArrayHeader = ["Restaurant Name"," Cost for Two "," Rating"];
				var thead = document.createElement('thead');

table.appendChild(thead);
for(var i=0;i<orderArrayHeader.length;i++){
    thead.appendChild(document.createElement("th")).
    appendChild(document.createTextNode(orderArrayHeader[i]));
}
 
 
					
var keys = ["cabtype", "maxfare", "minfare"];
for (var j = 0; j < this.zomato[keys[0]].length; j++) {
  var tr = table.insertRow();
  
  for (var k = 0; k < keys.length; k++) {
    var td = tr.insertCell();
  
    td.innerHTML = this.zomato[keys[k]][j];
  }
}
	
						
				

				container.appendChild(table)
				wrapper.appendChild(container)
				break	

			  	
			case "VIDEO":
			
				
		var videoWrapper = document.createElement("div")
        videoWrapper.className = "videoWrapper"
        var iframe = document.createElement('iframe')
        iframe.src =  this.videoURL 
        videoWrapper.appendChild(iframe)
        /*videoWrapper.style.position = "relative"*/
         var ico = document.createElement("div");
        ico.innerHTML = "<img src=\"" + this.file("yout.png") + "\" style=\"border-radius:50%;top:-3%;left:7%;position:absolute;transform:scale(.12);z-index:99;\">"
        /*ico.style.position = "absolute";*/
        videoWrapper.appendChild(ico)
        wrapper.appendChild(videoWrapper)

        var container = document.createElement("div");
		       container.className = "contain";
		       container.style.transform = "scale(.5)";
		       container.style.position = "absolute";
		       container.style.top = "800px";
		       container.style.left = "-571px";
		      /* container.style.marginTop = "-50em";
		       container.style.marginRight = "3em";*/
		       container.innerHTML = "<span>\"" + this.videoTITLE +  "\" </span><span>\"" + this.videoCHANNEL +  "\" </span>";
		      /* <img src=\"" + this.videoTHUMB + "\" style=\"border:1px solid black;width:10%;border-radius:50%;margin-right:10px;\">*/
              wrapper.appendChild(container)
               
				break

			/*case "MODULE":

			

				break	*/
			case "CAB":
				
				var circular = document.createElement("div");
circular.className = "circular--landscape"
circular.innerHTML = "<img src= 'http://is3.mzstatic.com/image/thumb/Purple20/v4/04/6b/25/046b25a7-e884-989a-bc3c-0a392247212f/source/392x696bb.jpg'><div class='est'>" + this.cab.minfare + " MIN</div><div class='carname'>Toyota Pyrus</div><div class='plate'>MH 14 BM 8998</div><div class='cost'>" + this.cab.maxfare + "</div><div class='status'>" + this.cab.status + "</div><div class='type'>" + this.cab.cabtype + "</div>";

var spans = document.createElement("div");
spans.className = "info"
spans.innerHTML = "<img src=\"" + this.cab.pic  + "\">";
circular.appendChild(spans)

wrapper.appendChild(circular)


var arriving = document.createElement("div");
arriving.className = "arr"
arriving.innerHTML = this.cab.driver;
wrapper.appendChild(arriving)
 
var box = document.createElement("div");
box.className = "box";
box.innerHTML = "<div class='card__face__path'></div><div class='card__face__from-to'><p><span style='margin-right:5px;'>Pickup:</span>" + this.cab.from + "</p><p><span style='margin-right:5px;'>Dropoff:</span>" + this.cab.to + "</p></div> <button type='button' class='flat-button large red'>Cancel Ride</button></div>";
wrapper.appendChild(box);

var ico = document.createElement("div");
ico.innerHTML = "<img src="+ this.file("ube.png") +" style=\"border-radius:50%;top:-48%;left:23%;position:absolute;transform:scale(.2);z-index:99;\">"
wrapper.appendChild(ico)

document.body.appendChild(wrapper);
				   break	
			case "WEATHER":
				var small = document.createElement("div");
				small.className = "normal medium";
				small.style.margin = "10px 0px"

				var windIcon = document.createElement("span");
				windIcon.className = "wi wi-strong-wind dimmed";
				small.appendChild(windIcon);

				var windSpeed = document.createElement("span");
				windSpeed.innerHTML = " " + this.weather.windSpeed + " mph" //this.windSpeed
				small.appendChild(windSpeed);

				var spacer = document.createElement("span");
				spacer.innerHTML = "&nbsp;";
				small.appendChild(spacer);

				var sunriseSunsetIcon = document.createElement("span"); 
				if (this.weather.hour >= 4 && this.weather.hour < 10) {
					sunriseSunsetIcon.className = "wi dimmed " + "wi-sunrise"; //this.sunriseSunsetIcon
				} else if (this.weather.hour >=10 && this.weather.hour < 18) {
					sunriseSunsetIcon.className = "wi dimmed " + "wi-day-sunny"; //this.sunriseSunsetIcon
				} else if (this.weather.hour >=18 && this.weather.hour < 22) {
					sunriseSunsetIcon.className = "wi dimmed " + "wi-sunset"; //this.sunriseSunsetIcon
				} else {
					sunriseSunsetIcon.className = "wi dimmed " + "wi-night-clear"; //this.sunriseSunsetIcon
				}
				small.appendChild(sunriseSunsetIcon);

				var sunriseSunsetTime = document.createElement("span");
				sunriseSunsetTime.innerHTML = " " +  "Now" //this.sunriseSunsetTime;
				small.appendChild(sunriseSunsetTime);

				var large = document.createElement("div");
				large.className = "xlarge light";

				var weatherIcon = document.createElement("span");
				weatherIcon.className = "wi weathericon " + this.config.iconTable[this.weather.icon] //this.weatherType;
				large.appendChild(weatherIcon);

				var temperature = document.createElement("span");
				temperature.className = "bright";
				temperature.innerHTML = " " + this.weather.temperature + "&deg;"; //this.temperature
				large.appendChild(temperature);

				large.style.margin = "20px 0px"

				wrapper.appendChild(small);
				wrapper.appendChild(large);
				break;
			case "FACE":
				wrapper.innerHTML = "<img src=\"" + this.file("face.gif") + "\" style=\"border:1px solid black;max-width:100%;\">"
				break
			case "HOLIDAYS":
				var title = document.createElement('div')
				title.innerHTML = this.holiday.localName
				title.className = "large bright";
				title.style.margin = "10px"

				var date = new Date(this.holiday.date.year, this.holiday.date.month - 1, this.holiday.date.month)

				var subtitle = document.createElement('div')
				subtitle.innerHTML = date.toDateString()
				subtitle.className = "medium bright";
				subtitle.style.margin = "10px" 

				wrapper.appendChild(title)
				wrapper.appendChild(subtitle)
				break
			case "NEWS":
				var title = document.createElement('div')
				title.innerHTML = "News"
				title.className = "medium bright";
				title.style.margin = "20px"

				wrapper.appendChild(title)

				var table = document.createElement("table");
				table.className = "medium";

				for (var a in this.articles) {
					var article = this.articles[a];

					var row = document.createElement("tr");
					table.appendChild(row);

					var iconCell = document.createElement("td");
					iconCell.className = "bright weather-icon";
					row.appendChild(iconCell);

					var icon = document.createElement("span");
					icon.innerHTML = "<img src=\"" + this.file("newspaper_icon.png") + "\" style=\"width:30px;height:30px;\">"
					icon.style.margin = "10px 10px"
					iconCell.appendChild(icon);

					var title = document.createElement("span");
					title.className = "day";
					title.innerHTML = article;
					iconCell.appendChild(title);
				}

				wrapper.appendChild(table)
				break
			default:
				break
		}
		return wrapper
	},

	// Override socket notification handler.
	socketNotificationReceived: function(notification, payload) {
		console.log("module received: " + notification)
		var self = this

		if (notification == "STATEMENT"){
			this.current_selection = "STATEMENT"
			this.text = payload.text
			this.updateDom(this.config.animationSpeed);
		} 
		else if (notification == "IMAGE") {
			this.imageURL = payload.imageurl
			this.current_selection = "IMAGE"
			this.updateDom(this.config.animationSpeed);
		} 

		else if (notification == "OTHER") {
			this.current_selection = "OTHER"
			this.other = payload
			
			
			this.updateDom(this.config.animationSpeed);

		}

		else if (notification == "ZOMATO") {
			this.current_selection = "ZOMATO"
			this.zomato = payload
			
			this.updateDom(this.config.animationSpeed);

		}


		else if (notification == "VIDEO") {
			this.videoURL = payload.videourl
			this.videoTHUMB = payload.videothumb
			this.videoTITLE = payload.videotitle
			this.videoCHANNEL = payload.chtitle
			
			this.current_selection = "VIDEO"
			this.updateDom(this.config.animationSpeed);
		}
		else if (notification == "MODULE") {
			 MM.getModules().enumerate(function(module) {
        if (module.name === payload.moduleName || payload.moduleName === "all_modules") {
          if (payload.turnOn) {
            if (module.name === self.name) {
              self.clear = false
              self.updateDom();
            }
            module.show(1000, function() {
              Log.log(module.name + ' is shown.');
            });
          } else {
            if (module.name === self.name) {
              self.clear = true
              self.updateDom();
            }
            module.hide(1000, function() {
              Log.log(module.name + ' is hidden.');
            });
          }
        }
      });
		}
		else if (notification == "CAB") {
			//this.cabURL = payload.cabt
			//this.maURL = payload.ma
			//this.miURL = payload.mi
			this.cab = payload
			this.current_selection = "CAB"
			this.updateDom(this.config.animationSpeed);
		}
		else if (notification == "WEATHER") {
			this.current_selection = "WEATHER"
			this.weather = payload
			this.updateDom(this.config.animationSpeed);
		} else if (notification == "CLEAR") {
			this.current_selection = ""
			this.updateDom(this.config.animationSpeed);
		} else if (notification == "FACE") {
			this.current_selection = "FACE"
			this.updateDom(this.config.animationSpeed);
		} else if (notification == "NEWS") {
			this.current_selection = "NEWS"
			this.articles = payload.articles
			this.updateDom(this.config.animationSpeed);
		} else if (notification == "HOLIDAYS") {
			this.current_selection = "HOLIDAYS"
			this.holiday = payload.holiday
			this.updateDom(this.config.animationSpeed);
		}
	}
});
