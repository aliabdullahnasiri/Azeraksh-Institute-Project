import { createListSectionItem, resetForm } from "./form.js";

(function () {
  document.addEventListener("show.bs.modal", (event) => {
    const form = event.target.querySelector("form[data-get]");

    if (form) {
      const get = form.dataset.get;
      const id =
        event.relatedTarget.dataset.id ||
        event.relatedTarget?.closest("[data-id]")?.dataset.id;
      const url = get.replace(
        String.fromCharCode(45).concat(String.fromCharCode(49)),
        id,
      );

      fetch(url, {
        method: "get",
      })
        .then((response) => response.json())
        .then((data) => {
          let names = ["input", "textarea", "select"];

          Array.from(
            form.querySelectorAll(names.join(String.fromCharCode(44))),
          ).forEach((input) => {
            let val = data[input.id];

            switch (input.type) {
              case "file":
                let dropZone = input.closest("div.drop-zone");

                if (dropZone) {
                  let ulElement = dropZone.querySelector(".list-section ul");

                  if (ulElement) {
                    ulElement.innerHTML = "";

                    if (data.files)
                      for (const f of data.files) {
                        if (f.file_for == input.id || input.id == "files") {
                          let selector = "li[data-url='%s']";
                          if (
                            !ulElement.querySelector(
                              selector.replace("%s", f.link),
                            )
                          ) {
                            let item = createListSectionItem(
                              f.extension,
                              f.human_size,
                              true,
                              f.file_url,
                            );
                            ulElement.append(item);
                          }
                        }

                        if (!input.multiple) break;
                      }
                  } else {
                    if (input.multiple) {
                    } else {
                      // Avatar
                      let fileOutput =
                        input.parentElement.querySelector(".output");

                      if (fileOutput) {
                        fileOutput.src = val;
                      }
                    }
                  }
                }
                break;

              case "select-one":
                const divElement = document.createElement("div");
                divElement.innerHTML = val;

                const v = divElement.querySelector(".value")?.innerText;

                if (v) input.value = v;

                break;

              default:
                if (val != undefined) {
                  let multiValueInput = input.closest("div.multi-value-input");

                  if (multiValueInput) {
                    const valuesElement =
                      multiValueInput.querySelector("div.values");

                    Array.from(val).forEach((v) => {
                      const spanElement = document.createElement("span");
                      spanElement.classList.value =
                        "badge badge-sm bg-gradient-secondary mx-2 my-2 cursor-pointer";
                      spanElement.innerHTML = v;
                      spanElement.dataset.role = "value";

                      valuesElement.append(spanElement);
                    });
                  } else {
                    input.value = data[input.id];

                    let inputGroup = input.closest("div.input-group");
                    if (inputGroup) inputGroup.classList.add("is-filled");
                  }
                }

                break;
            }
          });
        });
    }
  });

  document.addEventListener("hidden.bs.modal", (event) => {
    const form = event.target.querySelector("form");

    if (form && !form.hasAttribute("data-get")) {
      resetForm(form);
    }
  });
}).call();
