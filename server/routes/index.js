var express = require('express');
var router = express.Router();
const uuid = require('uuid/v1');

users = []

/* GET home page. */
router.get('/', function(req, res, next) {
  res.render('index', { title: 'Cyclops' });
});

router.post('/user', function(req, res, next) {
	console.log("adding new user");
	const user = {};
	user.uid = uuid()
	users.push(user);
	res.json(user)
});

router.post('/image', function(req, res, next) {
	console.log(req.body);
	res.json({});
});

module.exports = router;
