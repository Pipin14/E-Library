
/*************  Login.html JavaScript  *************/

const togglePassword = document.getElementById('togglePassword');
if (togglePassword) {
  togglePassword.addEventListener('click', function () {
    const passwordField = document.getElementById('password');
    const type = passwordField.type === 'password' ? 'text' : 'password';
    passwordField.type = type;
    this.innerHTML = type === 'password' ? '<i class="fas fa-eye"></i>' : '<i class="fas fa-eye-slash"></i>';
  });
}



/*************  Register.html JavaScript  *************/

document.addEventListener('DOMContentLoaded', function() {
  // Cek apakah elemen ada sebelum menambahkan event listener
  const togglePasswordRegister = document.getElementById('togglePasswordRegister');
  if (togglePasswordRegister) {
    togglePasswordRegister.addEventListener('click', function () {
      const passwordField = document.getElementById('password1');
      const type = passwordField.type === 'password' ? 'text' : 'password';
      passwordField.type = type;
      this.innerHTML =
        type === 'password'
          ? '<i class="fas fa-eye"></i>'
          : '<i class="fas fa-eye-slash"></i>';
    });
  }

  const toggleConfirmPasswordRegister = document.getElementById('toggleConfirmPasswordRegister');
  if (toggleConfirmPasswordRegister) {
    toggleConfirmPasswordRegister.addEventListener('click', function () {
      const confirmPasswordField = document.getElementById('password2');
      const type =
        confirmPasswordField.type === 'password' ? 'text' : 'password';
      confirmPasswordField.type = type;
      this.innerHTML =
        type === 'password'
          ? '<i class="fas fa-eye"></i>'
          : '<i class="fas fa-eye-slash"></i>';
    });
  }
});
