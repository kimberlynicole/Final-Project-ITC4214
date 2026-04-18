const wishlistBtns = document.querySelectorAll(".wishlist-btn");

/* =========================
   LOOP BUTTONS
========================= */
wishlistBtns.forEach(btn => {

    btn.addEventListener("mouseenter", handleWishlistHoverIn);
    btn.addEventListener("mouseleave", handleWishlistHoverOut);
    btn.addEventListener("click", handleWishlistToggle);

});

/* =========================
   HOVER IN (preview filled)
========================= */
function handleWishlistHoverIn() {

    const icon = this.querySelector("i");

    icon.classList.remove("bi-heart");
    icon.classList.add("bi-heart-fill");

}

/* =========================
   HOVER OUT (restore state)
========================= */
function handleWishlistHoverOut() {

    const icon = this.querySelector("i");

    if (!this.classList.contains("active")) {
        icon.classList.remove("bi-heart-fill");
        icon.classList.add("bi-heart");
    }

}

/* =========================
   CLICK TOGGLE
========================= */
function handleWishlistToggle() {

    const bookId = this.dataset.bookId;
    const icon = this.querySelector("i");

    fetch(`/books/wishlist/toggle/${bookId}/`, {
        method: "POST",
        headers: {
            "X-CSRFToken": getCSRFToken(),
        }
    })
    .then(res => res.json())
    .then(data => {

        if (data.status === "added") {
            icon.classList.remove("bi-heart");
            icon.classList.add("bi-heart-fill");
            this.classList.add("active");
        }

        if (data.status === "removed") {
            icon.classList.remove("bi-heart-fill");
            icon.classList.add("bi-heart");
            this.classList.remove("active");
        }

    });

}

/* =========================
   CSRF
========================= */
function getCSRFToken() {
    return document.querySelector('meta[name="csrf-token"]')?.content;
}