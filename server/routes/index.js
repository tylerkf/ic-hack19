var express = require('express');
var router = express.Router();
var fs = require('fs');
var util = require("util");
var spawn = require("child_process").spawn;

const uuid = require('uuid/v1');
var io = null;

users = {}

var setio = function(app) {
	console.log("setup");
	var server = app.listen(8810);
  io = require('socket.io').listen(server);

	io.on('connection', function(socket) {
		const user = {};
		user.uid = uuid();
		user.sessionid = socket.id;
		users[user.uid] = user;
		socket.emit("uid", user.uid);
		console.log("user!");
	});
}

/* GET home page. */
router.get('/', function(req, res, next) {
  res.render('index', { title: 'Cyclops' });
});

router.get('/stream/:uid', function(req, res, next) {
	console.log(req.params.uuid);
  res.render('stream', { username: 'Cyclopper', uid: req.params.uid });
});

// posts

router.post('/user', function(req, res, next) {
	console.log("adding new user");
	
});

router.post('/image', function(req, res, next) {
	//console.log(req.body);
	console.log("received data");
	stringData = req.body.image.replace(/^data:image\/(png|jpg);base64,/, "")
	console.log("got string data");
	var base64Data = new Buffer(stringData, 'base64');
	console.log("got data");

	fs.writeFile("image.png", base64Data, 'base64', function(err) {
		if (err) {
			console.log(err);
		} else {
			console.log("done");
		}
	});
	res.json({});
	//next();

	runPython(function(output) {
		console.log(output);
		sesid = users[req.body.uid].sessionid
		io.to(sesid).emit("action", output);
	});

});

async function runPython(callback) {
	console.log("running python");
	var process = spawn("python3",["../feature-detection/main_extracting_all_features.py", "--shape-predictor shape_predictor_68_face_landmarks.dat"]);
	var output = "";
	process.stdout.on("data", function(chunk) {
		callback(chunk.toString());
	});
}

router.setio = setio;

module.exports = router;
