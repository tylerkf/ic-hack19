console.log('hello');


document.addEventListener('DOMContentLoaded', function() {

  var link = document.getElementById('link');

  // onClick's logic below:

  link.addEventListener('click', function() {

    console.log('clicking');

    fetch('http://cyclopsx.duckdns.org/', {mode:"no-cors"})

      .then(function(response) {

        console.log(response);

        link.innerHTML = "got response!";

      })

      .then(function (data){

        link.innerHTML = "got response!";

      });

  });

});
