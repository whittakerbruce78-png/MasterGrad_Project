document.addEventListener("DOMContentLoaded", function () {
    // Find the relative prefix to root dynamically
    const scripts = document.getElementsByTagName('script');
    let relPrefix = './';
    for (let i = 0; i < scripts.length; i++) {
        const src = scripts[i].getAttribute('src');
        if (src && src.includes('reviews.js')) {
            const idx = src.indexOf('script/reviews.js');
            if (idx !== -1) {
                relPrefix = src.substring(0, idx);
            }
            break;
        }
    }

    const reviews = [
        {
            avatar: relPrefix + "img/avatar1.jpg",
            name: "Алексей",
            partner: relPrefix + "img/partner1.svg",
            stars: relPrefix + "img/stars.svg",
            text: "Ремонт стиральной машины произведен, быстро. Назвали цену по телефону. Мастер приехал в течении 2-х часов после обращения.Рекомендую!"
        },
        {
            avatar: relPrefix + "img/avatar8.jpg",
            name: "Никита Дронов",
            partner: relPrefix + "img/partner2.png",
            stars: relPrefix + "img/stars.svg",
            text: "Спасибо большое. Все отлично. Ремонтировали холодильник. Приезжал мастер Евгений."
        },
        {
            avatar: relPrefix + "img/avatar2.jpg",
            name: "Дмитрий Кравченко",
            partner: relPrefix + "img/partner1.svg",
            stars: relPrefix + "img/stars.svg",
            text: "Мастер приехал вовремя, работа выполнена оперативно, за один визит. Качественно. Доволен результатом."
        },
        {
            avatar: relPrefix + "img/avatar7.jpg",
            name: "Сергей",
            partner: relPrefix + "img/partner2.png",
            stars: relPrefix + "img/stars.svg",
            text: "Вызвали мастера через 2 ГИС. Назвали поломку по телефону, цена осталась такой же, без изменений. Мастер приехал в удобное нам время. Спасибо Роману."
        },
        {
            avatar: relPrefix + "img/avatar3.jpg",
            name: "Анна Смирнова",
            partner: relPrefix + "img/partner1.svg",
            stars: relPrefix + "img/stars.svg",
            text: "О цене ремонта сказали по телефону, такая она и осталась. За ремонт холодильника заплатили 4500р. Была замена патрубков и заправка. Довольна работой."
        },
        {
            avatar: relPrefix + "img/avatar6.jpg",
            name: "Андрей",
            partner: relPrefix + "img/partner2.png",
            stars: relPrefix + "img/stars.svg",
            text: "Привезли плату на перепайку в мастерскую. Починили за 2 дня. Проверили. Дали гарантийный талон."
        },
        {
            avatar: relPrefix + "img/avatar4.jpg",
            name: "Кристина Соболева",
            partner: relPrefix + "img/partner1.svg",
            stars: relPrefix + "img/stars.svg",
            text: "Хорошая компания, обращались к ним по ремонту стиральной машины и посудомойки. Ремонтом остались довольны. За два дня решили проблемы. Спасибо."
        },
        {
            avatar: relPrefix + "img/avatar5.jpg",
            name: "Александр Малахов",
            partner: relPrefix + "img/partner1.svg",
            stars: relPrefix + "img/stars.svg",
            text: "Все отлично. Рекомендую."
        },
        {
            avatar: relPrefix + "img/avatar9.jpg",
            name: "Ирина",
            partner: relPrefix + "img/partner1.svg",
            stars: relPrefix + "img/stars.svg",
            text: "Спасибо Алексею за проделанную работу, во время работы все время был на связи. По ходу работы было общение, мастер вежливый."
        },
        {
            avatar: relPrefix + "img/avatar10.jpg",
            name: "Торты на заказ",
            partner: relPrefix + "img/partner1.svg",
            stars: relPrefix + "img/stars.svg",
            text: "Спасибо,работа по ремонту посудомоечной машины проделала отлично. Мастер Артем отличный,сделал все качественно,нашел причину неисправности,заменил блок управления."
        },
        {
            avatar: relPrefix + "img/avatar11.jpg",
            name: "Елена HR",
            partner: relPrefix + "img/partner1.svg",
            stars: relPrefix + "img/stars.svg",
            text: "Пунктуальные, энергичные ребята, договорись о стоимости ремонта по телефону, стоимость не прибавилась. Спасибо."
        },
        {
            avatar: relPrefix + "img/avatar12.jpg",
            name: "Дима",
            partner: relPrefix + "img/partner2.png",
            stars: relPrefix + "img/stars.svg",
            text: "Мастер быстро ответил,оперативно и качественно выполнил свою работу,дал необходимые пояснения,цена соответствует рынку. Заказывала через 2 ГИС."
        },
        {
            avatar: relPrefix + "img/avatar13.jpg",
            name: "Ильнур",
            partner: relPrefix + "img/partner2.png",
            stars: relPrefix + "img/stars.svg",
            text: "Спасибо,работает👍"
        },
        {
            avatar: relPrefix + "img/avatar14.jpg",
            name: "Светлана Шелестова",
            partner: relPrefix + "img/partner3.png",
            stars: relPrefix + "img/stars.svg",
            text: "Благодарим мастера Бориса,заменил тены в водонагревателе, приехал сразу с запчастями."
        },
        {
            avatar: relPrefix + "img/avatar15.jpg",
            name: "Anastasia",
            partner: relPrefix + "img/partner1.svg",
            stars: relPrefix + "img/stars.svg",
            text: "Отличный мастер,починил холодильник быстро и качественно!!!"
        },
        {
            avatar: relPrefix + "img/avatar16.jpg",
            name: "Егор",
            partner: relPrefix + "img/partner2.png",
            stars: relPrefix + "img/stars.svg",
            text: "Мастер аккуратно провел диагностику,кондиционера, выявил проблему, показа. Работой полностью довольны."
        },
        {
            avatar: relPrefix + "img/avatar17.jpg",
            name: "Данил Пикалов",
            partner: relPrefix + "img/partner2.png",
            stars: relPrefix + "img/stars.svg",
            text: "Услуга оказана качественно!!!👌"
        },
        {
            avatar: relPrefix + "img/avatar18.jpg",
            name: "Lisa97",
            partner: relPrefix + "img/partner1.svg",
            stars: relPrefix + "img/stars.svg",
            text: "Большое спасибо мастеру Евгению, за ремонт стиральной машины, меняли подшипники,работой очень довольны."
        },
        {
            avatar: relPrefix + "img/avatar19.jpg",
            name: "ФураЦентр125",
            partner: relPrefix + "img/partner1.svg",
            stars: relPrefix + "img/stars.svg",
            text: "Цена соответствовала.Работа выполнена качественно. Исполнено быстро и грамотно. Спасибо."
        }
    ];

    const reviewsContainer = document.getElementById("reviews-container");
    if (!reviewsContainer) return;

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
