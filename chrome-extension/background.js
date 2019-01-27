const STREAM_URL = "http://cyclopsx.duckdns.org/stream";
var streamTabId = null;

chrome.extension.onConnect.addListener(function(port) {
  console.log("Connected .....");
  port.onMessage.addListener(function(msg) {
    if (msg == "start") {
      console.log("startd");

      chrome.tabs.create({url: STREAM_URL, active: false}, function(tab) {
        streamTabId = tab.id;
        console.log(streamTabId);
        port.postMessage("started");
      });

    } else if (msg == "stop") {
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

function runit() {
  chrome.tabs.query({active: true}, function(tabs){
    for (tab in tabs) {
      chrome.tabs.sendMessage(tabs[0].id, {action: "tab_to_next_focus"}, function(response) {}); 
    } 
  });
}

function runit2() {
  chrome.tabs.query({active: true}, function(tabs){
    for (tab in tabs) {
      chrome.tabs.sendMessage(tabs[0].id, {action: "click_active"}, function(response) {}); 
    } 
  });
}
