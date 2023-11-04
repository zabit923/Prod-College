import { updateSlider } from "../utils/slider.js";
import adaptiveSlider from "../utils/adaptive-slider.js";



///////////////////////////////////////////////////////////////////////////

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
	if( e.keyCode == 27 ){ // код клавиши Escape
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


//BURGER MENU////////////////////////////////////////////////////////////////////


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

//SLIDER////////////////////////////////////////////////////////////////////

if (window.innerWidth < 767) {
    adaptiveSlider();
    footerVK.src = "/static/src/images/newVK.svg";
    footerTG.src = "/static/src/images/newTG.png";
    line.style.height = 0;
} else {
    const prevButton = document.querySelector('.prev-button');
    const nextButton = document.querySelector('.next-button');
    const slides = document.querySelectorAll('.slide');
    let currentIndex = 0;

    function handleNextClick() {
        currentIndex = (currentIndex + 1) % slides.length;
        updateSlider(slides, currentIndex);
    }

    function handlePrevClick() {
        currentIndex = (currentIndex - 1 + slides.length) % slides.length;
        updateSlider(slides, currentIndex);
    }

    nextButton.addEventListener('click', handleNextClick);
    prevButton.addEventListener('click', handlePrevClick);

    updateSlider(slides, currentIndex);
}

 ////////////////////////////////////////////////////////////////////


