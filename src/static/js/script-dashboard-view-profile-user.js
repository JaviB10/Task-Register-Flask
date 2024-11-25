//Elementos del DOM
const buttonUpdateProject = document.getElementById('hidden-form-update-user');
const buttonDeleteProjectUser = document.getElementById('hidden-delete-user');
const buttonDetailProject = document.getElementById('hidden-detail-proyect');

const toggleMenu = (event, menuID) => {
    event.preventDefault();
    
    document.querySelectorAll('.menu-user').forEach(menu => {
        if (menu.dataset.menu !== menuID.toString()) {
            menu.classList.add('hidden-menu-user');
        }
    })

    const menu = document.querySelector(`.menu-user[data-menu="${menuID}"]`);
    if (menu) {
        menu.classList.toggle('hidden-menu-user')
    }
}

//Muestra el formulario para actualizar un proyecto y cierra el menu del usuario
const editProject = (menuID) => {  
    buttonUpdateProject.classList.remove('hidden-form-update');

    const menuUser = document.querySelector(`.menu-user[data-menu="${menuID}"]`);
    if (menuUser) {
        menuUser.classList.add('hidden-menu-user');
    }
} 

const closeFormUpdate = () => {
    buttonUpdateProject.classList.toggle('hidden-form-update'); //Alterna la visibilidad del formulario para actualizar el proyecto
}

//Muestra el modal para confirmar la eliminacion de un proyecto y cierra el menu del usuario
const deleteProject = (menuID) => {
    buttonDeleteProjectUser.classList.remove('hidden-delete');

    const deleteModal = document.querySelector(`.menu-user[data-menu="${menuID}"]`);
    if (deleteModal) {
        deleteModal.classList.add('hidden-menu-user')
    }
}

const closeDelete = () => {
    buttonDeleteProjectUser.classList.toggle('hidden-delete'); //Alterna la visibilidad del formulario para actualizar el proyecto
}

//Muestra el formulario para actualizar un proyecto y cierra el menu del usuario
const viewDetails = (menuID) => {  
    buttonDetailProject.classList.remove('hidden-detail');

    const menuUser = document.querySelector(`.menu-user[data-menu="${menuID}"]`);
    if (menuUser) {
        menuUser.classList.add('hidden-menu-user');
    }
} 

const closeDetail = () => {
    buttonDetailProject.classList.add('hidden-detail'); //Alterna la visibilidad del formulario para actualizar el proyecto
}