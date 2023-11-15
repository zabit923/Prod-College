import { updateSlider } from "../utils/slider.js";
import adaptiveSlider from "../utils/adaptive-slider.js";



//BURGER MENU////////////////////////////////////////////////////////////////////


const burgerBtn = document.getElementById('header_burger');
const headerMenu = document.getElementById('nav_right_path');
const footerTG = document.getElementById('footer_telegram');
const footerVK = document.getElementById('footer_vk');
const line = document.getElementById('footer_line');
const main = document.querySelector('main');
const footer = document.querySelector('footer');
const slider = document.getElementById('slider');


//////BURGER    /////////////////////////////////////////////////////////////

burgerBtn.addEventListener('click', () => {
    headerMenu.classList.toggle('active');

    if (headerMenu.classList.contains('active')) {
        burgerBtn.style.backgroundImage = 'url("/static/src/images/cross.png")';
        if (main && footer) {
            document.body.removeChild(main);
            document.body.removeChild(footer);
        }

        if (slider) {
            slider.style.display = 'none';
        }
    } else {
        burgerBtn.style.backgroundImage = 'url("/static/src/images/burger.svg")';
        if (main && footer) {
            document.body.appendChild(main);
            document.body.appendChild(footer);
        }
        if (slider) {
            slider.style.display = 'block';
        }
    }
})

//SLIDER////////////////////////////////////////////////////////////////////

if (window.innerWidth < 767) {
    adaptiveSlider();

    if (footerVK) {
        footerVK.src = "/static/src/images/newVK.svg";
    }
    if (footerTG) {
        footerTG.src = "/static/src/images/newTG.png";
    }
    if (line) {
        line.style.height = 0;
    }

} else {
    const prevButton = document.querySelector('.prev-button'),
          nextButton = document.querySelector('.next-button'),
          slides = document.querySelectorAll('.slide');
    let currentIndex = 0;

    function handleNextClick() {
        currentIndex = (currentIndex + 1) % slides.length;
        updateSlider(slides, currentIndex);
    }

    function handlePrevClick() {
        currentIndex = (currentIndex - 1 + slides.length) % slides.length;
        updateSlider(slides, currentIndex);
    }

    if (nextButton) {
        nextButton.addEventListener('click', handleNextClick);
    }

    if (prevButton) {
        prevButton.addEventListener('click', handlePrevClick);
    }

    updateSlider(slides, currentIndex);
}

////////////////////////////////////////////////////////////////////

const messageDropdown = document.getElementById('drop_down_msg_list'),
      btnStudDropdown = document.getElementById('btn_message');

document.addEventListener('keydown', (e) => {
    if (e.keyCode == 27) { // код клавиши Escape
        messageDropdown.classList.remove('active');
    }
});

if(btnStudDropdown){
    btnStudDropdown.addEventListener('click', (event) => {
        event.preventDefault();
        messageDropdown.classList.toggle('active');
    });
}


function updateLastListItemStyle() {
    const allListItem1 = document.querySelectorAll('.drop_down_msg_list li'),
          allListItem2 = document.querySelectorAll('.drop_down_msg_list_student li'),
          allListItems = [allListItem1, allListItem2];

    allListItems.forEach(el => {
        if (el.length > 0) {
            for (let i = 0; i < el.length - 1; i++) {
                el[i].style.borderBottom = '1px solid black';
            }
    
            el[el.length - 1].style.border = 'none';
        }
        return
    })
    
}

updateLastListItemStyle();


///////PROF_BD///////////////////
const profBdDroplist = document.getElementById('prof_bd_droplist'),
      profBdBtn = document.getElementById('prof_bd_btn');


if(profBdBtn){
    profBdBtn.addEventListener('click', () => {
    profBdDroplist.classList.toggle('active');
})
}