document.addEventListener("afterSubmit", (event) => {
  if (event.detail.category == "success") {
    const form = event.target;
    const data = new FormData(form);
    const div = document.querySelector("div.card.profile-info");

    for (const [key, val] of data.entries()) {
      const element = div.querySelector("[data-id='%s']".replace("%s", key));

      if (element)
        if (element.tagName == "IMG" && typeof val == "object") {
          if (val.size) element.src = URL.createObjectURL(val);
        } else {
          element.innerHTML = val;
        }
    }
  }
});
