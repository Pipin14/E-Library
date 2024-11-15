/*************  Base.html JavaScript  *************/


/*************  Login.html JavaScript  *************/
// Handle show/hide password toggle
document.getElementById('togglePassword').addEventListener('click', function () {
    const passwordField = document.getElementById('password');
    const type = passwordField.type === 'password' ? 'text' : 'password';
    passwordField.type = type;
    this.innerHTML = type === 'password' ? '<i class="fas fa-eye"></i>' : '<i class="fas fa-eye-slash"></i>';
});



/*************  Register.html JavaScript  *************/
// Toggle password visibility
document
.getElementById("togglePasswordRegister")
.addEventListener("click", function () {
  const passwordField = document.getElementById("password1");
  const type = passwordField.type === "password" ? "text" : "password";
  passwordField.type = type;
  this.innerHTML =
    type === "password"
      ? '<i class="fas fa-eye"></i>'
      : '<i class="fas fa-eye-slash"></i>';
});

// Toggle confirm password visibility
document
.getElementById("toggleConfirmPasswordRegister")
.addEventListener("click", function () {
  const confirmPasswordField = document.getElementById("password2");
  const type = confirmPasswordField.type === "password" ? "text" : "password";
  confirmPasswordField.type = type;
  this.innerHTML =
    type === "password"
      ? '<i class="fas fa-eye"></i>'
      : '<i class="fas fa-eye-slash"></i>';
});