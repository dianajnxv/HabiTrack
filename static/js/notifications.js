const Toast = {
  show(message, type = "success") {
    const icons = {
      success: `<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 6L9 17l-5-5"/></svg>`,
      error: `<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="15" y1="9" x2="9" y2="15"/><line x1="9" y1="9" x2="15" y2="15"/></svg>`,
      warning: `<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>`,
      info: `<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="12" y1="16" x2="12" y2="12"/><line x1="12" y1="8" x2="12.01" y2="8"/></svg>`,
    };

    const config = {
      success: { bg: "linear-gradient(to right, #10b981, #059669)" },
      error: { bg: "linear-gradient(to right, #f43f5e, #e11d48)" },
      warning: { bg: "linear-gradient(to right, #f59e0b, #d97706)" },
      info: { bg: "linear-gradient(to right, #6366f1, #4f46e5)" },
    };

    const style = config[type] || config.success;
    const icon = icons[type] || icons.success;

    const toastElement = document.createElement("div");
    toastElement.style.display = "flex";
    toastElement.style.alignItems = "center";
    toastElement.style.gap = "12px";
    toastElement.innerHTML = `${icon} <span>${message}</span>`;

    Toastify({
      node: toastElement,
      duration: 4000,
      close: true,
      gravity: "top",
      position: "right",
      style: {
        background: style.bg,
        borderRadius: "12px",
        fontSize: "14px",
        fontWeight: "500",
        boxShadow: "0 10px 15px -3px rgba(0, 0, 0, 0.15)",
        padding: "12px 20px",
        zIndex: 9999,
        color: "#ffffff",
      },
    }).showToast();
  },
};
