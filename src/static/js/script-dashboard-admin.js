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
const editProject = (menuID, project_name, comments, worked_hours, worked_minutes, to_do_list, status) => {  
    
    buttonUpdateProjectAdmin.classList.remove('hidden-form-update');

    const menuAdmin = document.querySelector(`.menu-admin[data-menu="${menuID}"]`);
    if (menuAdmin) {
        menuAdmin.classList.add('hidden-menu-admin');
    }
    
    const projectData = {
        id: menuID,
        project_name: project_name,
        comments: comments,
        worked_hours: worked_hours,
        worked_minutes: worked_minutes,
        to_do_list: to_do_list,
        status: status
    };

    document.querySelector('#project_id').value = projectData.id;
    document.querySelector('#project_name_update').value = projectData.project_name;
    document.querySelector('#comments_project').value = projectData.comments;
    document.querySelector('#worked_hours_update').value = projectData.worked_hours;
    document.querySelector('#worked_minutes_update').value = projectData.worked_minutes;
    document.querySelector('#to_do_list').value = projectData.to_do_list;
    document.querySelector('#status_project').value = projectData.status;
} 

const closeFormUpdate = () => {
    buttonUpdateProjectAdmin.classList.add('hidden-form-update'); //Alterna la visibilidad del formulario para actualizar el proyecto
}

const assignedProject = (menuID) => {
    buttonAssignedProjectAdmin.classList.remove('hidden-form-assigned');
    
    
    const menuAdmin = document.querySelector(`.menu-admin[data-menu="${menuID}"]`);
    if (menuAdmin) {
        console.log("este es el id que llega", menuID);
        menuAdmin.classList.add('hidden-menu-admin');
    }

    const projectData = {
        id: menuID,
    };
    console.log("este es el nuevo id", projectData.id);
    document.querySelector('#projectID').value = projectData.id
}

const closeFormAssigned = () => {
    buttonAssignedProjectAdmin.classList.toggle('hidden-form-assigned'); //Alterna la visibilidad del formulario para actualizar el proyecto
}

//Muestra el modal para confirmar la eliminacion de un proyecto y cierra el menu del admin
const deleteProject = (projectId) => {
    console.log(projectId);
    
    document.getElementById('projectId').value = projectId;

    buttonDeleteProjectAdmin.classList.remove('hidden-delete');

    const deleteModal = document.querySelector(`.menu-admin[data-menu="${projectId}"]`);
    if (deleteModal) {
        deleteModal.classList.add('hidden-menu-admin')
    }
}

const closeDelete = () => {
    buttonDeleteProjectAdmin.classList.toggle('hidden-delete'); //Alterna la visibilidad del formulario para actualizar el proyecto
}

document.addEventListener("DOMContentLoaded", function () {
    const form = document.querySelector("#hidden-form-admin form"); // Selecciona el formulario dentro del div
    const closeFormButton = document.getElementById("close-form"); // Botón para cerrar el formulario

    form.addEventListener("submit", async function (e) {
        e.preventDefault(); // Evita el comportamiento por defecto del formulario

        const formData = new FormData(form); // Captura los datos del formulario

        try {
            const response = await fetch(form.action, {
                method: form.method,
                body: formData,
            });

            const result = await response.json(); // Procesa la respuesta JSON
            
            if (result.status == 201) {
                closeForm()
                const Toast = Swal.mixin({
                    toast: true,
                    position: "top-end",
                    showConfirmButton: false,
                    timer: 3000,
                    timerProgressBar: true,
                    didOpen: (toast) => {
                        toast.onmouseenter = Swal.stopTimer;
                        toast.onmouseleave = Swal.resumeTimer;
                    }
                });
    
                Toast.fire({
                    icon: "success",
                    title: "Project created successfully"
                }).then((result) => {
                    if (result.dismiss === Swal.DismissReason.timer) {
                        // Refrescar la página si el temporizador completó
                        window.location.reload();
                    }
                });
            } else {
                closeForm()
                const Toast = Swal.mixin({
                    toast: true,
                    position: "top-end",
                    showConfirmButton: false,
                    timer: 3000,
                    timerProgressBar: true,
                    didOpen: (toast) => {
                        toast.onmouseenter = Swal.stopTimer;
                        toast.onmouseleave = Swal.resumeTimer;
                    }
                });
    
                Toast.fire({
                    icon: "error",
                    title: "The user has not provided all the required values"
                }).then((result) => {
                    if (result.dismiss === Swal.DismissReason.timer) {
                        // Refrescar la página si el temporizador completó
                        window.location.reload();
                    }
                });
            }
        } catch (error) {
            closeForm()
            const Toast = Swal.mixin({
                toast: true,
                position: "top-end",
                showConfirmButton: false,
                timer: 3000,
                timerProgressBar: true,
                didOpen: (toast) => {
                    toast.onmouseenter = Swal.stopTimer;
                    toast.onmouseleave = Swal.resumeTimer;
                }
            });
    
            Toast.fire({
                icon: "error",
                title: "Internal Server Error"
            }).then((result) => {
                if (result.dismiss === Swal.DismissReason.timer) {
                    // Refrescar la página si el temporizador completó
                    window.location.reload();
                }
            });
        }
    });

    // Cerrar el formulario
    closeFormButton.addEventListener("click", function () {
        document.getElementById("hidden-form-admin").classList.add("hidden-form");
    });
});

