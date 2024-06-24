var password = document.querySelector("#new_password");
var text, validIcons, invalidIcons;
var a = 0, b = 0, c = 0, d = 0;

function valid(item, validIcon, invalidIcon) {
    console.log(`Validating ${item}`);
    text = document.querySelector(`#${item}`);
    console.log(text);  // Check if the element is correctly selected
    text.style.opacity = "1";
    validIcons = document.querySelector(`#${item} .${validIcon}`);
    validIcons.style.opacity = '1';
    invalidIcons = document.querySelector(`#${item} .${invalidIcon}`);
    invalidIcons.style.opacity = "0";
}

function invalid(item, validIcon, invalidIcon) {
    console.log(`Invalidating ${item}`);
    text = document.querySelector(`#${item}`);
    console.log(text);  // Check if the element is correctly selected
    text.style.opacity = "0.5";
    validIcons = document.querySelector(`#${item} .${validIcon}`);
    validIcons.style.opacity = '0';
    invalidIcons = document.querySelector(`#${item} .${invalidIcon}`);
    invalidIcons.style.opacity = "1";
}


function textChange() {
    console.log("Password Value:", password.value);

    if (password.value.match(/[A-Z]/) != null) {
        valid('capital', 'fa-check', 'fa-times');
        a = 1;
    } else {
        invalid('capital', 'fa-check', 'fa-times');
        console.log("Uppercase Letter not found");
    }

    if (password.value.match(/[0-9]/) != null) {
        valid('number', 'fa-check', 'fa-times');
        b = 1;
    } else {
        invalid('number', 'fa-check', 'fa-times');
        console.log("Digit not found");
    }

    if (password.value.match(/[!@#$%^&*]/) != null) {
        valid('special-char', 'fa-check', 'fa-times');
        c = 1;
    } else {
        invalid('special-char', 'fa-check', 'fa-times');
        console.log("Special Character not found");
    }

    if (password.value.length >= 8) {
        valid('more-than-8', 'fa-check', 'fa-times');
        d = 1;
    } else {
        invalid('more-than-8', 'fa-check', 'fa-times');
        console.log("Password length less than 8");
    }

    console.log("Flags:", a, b, c, d);
}

document.querySelector('form').addEventListener('submit', function (event) {
    if ((a == 1) && (b == 1) && (c == 1) && (d == 1)) {
        // Form submission allowed
    } else {
        event.preventDefault();
        alert('Please set up a strong password according to the parameters!');
    }
});
