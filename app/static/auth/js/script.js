document.body.addEventListener("click", (event) => {
  if (
    event.target.classList.contains("register-btn") ||
    event.target.classList.contains("login-btn")
  ) {
    window.location.href = event.target.dataset.location;
  }
});
