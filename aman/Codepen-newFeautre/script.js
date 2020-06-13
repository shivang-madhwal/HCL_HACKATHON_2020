const overlay = document.getElementById("product-shape");

var el = document.getElementsByClassName("color");
for (var i = 0; i < el.length; i++) {
  el[i].onclick = changeColor;
}

function changeColor(e) {
  
  let hex = e.target.getAttribute("data-hex");
  
  overlay.style.fill = hex;
}