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

//Question 2 Responses
function editMajorResponse(questionId) {
    const majors = [
        "Accounting",
        "African-american/black studies",
        "Allied health diagnostic, intervention, and treatment professions",
        "Anthropology",
        "Architecture",
        "Art history, criticism and conservation",
        "Art/art studies",
        "Biology/biological sciences",
        "Business administration and management",
        "Business/managerial economics",
        "Chemistry",
        "Civil engineering",
        "Civil engineering technology/technician",
        "Computer engineering",
        "Computer science",
        "Criminal justice/safety studies",
        "Dance",
        "Drama and dramatics/theatre arts",
        "Economics",
        "Electrical and electronics engineering",
        "Electrical, electronic and communications engineering technology/technician",
        "Elementary education and teaching",
        "Engineering technologies and engineering-related fields",
        "English language and literature",
        "Exercise physiology",
        "Finance",
        "Fine/studio arts",
        "French language and literature",
        "Geography",
        "Geology/earth science",
        "German language and literature",
        "Graphic design",
        "Health and physical education/fitness",
        "Health/health care administration/management",
        "History",
        "Information technology",
        "International business/trade/commerce",
        "International/global studies",
        "Japanese language and literature",
        "Junior high/intermediate/middle school education and teaching",
        "Kindergarten/preschool education and teaching",
        "Latin american studies",
        "Management science",
        "Marketing/marketing management",
        "Mathematics",
        "Mathematics and computer science",
        "Mathematics and statistics",
        "Mechanical engineering",
        "Mechanical engineering/mechanical technology/technician",
        "Meteorology",
        "Music",
        "Music performance",
        "Operations management and supervision",
        "Philosophy",
        "Physics",
        "Political science and government",
        "Psychology",
        "Public health",
        "Registered nursing/registered nurse",
        "Religion/religious studies",
        "Respiratory care therapy/therapist",
        "Social work",
        "Sociology",
        "Spanish language and literature",
        "Special education and teaching",
        "Special education and teaching",
        "Speech communication and rhetoric",
        "Systems engineering",];


    //fetches the current value
    const element = document.querySelector(`[data-category="${questionId}"]`);
    const currentValue = element.innerText.trim();

    //dropdown with the current value preselected
    let dropdown = `<select onchange="updateMajorResponse('${questionId}')">`;
    majors.forEach(major => {
        const isSelected = major === currentValue ? "selected" : "";
        dropdown += `<option value="${major}" ${isSelected}>${major}</option>`;
    });
    dropdown += `</select>`;

    // Replace the span content with the dropdown
    if (element) {
        element.innerHTML = dropdown;
    }
}

function updateMajorResponse(questionId) {
    const selectedValue = document.querySelector(`[data-category="${questionId}"] select`).value;
    const element = document.querySelector(`[data-category="${questionId}"]`);
    if (element) {
        element.innerText = selectedValue; 
    }
}

function deleteMajorResponse(questionId) {
    const element = document.querySelector(`[data-category="${questionId}"]`);
    if (element) {
        element.innerText = "empty";
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


function editResponse(questionId) {
    // Extract the question key from questionId
    const questionKey = questionId.split('-')[0];

    // Get the list of options for the given question
    const options = questionOptions[questionKey];
    if (!options) {
        console.error(`No options available for question: ${questionKey}`);
        return;
    }

    // Generate the dropdown with the current options
    let dropdown = `<select onchange="updateResponse('${questionId}')">`;
    options.forEach(option => {
        dropdown += `<option value="${option}">${option}</option>`;
    });
    dropdown += `</select>`;

    // Find the element with the matching data-category attribute
    const element = document.querySelector(`[data-category="${questionId}"]`);
    if (element) {
        // Replace current text or content with the dropdown
        element.innerHTML = dropdown;
    } else {
        console.error(`Element with data-category="${questionId}" not found`);
    }
}

// Function to update the response with the selected dropdown value
async function updateResponse(questionId) {
    // Find the selected value from the dropdown
    const selectedValue = document.querySelector(`[data-category="${questionId}"] select`).value;

    // Extract question key and user ID from questionId
    const [questionKey, userId] = questionId.split('-');

    // Save the updated response to the server
    try {
        const response = await fetch('/save-response', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                questionKey: questionKey,
                userId: userId,
                selectedValue: selectedValue,
            }),
        });

        if (!response.ok) {
            throw new Error(`Failed to save response for ${questionId}`);
        }

        // Find the element to replace the dropdown with the selected value
        const element = document.querySelector(`[data-category="${questionId}"]`);
        if (element) {
            // Replace the dropdown with the selected value
            element.innerText = selectedValue;
        } else {
            console.error(`Element with data-category="${questionId}" not found`);
        }

        console.log(`Response for ${questionId} saved successfully.`);
    } catch (error) {
        console.error(`Error saving response: ${error.message}`);
    }
}



function deleteResponse(category) {
    const [question, responseId] = category.split('-');

    // Confirm deletion
    if (!confirm('Are you sure you want to delete this response?')) return;

    // Send delete request to the backend
    fetch('/delete_response', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ response_id: responseId, question: question }),
    })
    .then((response) => response.json())
    .then((data) => {
        if (data.success) {
            // Clear the content of the span
            const spanElement = document.querySelector(`[data-category="${category}"]`);
            spanElement.textContent = '(Deleted)';
        } else {
            alert('Failed to delete response: ' + data.error);
        }
    })
    .catch((err) => console.error('Error:', err));
}

function getQuestionType(event) {
    const identifier = document.querySelector("#questionTypeIdentifier");
    const selectedValue = event.target.value;
    let questionType = "";

    console.log("Hopefully this is working!");

    // Determine the question type
    if (selectedValue == 1) {
        questionType = "MC Question";
    } 
    else if (selectedValue == 3) {
        questionType = "One through Five Range";
    } 
    else if (selectedValue == 4) {
        questionType = "Multi-Select";
    } 
    else {
        questionType = "ERROR";
    }

    // This shows what type of Question was selected!
    identifier.innerText = "Type Selected: " + questionType;

    const numOptionsLabel = document.querySelector("#numberOfOptionsLabel");
    numOptionsLabel.for = "numOptionsID";
    numOptionsLabel.textContent = "Number of Options (Between 2 and 5)";
    numOptionsLabel.classList.add("addQuestionNumOptions");

    const numOptionsInput = document.createElement("input");
    numOptionsInput.type = "number";
    numOptionsInput.id = "numOptionsID";
    numOptionsInput.min = "2";
    numOptionsInput.max = "5";
    numberOfOptionsLabel.append(numOptionsInput);
}

// Add event listeners to the radio buttons
document.querySelector("#Type1").addEventListener('click', getQuestionType);
document.querySelector("#Type2").addEventListener("click", getQuestionType);
document.querySelector("#Type3").addEventListener("click", getQuestionType);




/* Matching in Progress */
document.querySelector('.start-matching-btn').addEventListener('click', (event) => {
    const loadingIndicator = document.getElementById('loading-indicator');
    loadingIndicator.classList.remove('hidden');
});

