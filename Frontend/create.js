document.addEventListener('DOMContentLoaded', function() {
  const createAccountForm = document.querySelector('form');

  createAccountForm.addEventListener('submit', function(event) {
      event.preventDefault(); // Prevent default form submission

      const emailInput = document.getElementById('email');
      const passwordInput = document.getElementById('password');

      const email = emailInput.value;
      const password = passwordInput.value;

      fetch('http://127.0.0.1:5000/create-account', { // Updated endpoint
          method: 'POST',
          headers: {
              'Content-Type': 'application/json',
          },
          body: JSON.stringify({ email: email, password: password }),
      })
      .then(response => {
          if (!response.ok) {
              // Handle HTTP errors with user-friendly messages
              return response.json().then(errorData => {
                  throw new Error(errorData.message || 'Account creation failed. Please try again.');
              });
          }
          return response.json();
      })
      .then(data => {
          // Handle successful account creation
          alert(data.message || 'Account created successfully!');
          // Optionally redirect to login or another page:
          window.location.href = '/login.html';
      })
      .catch(error => {
          // Handle errors from the fetch request or backend
          alert('Error: ' + error.message);
      });
  });
});
