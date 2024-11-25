const sidebar = document.getElementById('sidebar');
const menu = document.getElementById('menu');
const main = document.getElementById('main');

menu.addEventListener('click', () => {
    sidebar.classList.toggle('menu-toggle-app');
    main.classList.toggle('menu-toggle-app');
});