document.addEventListener('DOMContentLoaded', function() {
  const loginForm = document.getElementById('loginForm');

  loginForm.addEventListener('submit', function(event) {
      event.preventDefault();

      const emailInput = document.getElementById('email');
      const passwordInput = document.getElementById('password');

      const email = emailInput.value;
      const password = passwordInput.value;

      fetch('http://127.0.0.1:5000/login', {
          method: 'POST',
          headers: {
              'Content-Type': 'application/json',
          },
          body: JSON.stringify({ email: email, password: password }),
      })
      .then(response => {
          if (!response.ok) {
              return response.json().then(errorData => {
                  throw new Error(errorData.message || 'An error occurred. Please try again.');
              });
          }
          return response.json();
      })
      .then(data => {
          alert(data.message || 'Login successful!');
          // Optionally, redirect to another page upon successful login
          // window.location.href = '/dashboard.html';
      })
      .catch(error => {
          alert('Error: ' + error.message);
      });
  });
});
