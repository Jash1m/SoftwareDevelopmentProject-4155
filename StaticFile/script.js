//SURVEY PAGE

//Question 2 Dropdown
function filterMajors() {
    const input = document.getElementById("search").value.toLowerCase();
    const select = document.getElementById("majorSelect");
    const options = select.options;

    // Remove selected-border class when user starts typing
    document.getElementById("search").classList.remove("selected-border");

    // Show the dropdown if there's input, hide it if input is empty
    if (input) {
        select.style.display = "block";
    } else {
        select.style.display = "none";
    }

    // Filter options based on input
    for (let i = 0; i < options.length; i++) {
        const optionText = options[i].text.toLowerCase();
        if (optionText.includes(input)) {
            options[i].style.display = ""; // Show matching options
        } else {
            options[i].style.display = "none"; // Hide non-matching options
        }
    }
}

function selectMajor() {
    const select = document.getElementById("majorSelect");
    const input = document.getElementById("search");

    // Set input value to the selected option and hide dropdown
    input.value = select.value;
    select.style.display = "none";

    // Add the selected-border class to change the border color
    input.classList.add("selected-border");
}

//RESPONSES PAGE

//Response Page Dropdown
function toggleDropdown(id) {
    var dropdown = document.getElementById(id);
    if (dropdown.style.display === "none") {
        dropdown.style.display = "block";
    } else {
        dropdown.style.display = "none";
    }
}

 // Question 1
 const yearOptions = ['Freshman', 'Sophomore', 'Junior', 'Senior', 'Graduate Student'];

 // create dropdown for editing the "Year" response
 function editResponse(elementId) {
     let dropdown = `<select onchange="updateResponse('${elementId}')">`;
     yearOptions.forEach(option => {
         dropdown += `<option value="${option}">${option}</option>`;
     });
     dropdown += `</select>`;

     // find the element with the data-category attribute
     const element = document.querySelector(`[data-category="${elementId}"]`);
     if (element) {
         // replaced current text with the dropdown menu
         element.innerHTML = dropdown;
     } else {
         console.error(`Element with data-category="${elementId}" not found`);
     }
 }

 // update response with the selected option from the dropdown
 function updateResponse(elementId) {
     const selectedValue = document.querySelector(`[data-category="${elementId}"] select`).value;
     
     //update the element text with the selected value
     document.querySelector(`[data-category="${elementId}"]`).innerText = selectedValue;
 }

 // delete response and replace with the defualt response
 function deleteResponse(elementId) {
     document.querySelector(`[data-category="${elementId}"]`).innerText = 'empty';
 }
