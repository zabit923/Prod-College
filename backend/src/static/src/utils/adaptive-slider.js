const prevButton = document.querySelector('.prev-button');
const nextButton = document.querySelector('.next-button');
const slides = document.querySelectorAll('.slide');
let currentSlideIndex = 0;

export default function adaptiveSlider() {
    if (!prevButton || !nextButton || !slides.length) {
        return;
    }

    function showSlide(index) {
        slides.forEach((slide, i) => {
            if (slide) {
                slide.style.display = i === index ? 'block' : 'none';
            }
        });
    }
    

    function showNextSlide() {
        currentSlideIndex = (currentSlideIndex + 1) % slides.length;
        showSlide(currentSlideIndex);
    }

    function showPrevSlide() {
        currentSlideIndex = (currentSlideIndex - 1 + slides.length) % slides.length;
        showSlide(currentSlideIndex);
    }

    if (prevButton && nextButton) {
        prevButton.addEventListener('click', showPrevSlide);
        nextButton.addEventListener('click', showNextSlide);
    }

    showSlide(currentSlideIndex);
}