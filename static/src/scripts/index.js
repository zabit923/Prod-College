import { updateSlider } from "../utils/slider.js";
import adaptiveSlider from "../utils/adaptive-slider.js";

// registration();

//BURGER MENU////////////////////////////////////////////////////////////////////


const burgerBtn = document.getElementById('header_burger');
const headerMenu = document.getElementById('nav_right_path');
const footerTG = document.getElementById('footer_telegram');
const footerVK = document.getElementById('footer_vk');
const line = document.getElementById('footer_line');
const main = document.querySelector('main');
const footer = document.querySelector('footer');
const slider = document.getElementById('slider');

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

//  ////////////////////////////////////////////////////////////////////
