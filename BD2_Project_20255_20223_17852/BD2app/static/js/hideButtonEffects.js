const buttons = document.getElementsByClassName("btn btn-light d-inline");
Array.from(buttons).forEach(function (button) {
  button.addEventListener("click", function () {
    event.preventDefault();
  });
  button.addEventListener("mouseenter", function () {
    this.style.color = "inherit";
    this.style.backgroundColor = "inherit";
  });
  button.addEventListener("mouseleave", function () {
    this.style.color = "inherit";
    this.style.backgroundColor = "inherit";
  });
  button.addEventListener("mouseenter", function () {
    this.style.border = "0";
    this.style.backgroundColor = "inherit";
  });
});
