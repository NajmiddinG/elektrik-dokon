const navList = document.querySelectorAll('.navigation ul li'),
    toggler = document.getElementById('theme-toggle'),
    loyihalar = document.querySelectorAll('.loyihalar li');

navList.forEach(list => {
    list.addEventListener('click', () => {
        navList.forEach(i => {
            i.classList.remove('active')
        })
        list.classList.add('active')
    })
})

function mode() {
    if (!document.body.classList.contains('dark')) {
        document.body.classList.add('dark');
    } else {
        document.body.classList.remove('dark');
    }
}

toggler.addEventListener('change', mode);

loyihalar.forEach(btn => {
    btn.addEventListener('click', () => {
        loyihalar.forEach(btns => {
            btns.classList.remove('active')
        })
        btn.classList.add('active')
    })
})

window.addEventListener('unload', () => {
    if (document.body.classList.contains('dark')) {
        localStorage.setItem('mode', 'dark')
    } else {
        localStorage.setItem('mode', 'light')
    }
})

window.addEventListener('load', () => {
    let getMode = localStorage.getItem('mode')
    if (getMode == 'dark') {
        toggler.click();
    }
})