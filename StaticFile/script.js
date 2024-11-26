"use strict";

// const adminButton = document.querySelector("#adminContainer");
// adminButton.classList.toggle("hidden");


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
    q2: ['Accounting', 'African-American/Black studies', 'Allied Health Diagnostic, Intervention, and Treatment Professions', 'Anthropology', 
            'Architecture', 'Art History, Criticism and Conservation', 'Art/Art Studies', 'Biology/Biological Sciences', 'Business Administration and Management',
            'Business/Managerial Economics', 'Chemistry', 'Civil Engineering', 'Civil Engineering Technology/Technician', 'Computer Engineering',
            'Computer Science', 'Criminal Justice/Safety Studies', 'Dance', 'Drama and Dramatics/Theatre Arts', 'Economics', 'Electrical and Electronics Engineering',
            'Electrical, Electronic and Communications Engineering Technology/Technician', 'Engineering Technologies and Engineering-Related Fields',
            'English Language and Literature', 'Exercise Physiology', 'Finance', 'Fine/Studio Arts', 'French Language and Literature', 'Geography',
            'Geology/Earth Science', 'German Language and Literature', 'Graphic Design', 'Health and Physical Education/Fitness', 
            'Health/Health Care Administration/Management', 'History', 'Information Technology', 'International Business/Trade/Commerce',
            'International/Global Studies', 'Japanese Language and Literature', 'Junior High/Intermediate/Middle School Education and Teaching', 
            'Kindergarten/Preschool Education and Teaching', 'Latin American Studies', 'Management Science', 'Marketing/Marketing Management', 'Mathematics', 
            'Mathematics and Computer Science', 'Mathematics and Statistics', 'Mechanical Engineering', 'Mechanical Engineering/Mechanical Technology/Technician', 
            'Meteorology', 'Music', 'Music Performance', 'Operations Management and Supervision', 'Philosophy', 'Physics', 'Political Science and Government', 
            'Psychology', 'Public Health', 'Registered Nursing/Registered Nurse', 'Religion/Religious Studies', 'Respiratory Care Therapy/Therapist', 'Social Work', 
            'Sociology', 'Spanish Language and Literature', 'Special Education and Teaching', 'Speech Communication and Rhetoric', 'Systems Engineering'],
    q3: ['--', 'Yes', 'No', 'Does Not Matter'], 
    q4: ['--', '1', '2', '3', '4', '5'], 
    q5: ['--', '8pm', '10pm', 'Midnight'], 
    q6: ['--', '8pm - 10pm', '10pm - Midnight', 'After Midnight'], 
    q7: ['Quiet Study', 'Study Alone', 'Late Night Study', 'Common Areas Study', 'In Room Study', 'Background Noise Study'],
    q8: ['Sports', 'Reading', 'Gaming', 'Art', 'Cooking'],
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


// Temporary storage for selected values
let temporarySelections = {};

// edit multi-response questions
function editMultiResponse(questionId) {
    const questionKey = questionId.split('-')[0]; // extract question key
    const options = questionOptions[questionKey]; // get options for this question

    if (!options) {
        console.error(`No options available for question: ${questionKey}`);
        return;
    }

    // find the element with data-category
    const element = document.querySelector(`[data-category="${questionId}"]`);
    if (!element) {
        console.error(`Element with data-category="${questionId}" not found`);
        return;
    }

    // retrieve and store the original value
    const originalValue = element.innerText.trim();
    element.setAttribute("data-original-value", originalValue);

    // normalize and filter the original value into an array
    const selectedValues = originalValue
        .split(",")
        .map(val => val.trim().toLowerCase())
        .filter(Boolean);

    console.log(`Original value for ${questionId}: ${originalValue}`);
    console.log(`Normalized selected values for ${questionId}:`, selectedValues);

    //generate the multi-select dropdown with checkboxes
    let dropdown = `<div class="multi-select-dropdown">`;
    options.forEach(option => {
        const isChecked = selectedValues.includes(option.toLowerCase()) ? "checked" : "";
        dropdown += `
            <label class="multi-select-option">
                <span>${option}</span>
                <input type="checkbox" value="${option}" ${isChecked} onchange="updateMultiResponse('${questionId}')">
            </label>`;
    });
    dropdown += `
        <div class="multi-select-buttons">
            <button onclick="saveMultiResponse('${questionId}')">Save</button>
            <button onclick="cancelMultiResponse('${questionId}')">Cancel</button>
        </div>
    </div>`;

    // Replace the current content with the dropdown
    element.innerHTML = dropdown;
}

// save the selected values
function saveMultiResponse(questionId) {
    const element = document.querySelector(`[data-category="${questionId}"]`);
    if (!element) {
        console.error(`Element with data-category="${questionId}" not found`);
        return;
    }

    const checkboxes = element.querySelectorAll("input[type='checkbox']");
    const selectedValues = Array.from(checkboxes)
        .filter(checkbox => checkbox.checked)
        .map(checkbox => checkbox.value);

    // save the selected values in the DOM
    element.innerHTML = selectedValues.length > 0
        ? selectedValues.join(", ")
        : "empty";

    // update the original value attribute
    element.setAttribute("data-original-value", selectedValues.join(", "));
}

// cancel changes and reset to the original state
function cancelMultiResponse(questionId) {
    const element = document.querySelector(`[data-category="${questionId}"]`);
    if (!element) {
        console.error(`Element with data-category="${questionId}" not found`);
        return;
    }

    // restore the original value
    const originalValue = element.getAttribute("data-original-value") || "empty";
    element.innerHTML = originalValue;
}

// delete multi-select responses
function deleteMultiResponse(questionId) {
    const element = document.querySelector(`[data-category="${questionId}"]`);
    if (!element) {
        console.error(`Element with data-category="${questionId}" not found`);
        return;
    }
    element.innerHTML = "empty";
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

// MAJORS EDIT AND DELETE

function 