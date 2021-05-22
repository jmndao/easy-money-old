const togglePassword = document.querySelector('#togglePassword');
const password = document.querySelector('#password');

const links = document.querySelectorAll(".easy-sidebar-menu ul li a");
const activeLink = document.querySelector("a.active");

togglePassword.addEventListener('click', function(e) {
    // toggle the type attribute
    const type = password.getAttribute('type') === 'password' ? 'text' : 'password';
    password.setAttribute('type', type);
    // toggle the eye slash icon
    this.classList.toggle('fa-eye-slash');
});



links.forEach((link) => {
    link.addEventListener('hover', () => {
        link.classList.add('.redBackground');
    })
})