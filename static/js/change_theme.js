document.addEventListener("DOMContentLoaded", function () {
    const themeButton = document.getElementById("theme-button");
    const dropdown = document.getElementById("dropdown");
    const buttons = document.querySelectorAll("#dropdown button");

    if (themeButton && dropdown) {
        themeButton.addEventListener("click", function () {
            dropdown.style.display = dropdown.style.display === "block" ? "none" : "block";
        });

        document.addEventListener("click", function (e) {
            if (!themeButton.contains(e.target) && !dropdown.contains(e.target)) {
                dropdown.style.display = "none";
            }
        });
    }

    function applyTheme(theme) {
        document.body.classList.remove("light", "dark", "motivating");
        document.body.classList.add(theme);
        localStorage.setItem("selectedTheme", theme);
    }

    // Відправляємо тему на сервер
    function sendThemeToServer(theme) {
        const formData = new URLSearchParams();
        formData.append('theme', theme);

        fetch("/change-theme/", {
            method: "POST",
            headers: {
                "Content-Type": "application/x-www-form-urlencoded"
            },
            body: formData.toString(),
            credentials: 'same-origin' // якщо треба передавати cookie (залежить від налаштувань)
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === "success") {
                alert("Theme updated successfully on server");
            } else {
                alert("Server error: " + data.message);
            }
        })
        .catch(error => {
            alert("Network error: " + error);
        });
    }

    // Застосування теми при завантаженні
    const savedTheme = localStorage.getItem("selectedTheme") || "light";
    applyTheme(savedTheme);

    buttons.forEach(button => {
        button.addEventListener("click", function (e) {
            e.preventDefault();
            const theme = this.id.replace("-theme", "");
            applyTheme(theme);
            sendThemeToServer(theme);
        });
    });
});


// // Отримуємо елементи
// // Функція для отримання CSRF токена з cookie
// function getCookie(name) {
//   let cookieValue = null;
//   if (document.cookie && document.cookie !== '') {
//     const cookies = document.cookie.split(';');
//     for (let cookie of cookies) {
//       cookie = cookie.trim();
//       if (cookie.startsWith(name + '=')) {
//         cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
//         break;
//       }
//     }
//   }
//   return cookieValue;
// }

// const themeButton = document.getElementById("theme-button");
// const dropdown = document.getElementById("dropdown");

// // Кнопки для вибору теми
// const lightThemeButton = document.getElementById("light-theme");
// const darkThemeButton = document.getElementById("dark-theme");
// const motivatingThemeButton = document.getElementById("motivating-theme");

// // Відкриваємо/закриваємо випадаючий список при натисканні на кнопку
// themeButton.addEventListener("click", function () {
//   dropdown.style.display =
//     dropdown.style.display === "block" ? "none" : "block";
// });

// console.log("CSRF token:", getCookie('csrftoken'));

// // Функція для відправки POST запиту на зміну теми
// function changeTheme(theme) {
//   fetch("/change-theme/", {
//     method: "POST",
//     headers: {
//       "Content-Type": "application/json",
//       "X-CSRFToken": getCookie('csrftoken'),  // беремо CSRF токен з cookie
//     },
//     body: JSON.stringify({ theme: theme })
//   }).then(response => {
//     if (!response.ok) {
//       console.error('Помилка при зміні теми:', response.statusText);
//     }
//   }).catch(error => {
//     console.error('Помилка мережі:', error);
//   });
// }

// // Обробники для вибору тем
// lightThemeButton.addEventListener("click", () => {
//   document.body.classList.remove("dark-theme", "motivating-theme");
//   document.body.classList.add("light-theme");
//   dropdown.style.display = "none";
//   changeTheme("light");
// });

// darkThemeButton.addEventListener("click", () => {
//   document.body.classList.remove("light-theme", "motivating-theme");
//   document.body.classList.add("dark-theme");
//   dropdown.style.display = "none";
//   changeTheme("dark");
// });

// motivatingThemeButton.addEventListener("click", () => {
//   document.body.classList.remove("light-theme", "dark-theme");
//   document.body.classList.add("motivating-theme");
//   dropdown.style.display = "none";
//   changeTheme("motivating");
// });
