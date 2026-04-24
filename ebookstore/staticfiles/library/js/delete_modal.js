
// =========================
// SELECTORS
// =========================
const deleteButtons = document.querySelectorAll(".remove-book-btn");
const confirmDeleteBtn = document.querySelector("#confirmDeleteBtn");
const modalElement = document.querySelector("#deleteModal");

let selectedBookId = null;

// =========================
// EVENT LISTENERS
// =========================
deleteButtons.forEach(handleDeleteButtonClick);

if (confirmDeleteBtn) {
    confirmDeleteBtn.addEventListener("click", confirmDelete);
}

// =========================
// FUNCTIONS
// =========================

// Open modal + store book id
function handleDeleteButtonClick(button) {
    button.addEventListener("click", openDeleteModal);
}

function openDeleteModal(event) {
    selectedBookId = event.currentTarget.dataset.bookId;

    const modal = new bootstrap.Modal(modalElement);
    modal.show();
}

// Confirm deletion
function confirmDelete() {
    if (!selectedBookId) return;

    window.location.href = `/library/remove/${selectedBookId}/`;
}