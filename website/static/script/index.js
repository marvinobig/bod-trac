const validationAlert = document.getElementById("validation-alert");
if (validationAlert) {
  validationAlert.addEventListener("mouseover", () => {
    validationAlert.remove();
  });
}
