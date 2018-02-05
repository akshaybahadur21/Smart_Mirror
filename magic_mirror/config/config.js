/* Magic Mirror Config Sample
/* Magic Mirror Config Sample
 *
 * By Michael Teeuw http://michaelteeuw.nl
 * MIT Licensed.
 */

var config = {
	port: 8080,

	language: 'en',
	timeFormat: 24,
	units: 'metric',

	modules: [
    {
        module: 'aiclient',
        position: 'middle_center' // This can be any of the regions.
    },
    {
    	module: 'aiclientdebugger',
    	position: 'bottom_right'
    },

    
  
		{
			module: "updatenotification",
			position: "top_bar"
		},
		{
			module: "clock",
			position: "top_left"
		},
		{
			module: "calendar",
			header: "Indian Holidays",
			position: "top_left",
			config: {
				calendars: [
					{
						symbol: "calendar-check-o ",
						url: ""
					}
					

				]
			}
		},
		
		{
			module: "currentweather",
			position: "top_right",
			config: {
				location: "",
				locationID: "",  //ID from http://www.openweathermap.org/help/city_list.txt
				appid: ""
			}
		},
		{
			module: "weatherforecast",
			position: "top_right",
			header: "Weather Forecast",
			config: {
				location: "",
				locationID: "",  //ID from http://www.openweathermap.org/help/city_list.txt
				appid: ""
			}
		},
		{
			module: "newsfeed",
			position: "bottom_bar",
			config: {
				feeds: [
					{
						title: "Hindustan Times",
						url: "http://www.hindustantimes.com/rss/topnews/rssfeed.xml"
					}
				],
				showSourceTitle: true,
				showPublishDate: true
			}
		},

		
  {
    module: 'MMM-bitcoin',
    position: 'bottom_left',
    config: {
      fiat: 'usd',          // 'usd' and 'eur' available, defaults to 'usd'
      showBefore: 'Bitcoin',    // will display before the bitcoin price, default 'Bitstamp'
      updateInterval: 60000 // update interval in milliseconds
    }
  },


	{
		module: 'email',
                position: 'bottom_left',
                header: 'Email',
                config: {
                    accounts: [
                        {
                            user: 'example@gmail.com',
                            password: 'example',
                            host: 'imap.gmail.com',
                            port: 993,
                            tls: true,
                            authTimeout: 10000,
                            numberOfEmails: 6,

                        },
                        
                    ],
                    fade: false,
                    maxCharacters: 30
                }
	},


	]

};

/*************** DO NOT EDIT THE LINE BELOW ***************/
if (typeof module !== 'undefined') {module.exports = config;}
