function switch_attribute_hidden(element) {
    if (element.hasAttribute('hidden')) {
        element.removeAttribute('hidden');
    } else {
        element.setAttribute('hidden', 'hidden');
    }
}

function switch_attribute_class(element, attr_class) {
    if (element.classList.contains(attr_class)) {
        element.classList.remove(attr_class)
    } else {
        element.classList.add(attr_class)
    }
}

function attribute_name_add_or_remove_delete(element) {
    let name = element.getAttribute('name')
    if (name.includes('#delete#', 0)) {
        element.setAttribute('name', name.replace('#delete#', '', 0))
    } else {
        element.setAttribute('name', '#delete#' + name)
    }
}

document.addEventListener('DOMContentLoaded', function () {
    let editButtons = document.querySelectorAll('.edit-button');
    let isEditing = false; // Переменная для отслеживания режима редактирования

    editButtons.forEach(function (button) {
        button.addEventListener('click', function () {
            isEditing = true; // Устанавливаем режим редактирования
            const accordionItem = button.closest('.accordion-item');
            let actionButtons = accordionItem.querySelectorAll('.action-button');
            let inputs = accordionItem.querySelectorAll('.input-action');

            let button_to_add_input_item_1 = accordionItem.querySelectorAll('.btn-add-catalog-item-1')
            let button_to_add_input_item_2 = accordionItem.querySelectorAll('.btn-add-catalog-item-2')
            let button_to_delete = accordionItem.querySelectorAll('.delete_item')


            actionButtons.forEach(function (button) {
                if (button.hasAttribute('disabled')) {
                    button.removeAttribute('disabled');

                } else {
                    button.setAttribute('disabled', 'disabled');
                }
            });

            inputs.forEach(function (input) {
                if (input.hasAttribute('disabled')) {
                    input.removeAttribute('disabled');
                } else {
                    input.setAttribute('disabled', 'disabled');
                }
            });
            button_to_add_input_item_2.forEach(function (button) {
                switch_attribute_hidden(button)
            });
            button_to_add_input_item_1.forEach(function (button) {
                switch_attribute_hidden(button)
            });
            button_to_delete.forEach(function (button) {
                switch_attribute_hidden(button)
            });
        });
    });

    // Назначение кнопкам отправить возможность отправлять соответствующую форму.
    let submitButtons = document.querySelectorAll('.submit-btn')
    submitButtons.forEach(function (submitButton) {
        let formId = submitButton.getAttribute("data-form-id");
        let form = document.getElementById(formId);
        submitButton.addEventListener("click", function () {
            // Проверяем, в режиме редактирования или нет
            if (isEditing) {
                form.submit();
            } else {
                alert("Вы должны находиться в режиме редактирования перед отправкой формы.");
            }
        });
    });

    // Назначение кнопкам ".btn-add-catalog-item-2" возможность добавления новых inputs
    let button_add_input_item_2 = document.querySelectorAll('.btn-add-catalog-item-2')
    let number_input_2 = 0
    button_add_input_item_2.forEach(function (button) {
        button.addEventListener("click", function () {
            number_input_2 += 1
            let container = button.parentNode.parentNode.querySelector('.common-container-catalog-item1-item2')
            let data_slug_parent = container.querySelector('input').getAttribute('id')

            let new_name = `#new#${number_input_2}#${data_slug_parent}`;
            let empty_template = document.getElementById('empty_input_catalog_item_2')
            let input = empty_template.querySelector('input')

            input.setAttribute('name', new_name);
            input.setAttribute('id', new_name);
            container.insertAdjacentHTML('beforeend', empty_template.innerHTML);
        });
    });

    let button_add_input_item_1 = document.querySelectorAll('.btn-add-catalog-item-1')
    let number_input_1 = 0
    button_add_input_item_1.forEach(function (button) {
        button.addEventListener("click", function () {
            number_input_1 += 1
            let container = button.closest('form').querySelector('div')
            let data_slug_parent = container.closest('form').getAttribute('id')


            let empty_template = document.getElementById('empty_input_catalog_item_1');
            let input = empty_template.querySelector('input')
            let new_name = `#new#${number_input_1}#${data_slug_parent}`;
            input.setAttribute('name', new_name);
            input.setAttribute('id', new_name);

            container.insertAdjacentHTML('beforeend', empty_template.innerHTML);


        });
    });

    let button_to_delete = document.querySelectorAll('.delete_item')
    button_to_delete.forEach(function (button) {
        button.addEventListener("click", function () {
            let is_catalog_item_1 = button.closest('.catalog-item-1-name')

            if (is_catalog_item_1) {
                let input_item_1 = button.parentNode.querySelector('input')
                attribute_name_add_or_remove_delete(input_item_1)
                let inputs = button.closest('.common-container-catalog-item1-item2')
                    .querySelector('.catalog-item-2')
                    .querySelectorAll('input')

                if (input_item_1.classList.contains('item_text_deleted')) {
                    input_item_1.classList.remove('item_text_deleted')

                    inputs.forEach(function (input) {
                        input.classList.remove('item_text_deleted')
                        input.removeAttribute('disabled')
                        let button_delete = input.parentNode.querySelector('.delete_item')
                        button_delete.removeAttribute('disabled')


                    });
                } else {
                    input_item_1.classList.add('item_text_deleted')
                    inputs.forEach(function (input) {
                        input.classList.add('item_text_deleted')
                        input.setAttribute('disabled', 'disabled')
                        let button_delete = input.parentNode.querySelector('.delete_item')
                        button_delete.setAttribute('disabled', 'disabled')
                        button_delete.style.border = '0';


                    });
                }
            } else {
                let input = button.parentNode.querySelector('input')
                switch_attribute_class(input, 'item_text_deleted')
                attribute_name_add_or_remove_delete(input)
            }
        });
    });
});




