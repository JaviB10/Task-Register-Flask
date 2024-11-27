//Elementos del DOM
const buttonNewUserAdmin = document.getElementById('add-user-admin');
const formAdmin = document.getElementById('hidden-new-user');
const buttonCloseForm = document.getElementById('close-form');
const buttonUpdateUserAdmin = document.getElementById('hidden-form-update-user');
const buttonDeleteUserAdmin = document.getElementById('hidden-delete-user');

//Funcion para abrir el formulario y agregar un nuevo proyecto
const openForm = () => {
    formAdmin.classList.remove('hidden-new-user'); //Muestra el formulario
}

const closeForm = () => {
    formAdmin.classList.add('hidden-new-user'); //Oculta el formulario
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

//Muestra el formulario para actualizar un usuario y cierra el menu del admin
const editUser = (userID, name, last_name, position, email) => {  

    buttonUpdateUserAdmin.classList.remove('hidden-form-update');

    const menuAdmin = document.querySelector(`.menu-admin[data-menu="${userID}"]`);
    if (menuAdmin) {
        menuAdmin.classList.add('hidden-menu-admin');
    }

    const userData = {
        id: userID,
        name: name,
        last_name: last_name,
        position: position,
        email: email
    }

    document.querySelector('#first_name').value = userData.name
    document.querySelector('#last_name').value = userData.last_name
    document.querySelector('#position_user').value = userData.position
    document.querySelector('#email_user').value = userData.email
    document.querySelector('#user_id').value = userData.id
} 

const closeFormUpdate = () => {
    buttonUpdateUserAdmin.classList.toggle('hidden-form-update'); //Alterna la visibilidad del formulario para actualizar el proyecto
}

//Muestra el modal para confirmar la eliminacion de un proyecto y cierra el menu del admin
const deleteUser = (userId) => {
    console.log(userId);
    
    document.getElementById('userId').value = userId;

    buttonDeleteUserAdmin.classList.remove('hidden-delete');

    const deleteModal = document.querySelector(`.menu-admin[data-menu="${userId}"]`);
    if (deleteModal) {
        deleteModal.classList.add('hidden-menu-admin')
    }
}

const closeDelete = () => {
    buttonDeleteUserAdmin.classList.toggle('hidden-delete'); //Alterna la visibilidad del formulario para actualizar el proyecto
}
