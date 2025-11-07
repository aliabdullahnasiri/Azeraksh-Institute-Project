(function () {
  for (const element of document.querySelectorAll("nav .navbar-nav a")) {
    if (window.location.pathname == new URL(element.href).pathname)
      element.classList.add("active");
    else element.classList.remove("active");
  }
}).call();
