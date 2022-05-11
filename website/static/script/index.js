const validationAlert = document.getElementById("validation-alert");
if (validationAlert) {
  setTimeout(removeAlert, 4000);
}

function removeAlert() {
  validationAlert.remove();
}

function deleteWeight(id) {
  fetch("/deleteWeight", {
    method: "POST",
    body: JSON.stringify({ id: id }),
  }).then((_res) => {
    window.location.href = "/auth/account";
  });
}
