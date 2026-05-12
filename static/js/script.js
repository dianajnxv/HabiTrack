document.addEventListener("DOMContentLoaded", () => {
  const alerts = document.querySelectorAll(".alert");
  alerts.forEach((alert) => {
    setTimeout(() => {
      if (typeof bootstrap !== "undefined") {
        const bsAlert = new bootstrap.Alert(alert);
        bsAlert.close();
      }
    }, 5000);
  });

  const addHabitModal = document.getElementById("addHabit");
  if (addHabitModal) {
    addHabitModal.addEventListener("hidden.bs.modal", function () {
      const form = this.querySelector("form");
      if (form) form.reset();
    });
  }

  document.querySelectorAll('a[href^="/#"]').forEach((anchor) => {
    anchor.addEventListener("click", function (e) {
      const targetId = this.getAttribute("href").split("#")[1];
      const targetElement = document.getElementById(targetId);

      if (targetElement && window.location.pathname === "/") {
        e.preventDefault();
        targetElement.scrollIntoView({
          behavior: "smooth",
        });
      }
    });
  });
});
