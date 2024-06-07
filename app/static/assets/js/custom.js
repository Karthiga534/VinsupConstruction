var csrftoken = getCookie("csrftoken");
const successMesssage = { "message": "Successfully Added", "bgColor": "bg-success" }
const statusMesssage = { "message": "Status Changed", "bgColor": "bg-primary" }
const updateMessage = { "message": "Updated Successfully ", "bgColor": "bg-success" }
const deleteMessage = { "message": "Deleted Successfully", "bgColor": "bg-info" }
const errorAlertMessage = { "message": "something went wrong", "bgColor": "bg-danger" }
const errorOccured = { "message": "An error occured", "bgColor": "bg-danger" }

let pageLength = 20;
const TruncateLength = 20;
const TruncateExt = "...";

function goBack() {
  window.history.back();
}

let envVariable;

document.addEventListener("DOMContentLoaded", function() {
  // console.log('Environment Variable:', window.myEnvVar.PAGINATION_SIZE);
  envVariable =window.myEnvVar
  // pageLength = envVariable?.PAGINATION_SIZE || pageLength

  
});





// console.log(successMesssage)
function getCookie(name) {
  var cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    var cookies = document.cookie.split(";");
    for (var i = 0; i < cookies.length; i++) {
      var cookie = cookies[i].trim();
      // Check if the cookie contains the CSRF token
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

function getAuthToken() {
  // Function to retrieve authentication token from any source (localStorage, cookies, etc.)
  var authToken = localStorage.getItem("authToken");
  if (!authToken) {
    // Try retrieving from cookies or another source
    authToken = getCookie("authToken"); // Example: Function to get authToken from cookies
  }
  return authToken;
}

function getValueOrDefault(value) {
  return typeof value !== "undefined" && value !== null ? value : "";
  // return value
}

// ------------------------------------------------------------------------------------------------------------------------------------------

// Helper function to show Bootstrap toast notifications

function showToast(title, message, bgColor, reload) {
  var toastContainer = $("#toastContainer");
  var toastId = "toast-" + Math.floor(Math.random() * 1000); // Generate a random toast ID

  var toastHTML = `
      <div id="${toastId}" class="toast align-items-center text-white ${bgColor}" role="alert" aria-live="assertive" aria-atomic="true">
        <div class="d-flex">
          <div class="toast-body">
            <strong>${title}</strong><br>${message}
          </div>
          <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
        </div>
      </div>
    `;

  toastContainer.append(toastHTML);

  var toastElement = $("#" + toastId);
  var toastInstance = new bootstrap.Toast(toastElement);

  toastInstance.show();

  // Remove the toast after a delay (e.g., 5 seconds)
  setTimeout(function () {
    toastElement.remove();
    if (reload) {
      // alert(reload)
      // document.getElementById('searchInput').value = '';
      // location.reload();
      reloadWithoutQueryParams();
    }
  }, 1000);
}


function reloadWithoutQueryParams() {
  const url = new URL(window.location.href);

  url.search = '';
  // alert(url.toString())
  window.location.href = url.toString();
  window.location.reload();                  // Redirect to the URL without query parameters
}

function handleCreateErrors(errors, pre = "") {
  // console.log(errors);

  // Clear previous error styles and messages
  $(".form-control").removeClass("is-invalid");
  $(".error-message").text("");


  for (var fieldName in errors) {
    if (errors.hasOwnProperty(fieldName)) {
      var errorMessage = errors[fieldName][0]; // Get the first error message

      // console.log(pre+fieldName,"pppppppppp")

      // Add 'is-invalid' class to the input field
      $("#" + pre + fieldName).addClass("is-invalid");

      // Display error message in the adjacent invalid-feedback element
      $("#" + pre + fieldName + "Error").text(errorMessage);
    }
  }
}

// for breakerrors into custom
function transformErrors(errorObj) {
  const transformedErrors = {};
  for (const key in errorObj) {
    if (Array.isArray(errorObj[key])) {
      transformedErrors[key] = errorObj[key];
    } else if (typeof errorObj[key] === "object") {
      const nestedErrors = transformErrors(errorObj[key]); // Recursive call for nested objects
      for (const nestedKey in nestedErrors) {
        transformedErrors[key + "_" + nestedKey] = nestedErrors[nestedKey];
      }
    }
  }
  return transformedErrors;
}

function handleUpdateErrors(modelId, errorObj) {
  // console.log(modelId, errorObj);
  for (const key in errorObj) {
    const inputId = modelId + "_" + key;
    const errorMessage = errorObj[key][0]; // Assuming only one error message per field
    const errorSpan = document.getElementById(inputId + "Error");

    // console.log(errorMessage, errorSpan, inputId);
    $("#" + inputId).addClass("is-invalid");

    // Display error message in the adjacent invalid-feedback element
    if (errorSpan) {
      errorSpan.textContent = errorMessage;
    }

    //   errorSpan.innerText  =errorMessage
    //   errorSpan.innerHTML=errorMessage;
  }
}

// -----------------------------------------------------------------------------------------------------------------------------

let initialFormValues = {};
var model_Id;
var model_Name;
// remove validation errors
function openModal(modelName, modelId) {
  $(`#${modelName}_${modelId}`).modal("show");
  captureInitialValues(modelId);
  model_Id = modelId;
  model_Name = modelName;
  // Capture initial form values when modal is shown
}

// Function to capture initial form values based on model ID
function captureInitialValues(modelId) {
  $(`#editForm${modelId} input , #editForm${modelId} textarea`).each(
    function () {
      const fieldName = this.name;
      initialFormValues[fieldName] = this.value;
    }
  );
}

// close model
// Function to close the modal and reset form elements
function CloseModel(modelName, modelId) {
  var errorSpans = document.querySelectorAll(".error-message");
  errorSpans.forEach(function (span) {
    span.textContent = "";
  });

  var formControls = document.querySelectorAll(".form-control");
  formControls.forEach(function (control) {
    control.classList.remove("is-invalid");
  });
  // console.log(`${model_Name}_${model_Id}`);
  model_Id = "";
  model_Name = "";
  resetFormValues(modelName, modelId);
}



function resetFormValues(modelName, modelId) {

  // Reset form input and textarea values
  $(`#editForm${modelId} input, #editForm${modelId} textarea `).each(
    function () {
      const fieldName = this.name;
      const initialValue = initialFormValues[fieldName];
      if (initialValue !== undefined) {
        $(this).val(initialValue);
      }
    }
  );

  // Add event listener for modal hidden event
  $(`#${modelName}_${modelId}`).on("hidden.bs.modal", function () {
    // Enable all buttons with spinner inside modal
    $(`#${modelName}_${modelId} .btn[disabled]`).each(function () {
      enableButton(this);
    });
  });
}

// $(document).on("hidden.bs.modal", `#${model_Name}_${model_Id}`, function (e) {
//   alert(); // Just for testing, remove this line in your actual code
//   if (e.target === this) {
//     resetFormValues(model_Name, model_Id);
//   }
// });

// $(`#${model_Name}_${model_Id}`).on("hide.bs.modal", function (e) {
//   alert();
// });

// clear all errors
function clearErrors(modelId) {
  // alert()
  var errorSpans = document.querySelectorAll(".error-message");
  errorSpans.forEach(function (span) {
    span.textContent = "";
  });

  var formControls = document.querySelectorAll(".form-control");
  formControls.forEach(function (control) {
    control.classList.remove("is-invalid");
  });



  var formSelect = document.querySelectorAll(".form-select");
  formSelect.forEach(function (control) {
    control.classList.remove("is-invalid");
  });
}

// -------------------------------------------------------------------------------------------------------------------------------------

function disableButton(button) {
  button.disabled = true;
  // Create a spinner element
  const spinner = document.createElement("span");
  spinner.className = "spinner-border spinner-border-sm me-2";
  spinner.setAttribute("role", "status");
  spinner.setAttribute("aria-hidden", "true");
  spinner.innerHTML = "&nbsp;"; // Add space for visual separation
  // Insert the spinner before the button text
  // button.innerHTML = '';
  button.appendChild(spinner);
  // button.insertAdjacentHTML('beforeend', 'Loading...'); // Adjust text as needed
}

// Helper function to enable the button
// function enableButton(button) {
//   button.disabled = false;
//   // Remove the spinner and restore the original button text
//   if (
//     button.lastChild &&
//     button?.lastChild?.classList.contains("spinner-border")
//   ) {
//     button.removeChild(button?.lastChild);
//   }
// }

function enableButton(button) {
  button.disabled = false;

  // Remove the spinner and restore the original button text
  const lastChild = button.lastChild;
  if (lastChild && lastChild.classList && lastChild.classList.contains("spinner-border")) {
    button.removeChild(lastChild);
  }
}



function restoreForm(form, button) {

  $(`#${form} input, #${form} button`).prop('disabled', false);

  enableButton(button);
}



// -------------- currency formating -------------------------

const currencyFormatter = new Intl.NumberFormat('en-IN', {
  style: 'currency',
  currency: 'INR',
  minimumFractionDigits: 2,
});



// ------------------------------- Pagination and fiter ---------------------------------

// render pagination
function renderPagination(data, currentPage) {

  if (data.next === null && data.previous === null) {
    existingPaginationContainer.innerHTML = ''; // Clear existing content
    return;
  }


  const totalPages = Math.ceil(data.count / pageLength);

  const paginationComponent = document.createElement('nav');
  paginationComponent.setAttribute('aria-label', 'Page navigation example');

  const paginationList = document.createElement('ul');
  paginationList.classList.add('pagination');

  // Create Previous button
  if (currentPage > 1) {
    const prevItem = createPaginationItem(currentPage - 1, 'Previous',);
    paginationList.appendChild(prevItem);
  }

  // Create numbered buttons for pages
  for (let num = 1; num <= totalPages; num++) {
    const pageItem = createPaginationItem(num, num, currentPage === num ? 'active' : '');
    paginationList.appendChild(pageItem);
  }

  // Create Next button
  if (currentPage < totalPages) {
    const nextItem = createPaginationItem(currentPage + 1, 'Next',);
    paginationList.appendChild(nextItem);
  }

  paginationComponent.appendChild(paginationList);

  existingPaginationContainer.innerHTML = ''; // Clear existing content
  existingPaginationContainer.appendChild(paginationComponent);
}



// function renderPagination(data, currentPage) {
//   const totalPages = Math.ceil(data.count / 10); // Assuming 10 items per page

//   const paginationComponent = document.createElement('nav');
//   paginationComponent.setAttribute('aria-label', 'Page navigation example');

//   const paginationList = document.createElement('ul');
//   paginationList.classList.add('pagination');

//   // Helper function to create pagination items
//   const createPaginationItem = (pageNum, text, className = '') => {
//       const listItem = document.createElement('li');
//       listItem.classList.add('page-item', className);

//       const link = document.createElement('a');
//       link.classList.add('page-link');
//       link.href = '#';
//       link.textContent = text;
//       link.addEventListener('click', (event) => {
//           event.preventDefault();
//           renderPagination(data, pageNum);
//       });

//       listItem.appendChild(link);
//       return listItem;
//   };

//   // Create Previous button
//   if (currentPage > 1) {
//       const prevItem = createPaginationItem(currentPage - 1, 'Previous');
//       paginationList.appendChild(prevItem);
//   }

//   // Create numbered buttons for pages
//   for (let num = 1; num <= totalPages; num++) {
//       const pageItem = createPaginationItem(num, num, currentPage === num ? 'active' : '');
//       paginationList.appendChild(pageItem);
//   }

//   // Create Next button
//   if (currentPage < totalPages) {
//       const nextItem = createPaginationItem(currentPage + 1, 'Next');
//       paginationList.appendChild(nextItem);
//   }

//   paginationComponent.appendChild(paginationList);

//   // const existingPaginationContainer = document.getElementById('existingPaginationContainer');
//   existingPaginationContainer.innerHTML = ''; // Clear existing content
//   existingPaginationContainer.appendChild(paginationComponent);
// }



// create page component
function createPaginationItem(page, label, className = '') {

  const listItem = document.createElement('li');
  listItem.classList.add('page-item');
  if (className.trim() !== '') {
    listItem.classList.add(className.trim());
  }

  const link = document.createElement('a');
  link.classList.add('page-link');
  link.href = "#";
  link.textContent = label;

  listItem.appendChild(link);

  link.addEventListener('click', (event) => {
    event.preventDefault(); // Prevent default anchor behavior
    fetchData(page = page); // Assuming label is the page number
  });

  return listItem;
}


// get search query
function getSearchQuery() {
  const params = new URLSearchParams(window.location.search);
  return params.get('search');
}

// ------------------------------------------------  js modal data manipulate and edit and save -------------------------------------------



// // render table or message
function renderDataOrMessage(tableBody, data, page) {
 
  // Check if data is available and not empty
  if (data && Array.isArray(data.results) && data.results.length > 0) {
    // Render the data in the table

    let tdata = data?.results

    tdata.forEach((item, index) => {
      const newRow = createTableRow(index + 1, item);
      tableBody.appendChild(newRow);
    });

    renderPagination(data, page)

  } else {
    // Display a message indicating no data available
    tableBody.innerHTML = '<tr><td colspan="6">No data available.</td></tr>';

    existingPaginationContainer.innerHTML = ''; // Clear existing content
  }
}





//--------- for data modal
// openCustomDataModal
function openCustomDataModal(modalId) {
  const paymentHistoryModal = new bootstrap.Modal(document.getElementById(modalId));
  paymentHistoryModal.show();
}



function setModalInputValue(form, fieldName, value) {
  const inputElement = form.querySelector(`[name="${fieldName}"]`);
  if (!inputElement) {
    // console.error(`Input element with name "${fieldName}" not found in the form.`);
    return;
  }

  if (inputElement.tagName === 'TEXTAREA') {
    inputElement.value = value;
  } else if (inputElement.tagName === 'SELECT') {
    const option = inputElement.querySelector(`option[value="${value}"]`);
    if (option) {
      option.selected = true;
    } else {
      // console.error(`Option with value "${value}" not found in the select element.`);
    }
  } else {
    inputElement.value = value;
  }
}



function toggleFormEditing(form, readOnlyFields, readOnlyValue, enableEditing) {
  const inputs = form.querySelectorAll('input, textarea, select');
  inputs.forEach(input => {
    if (!readOnlyFields.includes(input.name)) {
      input.readOnly = !enableEditing;
      if (!input.readOnly) {
        input.classList.remove('read-only-field');
      }
    } else {
      input.readOnly = true;
      input.classList.add('read-only-field');

    }
  });
}



// function get_value(value) {
//   return value || "Nill";
// }



// get value function
function get_value(value) {

  // Check if value is null, undefined, or an empty string, then return 'Nill'
  if (value === null || value === undefined || value === '') {
    return 'Nill';
  }

  // Check if value is a number, not NaN, and not just whitespace, then return the value
  if (typeof value === 'number' && !isNaN(value)) {
    let valueStr = value.toString();
    var val = truncate(valueStr)
    return val;
  }

  // Check if value is a string and not just whitespace, then return the value
  if (typeof value === 'string' && value.trim() !== '') {
    var val = truncate(value)
    return val;
  }

  // Otherwise, return 'Nill'
  return 'Nill';
}


function truncate(value) {

  if (value.length > TruncateLength) {
    return value.substring(0, TruncateLength) + TruncateExt;
  }
  return value;


}



function get_filename(value) {
  if (value === null || value === undefined || value === '') {
    return 'Nill';
  }


  // return get_value(txt) + "." + ext
  const fileName = (value.substring(value.lastIndexOf('/') + 1));
  // return fileName

  const txtarray = fileName.split('.')  //["tezt",'png']
  const ext = txtarray.pop()
  const txt = truncate(txtarray.pop())
  return (txt) + "." + ext


}



// --------------------------  TABLE CELL CREATION ---------------------------------------


// Helper function to create custom status cells
const createStatusCell = (status, className) => {
  const cell = document.createElement('td');
  const statusComponent = document.createElement('span');
  statusComponent.textContent = status;
  if (className) {
    let classList = className.split(' ')
    // console.log(classList)
    statusComponent.classList.add(...classList)
    cell.appendChild(statusComponent);
    return cell;
  }
  else {
    statusComponent.style.color = status === 'Paid' ? 'green' : 'red';
  }

  cell.appendChild(statusComponent);
  return cell;
};

// Helper function to create custom amount cells with currency
const createAmountCell = (amount, currency = false) => {
  const cell = document.createElement('td');
  const amountComponent = document.createElement('span');
  const formattedAmount = formatAmount(amount); // Ensure 'amount' is parsed to a number
  // console.log(formattedAmount)
  amountComponent.textContent = currency ? currencyFormatter.format(formattedAmount) : formattedAmount;
  cell.appendChild(amountComponent);
  return cell;
};


function formatAmount(amount) {
  //  console.log(amount)
  if (amount == null || amount === '') {
    return 0.00;
  }
  const formattedAmount = parseFloat(amount).toFixed(2);

  if (isNaN(formattedAmount)) {
    return 0.00;
  }

  return formattedAmount;
}

// Helper function to create serial number cells
const createSerialCell = (serialNumber) => {
  const cell = document.createElement('td');
  cell.textContent = serialNumber;
  return cell;
};

// Helper function to create generic table cells
const createTableCell = (data) => {
  const cell = document.createElement('td');
  cell.textContent = data;
  return cell;
};




// acton cell modal for view
const createViewActionCell = (modalId) => {
  const actionCell = document.createElement('td');
  actionCell.innerHTML = `<button class="btn btn-soft-secondary btn-sm dropdown" type="button" onclick="openCustomDataModal('${modalId}')">
                  <i class="ri-eye-fill align-middle"></i>
              </button>`;
  return actionCell;
};


const createPayActionCell = (modalId) => {
  const actionCell = document.createElement('td');
  actionCell.innerHTML = `<button class="btn btn-soft-secondary btn-sm dropdown" type="button" onclick="openCustomDataModal('${modalId}')">
                  Pay
              </button>`;
  return actionCell;
};



function createPaidCell(value, amount) {
  const cell = document.createElement('td');
  const span = document.createElement('span');

  const i = document.createElement('i')

  if (parseFloat(amount) === 0) {
 
    span.classList.add("badge", "bg-success-subtle", "text-info", "fs-12");
    span.textContent = "Nill";

    span.appendChild(i)
    cell.appendChild(span)

    return cell;
  }

  if (parseFloat(value) > 0 || value === true) {

    span.classList.add("badge", "bg-success-subtle", "text-success", "fs-12");
    span.textContent = "Paid";

  } else if (parseFloat(value) < 0 || value === false) {

    span.classList.add("badge", "bg-danger-subtle", "text-danger", "fs-12");
    span.textContent = "unpaid";

  }
  span.appendChild(i)
  cell.appendChild(span)

  return cell;
}


function createPaidStatusCell(value, text) {
  const cell = document.createElement('td');
  const span = document.createElement('span');

  const i = document.createElement('i')

  span.textContent = text;

  if (value == 0 || value == "true") {

    span.classList.add("badge", "bg-success-subtle", "text-success", "fs-12");


  } else if (value == 1 || value == "false") {

    span.classList.add("badge", "bg-danger-subtle", "text-danger", "fs-12");


  }
  span.appendChild(i)
  cell.appendChild(span)

  return cell;
}




// ------------------------------------  close all models -----------------------------------------

// // openModal
function openHistoryModal(modalId) {
  const HistoryModal = new bootstrap.Modal(document.getElementById(modalId));
  HistoryModal.show();
}



function closeHistoryModal(modalId) {
  closeAllModals();
  restoreAllForms();
  clearErrors();
  return


  // console.log(modalId)
  var modalElement = document.getElementById(modalId);

  // console.log(modalElement)

  // If the modal element is found, close it using Bootstrap's modal method
  if (modalElement) {
    var modalInstance = bootstrap.Modal.getInstance(modalElement);
    if (modalInstance) {
      modalInstance.hide();
    } else {
      // If no instance exists, create a new one and then hide it
      modalInstance = new bootstrap.Modal(modalElement);
      modalInstance.hide();
    }
  } else {
    // console.error('Modal element not found for selector: ' + modalId);
  }

  var myModal = new bootstrap.Modal(document.getElementById(modalId));
  myModal.hide();
}



// close all modals
function closeAllModals() {
  var modals = document.querySelectorAll('.modal.show'); // Select all active modals
  modals.forEach(modalElement => {
    var modalInstance = bootstrap.Modal.getInstance(modalElement);
    if (modalInstance) {
      modalInstance.hide();
    } else {
      modalInstance = new bootstrap.Modal(modalElement);
      modalInstance.hide();
    }
  });
}


// reset all forms
function restoreAllForms() {
  var forms = document.querySelectorAll('form'); // Select all forms on the page
  forms.forEach(form => {
    form.reset(); // Reset each form to its default state
  });
}



// -------------------------------------- report generation -----------------





function getReport(button, tableId) {
  // Show loader
  button.disabled = true;
  const btnText = button.innerText;
  button.innerText = 'Generating Report...';

  const table = document.getElementById(tableId);
  const rows = table.getElementsByTagName('tr');

  let csv = '';
  const headers = table.getElementsByTagName('th');
  const columnsToSkip = [];

  // Get table headers
  for (let i = 0; i < headers.length; i++) {
    if (headers[i].innerText.toLowerCase() !== 'action') {
      csv += '"' + headers[i].innerText + '"' + (i < headers.length - 1 ? ',' : '');
    } else {
      columnsToSkip.push(i);
    }
  }
  csv += '\n';

  // Iterate over rows to build the CSV
  for (let i = 1; i < rows.length; i++) { // Start from 1 to skip header row
    const cells = rows[i].getElementsByTagName('td');
    for (let j = 0; j < cells.length; j++) {
      if (!columnsToSkip.includes(j)) {
        csv += '"' + cells[j].innerText + '"' + (j < cells.length - 1 ? ',' : '');
      }
    }
    csv += '\n';
  }

  // Trigger the download of the CSV file
  downloadCSV(csv, 'report.csv');

  // Hide loader
  button.disabled = false;
  button.innerText = btnText;
}

// Function to download the report as a CSV file
function downloadCSV(csv, filename) {
  const csvFile = new Blob([csv], { type: 'text/csv' });
  const downloadLink = document.createElement('a');

  downloadLink.download = filename;
  downloadLink.href = window.URL.createObjectURL(csvFile);
  downloadLink.style.display = 'none';
  document.body.appendChild(downloadLink);
  downloadLink.click();
  document.body.removeChild(downloadLink);
}



// --------- ----------------------
function console_log(...args) {
  const formattedArgs = args.map(arg => `${arg}`).join(', ');
  console.log(formattedArgs);
}
