const burgerBtn = document.getElementById('header_burger');
const headerMenu = document.getElementById('nav_right_path');
const footerTG = document.getElementById('footer_telegram');
const footerVK = document.getElementById('footer_vk');
const line = document.getElementById('footer_line');
const main = document.querySelector('main');
const footer = document.querySelector('footer');
const slider = document.getElementById('slider');


///////////////////////////////////////////////////////////////////

burgerBtn.addEventListener('click', () => {
    headerMenu.classList.toggle('active');

    if (headerMenu.classList.contains('active')) {
        burgerBtn.style.backgroundImage = 'url("/static/src/images/cross.png")';
        document.body.removeChild(main);
        document.body.removeChild(footer);
        slider.style.display = 'none';
    } else {
        burgerBtn.style.backgroundImage = 'url("/static/src/images/burger.svg")';
        document.body.appendChild(main);
        document.body.appendChild(footer);
        slider.style.display = 'block';
    }
})




const linksDropdown = document.getElementById('drop_down_link_list'),
      btnDropdown = document.getElementById('btn_important_links'),
      addLink = document.getElementById('add_link'),
      btnAddLink = document.getElementById('btn_add_link');



document.addEventListener('click', (e) => {
    const withinBoundaries = e.target.closest('#drop_down_link_list') || e.target.id === 'btn_important_links';
    const withinBoundaries2 = e.target.closest('#add_link') || e.target.id === 'btn_add_link';

    if (!withinBoundaries && !withinBoundaries2) {
        linksDropdown.classList.remove('active');
        addLink.classList.remove('active');
    }
});

document.addEventListener('keydown', (e) => {
	if( e.keyCode == 27 ){
		linksDropdown.classList.remove('active');
        addLink.classList.remove('active');
	}
});

btnAddLink.addEventListener('click', (event) => {
    event.preventDefault();

    addLink.classList.toggle('active');
})

btnDropdown.addEventListener('click', (event) => {
    event.preventDefault();

    linksDropdown.classList.toggle('active');
})

function updateLastListItemStyle() {
    const allListItems = document.querySelectorAll('.drop_down_link_list li');

    if (allListItems.length > 0) {
        for (let i = 0; i < allListItems.length - 1; i++) {
            allListItems[i].style.borderBottom = '1px solid black';
        }

        allListItems[allListItems.length - 1].style.border = 'none';
    }
    return
}

updateLastListItemStyle();



///////////////////////////////////////////////////////////////////////////////


const linksDropdown_ = document.getElementById('drop_down_link_list_');
const btnDropdown_ = document.getElementById('btn_important_links_');
const addLink_ = document.getElementById('add_link_');
const btnAddLink_ = document.getElementById('btn_add_link_');

document.addEventListener('click', (e) => {
    const withinBoundaries_ = e.target.closest('#drop_down_link_list_') || e.target.id === 'btn_important_links_';
    const withinBoundaries2_ = e.target.closest('#add_link_') || e.target.id === 'btn_add_link_';

    if (!withinBoundaries_ && !withinBoundaries2_) {
        linksDropdown_.classList.remove('active');
        if (addLink) {
            addLink_.classList.remove('active');
        }
    }
});

document.addEventListener('keydown', (e) => {
    if (e.keyCode == 27) { // код клавиши Escape
        linksDropdown_.classList.remove('active');
        if (addLink) {
            addLink_.classList.remove('active');
        }
    }
});

if (btnAddLink_) {
    btnAddLink_.addEventListener('click', (event) => {
        event.preventDefault();
        if (addLink_) {
            addLink_.classList.toggle('active');
        }
    });
}

if (btnDropdown_) {
    btnDropdown_.addEventListener('click', (event) => {
        event.preventDefault();
        linksDropdown_.classList.toggle('active');
    });
}

function updateLastListItemStyle_() {
    const allListItems_ = document.querySelectorAll('.drop_down_link_list_ li');

    if (allListItems_.length > 0) {
        for (let i = 0; i < allListItems_.length - 1; i++) {
            allListItems_[i].style.borderBottom = '1px solid black';
        }

        allListItems_[allListItems_.length - 1].style.border = 'none';
    }
    return;
}

updateLastListItemStyle_();