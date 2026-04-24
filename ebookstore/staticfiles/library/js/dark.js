
const reader = document.querySelector("#reader");
const toggleBtn = document.querySelector("#darkToggle");

/* =========================
   APPLY SAVED MODE FIRST
========================= */
function applySavedTheme() {
    if (!reader) return;

    const saved = localStorage.getItem("darkMode");

    if (saved === "on") {
        reader.classList.remove("reader-light");
        reader.classList.add("reader-dark");
    } else {
        reader.classList.remove("reader-dark");
        reader.classList.add("reader-light");
    }
}

/* =========================
   TOGGLE FUNCTION
========================= */
function toggleDarkMode() {

    if (!reader) return;

    if (reader.classList.contains("reader-dark")) {
        reader.classList.remove("reader-dark");
        reader.classList.add("reader-light");

        localStorage.setItem("darkMode", "off");

    } else {
        reader.classList.remove("reader-light");
        reader.classList.add("reader-dark");

        localStorage.setItem("darkMode", "on");
    }
}

/* =========================
   INIT
========================= */
applySavedTheme();

if (toggleBtn) {
    toggleBtn.addEventListener("click", toggleDarkMode);
}