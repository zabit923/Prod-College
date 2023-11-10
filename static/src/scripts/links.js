const linksDropdown_ = document.getElementById('drop_down_link_list_');
const btnDropdown_ = document.getElementById('btn_important_links_');


document.addEventListener('click', (e) => {
    const withinBoundaries_ = e.target.closest('#drop_down_link_list_') || e.target.id === 'btn_important_links_';

    if (!withinBoundaries_) {
        linksDropdown_.classList.remove('active');
    }
});

document.addEventListener('keydown', (e) => {
    if (e.keyCode == 27) { // код клавиши Escape
        linksDropdown_.classList.remove('active');
    }
});

if (btnDropdown_) {
    btnDropdown_.addEventListener('click', (event) => {
        event.preventDefault();
        linksDropdown_.classList.toggle('active');
    });
}







