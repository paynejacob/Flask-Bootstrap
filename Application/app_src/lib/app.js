import "babel-polyfill";
import "bootstrap-sass";
import AjaxInterceptor from "ajax-interceptor";
import $ from "jquery";

function overrideFormSubmit(){
  /*
  All form submits are ajax for error display.
  */
  $("form").submit( event => {
    event.preventDefault();
    var url = event.target.action;
    var method = event.target.method;
    var data = {};
    for (var i = event.target.length - 1; i >= 0; i--) {
      var name = event.target[i].name;
      var content = $(event.target[i]).val();
      data[name] = content;
    }
    return $.ajax(url, {
      "method": method,
      "data": data
    });
  });
}

function removeParentElement(e) {
  e.target.parentElement.remove();
}

function makeMessagesCloseable(){
  var messages = document.getElementsByTagName("messages")[0];
  var messageCloses = messages.getElementsByClassName("close");
  for (var i = 0; i < messageCloses.length; i++) {
    messageCloses[i].onclick = removeParentElement;
  }
}
$(
  AjaxInterceptor.addResponseCallback(function(xhr) {
    if(xhr.getResponseHeader("Content-Type") === "application/json"){
      var resp_obj = JSON.parse(xhr.response);
      var messages = resp_obj["messages"];
      if(messages){
        for (var i = 0; i < messages.length; i++) {
          var [category, messagetext] = messages[i];
          var id = "message-" + i;
          //This makes two dom nodes for the same message :(
          var messageWrapper = document.createElement("div");
          messageWrapper.setAttribute("id", id);
          messageWrapper.setAttribute("class", "message-wrapper message-" + category);
          var messageCategory = document.createElement("div");
          messageCategory.setAttribute("class", "message-category");
          messageCategory.textContent = category;
          var messageText = document.createElement("div");
          messageText.setAttribute("class", "message-text");
          messageText.textContent = messagetext;
          var closeButton = document.createElement("button");
          closeButton.setAttribute("class", "close fa fa-times-circle");
          closeButton.onclick = removeParentElement;
          messageWrapper.appendChild(messageCategory);
          messageWrapper.appendChild(messageText);
          messageWrapper.appendChild(closeButton);
          document.getElementsByTagName("messages")[0].appendChild(messageWrapper);
        }
      }
      var redirect = resp_obj["redirect"];
      if(redirect){
        //TODO: Deal with location.hash
        location.assign(redirect);
      }

    }
  })
);
$(function(){
  overrideFormSubmit();
  makeMessagesCloseable();
  AjaxInterceptor.wire();
});


module.exports = {

};
