document.getElementById("generate").addEventListener("click", async () => {
    const length = document.getElementById("length").value;

    // Ensure length is within valid range
    if (length < 1 || length > 128) {
        const passwordDisplay = document.getElementById("generated-password");
        passwordDisplay.textContent = "Password length must be between 1 and 128.";
        passwordDisplay.style.color = "red";
        document.getElementById("copy-password").style.display = "none"; // Hide the copy button
        return;
    }

    const includeUppercase = document.getElementById("uppercase").checked;
    const includeLowercase = document.getElementById("lowercase").checked;
    const includeDigits = document.getElementById("digits").checked;
    const includeSpecial = document.getElementById("special").checked;

    const response = await fetch(`http://127.0.0.1:8000/generate-password/?length=${length}&include_uppercase=${includeUppercase}&include_lowercase=${includeLowercase}&include_digits=${includeDigits}&include_special=${includeSpecial}`);
    const data = await response.json();

    // Display the generated password
    const passwordDisplay = document.getElementById("generated-password");
    passwordDisplay.textContent = `Generated Password: ${data.password}`;
    passwordDisplay.style.color = "#000000"; 

    // Show the copy button
    const copyButton = document.getElementById("copy-password");
    copyButton.style.display = "inline-block";
    copyButton.textContent = "Copy";

    // Attach the password to the button's dataset for copying
    copyButton.dataset.password = data.password;
});

document.getElementById("copy-password").addEventListener("click", () => {
    const copyButton = document.getElementById("copy-password");
    const password = copyButton.dataset.password;

    // Use the Clipboard API to copy the password
    navigator.clipboard.writeText(password).then(() => {
        // Change the button text to "Copied!" and update the color
        copyButton.textContent = "Copied!";
        copyButton.style.backgroundColor = "#b8a430";
        setTimeout(() => {
            copyButton.textContent = "Copy";
            copyButton.style.backgroundColor = ""; // Reset background color
        }, 2000); // Reset after 2 seconds
    }).catch(err => {
        console.error("Failed to copy password: ", err);
    });
});


document.getElementById("check-strength").addEventListener("click", async () => {
    const password = document.getElementById("password").value;

    // Validate if the password field is empty
    if (!password) {
        const passwordStrengthDisplay = document.getElementById("password-strength");
        passwordStrengthDisplay.textContent = "Please enter a password.";
        passwordStrengthDisplay.style.color = "red";
        document.getElementById("strength-level").style.width = "0%"; // Reset strength bar
        const tipsList = document.getElementById("password-tips");
        tipsList.innerHTML = ""; // Clear any existing tips
        return;
    }

    const response = await fetch(`http://127.0.0.1:8000/check-password-strength/?password=${encodeURIComponent(password)}`);
    const data = await response.json();

    // Display strength
    const passwordStrengthDisplay = document.getElementById("password-strength");
    passwordStrengthDisplay.textContent = `Password Strength: ${data.strength}`;
    passwordStrengthDisplay.style.color = "#333";

    // Update strength bar
    const strengthBar = document.getElementById("strength-level");
    let strengthPercentage = 0;
    let barColor = "red";

    switch (data.strength) {
        case "Weak":
            strengthPercentage = 25;
            barColor = "red";
            break;
        case "Fair":
            strengthPercentage = 50;
            barColor = "orange";
            break;
        case "Strong":
            strengthPercentage = 75;
            barColor = "yellow";
            break;
        case "Very Strong":
            strengthPercentage = 100;
            barColor = "green";
            break;
    }

    strengthBar.style.width = `${strengthPercentage}%`;
    strengthBar.style.backgroundColor = barColor;

    // Display tips
    const tipsList = document.getElementById("password-tips");
    tipsList.innerHTML = ""; // Clear previous tips
    data.tips.forEach((tip) => {
        const listItem = document.createElement("li");
        listItem.textContent = tip;
        tipsList.appendChild(listItem);
    });
});

//nice style: https://codepen.io/carol_costa/pen/jOQvjGq
