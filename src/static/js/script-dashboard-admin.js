//Elementos del DOM
const formNewProject = document.getElementById('hidden-form-admin');
const formUpdateProject = document.getElementById('hidden-form-update-admin');
const formDeleteProject = document.getElementById('hidden-delete-admin');
const detailProject = document.getElementById('hidden-detail-proyect');

const showToast = (icon, title, timer = 2000) => {
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

const openFormNewProject = (user_id) => {
    formNewProject.classList.remove('hidden-form'); //Muestra el formulario
    
    document.querySelector('#user_id').value = user_id;
}
const closeFormNewProject = () => {
    formNewProject.classList.add('hidden-form'); //Oculta el formulario
}

document.addEventListener("DOMContentLoaded", function () {
    const form = document.querySelector("#hidden-form-admin form"); // Selecciona el formulario dentro del div

    form.addEventListener("submit", async function (e) {
        e.preventDefault(); // Evita el comportamiento por defecto del formulario

        const formData = new FormData(form); // Captura los datos del formulario

        try {
            const response = await fetch(form.action, {
                method: form.method,
                body: formData,
            });

            const res = await response.json(); // Procesa la respuesta 
            
            closeFormNewProject()

            if (res.status == 200) {
                showToast("success", "Project created successfully");
            } else if (res.status == 400) {
                showToast("error", "The project must have at least one collaborator or include you as a participant");
            } else {
                showToast("error", "Internal Server Error");
            }
        } catch (error) {
            console.log(error);
        }
    });
});

const openFormUpdateProject = (project_id, project_name, comments, worked_hours, worked_minutes, to_do_list, status, assigned_id, collaborators, user_id, role) => {  
    
    const form = document.getElementById('form-update-project');
    
    const action = `/projects/update_project/${project_id}`;
    form.action = action;
    
    formUpdateProject.classList.remove('hidden-form-update');
    
    const menu = document.querySelector(`.menu-admin[data-menu="${project_id}"]`);
    if (menu) {
        menu.classList.add('hidden-menu-admin');
    }
    
    const projectData = {
        project_id: project_id,
        project_name: project_name,
        comments: comments,
        worked_hours: worked_hours,
        worked_minutes: worked_minutes,
        to_do_list: to_do_list,
        status: status
    }
    console.log(role);
    
    document.querySelector('#project_name_update').value = projectData.project_name;
    document.querySelector('#comments_project').value = projectData.comments;
    document.querySelector('#worked_hours_update').value = projectData.worked_hours;
    document.querySelector('#worked_minutes_update').value = projectData.worked_minutes;
    document.querySelector('#to_do_list').value = projectData.to_do_list;
    document.querySelector('#status_project').value = projectData.status;
    
    document.querySelector('#userID').value = user_id;
    document.querySelector('#role_user_update').value = role
    
    const checkbox = document.querySelector('#defaultCheck2'); // Cambiar el id al nuevo
    
    if (role == 0) {
        // Lógica para marcar/desmarcar el checkbox basado en assigned_id
        if (assigned_id === null || assigned_id === undefined || isNaN(assigned_id) || assigned_id == user_id) {
            checkbox.checked = true; // Desmarcar el checkbox
        } else {
            checkbox.checked = false; // Marcar el checkbox
        }
    }
    
    const select = document.getElementById('collaborators-select');
    const collaboratorIds = collaborators.split(','); // Convertir a array
    
    Array.from(select.options).forEach(option => {
        option.selected = collaboratorIds.includes(option.value);
    });

    $('#collaborators-select').selectpicker('refresh');
} 

const closeFormUpdateProject = () => {
    formUpdateProject.classList.add('hidden-form-update');
}

document.addEventListener("DOMContentLoaded", function () {
    const form = document.querySelector("#hidden-form-update-admin form");

    form.addEventListener("submit", async function (e) {
        e.preventDefault();

        const formData = new FormData(form);

        try {
            const response = await fetch(form.action, {
                method: form.method,
                body: formData,
            });

            const res = await response.json();

            closeFormUpdateProject()
            
            if (res.status == 200) {
                showToast("success", "Project updated successfully");
            } else if (res.status == 404) {
                showToast("error", "Project not found");
            } else if (res.status == 400 && res.message === "The creator of the project cannot be a collaborator.") {
                showToast("error", "The creator of the project cannot be a collaborator");
            } else if (res.status == 400 && res.message === "You are not the creator of the project, so you cannot assign yourself to it. If you wish to participate, you must do so as a collaborator.") {
                showToast("error", "You are not the creator of the project, so you cannot assign yourself to it. If you wish to participate, you must do so as a collaborator");
            } else {
                showToast("error", "Internal Server Error");
            }
        } catch (error) {
            console.log(error);
        }
    });
});

const openFormDeleteProject = (project_id, user_id) => {
    
    const form = document.getElementById('form-delete-project');
    
    const action = `/projects/delete_project/${project_id}`;
    form.action = action;

    formDeleteProject.classList.remove('hidden-delete');

    const menu = document.querySelector(`.menu-admin[data-menu="${project_id}"]`);
    if (menu) {
        menu.classList.add('hidden-menu-admin')
    }
    console.log(user_id);
    
    document.querySelector('#user_id_delete').value = user_id;
}

const closeFormDeleteProject = () => {
    formDeleteProject.classList.toggle('hidden-delete');
}

document.addEventListener("DOMContentLoaded", function () {
    const deleteForm = document.getElementById("form-delete-project");

    deleteForm.addEventListener("submit", async function (e) {
        e.preventDefault(); // Prevenir el envío estándar del formulario

        const formData = new FormData(deleteForm);

        try {
            const response = await fetch(deleteForm.action, {
                method: 'POST',
                body: formData,
            });

            const res = await response.json();

            closeFormDeleteProject()

            if (res.status == 200) {
                showToast("success", "Project deleted successfully");
            } else if (res.status == 400) {
                showToast("error", "The project is in progress, so it cannot be deleted");
            } else if (res.status == 404) {
                showToast("error", "Project not found");
            } else {
                showToast("error", "Internal Server Error");
            }
        } catch (error) {
            console.log(error);
        }
    });
});

const viewDetails = (project_id, project_name, comments, worked_hours, worked_minutes) => {  
    detailProject.classList.remove('hidden-detail');

    const menu = document.querySelector(`.menu-admin[data-menu="${project_id}"]`);
    if (menu) {
        menu.classList.add('hidden-menu-admin');
    }

    document.querySelector('#project_name_info').textContent = project_name;
    document.querySelector('#comments_info').textContent = comments;
    const formattedTime = `${worked_hours}:${worked_minutes.toString().padStart(2, '0')}hs`;
    document.querySelector('#worked_hours_info').textContent = formattedTime;
} 

const closeDetail = () => {
    detailProject.classList.add('hidden-detail'); //Alterna la visibilidad del formulario para actualizar el proyecto
}