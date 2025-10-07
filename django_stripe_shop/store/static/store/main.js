document.addEventListener("DOMContentLoaded", function () {
  const form = document.getElementById("buy-form");
  const buyBtn = document.getElementById("buy-btn");

  form.addEventListener("submit", function (e) {
    buyBtn.disabled = true;
    buyBtn.innerText = "Redirecting...";
  });

  window.addEventListener("pageshow", function(event) {
    if (event.persisted) { 
      buyBtn.disabled = false;
      buyBtn.innerText = "Buy";
    }
  });
});
