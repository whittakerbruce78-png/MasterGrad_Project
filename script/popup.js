document.addEventListener("DOMContentLoaded", function () {
    // Показываем всплывающее окно через 40 секунд
    setTimeout(function () {
        document.getElementById("popup").style.display = "flex";
    }, 40000); // 40 секунд

    // Закрытие всплывающего окна по кнопке
    document.getElementById("close-popup").addEventListener("click", function () {
        document.getElementById("popup").style.display = "none";
    });

    // Закрытие при клике вне окна
    document.getElementById("popup").addEventListener("click", function (event) {
        if (event.target === this) {
            this.style.display = "none";
        }
    });
	
	document.querySelectorAll(".issue-item").forEach(item => {
    item.addEventListener("click", function (event) {
        event.preventDefault(); // Предотвращаем переход по ссылке
        document.getElementById("popup").style.display = "flex";
    });
    });

    // Обработка отправки формы
    document.getElementById("popup-call-master-form").addEventListener("submit", async function (event) {
        event.preventDefault(); // Остановка стандартной отправки формы

        const token = "7614592363:AAEquIotRbbKNOUZRu_SEy2LtIhakd_UBz4"; // Ваш Telegram токен
        const chat_id = "7254104419"; // Ваш Chat ID
        const url = `https://api.telegram.org/bot${token}/sendMessage`;

        const phoneInput = document.getElementById("popup-phone");
        const phone = phoneInput.value.trim();

        // Проверка: пустое поле
        if (phone === "") {
            alert("Поле номера телефона не должно быть пустым!");
            return;
        }

        // Проверка: допустимые символы (только + и цифры)
        if (!/^\+?\d{9,12}$/.test(phone)) {
            alert("Введите корректный номер телефона!");
            return;
        }

        const message = `<b>Заявка на консультацию</b>%0A<b>Телефон:</b> ${phone}`;

        try {
            const response = await fetch(url, {
                method: "POST",
                headers: { "Content-Type": "application/x-www-form-urlencoded" },
                body: new URLSearchParams({
                    chat_id: chat_id,
                    parse_mode: "HTML",
                    text: message
                })
            });

            if (response.ok) {
                alert("Заявка успешно отправлена!");
                phoneInput.value = ""; // Очистка поля
                document.getElementById("popup").style.display = "none"; // Закрытие всплывающего окна
                window.location.href = "../спасибо"; // Замени на нужный URL
            } else {
                throw new Error("Ошибка отправки");
            }
        } catch (error) {
            console.error("Ошибка:", error);
            alert("Ошибка отправки заявки");
        }
    });
});
