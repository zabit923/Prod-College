export function updateSlider(slides, currentIndex) {
    slides.forEach((slide, index) => {
        if (index === currentIndex) {
            slide.classList.add('slide-right');
            slide.classList.remove('slide-center', 'slide-left');
        } else if (index === (currentIndex + 1) % slides.length) {
            slide.classList.add('slide-center');
            slide.classList.remove('slide-left', 'slide-right');
        } else {
            slide.classList.add('slide-left');
            slide.classList.remove('slide-center', 'slide-right');
        }
    });
}