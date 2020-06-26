document.addEventListener('DOMContentLoaded',() => {
    document.querySelector('#form').onsubmit = () => {
        const DisplayName = document.querySelector('#DisplayName').value;
        alert(`Hello ${DisplayName}!`);
    };
});
