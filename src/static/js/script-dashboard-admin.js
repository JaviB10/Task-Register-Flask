//Elementos del DOM
const buttonAddProjectAdmin = document.getElementById('add-project-admin');
const formAdmin = document.getElementById('hidden-form-admin');
const buttonCloseForm = document.getElementById('close-form');
const buttonUpdateProjectAdmin = document.getElementById('hidden-form-update-admin');
const buttonAssignedProjectAdmin = document.getElementById('hidden-form-assigned-admin');
const buttonDeleteProjectAdmin = document.getElementById('hidden-delete-admin');
const buttonCreateProjectAmdmin = document.getElementById('create-project');

//Funcion para abrir el formulario y agregar un nuevo proyecto
const openForm = () => {
    formAdmin.classList.remove('hidden-form'); //Muestra el formulario
}

const closeForm = () => {
    formAdmin.classList.add('hidden-form'); //Oculta el formulario
}

const toggleMenu = (event, menuID) => {
    event.preventDefault();
    
    document.querySelectorAll('.menu-admin').forEach(menu => {
        if (menu.dataset.menu !== menuID.toString()) {
            menu.classList.add('hidden-menu-admin');
        }
    })

    const menu = document.querySelector(`.menu-admin[data-menu="${menuID}"]`);
    if (menu) {
        menu.classList.toggle('hidden-menu-admin')
    }
}

//Muestra el formulario para actualizar un proyecto y cierra el menu del admin
const editProject = (menuID) => {  
    buttonUpdateProjectAdmin.classList.remove('hidden-form-update');

    const menuAdmin = document.querySelector(`.menu-admin[data-menu="${menuID}"]`);
    if (menuAdmin) {
        menuAdmin.classList.add('hidden-menu-admin');
    }
} 

const closeFormUpdate = () => {
    buttonUpdateProjectAdmin.classList.toggle('hidden-form-update'); //Alterna la visibilidad del formulario para actualizar el proyecto
}

const assignedProject = (menuID) => {
    buttonAssignedProjectAdmin.classList.remove('hidden-form-assigned');

    const menuAdmin = document.querySelector(`.menu-admin[data-menu="${menuID}"]`);
    if (menuAdmin) {
        menuAdmin.classList.add('hidden-menu-admin');
    }
}

const closeFormAssigned = () => {
    buttonAssignedProjectAdmin.classList.toggle('hidden-form-assigned'); //Alterna la visibilidad del formulario para actualizar el proyecto
}

//Muestra el modal para confirmar la eliminacion de un proyecto y cierra el menu del admin
const deleteProject = (menuID) => {
    buttonDeleteProjectAdmin.classList.remove('hidden-delete');

    const deleteModal = document.querySelector(`.menu-admin[data-menu="${menuID}"]`);
    if (deleteModal) {
        deleteModal.classList.add('hidden-menu-admin')
    }
}

const closeDelete = () => {
    buttonDeleteProjectAdmin.classList.toggle('hidden-delete'); //Alterna la visibilidad del formulario para actualizar el proyecto
}

const createProject = (event) => {
    buttonCreateProjectAmdmin.addEventListener('click', () => {
        event.preventDefault();
        const Toast = Swal.mixin({
            toast: true,
            position: "top-end",
            showConfirmButton: false,
            timer: 3000,
            timerProgressBar: true,
            didOpen: (toast) => {
              toast.onmouseenter = Swal.stopTimer;
              toast.onmouseleave = Swal.resumeTimer;
            },
            didClose: () => {
                // Recargar la página
                location.reload();
            }
          });
          Toast.fire({
            icon: "success",
            title: "Project created successfully"
          });
    })

    closeForm();
}

// Llamar a createProject cuando se cargue la página
window.addEventListener('DOMContentLoaded', () => {
    createProject();
});