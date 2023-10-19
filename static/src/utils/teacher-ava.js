let image = document.getElementById("image");
let file = document.getElementById("file");

file.addEventListener('change', function(){
  image.src = URL.createObjectURL(file.files[0]);
  image.style.display = "block";
});