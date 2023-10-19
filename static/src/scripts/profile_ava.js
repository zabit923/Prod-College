const fileInput = document.getElementById('fileInput');
const avatarImage = document.getElementById('avatar');

fileInput.addEventListener('change', function () {
    const file = fileInput.files[0];

    if (file) {
        const reader = new FileReader();
        reader.onload = function (e) {
            avatarImage.src = e.target.result;
        };

        reader.readAsDataURL(file);
    }
});