export function uploadFile(
  file,
  on_progress,
  on_abort,
  on_upload_load,
  on_load,
  on_loadstart,
  on_loadend,
) {
  let http = new XMLHttpRequest();
  let data = new FormData();

  data.append("file", file);

  http.upload.addEventListener("progress", on_progress);
  http.upload.addEventListener("abort", on_abort);
  http.upload.addEventListener("load", on_upload_load);
  http.upload.addEventListener("loadstart", on_loadstart);
  http.upload.addEventListener("loadend", on_loadend);

  http.addEventListener("load", on_load);

  http.open("POST", "/api/upload", true);
  http.send(data);

  return http;
}

export function resetForm(formElement) {}

async function submitForm(formElement) {
  const formData = new FormData(formElement);

  const links = {};

  let inputElement, dropZone, ulElement, liElements, liElement, outputElement;
  for (const [key, value] of formData.entries()) {
    if (typeof value == "object") {
      inputElement = formElement.querySelector(
        String.fromCharCode(35).concat(key),
      );
      dropZone = inputElement.closest("div.drop-zone");

      if (inputElement && inputElement.type == "file") {
        if (dropZone) {
          outputElement = dropZone.querySelector(".output");

          if (outputElement){
            if (!(key in links)) {
              if (outputElement.tagName == "IMG") {
                links[key] = outputElement.dataset.url;
              }
            }
          } else {
            if (!(key in links)) links[key] = new Array();
            ulElement = dropZone.querySelector(".list-section ul");

            if (ulElement) {
              liElements = ulElement.querySelectorAll("li");

              for (liElement of liElements) {
                if (!links[key].includes(liElement.dataset.url))
                  links[key].push(liElement.dataset.url);
              }
            }
          }
        }
      }
    }
  }

  for (const [key, val] of formData.entries()) {
    if (typeof val == "object") {
      formData.delete(key);
    }
  }

  formData.append("links", JSON.stringify(links));

  formElement.querySelectorAll("div.multi-value-input").forEach((element) => {
    const valuesElement = element.querySelector("div.values");
    const spanElements = valuesElement.querySelectorAll("span");
    const inputElement = element.querySelector("input");

    formData.set(
      inputElement.name,
      JSON.stringify(
        Array.from(spanElements).map((element) => element.innerHTML),
      ),
    );
  });

  let form = formElement;

  let eventInitDict = { bubbles: true };
  try {
    const response = await fetch(form.action, {
      method: form.method,
      body: formData,
    });

    const data = await response.json();

    eventInitDict.detail = data;

    // Clear previous errors
    form.querySelectorAll(".errors").forEach((el) => el.remove());
    form
      .querySelectorAll(".is-invalid")
      .forEach((el) => el.classList.remove("is-invalid"));

    if (data.errors) {
      Object.entries(data.errors).forEach(([key, messages]) => {
        const input = form.querySelector(`#${key}`);
        if (!input) return;

        if (input.dataset.onError == "alert") {
          Swal.fire({
            icon: "error",
            title: "Oops...",
            text: Array.from(messages).join("\n"),
          });
        } else {
          const parent = input.parentElement;
          parent.classList.add("is-invalid");

          const errorDiv = document.createElement("div");
          errorDiv.classList.add("errors");
          errorDiv.classList.add("px-2");

          messages.forEach((msg) => {
            const span = document.createElement("span");
            span.className = "text-danger small";
            span.textContent = msg;
            errorDiv.appendChild(span);
          });

          parent.parentElement.appendChild(errorDiv);
        }
      });
    } else {
      Swal.fire({
        title: data.title,
        text: data.message,
        icon: data.category,
      });
    }
  } catch (err) {
    console.log(err);
  }

  form.dispatchEvent(new CustomEvent("afterSubmit", eventInitDict));
}

export function humanizeFileSize(size, si = false) {
  const POWER = !si ? 1000 : 1024;

  if (size < 1000) {
    return size + "B";
  } else if (size > 1000 && size < 1000000) {
    return Math.round(size / POWER) + "K";
  } else if (size > 1000000 && size < 1000000000) {
    return Math.round(size / POWER ** 2) + "MB";
  } else if (size > 1000000000 && size < 1000000000000) {
    return Math.round(size / POWER ** 3) + "Gib";
  }

  return size;
}

export function shortFileType(type) {
  if (type.length <= 4) {
    return type;
  } else {
    if (type.includes("ISO")) {
      return "ISO";
    } else if (type.includes("ICO")) {
      return "ICO";
    }
  }

  return type.slice(0, 5).concat("...");
}

