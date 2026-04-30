// Simple client-side validation for role-button match (no server)
document.addEventListener('DOMContentLoaded', function() {
    const form = document.querySelector('form');
    const roleSelect = document.getElementById('role');
    const errorMsg = document.getElementById('error-msg');
    const userBtn = document.querySelector('button[formaction="lms ui.html"]');
    const staffBtn = document.querySelector('button[formaction="staff.html"]');

    [userBtn, staffBtn].forEach(btn => {
        btn.addEventListener('click', function(e) {
            const selectedRole = roleSelect.value;
    const expectedRole = this.getAttribute('formaction') === 'lms ui.html' ? 'user' : 'staff';
            if (selectedRole !== expectedRole) {
                e.preventDefault();
                errorMsg.textContent = 'Wrong sign up! Selected role does not match button.';
                errorMsg.style.display = 'block';
                setTimeout(() => {
                    errorMsg.style.display = 'none';
                }, 5000);
                return false;
            }
        });
    });
});
