const cancelBtn = document.querySelector("#cancelBtn");
const modal = new bootstrap.Modal(document.querySelector("#cancelModal"));

cancelBtn.addEventListener("click", () => {
    modal.show();
});