// Fixed Plugin
(function () {
  const asideElement = document.querySelector("aside");
  const fixedPluginElement = document.querySelector(".fixed-plugin");
  const badgeColorsElement = fixedPluginElement.querySelector(".badge-colors");
  const sideNavTypeElement = fixedPluginElement.querySelector(".sidenav-type");
  const darkVersionElement = fixedPluginElement.querySelector("#dark-version");

  badgeColorsElement.addEventListener("click", function (event) {
    if (event.target.tagName == "SPAN")
      localStorage.setItem("side-bar-color", event.target.dataset.color);
  });

  sideNavTypeElement.addEventListener("click", function (event) {
    if (event.target.tagName == "BUTTON") {
      localStorage.setItem("side-nav-type", event.target.dataset.class);
    }
  });

  darkVersionElement.addEventListener("change", function (event) {
    localStorage.setItem("dark-version", event.target.checked);
  });

  document.addEventListener("DOMContentLoaded", () => {
    Array.from(asideElement.querySelectorAll("a")).forEach((aElement) => {
      const url = new URL(aElement.href);
      if (url.pathname == location.pathname) aElement.classList.add("active");
      else aElement.classList.remove("active");
    });

    const badgeColor = localStorage.getItem("side-bar-color");
    const sideNavType = localStorage.getItem("side-nav-type");
    const darkVersion = localStorage.getItem("dark-version");

    try {
      sidebarColor(
        badgeColorsElement.querySelector(
          "span[data-color='%s']".replace(
            "%s",
            badgeColor ? badgeColor : "dark",
          ),
        ),
      );
    } catch (error) {
      console.error(error);
    }

    try {
      sidebarType(
        sideNavType
          ? fixedPluginElement.querySelector(
              `button[data-class='${sideNavType}']`,
            )
          : "bg-gradient-dark",
      );
    } catch (error) {}

    try {
      if (darkVersion == "true") {
        darkVersionElement.checked = darkVersion;
        darkMode(darkVersionElement);
      }
    } catch (error) {
      console.error(error);
    }
  });
}).call();
