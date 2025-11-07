async function fetchTableData(tableElement) {
  let URL = tableElement.dataset.getRows;

  let response = await fetch(URL);

  if (response.ok) {
    let data = await response.json();

    return data;
  }
}

async function initTable(tableElement, theadElement, tbodyElement) {
  let data = await fetchTableData(tableElement);

  if (data) {
    let cols = data?.cols;
    let rows = data?.rows;

    if (cols) {
      theadElement.innerHTML = "";
      initTableHeader(theadElement, cols);
    }

    if (rows) {
      tbodyElement.innerHTML = "";
      addTableRows(tableElement, tbodyElement, rows);
    }
  }
}

function addActionButtons(tableElement, trElement) {
  let tdElement = document.createElement("td");

  tdElement.classList.value = "align-middle";

  let editLinkElement = document.createElement("a");
  let deleteLinkElement = document.createElement("a");
  let viewLinkElement = document.createElement("a");

  editLinkElement.classList.value =
    deleteLinkElement.classList.value =
    viewLinkElement.classList.value =
      "text-secondary font-weight-bold text-xs m-1";

  editLinkElement.href =
    deleteLinkElement.href =
    viewLinkElement.href =
      "javascript:;";

  editLinkElement.dataset.role = "edit";
  editLinkElement.dataset.bsToggle = "modal";
  editLinkElement.dataset.bsPlacement = "top";
  editLinkElement.ariaLabel = "Edit Modal";
  editLinkElement.dataset.bsOriginalTitle = "Edit Modal";
  editLinkElement.dataset.bsTarget = tableElement.dataset.editRowModalId;
  editLinkElement.innerHTML = "Edit";

  deleteLinkElement.dataset.role = "delete";
  deleteLinkElement.innerHTML = "Delete";

  if (tableElement.dataset.viewRowModalId) {
    viewLinkElement.dataset.role = "view";
    viewLinkElement.dataset.bsToggle = "modal";
    viewLinkElement.dataset.bsPlacement = "top";
    viewLinkElement.ariaLabel = "View Modal";
    viewLinkElement.dataset.bsOriginalTitle = "View Modal";
    viewLinkElement.dataset.bsTarget = tableElement.dataset.viewRowModalId;
    viewLinkElement.innerHTML = "View";
  }

  tdElement.append(viewLinkElement);
  tdElement.append(editLinkElement);
  tdElement.append(deleteLinkElement);

  trElement.append(tdElement);
}

function addCheckBox(trElement) {
  let tdElement = document.createElement("td");
  let divElement = document.createElement("div");
  let inputElement = document.createElement("input");

  tdElement.classList.value = "checkbox-td text-center";

  divElement.classList.value = "form-check form-check-info p-0";

  inputElement.type = "checkbox";
  inputElement.name = "delete";
  inputElement.dataset.role = "multiple-delete";
  inputElement.classList.add("form-check-input");

  divElement.append(inputElement);
  tdElement.append(divElement);
  trElement.append(tdElement);
}

function resetForm(formElement) {
  const inputGroupElement = formElement.querySelectorAll(".input-group");

  Array.from(inputGroupElement).forEach((inputGroupElement) => {
    let input = inputGroupElement.querySelector("input,textarea");

    if (input) input.value = null;

    inputGroupElement.classList.remove("is-filled");
    inputGroupElement.classList.remove("is-valid");
    inputGroupElement.classList.remove("is-invalid");
  });

  Array.from(formElement.querySelectorAll("div.errors")).forEach((element) =>
    element.remove(),
  );

  Array.from(
    formElement.querySelectorAll("div.multi-value-input div.values span"),
  ).forEach((element) => element.remove());
}

