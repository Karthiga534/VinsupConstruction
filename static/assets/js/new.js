// var csrftoken = getCookie('csrftoken');
// function getCookie(name) {
//     var cookieValue = null;
//     if (document.cookie && document.cookie !== '') {
//         var cookies = document.cookie.split(';');
//         for (var i = 0; i < cookies.length; i++) {
//             var cookie = cookies[i].trim();
//             if (cookie.substring(0, name.length + 1) === (name + '=')) {
//                 cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
//                 break;
//             }
//         }
//     }
//     return cookieValue;
// }


// function getAuthToken() {
//     var authToken = localStorage.getItem('authToken');
//     if (!authToken) {
//         authToken = getCookie('authToken');
//     }
//     return authToken;
// }


// function getValueOrDefault(value) {
//     return (typeof value !== 'undefined' && value !== null) ? value : '';
//     // return value
// }

// // ------------------------------------------------------------------------------------------------------------------------------------------

// // Helper function to show Bootstrap toast notifications
// function showToast(title, message, bgColor, reload) {

//     var toastContainer = $('#toastContainer');
//     var toastId = 'toast-' + Math.floor(Math.random() * 1000); // Generate a random toast ID

//     var toastHTML = `
//       <div id="${toastId}" class="toast align-items-center text-white ${bgColor}" role="alert" aria-live="assertive" aria-atomic="true">
//         <div class="d-flex">
//           <div class="toast-body">
//             <strong>${title}</strong><br>${message}
//           </div>
//           <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
//         </div>
//       </div>
//     `;

//     toastContainer.append(toastHTML);

//     var toastElement = $('#' + toastId);
//     var toastInstance = new bootstrap.Toast(toastElement);

//     toastInstance.show();

//     // Remove the toast after a delay (e.g., 5 seconds)
//     setTimeout(function () {
//         toastElement.remove();
//         if (reload) {
//             location.reload();
//         }
//     }, 2000);
// }


// function handleCreateErrors(errors) {
//     console.log(errors);


//     $('.form-control').removeClass('is-invalid');
//     $('.error-message').text('');

//     for (var fieldName in errors) {
//         if (errors.hasOwnProperty(fieldName)) {
//             var errorMessage = errors[fieldName][0];

//             $('#' + fieldName).addClass('is-invalid');
//             $('#' + fieldName + 'Error').text(errorMessage);
//         }
//     }
// }



// // for breakerrors into custom
// function transformErrors(errorObj) {
//     const transformedErrors = {};
//     for (const key in errorObj) {
//         if (Array.isArray(errorObj[key])) {
//             transformedErrors[key] = errorObj[key];
//         } else if (typeof errorObj[key] === 'object') {
//             const nestedErrors = transformErrors(errorObj[key]);
//             for (const nestedKey in nestedErrors) {
//                 transformedErrors[key + '_' + nestedKey] = nestedErrors[nestedKey];
//             }
//         }
//     }
//     return transformedErrors;
// }




// function handleUpdateErrors(modelId, errorObj) {
//     console.log(modelId, errorObj)
//     for (const key in errorObj) {
//         const inputId = modelId + '_' + key;
//         const errorMessage = errorObj[key][0];
//         const errorSpan = document.getElementById(inputId + 'Error');

//         console.log(errorMessage, errorSpan, inputId)
//         $('#' + inputId).addClass('is-invalid');

//         errorSpan.textContent = errorMessage;

//     }
// }

// // -----------------------------------------------------------------------------------------------------------------------------

// let initialFormValues = {};
// var model_Id;
// var model_Name;


// function openModal(modelName, modelId) {
//     $(`#${modelName}_${modelId}`).modal('show');
//     captureInitialValues(modelId);
//     model_Id = modelId;
//     model_Name = modelName;

// }

// // Function to capture initial form values based on model ID
// function captureInitialValues(modelId) {

//     $(`#edituserForm${modelId} input , #edituserForm${modelId} textarea ,
//      #editinfoForm${modelId} input , #editinfoForm${modelId} textarea ,
//     #editcompanyForm${modelId} input ,  #editcompanyForm${modelId} textarea`).each(function () {
//         const fieldName = this.name;
//         initialFormValues[fieldName] = this.value;
//     });

