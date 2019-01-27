var running = false;

function startup() {
  var runningButton = document.getElementById("runningButton");
  var port = chrome.extension.connect({
      name: "Background Communication"
    });
  port.postMessage("status");
  runningButton.addEventListener('click', function(ev){
      if (running) {
        port.postMessage("stop");
      } else {
        port.postMessage("start");
      }
    }, false);

  port.onMessage.addListener(function(msg) {
    if (msg == "stopped") {
      runningButton.innerHTML = "Start";
      running = false;
    } else if (msg == "started") {
      runningButton.innerHTML = "Stop"
      running = true;
    }
  });
}

window.onload = startup;