//SURVEY PAGE: Question 2
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

            // Implement Algorithm to include proper scaling of the size
            // const currentHeight = select.style.maxHeight.value;
            // currentHeight = currentHeight - 40;
            // select.style.maxHeight = currentHeight;
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

// DROPDOWN FOR RESPONSES
function toggleDropdown(id) {
    var dropdown = document.getElementById(id);
    if (dropdown.style.display === "none") {
        dropdown.style.display = "block";
    } else {
        dropdown.style.display = "none";
    }
}

// MODIFYING RESPONSE ANSWERS
const questionOptions = {
    q1: ['--', 'Freshman', 'Sophomore', 'Junior', 'Senior', 'Graduate Student'], 
    q3: ['--', 'Yes', 'No', 'Does Not Matter'], 
    q4: ['--', '1', '2', '3', '4', '5'], 
    q5: ['--', '8pm', '10pm', 'Midnight'], 
    q6: ['--', '8pm - 10pm', '10pm - Midnight', 'After Midnight'], 
    q9: ['--', 'Cool', 'Warm', 'Moderate'], 
    q10: ['--', 'Tidy', 'Messy'], 
    q11: ['--', 'Confront it', 'Avoid it'] 
};

// Function to create a dropdown for editing a response
function editResponse(questionId) {
    const questionKey = questionId.split('-')[0];
    const options = questionOptions[questionKey]; //options

    let dropdown = `<select onchange="updateResponse('${questionId}')">`;
    options.forEach(option => {
        dropdown += `<option value="${option}">${option}</option>`;
    });
    dropdown += `</select>`;

    // find the element with the data-catagory attribute
    const element = document.querySelector(`[data-category="${questionId}"]`);
    if (element) {
        // replaced current text with the dropdown menu
        element.innerHTML = dropdown;
    } else {
        console.error(`Element with data-category="${questionId}" not found`);
    }
}

// update response with the selected option from the dropdown
function updateResponse(questionId) {
    const selectedValue = document.querySelector(`[data-category="${questionId}"] select`).value;
    const element = document.querySelector(`[data-category="${questionId}"]`);

    //replace the dropdown with the selected value
    if (element) {
        element.innerText = selectedValue;
    }
}

// delete response and replace with the defualt response
function deleteResponse(questionId) {
    const element = document.querySelector(`[data-category="${questionId}"]`);
    if (element) {
        element.innerText = 'empty';
    }
}

// SEARCH BAR FOR RESPONSES PAGE
function filterResponses(event) {
    event.preventDefault(); // stops the page reloading whgen submitted

    // get the value entered in the search input
    const searchValue = document.getElementById("search").value.trim();
    // get all the response boxes on the page
    const responseBoxes = document.querySelectorAll(".response-box");

    responseBoxes.forEach(box => {
        const responseIdElement = box.querySelector(".response-header h3");
        //replace text to the ID number
        const responseId = responseIdElement.textContent.replace("Response ID: ", "").trim();

        if (searchValue === "" || responseId === searchValue) {
            box.style.display = "block";
        } else {
            box.style.display = "none";
        }
    });

}