function deleteRows(tableElement, tbodyElement, ids) {
  if (ids && ids?.length > 0) {
    const URL = tableElement.dataset.deleteRow;

    Swal.fire({
      title: "Are you sure?",
      text: "You won't be able to revert this!",
      icon: "warning",
      showCancelButton: true,
      confirmButtonColor: "#3085d6",
      cancelButtonColor: "#d33",
      confirmButtonText: "Yes, delete it!",
    }).then((result) => {
      if (result.isConfirmed) {
        Array.from(ids).forEach((id) => {
          if (id != undefined) {
            let trElement = tbodyElement.querySelector(
              "tr[data-id='%s']".replace("%s", id),
            );

            fetch(URL.replace("-1", id), { method: "delete" })
              .then((response) => response.json())
              .then((data) => {
                if (data.status == 200) {
                  delete document.ids[
                    document.ids.findIndex((value) => value == id)
                  ];

                  trElement.classList.add("row-deleting");

                  trElement.addEventListener(
                    "animationend",
                    () => {
                      trElement.remove();

                      if (tbodyElement.querySelectorAll("tr").length == 0) {
                        addNoRowLabel(
                          tableElement.querySelector("thead"),
                          tbodyElement,
                        );
                      }
                    },
                    { once: true },
                  );
                }
              });
          }
        });
      }
    });
  } else {
    Swal.fire({
      icon: "error",
      title: "Oops...",
      text: "Something went wrong!",
    });
  }
}

function deleteRow(rowElement) {
  Swal.fire({
    title: "Are you sure?",
    text: "You won't be able to revert this!",
    icon: "warning",
    showCancelButton: true,
    confirmButtonColor: "#3085d6",
    cancelButtonColor: "#d33",
    confirmButtonText: "Yes, delete it!",
  }).then((result) => {
    if (result.isConfirmed) {
      let tableElement = rowElement.closest("table");
      let tbodyElement = tableElement.querySelector("tbody");
      let theadElement = tableElement.querySelector("thead");

      let url = tableElement.dataset.deleteRow?.replace(
        "-1",
        rowElement.dataset.id,
      );

      fetch(url, {
        method: "delete",
      })
        .then((response) => {
          return response.json();
        })

        .then((data) => {
          if (data.status == 200) {
            Swal.fire({
              title: data?.title,
              text: data?.message,
              icon: data?.category,
            });

            rowElement.classList.add("row-deleting");

            rowElement.addEventListener(
              "animationend",
              () => {
                rowElement.remove();

                if (tbodyElement.querySelectorAll("tr").length == 0) {
                  addNoRowLabel(theadElement, tbodyElement);
                }
              },
              { once: true },
            );
          } else {
            Swal.fire({
              icon: "error",
              title: "Oops...",
              text: "Something went wrong!",
            });
          }
        });
    }
  });
}

function addTableRow(tableElement, theadElement, tbodyElement, id) {
  deleteNoRowLabel(tbodyElement);

  let url = tableElement.dataset.getRow.replace("-1", id);
  fetch(url, { method: "get" })
    .then((response) => response.json())
    .then((data) => {
      let row = [];

      Array.from(
        theadElement.querySelector("tr").querySelectorAll("th"),
      ).forEach((thElement) => {
        row.push(data[thElement.dataset.name]);
      });

      let trElement = document.createElement("tr");
      let tdElement;

      trElement.dataset.id = id;

      addCheckBox(trElement);

      row.forEach((value, index) => {
        if (value !== undefined) {
          tdElement = document.createElement("td");

          if (index == 1) {
            tdElement.classList.value = "text-xs align-middle text-center";
          } else {
            tdElement.classList.add("text-xs");
          }

          tdElement.innerHTML = value;

          trElement.append(tdElement);
        }
      });

      addActionButtons(tableElement, trElement);

      tbodyElement.append(trElement);
    });
}

function reloadRow(tableElement, theadElement, rowElement) {
  const dataID = rowElement.dataset.id;

  let thElement, trElement, indexOf, url;

  url = tableElement.dataset.getRow.replace("-1", dataID);

  fetch(url, {
    method: "get",
  })
    .then((response) => response.json())
    .then((data) => {
      Object.entries(data).forEach(([key, value]) => {
        thElement = theadElement.querySelector(
          "th[data-name='%s']".replace("%s", key),
        );

        if (thElement) {
          trElement = thElement.closest("tr");
          indexOf = Array.from(trElement.children).indexOf(thElement);

          rowElement.children[indexOf].innerHTML = value;
        }
      });
    });
}

function addTableRows(tableElement, tbodyElement, rows) {
  let trElement;
  let tdElement;

  tbodyElement.innerHTML = "";

  if (rows.length > 0) {
    Array.from(rows).forEach((row) => {
      trElement = document.createElement("tr");

      addCheckBox(trElement);

      Array.from(row).forEach((item, index) => {
        tdElement = document.createElement("td");
        tdElement.classList.value = "text-xs";

        if (!index) {
          tdElement.classList.add("align-middle");
          tdElement.classList.add("text-center");

          trElement.setAttribute("data-id", item);
        }

        tdElement.innerHTML = item;

        trElement.append(tdElement);
      });

      addActionButtons(tableElement, trElement);

      tbodyElement.append(trElement);
    });
  } else {
    addNoRowLabel(tableElement.querySelector("thead"), tbodyElement);
  }
}

