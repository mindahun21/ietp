function resetForm() {
  const form = document.getElementById('add-staff-form');
  form.reset();
}

document.body.addEventListener('htmx:afterSwap', (event) => {
  const messageArea = document.getElementById('message-area');
  if (messageArea.querySelector('[data-success="true"]')) {
    resetForm();
  }
});
