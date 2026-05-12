document.addEventListener("DOMContentLoaded", function () {
  const track = document.getElementById("habitsTrack");
  const prevBtn = document.getElementById("habitsPrev");
  const nextBtn = document.getElementById("habitsNext");
  const cards = document.querySelectorAll(".habit-card-wrapper");

  if (!track || !prevBtn || !nextBtn) return;

  let position = 0;

  function getVisibleCount() {
    const width = window.innerWidth;
    if (width < 600) return 1;
    if (width < 992) return 2;
    return 3;
  }

  function updateCarousel() {
    const visibleCards = getVisibleCount();
    const cardWidthPercent = 100 / visibleCards;
    track.style.transform = `translateX(${-position * cardWidthPercent}%)`;
  }

  nextBtn.addEventListener("click", () => {
    const visibleCards = getVisibleCount();
    if (position < cards.length - visibleCards) {
      position++;
      updateCarousel();
    }
  });

  prevBtn.addEventListener("click", () => {
    if (position > 0) {
      position--;
      updateCarousel();
    }
  });

  window.addEventListener("resize", updateCarousel);
  updateCarousel();
});
