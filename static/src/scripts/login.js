import { updateSlider } from "../utils/slider.js";
import adaptiveSlider from "../utils/adaptive-slider.js";



const isTeacherCheckbox = document.getElementById('is_teacher_chexbox');
const loginLastName = document.getElementById('login_last_name');
const loginPassword = document.getElementById('login_password');

isTeacherCheckbox.addEventListener('change', function() {
    if (isTeacherCheckbox.checked) {
        loginLastName.innerText = 'Отчество';
        loginPassword.innerText = 'Пароль'
    } else {
        loginLastName.innerText = 'Фамилия';
        loginPassword.innerText = 'Номер зачетной книжки'
    }
});