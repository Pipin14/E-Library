/*************  Base.html JavaScript  *************/

// Function to toggle mobile menu visibility    
function toggleMobileMenu() {
    const menu = document.getElementById('mobileMenu');
    menu.classList.toggle('hidden');
}

// Function to toggle dropdown for user profile
function toggleDropdown() {
    const dropdown = document.getElementById('profileDropdown');
    dropdown.classList.toggle('hidden');
}

// Close dropdown when screen is resized to desktop
window.addEventListener('resize', function() {
    const dropdown = document.getElementById('profileDropdown');
    if (window.innerWidth >= 1024) {
        dropdown.classList.add('hidden');
    }
});


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