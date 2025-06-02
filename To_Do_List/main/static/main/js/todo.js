function toggleForm(formType) {
    const form = document.getElementById(formType + 'Form');
    form.classList.toggle('hidden');
    if (formType === 'task') {
        clearTaskForm();
    } else if (formType === 'category') {
        clearCategoryForm();
    } else {
        clearPriorityForm();
    }
    revealButton(formType + 'Add');
    hideButton(formType + 'Update');
}

function clearTaskForm() {
    document.getElementById('taskTitle').value = '';
    document.getElementById('taskDescription').value = '';
    document.getElementById('taskStatus').value = 'Pending';
}

function clearCategoryForm() {
    document.getElementById('categoryName').value = '';
    document.getElementById('categoryDescription').value = '';
}

function clearPriorityForm() {
    document.getElementById('priorityName').value = '';
}

function hideButton(buttonId) {
    const button = document.getElementById(buttonId);
    button.classList.add('hidden');
}

function revealButton(buttonId) {
    const button = document.getElementById(buttonId);
    button.classList.remove('hidden');
}

function getCsrfToken() {
    let csrfToken = null;
    const name = 'csrftoken';
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        if (cookie.substring(0, name.length + 1) === (name + '=')) {
            csrfToken = decodeURIComponent(cookie.substring(name.length + 1));
            break;
        }
    }
    return csrfToken;
}
const csrfToken = getCsrfToken();
const editButton = gettext('Редактировать');
const deleteButton = gettext('Удалить');
const logoutButton = gettext('Выход');

function showPrioritiesData(prioritiesData) {
    const tableBody = document.getElementById('priorityTable').getElementsByTagName('tbody')[0];
    tableBody.innerHTML = '';

    prioritiesData.forEach(priority => {
        const row = document.createElement('tr');
        row.innerHTML = `
          <td>${priority.name}</td>
          <td>
            <button class="update-button" onclick="getPriorityForUpdate(${priority.id})">${editButton}</button>
            <button class="delete-button" onclick="deletePriority(${priority.id})">${deleteButton}</button>
          </td>
        `;
        tableBody.appendChild(row);
    });
}

function showCategoriesData(categoriesData) {
    const tableBody = document.getElementById('categoryTable').getElementsByTagName('tbody')[0];
    tableBody.innerHTML = '';

    categoriesData.forEach(category => {
        const row = document.createElement('tr');
        row.innerHTML = `
          <td>${category.name}</td>
          <td>${category.description}</td>
          <td>
            <button class="update-button" onclick="getCategoryForUpdate(${category.id})">${editButton}</button>
            <button class="delete-button" onclick="deleteCategory(${category.id})">${deleteButton}</button>
          </td>
        `;
        tableBody.appendChild(row);
    });
}

function showTasksData(tasksData) {
    const tableBody = document.getElementById('taskTable').getElementsByTagName('tbody')[0];
    const categoriesMap = new Map(JSON.parse(window.localStorage.categories));
    const prioritiesMap = new Map(JSON.parse(window.localStorage.priorities));
    tableBody.innerHTML = '';

    tasksData.forEach(task => {
        const row = document.createElement('tr');
        row.innerHTML = `
          <td>${task.title}</td>
          <td>${task.description}</td>
          <td>${task.status}</td>
          <td>${categoriesMap.get(task.category)}</td>
          <td>${prioritiesMap.get(task.priority)}</td>
          <td>
            <button class="update-button" onclick="getTaskForUpdate(${task.id})">${editButton}</button>
            <button class="delete-button" onclick="deleteTask(${task.id})">${deleteButton}</button>
          </td>
        `;
        tableBody.appendChild(row);
    });
}

async function getAndStorePrioritiesData() {
    const prioritiesResponse = await fetch('/api/priorities/', {
        method: 'GET',
        headers: {
            'X-CSRFToken': csrfToken
        }
    });

    if (!prioritiesResponse.ok) {
        throw new Error(`Ошибка API при загрузке приоритетов: ${prioritiesResponse.status}`);
    }
    var prioritiesData = await prioritiesResponse.json();
    var prioritiesMap = new Map(prioritiesData.map(i => [i.id, i.name]));
    window.localStorage.setItem('priorities', JSON.stringify(Array.from(prioritiesMap.entries())));
    return prioritiesData;
}

async function getAndStoreCategoriesData() {
    const categoriesResponse = await fetch('/api/categories/', {
        method: 'GET',
        headers: {
            'X-CSRFToken': csrfToken
        }
    });

    if (!categoriesResponse.ok) {
        throw new Error(`Ошибка API при загрузке категорий: ${categoriesResponse.status}`);
    }
    var categoriesData = await categoriesResponse.json();
    var categoriesMap = new Map(categoriesData.map(i => [i.id, i.name]));
    window.localStorage.setItem('categories', JSON.stringify(Array.from(categoriesMap.entries())));
    return categoriesData;
}

