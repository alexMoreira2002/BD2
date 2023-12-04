var addProductButton = document.getElementById("addProductButton");
var productName = document.getElementById("productName");
var productType = document.getElementById("productType");
var productQuantity = document.getElementById("productQuantity");
var productPriceStart = document.getElementById("productPriceStart");
var productDescription = document.getElementById("productDescription");
var productImage = document.getElementById("productImage");

productName.addEventListener("input", checkInput);
productQuantity.addEventListener("input", checkInput);
productPriceStart.addEventListener("input", checkInput);
productDescription.addEventListener("input", checkInput);
productImage.addEventListener("input", checkInput);
addProductButton.addEventListener("click", checkInput);

function checkInput() {
  if (
    productName.value == "" ||
    productQuantity.value == "" ||
    productPriceStart.value == "" ||
    productDescription.value == ""
  ) {
    addProductButton.disabled = true;
  } else {
    addProductButton.disabled = false;
  }
}
