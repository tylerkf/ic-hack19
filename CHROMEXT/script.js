function req() {
  console.log('hello');
  fetch('https://ichack.org/')
    .then(function(response) {
      console.log(response);
      return response.json()
    })
    .then(function (data){
      console.log('the data', data)
    });
}
