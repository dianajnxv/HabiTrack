// document.addEventListener("DOMContentLoaded", () => {
//     const themeButton = document.getElementById("theme-button");
//     const dropdown = document.getElementById("dropdown");

//     if (themeButton && dropdown) {
//         themeButton.addEventListener("click", function () {
//             dropdown.style.display = dropdown.style.display === "block" ? "none" : "block";
//         });
//     }

//     const lightThemeButton = document.getElementById("light-theme");
//     const darkThemeButton = document.getElementById("dark-theme");
//     const motivatingThemeButton = document.getElementById("motivating-theme");

//     if (lightThemeButton) {
//         lightThemeButton.addEventListener("click", () => {
//             document.body.classList.remove("dark-theme", "motivating-theme");
//             document.body.classList.add("light-theme");
//             dropdown.style.display = "none";
//         });
//     }

//     if (darkThemeButton) {
//         darkThemeButton.addEventListener("click", () => {
//             document.body.classList.remove("light-theme", "motivating-theme");
//             document.body.classList.add("dark-theme");
//             dropdown.style.display = "none";
//         });
//     }

//     if (motivatingThemeButton) {
//         motivatingThemeButton.addEventListener("click", () => {
//             document.body.classList.remove("light-theme", "dark-theme");
//             document.body.classList.add("motivating-theme");
//             dropdown.style.display = "none";
//         });
//     }
// });


// //Modal window
// document.addEventListener("DOMContentLoaded", () => {
//   const addHabitButton = document.querySelector(".add-habit-button");
//   const modal = document.getElementById("add-habit-modal");
//   const cancelBtn = document.getElementById("cancel-btn");

//   const priorityBtn = document.getElementById("priority-btn");
//   const categoryBtn = document.getElementById("category-btn");
//   const prioritySection = document.querySelector(".priority-section");
//   const categorySection = document.querySelector(".category-section");

//   prioritySection.style.display = "none";
//   categorySection.style.display = "none";

//   addHabitButton.addEventListener("click", () => {
//     modal.style.display = "flex";
//   });

//   // Закрити модальне вікно
//   cancelBtn.addEventListener("click", () => {
//     modal.style.display = "none";
//   });

//   // Закриття модального вікна при кліку поза контентом
//   window.addEventListener("click", (event) => {
//     if (event.target === modal) {
//       modal.style.display = "none";
//     }
//   });

//   priorityBtn.addEventListener("click", () => {
//     prioritySection.style.display = prioritySection.style.display === "none" ? "block" : "none";
//     categorySection.style.display = "none";
//   });

//   categoryBtn.addEventListener("click", () => {
//     categorySection.style.display = categorySection.style.display === "none" ? "block" : "none";
//     prioritySection.style.display = "none";
//   });
// });



