
const reader = document.querySelector("#reader");
const toggleBtn = document.querySelector("#darkToggle");

/* EVENT */
if (toggleBtn) {
    toggleBtn.addEventListener("click", toggleDarkMode);
}

/* FUNCTION */
function toggleDarkMode() {

    if (!reader) return;

    reader.classList.toggle("reader-dark");
    reader.classList.toggle("reader-light");
}