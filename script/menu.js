function initMenu() {
    const menuBtn = document.getElementById("menu-btn");
    const sidebar = document.getElementById("sidebar");
    const closeBtn = document.querySelector(".close-btn");

    if (menuBtn && sidebar) {
        menuBtn.addEventListener("click", function (event) {
            // Если меню открыто (left равен '0px' или '0'), закрываем его.
            // Во всех остальных случаях (например, '-250px' или пустая строка) — открываем.
            if (sidebar.style.left === "0px" || sidebar.style.left === "0") {
                sidebar.style.left = "-250px";
            } else {
                sidebar.style.left = "0px";
            }
            event.stopPropagation();
        });
    }

    if (closeBtn && sidebar) {
        closeBtn.addEventListener("click", function () {
            sidebar.style.left = "-250px";
        });
    }

    document.addEventListener("click", function (event) {
        if (sidebar && menuBtn) {
            if (!sidebar.contains(event.target) && !menuBtn.contains(event.target)) {
                sidebar.style.left = "-250px";
            }
        }
    });
}

if (document.readyState !== "loading") {
    initMenu();
} else {
    document.addEventListener("DOMContentLoaded", initMenu);
}