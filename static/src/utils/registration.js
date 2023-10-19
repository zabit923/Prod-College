export default function registration(){
    document.getElementById('myForm').addEventListener('submit', function (event) {
        event.preventDefault();
        
        const form = event.target;
        const formData = new FormData(form);
        
        const jsonData = {};
        formData.forEach((value, key) => {
            jsonData[key] = value;
        });
        
        const jsonBody = JSON.stringify(jsonData);
        
        fetch('https://fbab-185-244-21-72.ngrok-free.app/auth/register', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: jsonBody
        })
        .then(response => response.json())
        .then(data => {
            console.log(data);
        })
        .catch(error => {
            console.error(error);
        });
    });
}