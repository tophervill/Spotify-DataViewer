document.querySelectorAll('.flash').forEach((message) => {
    window.setTimeout(() => message.remove(), 5000);
});
