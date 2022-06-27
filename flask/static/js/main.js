const toggleMobileMenu = (menu) => {
  menu.classList.toggle('open');
};

if (window.history.replaceState) {
  window.history.replaceState(null, null, window.location.href);
}