document.addEventListener("DOMContentLoaded", function () {
    const form = document.querySelector("#hidden-form-update-admin form"); // Selecciona el formulario dentro del div
    const closeFormButton = document.getElementById("close-form"); // Botón para cerrar el formulario

    form.addEventListener("submit", async function (e) {
        e.preventDefault(); // Evita el comportamiento por defecto del formulario

        const formData = new FormData(form); // Captura los datos del formulario

        try {
            const response = await fetch(form.action, {
                method: form.method,
                body: formData,
            });

            const result = await response.json(); // Procesa la respuesta JSON
            
            if (result.status == 200) {
                closeFormUpdate()
                const Toast = Swal.mixin({
                    toast: true,
                    position: "top-end",
                    showConfirmButton: false,
                    timer: 3000,
                    timerProgressBar: true,
                    didOpen: (toast) => {
                        toast.onmouseenter = Swal.stopTimer;
                        toast.onmouseleave = Swal.resumeTimer;
                    }
                });
    
                Toast.fire({
                    icon: "success",
                    title: "Project updated successfully"
                }).then((result) => {
                    if (result.dismiss === Swal.DismissReason.timer) {
                        // Refrescar la página si el temporizador completó
                        window.location.reload();
                    }
                });
            } else {
                closeFormUpdate()
                const Toast = Swal.mixin({
                    toast: true,
                    position: "top-end",
                    showConfirmButton: false,
                    timer: 3000,
                    timerProgressBar: true,
                    didOpen: (toast) => {
                        toast.onmouseenter = Swal.stopTimer;
                        toast.onmouseleave = Swal.resumeTimer;
                    }
                });
    
                Toast.fire({
                    icon: "error",
                    title: "The user has not provided all the required values"
                }).then((result) => {
                    if (result.dismiss === Swal.DismissReason.timer) {
                        // Refrescar la página si el temporizador completó
                        window.location.reload();
                    }
                });
                
            }
        } catch (error) {
            closeForm()
                const Toast = Swal.mixin({
                    toast: true,
                    position: "top-end",
                    showConfirmButton: false,
                    timer: 3000,
                    timerProgressBar: true,
                    didOpen: (toast) => {
                        toast.onmouseenter = Swal.stopTimer;
                        toast.onmouseleave = Swal.resumeTimer;
                    }
                });
    
            Toast.fire({
                icon: "error",
                title: "Internal Server Error"
            }).then((result) => {
                if (result.dismiss === Swal.DismissReason.timer) {
                    // Refrescar la página si el temporizador completó
                    window.location.reload();
                }
            });
        }
    });

    // Cerrar el formulario
    closeFormButton.addEventListener("click", function () {
        document.getElementById("hidden-form-update-admin").classList.add("hidden-form-update");
    });
});