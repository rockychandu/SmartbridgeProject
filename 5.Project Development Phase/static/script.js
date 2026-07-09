
document.addEventListener("DOMContentLoaded", function () {

    const form = document.querySelector("form");

    form.addEventListener("submit", function (event) {

        const inputs = document.querySelectorAll("input");

        for (let input of inputs) {

            if (input.value.trim() === "") {
                alert("Please fill all fields.");
                event.preventDefault();
                return;
            }

            if (isNaN(input.value)) {
                alert("Only numeric values are allowed.");
                event.preventDefault();
                return;
            }
        }

        const button = document.querySelector("button");
        button.innerHTML = "Predicting...";
        button.disabled = true;

    });

});