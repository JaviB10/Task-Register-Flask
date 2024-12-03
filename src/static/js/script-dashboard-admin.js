//Elementos del DOM
const formNewProject = document.getElementById('hidden-form-admin');
const formUpdateProject = document.getElementById('hidden-form-update-admin');
const formDeleteProject = document.getElementById('hidden-delete-admin');
const formAssignedProject = document.getElementById('hidden-form-assigned-admin');
const detailProject = document.getElementById('hidden-detail-proyect');

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
            } else {
                showToast("error", "Internal Server Error");
            }
        } catch (error) {
            console.log(error);
        }
    });
});

const openFormUpdateProject = (project_id, project_name, comments, worked_hours, worked_minutes, to_do_list, status, assigned_id, collaborators, role) => {  
    
    formUpdateProject.classList.remove('hidden-form-update');
    
    const menu = document.querySelector(`.menu-admin[data-menu="${project_id}"]`);
    if (menu) {
        menu.classList.add('hidden-menu-admin');
    }
    
    const projectData = {
        id: project_id,
        project_name: project_name,
        comments: comments,
        worked_hours: worked_hours,
        worked_minutes: worked_minutes,
        to_do_list: to_do_list,
        status: status
    };
    
    const collaboratorIds = collaborators.split(','); // Convertir a array

    document.querySelector('#project_id').value = projectData.id;
    document.querySelector('#project_name_update').value = projectData.project_name;
    document.querySelector('#comments_project').value = projectData.comments;
    document.querySelector('#worked_hours_update').value = projectData.worked_hours;
    document.querySelector('#worked_minutes_update').value = projectData.worked_minutes;
    document.querySelector('#to_do_list').value = projectData.to_do_list;
    document.querySelector('#status_project').value = projectData.status;
    document.querySelector('#role_user').value = role

    const checkbox = document.querySelector('#defaultCheck2'); // Cambiar el id al nuevo
    console.log(assigned_id);
    
    if (role == 0) {
        // Lógica para marcar/desmarcar el checkbox basado en assigned_id
        if (assigned_id === null || assigned_id === undefined || isNaN(assigned_id) || assigned_id == 0) {
            checkbox.checked = true; // Desmarcar el checkbox
        } else {
            checkbox.checked = false; // Marcar el checkbox
        }
    }

    const select = document.getElementById('collaborators-select');
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
            } else if (res.status == 400) {
                showToast("error", "The creator of the project cannot be a collaborator");
            } else {
                showToast("error", "Internal Server Error");
            }
        } catch (error) {
            console.log(error);
        }
    });
});

const openFormDeleteProject = (project_id) => {
    
    const form = document.getElementById('form-delete');
    
    const action = `/projects/delete_project/${project_id}`;
    form.action = action;

    formDeleteProject.classList.remove('hidden-delete');

    const menu = document.querySelector(`.menu-admin[data-menu="${project_id}"]`);
    if (menu) {
        menu.classList.add('hidden-menu-admin')
    }
}

const closeFormDeleteProject = () => {
    formDeleteProject.classList.toggle('hidden-delete');
}

document.addEventListener("DOMContentLoaded", function () {
    const deleteForm = document.getElementById("form-delete");

    deleteForm.addEventListener("submit", async function (e) {
        e.preventDefault(); // Prevenir el envío estándar del formulario

        try {
            const response = await fetch(deleteForm.action, {
                method: 'POST',
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

const openFormAssignedProject = (project_id) => {
    const form = document.getElementById('form-assigned-project');
    
    const action = `/projects/update_assigned_project/${project_id}`;
    form.action = action;

    formAssignedProject.classList.remove('hidden-form-assigned');
    
    const menu = document.querySelector(`.menu-admin[data-menu="${project_id}"]`);
    if (menu) {
        menu.classList.add('hidden-menu-admin');
    }
}

const closeFormAssignedProject = () => {
    formAssignedProject.classList.toggle('hidden-form-assigned');
}

document.addEventListener("DOMContentLoaded", function () {
    const form = document.querySelector("#hidden-form-assigned-admin form")

    form.addEventListener("submit", async function (e) {
        e.preventDefault();

        const formData = new FormData(form);

        try {
            const response = await fetch(form.action, {
                method: form.method,
                body: formData,
            });

            const res = await response.json();

            closeFormAssignedProject()

            if (res.status == 200) {
                showToast("success", "Project assigned successfully");
            } else if (res.status == 404) {
                showToast("error", "Project or User not found");
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