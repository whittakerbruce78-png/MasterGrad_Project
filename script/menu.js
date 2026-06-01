document.getElementById("menu-btn").addEventListener("click", function (event) {
    let sidebar = document.getElementById("sidebar");
    // Проверяем текущее положение sidebar
    if (sidebar.style.left === "0px" || sidebar.style.left === "") {
        sidebar.style.left = "-250px"; // Закрываем, если открыто
    } else {
        sidebar.style.left = "0"; // Открываем, если закрыто
    }
    event.stopPropagation(); // Останавливаем всплытие клика
});

document.querySelector(".close-btn").addEventListener("click", function () {
    document.getElementById("sidebar").style.left = "-250px"; // Закрываем меню
});

// Закрытие при клике вне меню
document.addEventListener("click", function (event) {
    let sidebar = document.getElementById("sidebar");
    let menuBtn = document.getElementById("menu-btn");
    
    // Проверяем, кликнули ли НЕ на меню и НЕ на кнопку "Меню"
    if (!sidebar.contains(event.target) && !menuBtn.contains(event.target)) {
        sidebar.style.left = "-250px"; // Закрываем меню
    }
});