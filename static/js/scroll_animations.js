gsap.registerPlugin(ScrollTrigger);

const track = document.querySelector(".details-track");

const getScrollAmount = () => {
  let trackWidth = track.scrollWidth;
  return -(trackWidth + window.innerWidth);
};

gsap.set(".p-left-bottom", { x: "-45vw", y: "40vh", opacity: 0 });
gsap.set(".p-center-top", { x: "-5vw", y: "-35vh", opacity: 0 });
gsap.set(".p-right-middle", { x: "35vw", y: "-25vh", opacity: 0 });
gsap.set(".scroll-content", { y: "100vh", opacity: 0 });

const masterTl = gsap.timeline({
  scrollTrigger: {
    trigger: ".about-scroll-wrapper",
    start: "top top",
    end: () => `+=${track.scrollWidth}`,
    scrub: 1.5,
    pin: true,
    invalidateOnRefresh: true,
  },
});

masterTl.to(".scroll-photo", { opacity: 1, duration: 2, stagger: 0.3 });

masterTl
  .to(".p-left-bottom", { x: "-30vw", y: 0, duration: 4 }, "row")
  .to(".p-center-top", { x: 0, y: 0, duration: 4 }, "row")
  .to(".p-right-middle", { x: "30vw", y: 0, duration: 4 }, "row")
  .to(
    ".scroll-content",
    {
      y: "-30vh",
      opacity: 1,
      duration: 3,
      ease: "power2.out",
    },
    "row+=2",
  );

masterTl.to(
  ".scroll-photo",
  {
    x: 0,
    xPercent: -50,
    yPercent: -50,
    duration: 3,
    stagger: 0.2,
    ease: "power1.inOut",
  },
  "column",
);

masterTl
  .to(".scroll-content", { y: "-120vh", opacity: 0, duration: 2 }, "lift")
  .to(".photo-system", { y: "-15vh", duration: 3 }, "lift")
  .to(".details-track", { opacity: 1, duration: 1 }, "lift+=0.5");

masterTl.to(
  ".details-track",
  {
    x: () => getScrollAmount(),
    ease: "none",
    duration: 60,
  },
  "lift+=0.5",
);