async function getTasksData() {
    const tasksResponse = await fetch('/api/tasks/', {
        method: 'GET',
        headers: {
            'X-CSRFToken': csrfToken
        }
    });

    if (!tasksResponse.ok) {
        throw new Error(`Ошибка API при загрузке задач: ${tasksResponse.status}`);
    }
    return tasksResponse.json();
}

async function addTask() {
    const title = document.getElementById('taskTitle').value;
    const description = document.getElementById('taskDescription').value;
    const status = document.getElementById('taskStatus').value;
    const category = document.getElementById('taskCategory').value;
    const priority = document.getElementById('taskPriority').value;

    const data = {
        title: title,
        description: description,
        status: status,
        category: category,
        priority: priority
    };

    try {
        const response = await fetch('/api/tasks/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            },
            body: JSON.stringify(data)
        });

        if (!response.ok) {
            throw new Error(`Ошибка API: ${response.status}`);
        }

        document.getElementById('taskForm').classList.add('hidden');
        document.getElementById('taskTitle').value = '';
        document.getElementById('taskDescription').value = '';
        location.reload();
    } catch (error) {
        console.error("Ошибка при создании задачи:", error);
        alert("Ошибка при создании задачи: " + error.message);
    }
}

async function getTaskForUpdate(id) {
    try {
        const response = await fetch('/api/tasks/' + id + '/', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            }
        });

        if (!response.ok) {
            throw new Error(`Ошибка API: ${response.status}`);
        }
        var task = await response.json();

        document.getElementById('taskTitle').value = task.title;
        document.getElementById('taskDescription').value = task.description;
        document.getElementById('taskStatus').value = task.status;
        document.getElementById('taskCategory').value = task.category;
        document.getElementById('taskPriority').value = task.priority;
        const formType = 'task';
        const form = document.getElementById(formType + 'Form');
        form.classList.toggle('hidden');
        hideButton('taskAdd');
        revealButton('taskUpdate');
        window.localStorage.setItem('taskId', task.id);
    } catch (error) {
        console.error("Ошибка при получении задачи:", error);
        alert("Ошибка при получении задачи: " + error.message);
    }
}

async function updateTask() {
    var id = window.localStorage.getItem('taskId');
    const title = document.getElementById('taskTitle').value;
    const description = document.getElementById('taskDescription').value;
    const status = document.getElementById('taskStatus').value;
    const category = document.getElementById('taskCategory').value;
    const priority = document.getElementById('taskPriority').value;

    const data = {
        title: title,
        description: description,
        status: status,
        category: category,
        priority: priority
    };

    try {
        const response = await fetch('/api/tasks/' + id + '/', {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            },
            body: JSON.stringify(data)
        });

        if (!response.ok) {
            throw new Error(`Ошибка API: ${response.status}`);
        }

        document.getElementById('taskForm').classList.add('hidden');
        document.getElementById('taskTitle').value = '';
        document.getElementById('taskDescription').value = '';
        location.reload();
    } catch (error) {
        console.error("Ошибка при изменении задачи:", error);
        alert("Ошибка при изменении задачи: " + error.message);
    }
}

async function deleteTask(id) {
    try {
        const response = await fetch('/api/tasks/' + id + '/', {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            },
            body: JSON.stringify({})
        });

        if (!response.ok) {
            throw new Error(`Ошибка API: ${response.status}`);
        }

        location.reload();
    } catch (error) {
        console.error("Ошибка при удалении задачи:", error);
        alert("Ошибка при удалении задачи: " + error.message);
    }
}

async function addCategory() {
    const name = document.getElementById('categoryName').value;
    const description = document.getElementById('categoryDescription').value;

    const data = {
        name: name,
        description: description
    };

    try {
        const response = await fetch('/api/categories/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            },
            body: JSON.stringify(data)
        });

        if (!response.ok) {
            throw new Error(`Ошибка API: ${response.status}`);
        }

        document.getElementById('categoryForm').classList.add('hidden');
        document.getElementById('categoryName').value = '';
        document.getElementById('categoryDescription').value = '';
        location.reload();
    } catch (error) {
        console.error("Ошибка при создании категории:", error);
        alert("Ошибка при создании категории: " + error.message);
    }
}

async function getCategoryForUpdate(id) {
    try {
        const response = await fetch('/api/categories/' + id + '/', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            }
        });

        if (!response.ok) {
            throw new Error(`Ошибка API: ${response.status}`);
        }
        var category = await response.json();

        document.getElementById('categoryName').value = category.name;
        document.getElementById('categoryDescription').value = category.description;
        const formType = 'category';
        const form = document.getElementById(formType + 'Form');
        form.classList.toggle('hidden');
        hideButton('categoryAdd');
        revealButton('categoryUpdate');
        window.localStorage.setItem('categoryId', category.id);
    } catch (error) {
        console.error("Ошибка при получении категории:", error);
        alert("Ошибка при получении категории: " + error.message);
    }
}

