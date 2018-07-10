var express = require('express');
var fs = require('fs');
var request = require('request');
var cheerio = require('cheerio');

var app = express();


app.get('/scrape', function(req, res){
	// The URL we will scrape from
	
	url = 'https://www.imdb.com/movies-in-theaters/?ref_=nv_mv_inth_1'; 

	// The structure of our request call
	// First parameter is our URL
	// Callback function takes 3 parameter:
	// error, response status code, html
	
	request(url, function(error, response, html){
		// Firstly check whether or not there is any error while request
		if (error) throw error;

		// Next, utilize the cheerio library on the returned html
		var $ = cheerio.load(html);

		// Finally, define variable we are going to capture

		var title, director, rating;
		var json = {title: "", director: "", rating : ""};

		// Use unique header class as a starting point
		$('.nm-title-overview-widget-layout').each(function(i, element){
			// store data we filter into variable
			var data = $(this);

			title = data.children().first().children().first().children().last().children().first().children().first().text();
			director = data.children().first().children().first().children().last().children().first().next().next().next().children();

			json.title = title;
			json.director = director;
				
		});

		$('.star-box-giga-star').filter(function(){
			var data = $(this);

			rating = data.text();

			json.rating = rating;
		});

		fs.writeFile('output.json', JSON.stringify(json, null, 4), function(err){
			console.log('File successfully written! - Check your project directory for the output.json file');
		});

		res.send('Check your console!');
	});
});

app.listen('8081');

console.log('Magic happens on port 8081')

exports = module.exports = app;
