window.addEventListener('scroll', function() {
    let navbar = document.querySelector('.header-1');
    if (window.scrollY > 0) {
        navbar.classList.add('active'); // optional, if you want to add effects
    } else {
        navbar.classList.remove('active');
    }
});
  

