/*
========================================================
BOOK CARD HOVER EFFECT
========================================================
*/

const cards = document.querySelectorAll(".book-card");

function handleMouseEnter() {
    this.style.transform = "scale(1.05)";
    this.style.transition = "0.3s ease";
    this.style.boxShadow = "0 10px 25px rgba(0,0,0,0.2)";
    this.style.zIndex = "10";
}

function handleMouseLeave() {
    this.style.transform = "scale(1)";
    this.style.boxShadow = "none";
    this.style.zIndex = "1";
}

/* SAFE CHECK */
if (cards && cards.length > 0) {
    cards.forEach(card => {
        card.addEventListener("mouseenter", handleMouseEnter);
        card.addEventListener("mouseleave", handleMouseLeave);
    });
}

/*
========================================================
STAR RATING SYSTEM
========================================================
*/

const starContainer = document.querySelector('#star-rating');
const ratingInput = document.querySelector('#rating-value');

let selectedValue = 0;

/* SAFE CHECK */
if (starContainer && ratingInput) {

    starContainer.addEventListener('click', handleStarClick);
    starContainer.addEventListener('mousemove', handleStarHover);
    starContainer.addEventListener('mouseleave', handleStarLeave);

}

function handleStarClick(event) {
    const star = event.target.closest('.star');
    if (!star) return;

    selectedValue = star.dataset.value;
    ratingInput.value = selectedValue;

    fillStars(selectedValue);
}

function handleStarHover(event) {
    const star = event.target.closest('.star');
    if (!star) return;

    fillStars(star.dataset.value);
}

function handleStarLeave() {
    fillStars(selectedValue);
}

function fillStars(value) {
    for (let i = 1; i <= 5; i++) {

        const star = document.querySelector(`.star[data-value="${i}"]`);
        if (!star) continue;

        if (i <= value) {
            star.classList.add('bi-star-fill');
            star.classList.remove('bi-star');
        } else {
            star.classList.add('bi-star');
            star.classList.remove('bi-star-fill');
        }
    }
}