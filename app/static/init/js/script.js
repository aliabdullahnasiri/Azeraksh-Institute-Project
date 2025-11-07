document.addEventListener("afterSubmit", (event) => {
  if (event.detail?.redirect) {
    setTimeout(() => {
      window.location.href = event.detail.redirect;
    }, 2500);
  }
});
