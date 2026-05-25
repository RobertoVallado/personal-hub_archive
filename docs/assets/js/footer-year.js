// Refresh the year label on Material instant-navigation page swaps.
document.addEventListener("DOMContentSwitch", function () {
  const yearSpan = document.getElementById("year");
  if (yearSpan) yearSpan.textContent = new Date().getFullYear();
});
