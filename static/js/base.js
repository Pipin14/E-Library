const hamburgerButton = document.getElementById('hamburgerButton');
const mobileMenu = document.getElementById('mobileMenu');

hamburgerButton.addEventListener('click', () => {
    mobileMenu.classList.toggle('hidden');
});

function toggleMobileDropdown() {
    const dropdown = document.getElementById('mobileProfileDropdown');
    dropdown.classList.toggle('hidden');
}

function toggleDesktopDropdown() {
    const dropdown = document.getElementById('desktopProfileDropdown');
    dropdown.classList.toggle('hidden');
}

document.addEventListener('click', function(event) {
    const mobileDropdown = document.getElementById('mobileProfileDropdown');
    const desktopDropdown = document.getElementById('desktopProfileDropdown');
    const avatarButtonMobile = document.querySelector('button[onclick="toggleMobileDropdown()"]');
    const avatarButtonDesktop = document.querySelector('button[onclick="toggleDesktopDropdown()"]');

    if (!mobileDropdown.contains(event.target) && !avatarButtonMobile.contains(event.target)) {
        mobileDropdown.classList.add('hidden');
    }

    if (!desktopDropdown.contains(event.target) && !avatarButtonDesktop.contains(event.target)) {
        desktopDropdown.classList.add('hidden');
    }
});
