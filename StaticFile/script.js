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