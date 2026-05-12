const testimonials = [
  {
    text: "“This app completely changed the way I build habits! I finally stay consistent thanks to the daily reminders and progress tracking. Highly recommend for anyone trying to improve their routine.”",
    name: "James M.",
    img: "static/images/testimonials/james.webp",
    bgClass: "testimonials--james",
  },
  {
    text: "“Simple, clean, and effective. I love how easy it is to create new habits and check them off every day. The interface is intuitive and distraction-free.”",
    name: "Sarah K.",
    img: "static/images/testimonials/sara.webp",
    bgClass: "testimonials--sarah",
  },
  {
    text: "“I’ve tried multiple habit trackers, but this one is my favorite. The combination of motivation quotes and weekly reports really keeps me going.”",
    name: "Kathleen J.",
    img: "static/images/testimonials/kathleen.webp",
    bgClass: "testimonials--kathleen",
  },
  {
    text: "“Great tool for staying accountable! I use it to track both personal and professional goals. A must-have if you're into self-development.”",
    name: "Jadis E.",
    img: "static/images/testimonials/jadis.webp",
    bgClass: "testimonials--jadis",
  },
];

const carouselTrack = document.getElementById("carouselTrack");

testimonials.forEach((t) => {
  carouselTrack.innerHTML += createCard(t);
});

testimonials.forEach((t) => {
  carouselTrack.innerHTML += createCard(t);
});

function createCard(t) {
  return `
        <div class="testimonials__card">
          <div class="testimonials__inner ${t.bgClass}">
            <img src="${t.img}" class="testimonials__img" alt="">
            <p>${t.text}</p>
            <div class="testimonials__name">— ${t.name}</div>
          </div>
        </div>
      `;
}

let position = 0;
let visibleCards;
let cardWidthPercent;

function getVisibleCardsCount() {
  const width = window.innerWidth;
  if (width < 768) return 1;
  if (width < 992) return 2;
  return 3;
}

function updateCardWidths() {
  visibleCards = getVisibleCardsCount();
  cardWidthPercent = 100 / visibleCards;

  carouselTrack.style.transition = "none";
  carouselTrack.style.transform = `translateX(${
    -position * cardWidthPercent
  }%)`;

  setTimeout(() => {
    carouselTrack.style.transition = "transform 0.5s ease-in-out";
  }, 0);
}

function moveCarousel(direction) {
  position += direction;
  const totalCards = testimonials.length;

  if (position < 0) {
    position = totalCards;
    updateCarouselPosition();
    return;
  }

  if (position >= totalCards) {
    position = 0;
    updateCarouselPosition();
    return;
  }

  updateCarouselPosition();
}

function updateCarouselPosition() {
  carouselTrack.style.transition = "none";
  carouselTrack.style.transform = `translateX(${
    -position * cardWidthPercent
  }%)`;

  setTimeout(() => {
    carouselTrack.style.transition = "transform 0.5s ease-in-out";
  }, 0);
}

updateCardWidths();
window.addEventListener("resize", updateCardWidths);

document
  .querySelector(".testimonials__btn--prev")
  .addEventListener("click", () => moveCarousel(-1));
document
  .querySelector(".testimonials__btn--next")
  .addEventListener("click", () => moveCarousel(1));
