sideLinks1.forEach(item => {
    item.addEventListener('click', () => {
        sideLinks1.forEach(i => {
            i.classList.remove('active');
        })
        item.classList.add('active');

        mains.forEach(main => {
            main.classList.add('hide')

            if (main.dataset.name === item.dataset.name) {
                main.classList.remove('hide')
            }
        })
    })
});

boxPrays.forEach(item => {
    item.addEventListener('click', ()=>{
        boxPrays.forEach(item2 => {
            item2.classList.remove('active');
        })
        item.classList.add('active');
        let itemName = item.dataset.name;
        tableBox.forEach(label => {
            let labelName = label.dataset.name;
            label.classList.remove('show');
            if (itemName === labelName) {
                label.classList.add('show')
            }
        })
    })
})

menuBar.addEventListener('click', () => {
    sideBar.classList.toggle('close');
});

window.addEventListener('resize', () => {
    if (window.innerWidth < 768) {
        sideBar.classList.add('close');
    } else {
        sideBar.classList.remove('close');
    }
});

function mode() {
    if (!document.body.classList.contains('dark')) {
        document.body.classList.add('dark');
    } else {
        document.body.classList.remove('dark');
    }
}

toggler.addEventListener('change', mode);

etirozlar.forEach(btn => {
    btn.addEventListener('click', () => {
        if (!btn.classList.contains('active')) {
            etirozlar.forEach(btns => {
                btns.classList.remove('active')
            })
            btn.classList.add('active')
        } else {
            btn.classList.remove('active')
        }
    })
})

function showHide() {
    pswBtn.classList.toggle('bx-lock')
    pswBtn.classList.toggle('bx-lock-open')

    if (pswInput.type == 'password') {
        pswInput.setAttribute('type', 'text')
    } else {
        pswInput.setAttribute('type', 'password')
    }
}

personBtn.forEach(btn => {
    btn.addEventListener('click', () => {
        personBox.forEach(main => {
            let mainBox = main.parentElement;
            mainBox.classList.add('active')
            main.classList.remove('active')

            if (main.dataset.name === btn.dataset.name) {
                main.classList.add('active')
            }

            mainBox.addEventListener('click', (e) => {

                if (e.target.classList.contains('person_box_container')) {
                    mainBox.classList.remove('active')
                    personBox.forEach(i => {
                        i.classList.remove('active')
                    })
                }
            })
        })
    })
});

addBtn.forEach(btn => {
    btn.addEventListener('click', () => {
        addBox.forEach(main => {
            let mainBox = main.parentElement;
            mainBox.classList.add('active')
            main.classList.remove('active')

            if (main.dataset.label === btn.dataset.label) {
                main.classList.add('active')
            }

            mainBox.addEventListener('click', (e) => {

                if (e.target.classList.contains('add_box_container')) {
                    mainBox.classList.remove('active')
                    addBox.forEach(i => {
                        i.classList.remove('active')
                    })
                }
            })
        })
    })
});

window.addEventListener('unload', () => {
    if (document.body.classList.contains('dark')) {
        localStorage.setItem('mode', 'dark')
    } else {
        localStorage.setItem('mode', 'light')
    }
})

document.addEventListener('DOMContentLoaded', function () {

    window.addEventListener('load', () => {
        let getMode = localStorage.getItem('mode')
        if (getMode == 'dark') {
            toggler.click();
        }

        var table = document.getElementById('myTable3');
        var rows = table.getElementsByTagName('tbody')[0].getElementsByTagName('tr');

        // Проходим по каждой строке таблицы
        for (var i = 0; i < rows.length; i++) {
            var row = rows[i];

            // Получаем значения foiz-narxi и soni
            var foizNarxi = parseFloat(row.querySelector('[data-active="foiz-narxi"]').innerText.replace('so`m', '').trim());
            var soni = parseFloat(row.querySelector('[data-active="soni"]').innerText.replace('ta', '').trim());

            // Вычисляем summa
            var summa = foizNarxi * soni;

            // Вставляем результат в data-active="summa"
            row.querySelector('[data-active="summa"]').innerText = summa.toFixed(2) + 'so`m';
        }
    })

    var narxiInput = document.getElementById('narxi');
    var foizInput = document.getElementById('foiz');
    var foizNarxiInput = document.getElementById('foiz_narxi');

        // Обработчик события ввода для полей narxi и foiz
    narxiInput.addEventListener('input', updateFoizNarxi);
    foizInput.addEventListener('input', updateFoizNarxi);

    function updateFoizNarxi() {
            // Получаем значения narxi и foiz
            var narxiValue = parseFloat(narxiInput.value) || 0;
            var foizValue = parseFloat(foizInput.value) || 0;

            // Вычисляем новое значение foiz_narxi
            var foizNarxiValue = narxiValue * ((100 + foizValue) / 100);

            // Устанавливаем новое значение в поле foiz_narxi
            foizNarxiInput.value = foizNarxiValue.toFixed(2);
    }
    
    function updateAllProductCount() {
        const allProductCountValue = tableList.querySelectorAll('tr').length;
        zakazSoni.textContent = `${allProductCountValue} xil`;
    }
});

// Функция для обработки нажатия кнопки "Изменить"
function editData() {
    // Реализуйте здесь логику изменения данных
    alert("Логика изменения данных. Замените этот алерт своей логикой.");
}