export function validateFileType(file) {}

export function createListSectionItem(extension, size, uploaded, link) {
  let liElement = document.createElement("li");
  let divHeaderElement = document.createElement("div");
  let divFooterElement = document.createElement("div");
  let divBodyElement = document.createElement("div");
  let divContentElement = document.createElement("div");
  let deleteButtonElement = document.createElement("button");
  let deleteIconElement = document.createElement("i");
  let typeSpanElement = document.createElement("span");
  let sizeSpanElement = document.createElement("span");

  if (uploaded && link) {
    liElement.dataset.url = link;
  }

  liElement.classList.value =
    "card w-20 height-100 p-2 mx-2 my-2 position-relative cursor-pointer";
  divHeaderElement.classList.value =
    "header position-absolute end-0 mt-n3 me-n2";
  divBodyElement.classList.value = "body h-100 d-grid align-items-end";
  divFooterElement.classList.value = "footer mt-2";
  deleteButtonElement.classList.value =
    "btn btn-danger btn-sm rounded-circle p-0 m-0 delete-item";
  deleteIconElement.classList.value = "material-symbols-rounded fs-5";
  divContentElement.classList.value = "d-grid";

  typeSpanElement.style.lineHeight = "20px";
  sizeSpanElement.classList.value = "text-xs";

  deleteButtonElement.dataset.role = uploaded ? "delete-file" : "abort";

  deleteIconElement.innerHTML = uploaded ? "delete" : "close";

  typeSpanElement.innerText = extension;
  sizeSpanElement.innerText = size;

  deleteButtonElement.type = "button";

  deleteButtonElement.append(deleteIconElement);
  divHeaderElement.append(deleteButtonElement);
  divContentElement.append(typeSpanElement, sizeSpanElement);
  divBodyElement.append(divContentElement);

  liElement.append(divHeaderElement, divBodyElement);

  if (!uploaded) {
    let progressBarElement = createProgressBar("0", "0", "100");

    divFooterElement.append(progressBarElement);
    liElement.append(divFooterElement);
  }

  return liElement;
}

function u(file, ulElement, formElement, submitElement) {
  const [type, size] = [
    shortFileType(
      file.type.split(String.fromCharCode(47)).pop().toUpperCase(),
    ),
    humanizeFileSize(file.size),
  ];

  let item = createListSectionItem(type, size);
  let progressBar = item.querySelector("div.progress-bar");
  let abortButton = item.querySelector("div.header button");

  ulElement.append(item);

  let http = uploadFile(
    file,
    (e) => {
      progressBar.style.width = String(
        (e.loaded / e.total) * 100,
      ).concat(String.fromCharCode(37));
    },
    () => {
      item.remove();
    },
    () => {
      item.querySelector("div.header button i").innerHTML = "delete";
      item.querySelector("div.header button").dataset.role =
        "delete-file";

      progressBar.closest("div.footer")?.remove();
    },

    (e) => {
      try {
        let data = JSON.parse(e.target.response);

        for (let d of data) {
          if (d?.file?.url) item.dataset.url = d.file.url;

          break;
        }
      } catch (err) {
        console.log(err);
      }
    },
    (e) => {
      if (formElement) {
        submitElement.disabled = true;
      }
    },
    (e) => {
      if (formElement) {
        submitElement.disabled = false;
      }
    },
  );

  abortButton.addEventListener("click", () => {
    http.abort();
  });
}

export function createProgressBar(now_value, min_value, max_value) {
  let divElement = document.createElement("div");
  let progressBarElement = document.createElement("div");

  divElement.classList.value = "progress";
  progressBarElement.classList.value =
    "bg-gradient-success progress-bar progress-bar-animated progress-bar-striped";

  progressBarElement.setAttribute("role", "progressbar");
  progressBarElement.setAttribute("aria-valuenow", now_value ? now_value : "0");
  progressBarElement.setAttribute("aria-valuemin", min_value ? min_value : "0");
  progressBarElement.setAttribute(
    "aria-valuemax",
    max_value ? max_value : "100",
  );

  progressBarElement.style.width = (max_value / 100) * now_value + "%";

  divElement.append(progressBarElement);

  return divElement;
}

