// CLICK ADD CART
var updateBtns = document.getElementsByClassName("update-cart");

for (var i = 0; i < updateBtns.length; i++) {
  updateBtns[i].addEventListener("click", function () {
    var productId = this.dataset.item;
    var action = this.dataset.action;
    console.log("productId:", productId, "action", action);
    console.log(("USER", user));
    if (user === "AnonymousUser") {
      addCookieItem(productId, action);
    } else {
      updateUserOrder(productId, action);
    }
  });
}

// for non-logged user
function addCookieItem(productId, action) {
  console.log("not logged in.....");
  if (action == "add") {
    if (cart[productId] == undefined) {
      cart[productId] = { quantity: 1 }; // add + 1 for the item quantity
    } else {
      cart[productId]["quantity"] += 1;
    }
  }
  if (action == "remove") {
    cart[productId]["quantity"] -= 1;
    if (cart[productId]["quantity"] <= 0) {
      console.log("Remove item");
      delete cart[productId]; // remove item from the cart and all nested element
    }
  }
  console.log("Cart", cart);
  document.cookie = "cart=" + JSON.stringify(cart) + ";domain=;path=/";
  location.reload();
}

// for logged user
function updateUserOrder(productId, action) {
  console.log("User is logged in, data ok");
  var url = "/update_item/";
  fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrftoken,
    },
    body: JSON.stringify({ productId: productId, action: action }),
  })
    .then((response) => {
      return response.json();
    })
    .then((data) => {
      console.log("data", data);
      location.reload();
    });
}

// MENU TOGGLER

$(document).ready(function () {
  // Check for click events on the navbar burger icon
  $(".navbar-burger").click(function () {
    // Toggle the "is-active" class on both the "navbar-burger" and the "navbar-menu"
    $(".navbar-burger").toggleClass("is-active");
    $(".navbar-menu").toggleClass("is-active");
  });
});
