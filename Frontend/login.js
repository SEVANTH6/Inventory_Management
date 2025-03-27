document.addEventListener('DOMContentLoaded', function() {
    const createAccountForm = document.querySelector('form');
  
    createAccountForm.addEventListener('submit', function(event) {
      event.preventDefault();
  
      const emailInput = document.getElementById('email');
      const passwordInput = document.getElementById('password');
  
      const email = emailInput.value;
      const password = passwordInput.value;
  
      fetch('/create-account', { // Assuming your Flask route is '/create-account'
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email: email, password: password }),
      })
      .then(response => {
        if (!response.ok) {
          // Handle HTTP errors more user-friendly
          return response.json().then(errorData => {
            throw new Error(errorData.message || 'An error occurred. Please try again.');
          });
        }
        return response.json();
      })
      .then(data => {
        alert(data.message || 'Account created successfully!'); // Display success message
        // Optionally redirect to login or another page:
        window.location.href = '/login.html';
      })
      .catch(error => {
        // Display user-friendly error message
        alert('Error: ' + error.message);
      });
    });
  });