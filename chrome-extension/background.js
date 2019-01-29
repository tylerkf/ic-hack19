const STREAM_URL = "http://cyclopsx.duckdns.org/stream/";
const SOCKET_URL = "http://cyclopsx.duckdns.org:8810";
var streamTabId = null;
var uid = null;
var socket = null;

var lastAction = {}


chrome.extension.onConnect.addListener(function(port) {

  console.log("Connected .....");

  port.onMessage.addListener(function(msg) {

    if (msg == "start") {

      console.log("startd");
      startSockets();
    } else if (msg == "stop") {
      stopSockets();
      console.log("stop");

      chrome.tabs.remove(streamTabId, function() {

        streamTabId = null;

        port.postMessage("stopped");

      });

    } else if (msg == "status") {

      if (streamTabId !== null) {

        port.postMessage("started");

      } else {

        port.postMessage("stopped");

      }

    }

  });

});


chrome.tabs.onRemoved.addListener(function(tabId, removeInfo) {

  if (tabId == streamTabId) {

    console.log("dangit");

  }
});

function stopSockets() {
  if (socket != null) {
    socket.disconnect()
  }
}

function startSockets() {
  socket = io(SOCKET_URL);

  socket.on('action', function(msg) {
    try {
      json_str = msg.replace("'", '"');
      json_str = json_str.replace(/'/g, '"');
      lastAction = JSON.parse(json_str);
      console.log(json_str);

      if (lastAction["head_inclination"] == 1) {
        tab_it();
      } else if (lastAction["winking"] == 1) {
        click_it();
      } else if (lastAction["winking"] == -1 || lastAction["head_inclination"] == -1) {
        back_it();
      }
    } catch(e) {
      console.log(e);
    }
  });

  socket.on('uid', function(msg) {
    uid = msg;
    chrome.tabs.create({url: STREAM_URL + uid, active: false}, function(tab) {
        streamTabId = tab.id;
        console.log(streamTabId);
      });
  });
}

function tab_it() {
  console.log("tab");
  chrome.tabs.query({active: true}, function(tabs){
    console.log(tabs.length);
    for (var i=0; i < tabs.length; i++) {
      if (tabs[i].id === undefined) {
        continue
      }
      chrome.tabs.sendMessage(tabs[i].id, {action: "tab_to_next_focus"}, function(response) {});
    }
  });
}

function click_it() {
  console.log("click");
  chrome.tabs.query({active: true}, function(tabs){
    console.log(tabs.length);
    for (var i=0; i < tabs.length; i++) {
      if (tabs[i].id === undefined) {
        continue
      }
      chrome.tabs.sendMessage(tabs[i].id, {action: "click_active"}, function(response) {});
    }
  });
}

function back_it() {
  console.log("back");
  chrome.tabs.query({active: true}, function(tabs){
    console.log(tabs.length);
    for (var i=0; i < tabs.length; i++) {
      if (tabs[i].id === undefined) {
        continue
      }
      console.log("in the loop");
      chrome.tabs.sendMessage(tabs[i].id, {action: "go_bback"}, function(response) {});
    }
  });
}