// }


// // close model
// // Function to close the modal and reset form elements
// function CloseModel(modelName, modelId) {
//     var errorSpans = document.querySelectorAll('.error-message');
//     errorSpans.forEach(function (span) {
//         span.textContent = '';
//     });

//     var formControls = document.querySelectorAll('.form-control');
//     formControls.forEach(function (control) {
//         control.classList.remove('is-invalid');
//     });
//     console.log(`${model_Name}_${model_Id}`)
//     model_Id = ''
//     model_Name = ''
//     resetFormValues(modelName, modelId);
// }


// // Function to capture initial form values based on model ID
// function resetFormValues(modelName, modelId) {
//     console.log(initialFormValues)
//     $(`#edituserForm${modelId} input , #edituserForm${modelId} textarea ,
//     #editinfoForm${modelId} input , #editinfoForm${modelId} textarea ,
//    #editcompanyForm${modelId} input ,  #editcompanyForm${modelId} textarea`).each(function () {
//         const fieldName = this.name;
//         const initialValue = initialFormValues[fieldName];
//         if (initialValue !== undefined) {
//             this.value = initialValue;
//         }
//     });
// }


// $(document).on('hidden.bs.modal', `#${model_Name}_${model_Id}`, function (e) {
//     if (e.target === this) {
//         resetFormValues(model_Name, model_Id);
//     }
// });


// $(`#${model_Name}_${model_Id}`).on('hide.bs.modal', function (e) {
//     alert()
// })




// // clear all errors
// function clearErrors(modelId) {
//     var errorSpans = document.querySelectorAll('.error-message');
//     errorSpans.forEach(function (span) {
//         span.textContent = '';
//     });

//     var formControls = document.querySelectorAll('.form-control');
//     formControls.forEach(function (control) {
//         control.classList.remove('is-invalid');
//     });

// }




// function disableButton(button) {
//     button.disabled = true;
//     // Create a spinner element
//     const spinner = document.createElement('span');
//     spinner.className = 'spinner-border spinner-border-sm me-2';
//     spinner.setAttribute('role', 'status');
//     spinner.setAttribute('aria-hidden', 'true');
//     spinner.innerHTML = '&nbsp;'; // Add space for visual separation
//     // Insert the spinner before the button text
//     // button.innerHTML = '';
//     button.appendChild(spinner);
//     // button.insertAdjacentHTML('beforeend', 'Loading...'); // Adjust text as needed
// }

// // Helper function to enable the button
// function enableButton(button) {
//     button.disabled = false;
//     // Remove the spinner and restore the original button text
//     if (button.lastChild && button.lastChild.classList.contains('spinner-border')) {
//         button.removeChild(button.lastChild);
//     }
// }



// // -------------------------------------------------------------------------------------------------------------------------------------



// document.addEventListener('DOMContentLoaded', function () {


//     const table = document.getElementById('example');
//     const rowNumbers = table.querySelectorAll('.row-number');

//     rowNumbers.forEach((row, index) => {
//         row.textContent = index + 1;
//     });



//     const viewButtons = document.querySelectorAll('.view-btn');
//     const editButtons = document.querySelectorAll('.edit-btn');

//     viewButtons.forEach(button => {
//         button.addEventListener('click', function () {
//             const modalId = this.getAttribute('data-target');
//             const modal = document.querySelector(modalId);
//             if (modal) {
//                 $(modal).modal('show');
//             }
//         });
//     });


//     editButtons.forEach(button => {
//         button.addEventListener('click', function () {
//             const modalId = this.getAttribute('data-target');
//             const modal = document.querySelector(modalId);
//             if (modal) {
//                 $(modal).modal('show');
//             }
//         });
//     });


// });




// function updateFunction(button,saveId) {

//     disableButton(button)

//     clearErrors();

//     const userData = $(`#edituserForm${saveId}`).serialize();
//     const companyData = $(`#editinfoForm${saveId}`).serialize();
//     const addressData = $(`#editcompanyForm${saveId}`).serialize();

//     const formData = `${userData}&${companyData}&${addressData}`;
 

