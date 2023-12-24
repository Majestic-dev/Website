document.addEventListener('DOMContentLoaded', function() {
    var loginButton = document.getElementById('login');
    var signupButton = document.getElementById('signup');
    var loginForm = document.getElementById('loginForm');
    var signupForm = document.getElementById('signupForm');
    var submitLogin = document.getElementById('submitLogin');
    var submitSignup = document.getElementById('submitSignup');
    var pageTitle = document.getElementById('pageTitle');

    loginButton.addEventListener('click', function() {
        loginForm.style.display = 'block';
        signupForm.style.display = 'none';
        pageTitle.textContent = 'Log In';
    });

    signupButton.addEventListener('click', function() {
        signupForm.style.display = 'block';
        loginForm.style.display = 'none';
        pageTitle.textContent = 'Sign Up';
    });

    submitLogin.addEventListener('click', function() {
        var username = document.getElementById('username');
        var password = document.getElementById('password');
        if (!username.value || !password.value) {
            alert('Both fields are required.');
            return;
        }

        fetch('http://localhost:5000/users/login_user', {  // Replace with the correct URL
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                username: username.value,
                password: password.value
            })
        })
        .then(response => response.json())
        .then(data => {
            // Handle the response from the server
            console.log(data);
        })
        .catch(error => {
            // Handle the error
            console.error('Error:', error);
        });
    
        // Clear the input fields
        username.value = '';
        password.value = '';
    });
    
    submitSignup.addEventListener('click', function() {
        var newUsername = document.getElementById('newUsername');
        var newPassword = document.getElementById('newPassword');
        if (!newUsername.value || !newPassword.value) {
            alert('Both fields are required.');
            return;
        }
        
        // Form a request to the Flask application
        fetch('http://localhost:5000/users/register_user', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                username: newUsername.value,
                password: newPassword.value
            })
        })
        .then(response => response.json())
        .then(data => {
            // Handle the response from the server
            console.log(data);
        })
        .catch(error => {
            // Handle the error
            console.error('Error:', error);
        });

        // Clear the input fields
        newUsername.value = '';
        newPassword.value = '';
    });
});