//Elementos del DOM
const formNewUser = document.getElementById('hidden-new-user');
const formUpdateUser = document.getElementById('hidden-form-update-user');
const formDeleteUser = document.getElementById('hidden-delete-user');

const showToast = (icon, title, timer = 1500) => {
    const Toast = Swal.mixin({
        toast: true,
        position: "top-end",
        showConfirmButton: false,
        timer: timer,
        timerProgressBar: true,
        didOpen: (toast) => {
            toast.onmouseenter = Swal.stopTimer;
            toast.onmouseleave = Swal.resumeTimer;
        }
    });

    Toast.fire({
        icon: icon,
        title: title
    }).then((result) => {
        if (result.dismiss === Swal.DismissReason.timer) {
            window.location.reload();
        }
    });
};

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

const openFormNewUser = () => {
    formNewUser.classList.remove('hidden-new-user');
}

const closeFormNewUser = () => {
    formNewUser.classList.add('hidden-new-user'); 
}

document.addEventListener("DOMContentLoaded", function () {
    const form = document.querySelector("#hidden-new-user form");

    form.addEventListener("submit", async function (e) {
        e.preventDefault(); // Evita el comportamiento por defecto del formulario

        const formData = new FormData(form); // Captura los datos del formulario

        try {
            const response = await fetch(form.action, {
                method: form.method,
                body: formData,
            });

            const res = await response.json();
            
            closeFormNewUser()

            if (res.status == 200) {
                showToast("success", "User created successfully");
            } else if (res.status == 400) {
                showToast("error", "The email has already been taken");
            }else {
                showToast("error", "Internal Server Error");
            }
        } catch (error) {
            console.log(error);
        }
    });
});

const openFormUpdateUser = (userID, name, last_name, position, email) => {  

    formUpdateUser.classList.remove('hidden-form-update');

    const menu = document.querySelector(`.menu-admin[data-menu="${userID}"]`);
    if (menu) {
        menu.classList.add('hidden-menu-admin');
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

const closeFormUpdateUser = () => {
    formUpdateUser.classList.toggle('hidden-form-update'); //Alterna la visibilidad del formulario para actualizar el proyecto
}

document.addEventListener("DOMContentLoaded", function () {
    const form = document.querySelector("#hidden-form-update-user form");

    form.addEventListener("submit", async function (e) {
        e.preventDefault(); // Evita el comportamiento por defecto del formulario

        const formData = new FormData(form); // Captura los datos del formulario

        try {
            const response = await fetch(form.action, {
                method: form.method,
                body: formData,
            });

            const res = await response.json();
            
            closeFormUpdateUser()

            if (res.status == 200) {
                showToast("success", "User updated successfully");
            } else if (res.status == 400) {
                showToast("error", "The email has already been taken");
            } else if (res.status == 404) {
                showToast("error", "User not found");
            } else {
                showToast("error", "Internal Server Error");
            }
        } catch (error) {
            console.log(error);
        }
    });
});

const openFormDeleteUser = (user_id) => {
    
    const form = document.getElementById('form-delete-user');
    
    const action = `/users/delete_user/${user_id}`;
    form.action = action;

    formDeleteUser.classList.remove('hidden-delete');

    const menu = document.querySelector(`.menu-admin[data-menu="${user_id}"]`);
    if (menu) {
        menu.classList.add('hidden-menu-admin')
    }
}

const closeFormDeleteUser = () => {
    formDeleteUser.classList.toggle('hidden-delete'); //Alterna la visibilidad del formulario para actualizar el proyecto
}

document.addEventListener("DOMContentLoaded", function () {
    const form = document.querySelector("#hidden-delete-user form");

    form.addEventListener("submit", async function (e) {
        e.preventDefault(); // Prevenir el envío estándar del formulario

        try {
            const response = await fetch(form.action, {
                method: 'POST',
            });

            const res = await response.json();

            closeFormDeleteUser()

            if (res.status == 200) {
                showToast("success", "User deleted successfully");
            } else if (res.status == 400) {
                showToast("error", "The user cannot be deleted because they have unfinished projects");
            } else if (res.status == 404) {
                showToast("error", "User not found");
            } else {
                showToast("error", "Internal Server Error");
            }
        } catch (error) {
            console.log(error);
        }
    });
});
