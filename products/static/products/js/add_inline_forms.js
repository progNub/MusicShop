// Добавляем обработчик события, который будет выполняться после полной загрузки содержимого документа
document.addEventListener('DOMContentLoaded', function () {
    // Получаем элементы страницы: кнопку добавления формы, контейнер для форм и шаблон пустой формы
    const addButton = document.getElementById('add-form-btn');
    const container = document.getElementById('formset-container');
    const emptyFormTemplate = document.getElementById('empty-form-template').innerHTML;

    // Находим скрытый input, который хранит общее количество форм
    let totalForms = document.querySelector('input[name$="TOTAL_FORMS"]');
    // Определяем текущее количество форм в контейнере
    let formCount = container.getElementsByClassName('inline-form').length;

    // Добавляем обработчик события клика на кнопку добавления формы
    addButton.addEventListener('click', function () {
        // Создаем новую форму, заменяя плейсхолдер __prefix__ на текущее количество форм
        let newForm = emptyFormTemplate.replace(/__prefix__/g, formCount);
        // Вставляем новую форму в конец контейнера
        container.insertAdjacentHTML('beforeend', newForm);
        // Увеличиваем общее количество форм и обновляем значение в скрытом input
        totalForms.setAttribute('value', `${++formCount}`)
    });

    // Добавляем обработчик события клика на контейнер форм
    container.addEventListener('click', function (e) {
        // Проверяем, содержит ли элемент, по которому был совершен клик, класс кнопки удаления формы
        if (e.target.classList.contains('remove-form-btn')) {
            // Удаляем родительский элемент кнопки, тем самым удаляя форму
            e.target.parentNode.parentNode.remove();
            // Уменьшаем общее количество форм и обновляем значение в скрытом input
            totalForms.setAttribute('value', `${--formCount}`)
        }
    });
});