//     console.log(saveId)

//     console.log(csrftoken)
//     $.ajax({
//         url: '/update-user/' + saveId + '/',
//         type: 'PUT',

//         headers: {
//             'X-CSRFToken': csrftoken,
//             // 'Authorization': 'Token ' + authToken 
//         },
//         data: formData,
//         success: function (response, status, xhr) {
//             if (xhr.status === 200) {
//                 showToast('Successfully Updated', '', 'bg-success', true);
//                 // location.reload();
//             }
//             else {
//                 showToast('something went wrong', '', 'bg-danger');
//                 enableButton(button)
//                 console.error(error);
//             }
            
//         },
//         error: function (xhr, status, error) {
//             console.log(xhr, status, error)
//             if (xhr.status === 400) {
//                 if (xhr?.responseJSON || xhr?.responseJSON?.errors) {
                   
//                     handleUpdateErrors(saveId, transformErrors(xhr.responseJSON));
//                     enableButton(button)
//                 } else {
                   
//                     showToast('something went wrong', '', 'bg-danger');
//                     enableButton(button)
//                 }

//             }
//             else {
//                 showToast('something went wrong', '', 'bg-danger');
//                 enableButton(button)
//             }

//         }
//     });
// }



// // create form

// function createFunction(button) {

//     disableButton(button)

//     var isValid = true;
//     var errors = {};
//     var formData = new FormData();

   

//     var proofFile = document.querySelector('#createinfoForm input[type="file"]').files[0];
//     if (proofFile) {
//         formData.append("proof", proofFile);
//     }

//     formData.append('name', getValueOrDefault($('#createuserForm input[name="name"]').val()));
//     formData.append('email', getValueOrDefault($('#createuserForm input[name="email"]').val()));
//     formData.append('phone_number', getValueOrDefault($('#createuserForm input[name="phone_number"]').val()));

//     formData.append('company_name', getValueOrDefault($('#createcompanyForm input[name="company_name"]').val()));
//     formData.append('company_email', getValueOrDefault($('#createcompanyForm input[name="company_email"]').val()));
//     formData.append('company_phone', getValueOrDefault($('#createcompanyForm input[name="company_phone"]').val()));
//     formData.append('company_address', getValueOrDefault($('#createcompanyForm textarea[name="company_address"]').val()));

//     formData.append('address', getValueOrDefault($('#createinfoForm textarea[name="address"]').val()));

//     console.log('FormData:', formData);

//     formData.forEach(function (value, key) {
//         console.log(key, value)
//         // Check if the value is empty or contains only whitespace
//         if (!value.trim()) {
//             isValid = false;
//             errors[key] = ['This field may not be blank.'];
//         }
//     });

//     if (!isValid) {
//         enableButton(button)
//         console.log(errors)
       
//         handleCreateErrors(errors);
        
//         return
//     } else {
       
//         $('#createForm input, #createForm button').prop('disabled', true);
//         enableButton(button)


//     }
//     $.ajax({
//         url: '/create-user/',
//         type: 'POST',

//         headers: {
//             'X-CSRFToken': csrftoken,
//             // 'Authorization': 'Token ' + authToken 
//         },
//         data: formData,

//         processData: false, 
//         contentType: false, 

//         success: function (response, status, xhr) {

//             console.error(status);
//             if (xhr.status === 201) {
//                 showToast('Successfully Updated', '', 'bg-success', true);
//                 // location.reload();
//             }
//             else {
//                 console.error(error);
//                 enableButton(button)
//             }

//         },
//         error: function (xhr, status, error) {
//             console.log(xhr, status, error)
//             if (xhr.status === 400) {
//                 if (xhr?.responseJSON || xhr?.responseJSON?.errors) {
                   
//                     handleCreateErrors(saveId, transformErrors(xhr.responseJSON));
//                     enableButton(button)
//                 } else {
                  
//                     showToast('something went wrong', '', 'bg-danger');
//                     enableButton(button)
//                 }

//             }
//             else {
//                 showToast('something went wrong', '', 'bg-danger');
//                 enableButton(button)
//             }
//         }
//     });
// }