function initTableHeader(theadElement, cols) {
  let trElement = document.createElement("tr");
  let thElement;

  cols = [["checkbox", null], ...cols, ["action", null]];

  Array.from(cols).forEach(([id, name], index) => {
    thElement = document.createElement("th");

    thElement.classList.value =
      "text-uppercase text-secondary text-xxs font-weight-bolder opacity-7";

    if (index <= 1) {
      thElement.classList.add("align-middle");
      thElement.classList.add("text-center");
    }

    thElement.dataset.name = id;

    thElement.innerHTML = name;

    trElement.append(thElement);
  });

  theadElement.append(trElement);
}

function addNoRowLabel(theadElement, tbodyElement) {
  if (!tbodyElement.querySelector("tr.no-rows-label")) {
    let trElement = document.createElement("tr");
    let tdElement = document.createElement("td");
    let thCounts = theadElement
      .querySelector("tr")
      .querySelectorAll("th").length;

    trElement.classList.add("no-rows-label");

    tdElement.classList.value = "text-center py-4";
    tdElement.innerHTML = "No rows yet — add one above.";
    tdElement.colSpan = thCounts;

    trElement.append(tdElement);
    tbodyElement.append(trElement);
  }
}

function deleteNoRowLabel(tbodyElement) {
  let trElement = tbodyElement.querySelector("tr.no-rows-label");

  if (trElement) trElement.remove();
}

function viewRow(tableElement, row) {
  const rowID = row.dataset.id;
  const viewURL = tableElement.dataset.viewRow.replace("-1", rowID);
  const viewModalID = tableElement.dataset.viewRowModalId;
  const viewModalElement = document.querySelector(viewModalID);
  const viewModalBodyElement = viewModalElement.querySelector("div.modal-body");

  fetch(viewURL, { method: "GET" })
    .then((response) => response.text())
    .then((data) => {
      viewModalBodyElement.innerHTML = data;
    });
}

function initTableContol(
  tableElement,
  tableControlElement,
  tbodyElement,
  theadElement,
) {
  // Add Row
  let addRowContainerDivElement = document.createElement("div");
  let addRowButtonElement = document.createElement("button");
  let addRowIconElement = document.createElement("i");

  addRowIconElement.classList.value = "material-symbols-rounded fs-5";
  addRowIconElement.innerHTML = "add";

  addRowButtonElement.classList.value = "btn btn-info m-0 mx-2";
  addRowButtonElement.dataset.bsToggle = "modal";
  addRowButtonElement.dataset.bsPlacement = "top";
  addRowButtonElement.dataset.bsTarget = tableElement.dataset.addRowModalId;
  addRowButtonElement.dataset.bsAdd = "add";

  addRowButtonElement.append(addRowIconElement);
  addRowContainerDivElement.append(addRowButtonElement);

  addRowButtonElement.addEventListener("click", function () {
    resetForm(
      document.querySelector(
        addRowButtonElement.dataset.bsTarget.concat(" form"),
      ),
    );
  });

  // Delete Multiple Rows
  let deleteRowsContainerDivElement = document.createElement("div");
  let deleteRowButtonElement = document.createElement("button");
  let deleteRowIconElement = document.createElement("i");

  deleteRowButtonElement.dataset.bsRole = "multiple-delete";

  deleteRowIconElement.classList.value = "material-symbols-rounded fs-5";
  deleteRowIconElement.innerHTML = "delete";

  deleteRowButtonElement.classList.value = "btn btn-danger m-0 mx-2";

  deleteRowButtonElement.append(deleteRowIconElement);
  deleteRowsContainerDivElement.append(deleteRowButtonElement);

  // Reload Button
  let reloadsContainerDivElement = document.createElement("div");
  let reloadButtonElement = document.createElement("button");
  let reloadIconElement = document.createElement("i");

  reloadIconElement.classList.value = "material-symbols-rounded fs-5";
  reloadIconElement.innerHTML = "refresh";
  reloadButtonElement.classList.value = "btn btn-info m-0 mx-2";
  reloadButtonElement.append(reloadIconElement);
  reloadsContainerDivElement.append(reloadButtonElement);

  reloadButtonElement.addEventListener("click", function () {
    initTable(tableElement, theadElement, tbodyElement);
  });

  // Search
  let searchInputContainerDivElement = document.createElement("div");
  let searchInputLabel = document.createElement("label");
  let searchInputElement = document.createElement("input");
  let timer;

  searchInputElement.addEventListener("input", (event) => {
    clearTimeout(timer);

    const searchTerm = event.target.value.toLowerCase();

    timer = setTimeout(() => {
      Array.from(tbodyElement.querySelectorAll("tr")).forEach((row) => {
        const text = row.textContent.toLowerCase();

        row.style.display = text.includes(searchTerm) ? "" : "none";
      });
    }, 500);
  });

  searchInputContainerDivElement.classList.value =
    "input-group input-group-outline mx-2";

  searchInputLabel.classList.add("form-label");
  searchInputLabel.innerHTML = "Search...";

  searchInputElement.type = "text";
  searchInputElement.classList.value = "form-control search";

  searchInputContainerDivElement.append(searchInputLabel);
  searchInputContainerDivElement.append(searchInputElement);

  // Append
  tableControlElement.append(addRowContainerDivElement);
  tableControlElement.append(deleteRowsContainerDivElement);
  tableControlElement.append(reloadsContainerDivElement);
  tableControlElement.append(searchInputContainerDivElement);
}

