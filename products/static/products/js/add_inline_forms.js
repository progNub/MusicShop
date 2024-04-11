document.addEventListener('DOMContentLoaded', function () {
    const addButton = document.getElementById('add-form-btn');
    const container = document.getElementById('formset-container');
    const emptyFormTemplate = document.getElementById('empty-form-template').innerHTML;
    let totalForms = document.querySelector('input[name$="TOTAL_FORMS"]');
    let formCount = container.getElementsByClassName('inline-form').length;

    const updateTotalForms = () => {
        // Обновляем значение TOTAL_FORMS в соответствии с текущим количеством форм
        totalForms.value = formCount.toString();
    };

    addButton.addEventListener('click', function () {
        let newForm = emptyFormTemplate.replace(/__prefix__/g, formCount);
        container.insertAdjacentHTML('beforeend', newForm);
        formCount++;
        updateTotalForms(); // Обновляем TOTAL_FORMS при добавлении формы
    });

    container.addEventListener('click', function (e) {
        if (e.target.classList.contains('remove-form-btn')) {
            e.target.parentNode.parentNode.remove();
            formCount--;
            updateTotalForms(); // Обновляем TOTAL_FORMS при удалении формы
        }
    });

    // Инициализируем TOTAL_FORMS при загрузке страницы
    updateTotalForms();
});