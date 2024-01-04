document.addEventListener('DOMContentLoaded', function () {
    const loyihalar = document.querySelectorAll('.loyihalar li');
    const maxsulotlar = document.querySelectorAll('.maxsulotlar li');
    const addBtn = document.querySelectorAll('.add-button');
    const addBox = document.querySelectorAll('.add_box_container .add_box');

    maxsulotlar.forEach(item => {
        let itemSpan = item.querySelectorAll(".soni span")
        let itemInput = item.querySelector(".soni .input input")
        let umumiy = item.querySelector(".umumiy p")

        itemSpan.forEach(label => {
            label.addEventListener('click', () => {
                if (label.classList.contains('minus')) {
                    if (parseInt(itemInput.value) > 0) {
                        itemInput.value = parseInt(itemInput.value) - 1;
                    } else {
                        itemInput.value = 0;
                    }
                } else if (label.classList.contains('plus')) {
                    if (parseInt(itemInput.value) < parseInt(umumiy.textContent)) {
                        itemInput.value = parseInt(itemInput.value) + 1;
                    } else {
                        itemInput.value = parseInt(umumiy.textContent);
                    }
                }
            })
        })
    })

    loyihalar.forEach(btn => {
        btn.addEventListener('click', () => {
            loyihalar.forEach(btns => {
                btns.classList.remove('active')
            })
            btn.classList.add('active')
        })
    })

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
});