async function updateCategory() {
    var id = window.localStorage.getItem('categoryId');
    const name = document.getElementById('categoryName').value;
    const description = document.getElementById('categoryDescription').value;

    const data = {
        name: name,
        description: description
    };

    try {
        const response = await fetch('/api/categories/' + id + '/', {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            },
            body: JSON.stringify(data)
        });

        if (!response.ok) {
            throw new Error(`Ошибка API: ${response.status}`);
        }

        document.getElementById('categoryForm').classList.add('hidden');
        document.getElementById('categoryName').value = '';
        document.getElementById('categoryDescription').value = '';
        location.reload();
    } catch (error) {
        console.error("Ошибка при изменении категории:", error);
        alert("Ошибка при изменении категории: " + error.message);
    }
}

async function deleteCategory(id) {
    try {
        const response = await fetch('/api/categories/' + id + '/', {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            },
            body: JSON.stringify({})
        });

        if (!response.ok) {
            throw new Error(`Ошибка API: ${response.status}`);
        }

        location.reload();
    } catch (error) {
        console.error("Ошибка при удалении категории:", error);
        alert("Ошибка при удалении категории: " + error.message);
    }
}

async function addPriority() {
    const name = document.getElementById('priorityName').value;

    const data = {
        name: name,
    };

    try {
        const response = await fetch('/api/priorities/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            },
            body: JSON.stringify(data)
        });

        if (!response.ok) {
            throw new Error(`Ошибка API: ${response.status}`);
        }

        document.getElementById('priorityForm').classList.add('hidden');
        document.getElementById('priorityName').value = '';
        location.reload();
    } catch (error) {
        console.error("Ошибка при создании приоритета:", error);
        alert("Ошибка при создании приоритета: " + error.message);
    }
}

async function getPriorityForUpdate(id) {
    try {
        const response = await fetch('/api/priorities/' + id + '/', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            }
        });

        if (!response.ok) {
            throw new Error(`Ошибка API: ${response.status}`);
        }
        var priority = await response.json();

        document.getElementById('priorityName').value = priority.name;
        const formType = 'priority';
        const form = document.getElementById(formType + 'Form');
        form.classList.toggle('hidden');
        hideButton('priorityAdd');
        revealButton('priorityUpdate');
        window.localStorage.setItem('priorityId', priority.id);
    } catch (error) {
        console.error("Ошибка при получении приоритета:", error);
        alert("Ошибка при получении приоритета: " + error.message);
    }
}

async function updatePriority() {
    var id = window.localStorage.getItem('priorityId');
    const name = document.getElementById('priorityName').value;

    const data = {
        name: name,
    };

    try {
        const response = await fetch('/api/priorities/' + id + '/', {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            },
            body: JSON.stringify(data)
        });

        if (!response.ok) {
            throw new Error(`Ошибка API: ${response.status}`);
        }

        document.getElementById('priorityForm').classList.add('hidden');
        document.getElementById('priorityName').value = '';
        location.reload();
    } catch (error) {
        console.error("Ошибка при изменении приоритета:", error);
        alert("Ошибка при изменении приоритета: " + error.message);
    }
}

async function deletePriority(id) {
    try {
        const response = await fetch('/api/priorities/' + id + '/', {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            },
            body: JSON.stringify({})
        });

        if (!response.ok) {
            throw new Error(`Ошибка API: ${response.status}`);
        }

        location.reload();
    } catch (error) {
        console.error("Ошибка при удалении приоритета:", error);
        alert("Ошибка при удалении приоритета: " + error.message);
    }
}

async function logout() {
    fetch('/logout/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
        },
            body: JSON.stringify({})
    });
}

async function loadCategoriesAndPriorities() {
    try {
        const categoriesData = await getAndStoreCategoriesData();

        const categorySelect = document.getElementById('taskCategory');
        categoriesData.forEach(category => {
            const option = document.createElement('option');
            option.value = category.id;
            option.text = category.name;
            categorySelect.appendChild(option);
        });
        showCategoriesData(categoriesData);

        const prioritiesData = await getAndStorePrioritiesData();

        const prioritySelect = document.getElementById('taskPriority');
        prioritiesData.forEach(priority => {
            const option = document.createElement('option');
            option.value = priority.id;
            option.text = priority.name;
            prioritySelect.appendChild(option);
        });
        showPrioritiesData(prioritiesData);

        const tasksData = await getTasksData();
        showTasksData(tasksData);
    } catch (error) {
        console.error("Ошибка при загрузке категорий и приоритетов:", error);
        alert("Ошибка при загрузке категорий и приоритетов: " + error.message);
    }
}

window.onload = loadCategoriesAndPriorities;
