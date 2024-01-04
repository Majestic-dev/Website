var hostAddress = null;
var logged_in = false;

fetch("data/config.json")
    .then(response => response.json())
    .then(config => {
        hostAddress = config.host;
    })
    .catch(error => console.error('Error:', error));

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

    submitLogin.addEventListener('click', async function(event) {
        event.preventDefault();
        var username = document.getElementById('username');
        var password = document.getElementById('password');
        if (!username.value || !password.value) {
            alert('Both fields are required.');
            return;
        }
    
        try {
            const response = await fetch(hostAddress + "/users/login_user", {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    username: username.value,
                    password: password.value
                })
            });
    
            const data = await response.json();
    
            // Handle the response from the server
            console.log(data);
    
            // If login is successful, show the buttons and hide all others
            if (data["status"] == "success") {
                logged_in = true;
                document.getElementById('createKey').style.display = 'block';
                document.getElementById('logout').style.display = 'block';
    
                // Hide all buttons with the 'hide-on-login' class
                const buttonsToHide = document.getElementsByClassName('hide-on-login');
                for (let button of buttonsToHide) {
                    button.style.display = 'none';
                }
                pageTitle.textContent = null;
            }
        } catch (error) {
            // Handle the error
            console.error('Error:', error);
        }

        // Clear the input fields
        username.value = '';
        password.value = '';
    });
    
    submitSignup.addEventListener('click', function(event) {
        event.preventDefault();
        var newUsername = document.getElementById('newUsername');
        var newPassword = document.getElementById('newPassword');
        
        if (!newUsername.value || !newPassword.value) {
            alert('Both fields are required.');
            return;
        }
        
        fetch(hostAddress + "/users/register_user", {
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

            // If signup is successful, show the buttons and hide all others
            if (data["status"] == "success") {
                location.reload();
            }

            // If signup is unsuccessful, show an alert
            if (data["status"] == "failure") {
                alert('Username is already taken.');
            }
        })
        .catch(error => {
            // Handle the error
            console.error('Error:', error);
        });

        // Clear the input fields
        newUsername.value = '';
        newPassword.value = '';
    });

    document.getElementById('logout').addEventListener('click', function() {
        // Show the 'login' and 'signup' buttons
        document.getElementById('login').style.display = 'block';
        document.getElementById('signup').style.display = 'block';
    
        // Hide the 'createKey' and 'logout' buttons
        document.getElementById('createKey').style.display = 'none';
        this.style.display = 'none';
        pageTitle.textContent = null;
    });

    document.getElementById('createKey').addEventListener('click', async function(event) {
        event.preventDefault();
        let username = prompt('Enter your username');
        let password = prompt('Enter your password');
        
        fetch(hostAddress + "/api/get_key", {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                username: username,
                password: password
            })
        })
        .then(response => response.json()) 
        .then(data => {
            // Handle the response from the server
            console.log(data);

            if (data["status"] == "failure, invalid credentials") {
                alert('Invalid username');
                return;
            }

            if (data["status"] == "success") {
                pageTitle.textContent = 'Your API Key: ' + data["key"];
                document.getElementById('createKey').style.display = 'none';
            }
        })
        .catch(error => {
            // Handle the error
            console.error('Error:', error);
        });
    });
});