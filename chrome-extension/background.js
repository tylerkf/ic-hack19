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
        port.postMessage("started");
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
    console.log(msg);
    try {
      lastAction = JSON.parse(msg);
      if (lastAction["head_inclination"] >= 10) {
        tab();
      } else if (winking == 1) {
        click_it();
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

function tab() {
  chrome.tabs.query({active: true}, function(tabs){
    for (tab in tabs) {
      chrome.tabs.sendMessage(tabs[0].id, {action: "tab_to_next_focus"}, function(response) {}); 
    } 
  });
}

function click_it() {
  chrome.tabs.query({active: true}, function(tabs){
    for (tab in tabs) {
      chrome.tabs.sendMessage(tabs[0].id, {action: "click_active"}, function(response) {}); 
    } 
  });
}
