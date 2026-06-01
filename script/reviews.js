document.addEventListener("DOMContentLoaded", function () {
    const reviews = [
        {
            avatar: "/img/avatar1.jpg",
            name: "Алексей",
            partner: "/img/partner1.svg",
            stars:"/img/stars.svg",
            text: "Ремонт стиральной машины произведен, быстро. Назвали цену по телефону. Мастер приехал в течении 2-х часов после обращения.Рекомендую!"
        },
        {
            avatar: "/img/avatar8.jpg",
            name: "Никита Дронов",
            partner: "/img/partner2.png",
            stars: "/img/stars.svg",
            text: "Спасибо большое. Все отлично. Ремонтировали холодильник. Приезжал мастер Евгений."
        },
        {
            avatar: "/img/avatar2.jpg",
            name: "Дмитрий Кравченко",
            partner: "/img/partner1.svg",
            stars: "/img/stars.svg",
            text: "Мастер приехал вовремя, работа выполнена оперативно, за один визит. Качественно. Доволен результатом."
        },
        {
            avatar: "/img/avatar7.jpg",
            name: "Сергей",
            partner: "/img/partner2.png",
            stars: "/img/stars.svg",
            text: "Вызвали мастера через 2 ГИС. Назвали поломку по телефону, цена осталась такой же, без изменений. Мастер приехал в удобное нам время. Спасибо Роману."
        },
        {
            avatar: "/img/avatar3.jpg",
            name: "Анна Смирнова",
            partner: "/img/partner1.svg",
            stars: "/img/stars.svg",
            text: "О цене ремонта сказали по телефону, такая она и осталась. За ремонт холодильника заплатили 4500р. Была замена патрубков и заправка. Довольна работой."
        },
        {
            avatar: "/img/avatar6.jpg",
            name: "Андрей",
            partner: "/img/partner2.png",
            stars: "/img/stars.svg",
            text: "Привезли плату на перепайку в мастерскую. Починили за 2 дня. Проверили. Дали гарантийный талон."
        },
        {
            avatar: "/img/avatar4.jpg",
            name: "Кристина Соболева",
            partner: "/img/partner1.svg",
            stars: "/img/stars.svg",
            text: "Хорошая компания, обращались к ним по ремонту стиральной машины и посудомойки. Ремонтом остались довольны. За два дня решили проблемы. Спасибо."
        },
        {
            avatar: "/img/avatar5.jpg",
            name: "Александр Малахов",
            partner: "/img/partner1.svg",
            stars: "/img/stars.svg",
            text: "Все отлично. Рекомендую."
        },
        {
            avatar: "/img/avatar9.jpg",
            name: "Ирина",
            partner: "/img/partner1.svg",
            stars: "/img/stars.svg",
            text: "Спасибо Алексею за проделанную работу, во время работы все время был на связи. По ходу работы было общение, мастер вежливый."
        },
        {
            avatar: "/img/avatar10.jpg",
            name: "Торты на заказ",
            partner: "/img/partner1.svg",
            stars: "/img/stars.svg",
            text: "Спасибо,работа по ремонту посудомоечной машины проделала отлично. Мастер Артем отличный,сделал все качественно,нашел причину неисправности,заменил блок управления."
        },
        {
            avatar: "/img/avatar11.jpg",
            name: "Елена HR",
            partner: "/img/partner1.svg",
            stars: "/img/stars.svg",
            text: "Пунктуальные, энергичные ребята, договорись о стоимости ремонта по телефону, стоимость не прибавилась. Спасибо."
        },
        {
            avatar: "/img/avatar12.jpg",
            name: "Дима",
            partner: "/img/partner2.png",
            stars: "/img/stars.svg",
            text: "Мастер быстро ответил,оперативно и качественно выполнил свою работу,дал необходимые пояснения,цена соответствует рынку. Заказывала через 2 ГИС."
        },
        {
            avatar: "/img/avatar13.jpg",
            name: "Ильнур",
            partner: "/img/partner2.png",
            stars: "/img/stars.svg",
            text: "Спасибо,работает👍"
        },
        {
            avatar: "/img/avatar14.jpg",
            name: "Светлана Шелестова",
            partner: "/img/partner3.png",
            stars: "/img/stars.svg",
            text: "Благодарим мастера Бориса,заменил тены в водонагревателе, приехал сразу с запчастями."
        },
        {
            avatar: "/img/avatar15.jpg",
            name: "Anastasia",
            partner: "/img/partner1.svg",
            stars: "/img/stars.svg",
            text: "Отличный мастер,починил холодильник быстро и качественно!!!"
        },
        {
            avatar: "/img/avatar16.jpg",
            name: "Егор",
            partner: "/img/partner2.png",
            stars: "/img/stars.svg",
            text: "Мастер аккуратно провел диагностику,кондиционера, выявил проблему, показа. Работой полностью довольны."
        },
        {
            avatar: "/img/avatar17.jpg",
            name: "Данил Пикалов",
            partner: "/img/partner2.png",
            stars: "/img/stars.svg",
            text: "Услуга оказана качественно!!!👌"
        },
        {
            avatar: "/img/avatar18.jpg",
            name: "Lisa97",
            partner: "/img/partner1.svg",
            stars: "/img/stars.svg",
            text: "Большое спасибо мастеру Евгению, за ремонт стиральной машины, меняли подшипники,работой очень довольны."
        },
        {
            avatar: "/img/avatar19.jpg",
            name: "ФураЦентр125",
            partner: "/img/partner1.svg",
            stars: "/img/stars.svg",
            text: "Цена соответствовала.Работа выполнена качественно. Исполнено быстро и грамотно. Спасибо."
        }
    ];

    const reviewsContainer = document.getElementById("reviews-container");

    reviews.forEach(review => {
        const reviewCard = document.createElement("div");
        reviewCard.classList.add("review-card");

        reviewCard.innerHTML = `
            <div class="review-header">
                <img src="${review.avatar}" alt="Аватар" class="review-avatar">
                <div class="review-name">${review.name}</div>
                <img src="${review.partner}" alt="Партнер" class="review-partner">
            </div>
            <img src="${review.stars}" alt="Рейтинг" class="review-stars">
            <p class="review-text">${review.text}</p>
        `;

        reviewsContainer.appendChild(reviewCard);
    });
});
