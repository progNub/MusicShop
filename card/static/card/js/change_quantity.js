document.addEventListener('DOMContentLoaded', function () {
    const quantityInputs = document.querySelectorAll('.quantity-input');

    quantityInputs.forEach(input => {
        input.addEventListener('input', function () {
            const form = this.closest('.update-cart-form');
            const quantity = parseFloat(this.value); // Преобразуем строку в число
            const priceDisplay = form.querySelector('.product-price');
            const originalPrice = this.getAttribute('data-price');
            console.log(originalPrice)
            if (isNaN(quantity) || quantity < 0) { // Проверяем, является ли результат числом и не отрицательным
                console.error('Количество продуктов должно быть положительным числом');
                this.value = '1'; // Очищаем поле ввода, если введено недопустимое значение
                priceDisplay.textContent = originalPrice
            } else {
                // Ваш код для обработки корректного значения


                const productId = this.getAttribute('data-product-id');
                const url = this.getAttribute('data-url')
                const csrfToken = form.querySelector('[name=csrfmiddlewaretoken]').value;


                fetch(url, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': csrfToken
                    },
                    body: JSON.stringify({productId: productId, quantity: quantity})
                })
                    .then(response => {
                        if (!response.ok) {
                            throw new Error('Network response was not ok');
                        }
                        return response.json();
                    })
                    .then(data => {
                        // сервер возвращает новое количество и новую цену
                        // Обновляем отображаемое количество и цену на странице
                        input.value = data.new_quantity; // Обновляем значение в поле ввода количества
                        priceDisplay.textContent = data.new_price; // Обновляем отображаемую цену
                    })
                    .catch(error => {
                        console.error('Ошибка при выполнении запроса:', error);
                    });

            }
        });
    });
});