var express = require('express');
var router = express.Router();
var fs = require('fs');
const uuid = require('uuid/v1');

users = []

/* GET home page. */
router.get('/', function(req, res, next) {
  res.render('index', { title: 'Cyclops' });
});

router.get('/stream', function(req, res, next) {
  res.render('stream', { username: 'Cyclopper' });
});

// posts

router.post('/user', function(req, res, next) {
	console.log("adding new user");
	const user = {};
	user.uid = uuid()
	users.push(user);
	res.json(user)
});

router.post('/image', function(req, res, next) {
	//console.log(req.body);
	console.log("received data");
	stringData = req.body.image.replace(/^data:image\/(png|jpg);base64,/, "")
	console.log("got string data");
	var base64Data = new Buffer(stringData, 'base64');
	console.log("got data");

	fs.writeFile("ttest.png", base64Data, 'base64', function(err) {
		if (err) {
			console.log(err);
		} else {
			console.log("done");
		}
	});
	res.json({});
});

module.exports = router;
