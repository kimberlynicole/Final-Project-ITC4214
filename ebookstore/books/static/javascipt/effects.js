/*
========================================================
BOOK CARD HOVER EFFECT
- Adds interactive hover animation to all book cards
- Uses event listeners (mouseenter + mouseleave)
========================================================
*/

// Select all book cards from the page
const cards = document.querySelectorAll(".book-card");
/*
--------------------------------------------------------
FUNCTION: handleMouseEnter
- Runs when mouse enters a book card
- Adds zoom + shadow effect
--------------------------------------------------------
*/
function handleMouseEnter() {
    this.style.transform = "scale(1.05)";
    this.style.transition = "0.3s ease";
    this.style.boxShadow = "0 10px 25px rgba(0,0,0,0.2)";
    this.style.zIndex = "10";
}
/*
--------------------------------------------------------
FUNCTION: handleMouseLeave
- Runs when mouse leaves a book card
- Resets styles back to normal
--------------------------------------------------------
*/
function handleMouseLeave() {
    this.style.transform = "scale(1)";
    this.style.boxShadow = "none";
    this.style.zIndex = "1";
}

cards.forEach(card => {
    card.addEventListener("mouseenter", handleMouseEnter);
    card.addEventListener("mouseleave", handleMouseLeave);
});


/*
--------------------------------------------------------
Rating of the Stars
- Runs when mouse leaves a book card
- Resets styles back to normal
--------------------------------------------------------
*/

const starContainer = document.querySelector('#star-rating');
const ratingInput = document.querySelector('#rating-value');

let selectedValue = 0;

// =====================
// EVENTS
// =====================
starContainer.addEventListener('click', handleStarClick);
starContainer.addEventListener('mousemove', handleStarHover);
starContainer.addEventListener('mouseleave', handleStarLeave);

// =====================
// CLICK HANDLER
// =====================
function handleStarClick(event) {

    const star = event.target.closest('.star');
    if (!star) return;

    selectedValue = star.dataset.value;
    ratingInput.value = selectedValue;

    fillStars(selectedValue);
}

// =====================
// HOVER HANDLER
// =====================
function handleStarHover(event) {

    const star = event.target.closest('.star');
    if (!star) return;

    fillStars(star.dataset.value);
}

// =====================
// MOUSE LEAVE HANDLER
// =====================
function handleStarLeave() {

    fillStars(selectedValue);
}

// =====================
// FILL STARS FUNCTION
// =====================
function fillStars(value) {

    for (let i = 1; i <= 5; i++) {

        const star = document.querySelector(`.star[data-value="${i}"]`);

        if (i <= value) {
            star.classList.add('bi-star-fill');
            star.classList.remove('bi-star');
        } else {
            star.classList.add('bi-star');
            star.classList.remove('bi-star-fill');
        }
    }
}






