const btn = document.getElementById("toggle");

function updateUI(enabled) {
  btn.textContent = enabled ? "on" : "off";
  btn.className = btn.textContent;
}

getEnabled(updateUI);

btn.addEventListener("click", () => {
  toggleEnabled(updateUI);
});
