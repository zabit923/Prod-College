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



/////////////////////////////////////////////////////////////////////////////