export function upload(files, dropZone) {
  if (dropZone) {
    let formElement = dropZone.closest("form");
    let submitElement = formElement?.querySelector("input[type=submit]");
    let inputElement = dropZone.querySelector("input[type=file]");

    if (inputElement) {
      if (inputElement.multiple) {
        let ulElement = dropZone.querySelector(".list-section ul");

        if (ulElement) {
          for (const file of files) {
            u(file, ulElement, formElement, submitElement);
          }
        }
      } else {
        for (const file of files) {
          let ulElement = dropZone.querySelector(".list-section ul");

          if (ulElement) {
            ulElement.innerHTML = String();

            u(file, ulElement, formElement, submitElement);
          } else if (file?.type.includes("image")) {
            let outputElement = dropZone.querySelector("img.output");

            uploadFile(
              file,
              () => {}, // on progress
              () => {}, // on abort
              () => {}, // on upload load
              (e) => {
                try {
                  let data = JSON.parse(e.target.response);

                  if (outputElement) {
                    for (const d of data) {
                      if (d?.file?.url) {
                        outputElement.dataset.url = d.file.url;
                        outputElement.src = d.file.url;
                      }

                      break;
                    }
                  }
                } catch (err) {
                  console.log(err);
                }
              }, // on load
            );
          }

          break;
        }
      }

      const dataTransfer = new DataTransfer();

      if (inputElement.multiple) {
        for (const file of inputElement.files) {
          dataTransfer.items.add(file);
        }

        for (const file of files) {
          dataTransfer.items.add(file);
        }
      } else {
        for (const file of files) {
          dataTransfer.items.add(file);

          break;
        }
      }

      inputElement.files = dataTransfer.files;
    }
  }
}

(function () {
  document.addEventListener("dragover", (event) => {
    const dropZoneElement = event.target.closest("div.drop-zone");
    if (dropZoneElement) {
      event.preventDefault();

      dropZoneElement.classList.add("drag-over-effect");
    }
  });

  document.addEventListener("dragleave", (event) => {
    if (event.target.classList.contains("drop-zone")) {
      event.preventDefault();

      event.target.classList.remove("drag-over-effect");
    }
  });

  document.addEventListener("drop", (event) => {
    let dropZone = event.target.closest("div.drop-zone");

    if (dropZone) {
      event.preventDefault();

      event.target.classList.remove("drag-over-effect");

      upload(event.dataTransfer.files, dropZone);
    }
  });

  document.addEventListener("submit", (event) => {
    event.preventDefault();

    switch (event.target.tagName) {
      case "FORM":
        submitForm(event.target);

        break;
    }
  });

  document.addEventListener("click", (event) => {
    if (event.target.tagName == "IMG") {
      if (event.target.classList.contains("output")) {
        let fileOutput = event.target;
        let dropZone = event.target.closest("div.drop-zone.avatar");
        let fileInput = dropZone.querySelector("input[type=file]");

        if (fileInput && fileOutput) fileInput.click();
      }
    } else if (
      event.target.tagName == "SPAN" &&
      event.target.closest("div.multi-value-input") &&
      event.target.dataset.role == "value"
    ) {
      event.target.remove();
    } else if (
      (event.target.tagName == "BUTTON" &&
        event.target.closest("div.drop-zone") &&
        event.target.classList.contains("delete-item")) ||
      (event.target.tagName == "I" &&
        event.target.closest("button.delete-item") &&
        event.target.closest("div.drop-zone"))
    ) {
      let liElement = event.target.closest("li[data-url]");

      if (liElement) liElement.remove();
    } else if (
      event.target.tagName == "STRONG" &&
      event.target.classList.contains("open-default-file-input-modal")
    ) {
      let formElement = event.target.closest("form");
      let inputElement = formElement.querySelector(
        "input#".concat(event.target.dataset.id),
      );

      inputElement?.click();
    } else {
      let closest = event.target.closest("li.file-card[data-url]");
      if (closest) {
        window.open(
          window.location.protocol +
            "//" +
            window.location.host +
            closest.dataset.url,
          "blank",
        );
      }
    }
  });

  document.addEventListener("change", (event) => {
    if (event.target.type == "file") {
      const dropZone = event.target.closest("div.drop-zone");
      if (dropZone) upload(event.target.files, dropZone);
    }
  });

  document.addEventListener("keydown", (event) => {
    {
      let multiValueInput = event.target.closest("div.multi-value-input");

      if (multiValueInput && event.key == "Enter") {
        event.preventDefault();

        let valuesElement = multiValueInput.querySelector("div.values");
        let spanElement = document.createElement("span");

        spanElement.classList.value =
          "badge badge-sm bg-gradient-secondary mx-2 my-2 cursor-pointer";
        spanElement.innerHTML = event.target.value;
        spanElement.dataset.role = "value";

        valuesElement.append(spanElement);

        event.target.value = "";
      }
    }
  });

  document.querySelectorAll("form").forEach((formElement) => {
    formElement.noValidate = true;
  });
})();
