document.getElementById("call-master-form").addEventListener("submit", async function (event) {
    event.preventDefault(); // Остановка стандартной отправки формы

    const token = "7614592363:AAEquIotRbbKNOUZRu_SEy2LtIhakd_UBz4"; // Ваш Telegram токен
    const chat_id = "7254104419"; // Ваш Chat ID
    const url = `https://api.telegram.org/bot${token}/sendMessage`;

    const phoneInput = document.getElementById("phone");
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
            window.location.href = "../спасибо"; // Замени на нужный URL
        } else {
            throw new Error("Ошибка отправки");
        }
    } catch (error) {
        console.error("Ошибка:", error);
        alert("Ошибка отправки заявки");
    }
});