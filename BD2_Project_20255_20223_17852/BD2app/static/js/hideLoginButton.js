var loginButton = document.getElementById("loginButton");
var username = document.getElementById("username");
var password = document.getElementById("password");
username.addEventListener("keyup", checkInput);
password.addEventListener("keyup", checkInput);
loginButton.addEventListener("click", checkInput);
function checkInput() {
  if (username.value == "" || password.value == "") {
    loginButton.disabled = true;
  } else {
    loginButton.disabled = false;
  }
}
