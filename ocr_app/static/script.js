function copyText() {
    const text = document.querySelector('pre').innerText;
    navigator.clipboard.writeText(text).then(() => {
        alert('Text copied to clipboard!');
    });
}