(function () {
  document
    .querySelectorAll("table[data-type=dynamic]")
    .forEach(function (tableElement) {
      const theadElement = tableElement.querySelector("thead");
      const tbodyElement = tableElement.querySelector("tbody");
      const cardElement = tableElement.closest("div.card");
      const tableControlDivElement =
        cardElement.querySelector("div.table-control");

      initTableContol(
        tableElement,
        tableControlDivElement,
        tbodyElement,
        theadElement,
      );
      initTable(tableElement, theadElement, tbodyElement);
    });

  document.addEventListener("click", (event) => {
    const target = event.target;
    const table = target.closest("table[data-type='dynamic']");

    if (!document.ids) document.ids = [];

    if (table) {
      const allowedTags = ["A", "INPUT"];
      if (!allowedTags.includes(target.tagName)) return;

      const row = target.closest("tr");
      const role = target.dataset.role;

      switch (role) {
        case "delete":
          deleteRow(row);
          break;

        case "view":
          viewRow(table, row);
          break;

        case "multiple-delete": {
          const id = row.dataset.id;
          const isChecked = target.checked;

          if (isChecked && !document.ids.includes(id)) {
            document.ids.push(id);
          } else if (!isChecked) {
            document.ids = document.ids.filter((x) => x !== id);
          }

          break;
        }
      }

      return;
    }

    const btn = target.closest("[data-bs-role='multiple-delete']");
    if (!btn) return;

    const card = btn.closest("div.card");
    const tableInCard = card?.querySelector("table[data-type='dynamic']");
    const tbody = tableInCard?.querySelector("tbody");

    if (document.ids.length > 0) {
      deleteRows(tableInCard, tbody, document.ids);
    }
  });

  document.addEventListener("afterSubmit", (event) => {
    const form = event.target;
    const d = event.detail;

    if (!form) return;

    let modal = event.target.closest("div.modal");

    if (modal) {
      let selector = "[data-bs-target='#%s']".replace("%s", modal.id);
      let target = document.querySelector(selector);
      let cardElement = target?.closest(
        "div.card:has(table[data-type=dynamic])",
      );

      if (cardElement) {
        let tableElement = cardElement.querySelector("table");
        let theadElement = tableElement.querySelector("thead");
        let tbodyElement = tableElement.querySelector("tbody");

        if (tableElement && theadElement && tbodyElement)
          if (!form.hasAttribute("data-get")) {
            if (event.detail.id != undefined) {
              addTableRow(tableElement, theadElement, tbodyElement, d.id);
            }
          } else {
            const id = form.querySelector("input[id$=_id]")?.value;

            if (id) {
              const row = tableElement.querySelector(
                "tr[data-id='%s']".replace("%s", id),
              );

              if (row) reloadRow(tableElement, theadElement, row);
            }
          }
      }
    }
  });
}).call();
