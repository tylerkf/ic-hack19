console.log('hello');

document.addEventListener('DOMContentLoaded', function() {
  var link = document.getElementById('link');
  // onClick's logic below:
  link.addEventListener('click', function() {
    console.log('clicking');
    fetch('http://146.169.200.26/', {mode:"no-cors"})
      .then(function(response) {
        console.log(response);
        link.innerHTML = "got response!";
      })
      .then(function (data){
        link.innerHTML = "got response!";
      });
  });
});
