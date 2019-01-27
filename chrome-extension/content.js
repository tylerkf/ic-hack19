console.log("alive");

chrome.runtime.onMessage.addListener(
  function(request, sender, sendResponse) {
    console.log(request);
    if (request.action == "tab_to_next_focus") {
      console.log("tabbing");
      tabToNextFocus();
      console.log("print");
    } else if (request.action == "click_active") {
      console.log("clicking");
      clickActive();
    }
  });

var tabToElement = {};
var maxTabIndex = 0;

function getTabIndexes() {
  tabToElement = {};
  maxTabIndex = 0;
  focusables = document.querySelectorAll("button, [href], input, select, textarea");

  for (var i=0; i < focusables.length; i++) {
    element = focusables[i];
    tabIndex = element.tabIndex;
    if (tabIndex != null && tabIndex >= 0) {
      tabToElement[tabIndex] = element;
      if (tabIndex > maxTabIndex) {
        maxTabIndex = tabIndex;
      }
    }
  }

  return tabToElement
}

function tabToNextFocus() {
  console.log("printt");
  if (Object.keys(tabToElement).length == 0) {
    tabToElement = getTabIndexes();
    if (Object.keys(tabToElement).length == 0) {
      return;
    } else {
      console.log("deffo something in there");
    }
  }

  currentTabIndex = document.activeElement.tabIndex;

  if (currentTabIndex == null || currentTabIndex < 0) {
    currentTabIndex = -1;
  }

  while (currentTabIndex <= maxTabIndex) {
    currentTabIndex += 1;
    if (currentTabIndex in tabToElement && tabToElement[currentTabIndex] != undefined) {
      break
    } else if (currentTabIndex == maxTabIndex) {
      console.log("didnt find tab index");
      return;
    }
  }

  tabToElement[currentTabIndex].focus();
}

function clickActive() {
  document.activeElement.click();
}