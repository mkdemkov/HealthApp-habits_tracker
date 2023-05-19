document.addEventListener('DOMContentLoaded', () => {
    const apiUrl = 'http://127.0.0.1:8080/task/list?email=mkdemkov@edu.hse.ru';
    const taskContainer = document.getElementById('task-container');
    const addTaskBtn = document.getElementById('add-task-btn');
    const taskForm = document.getElementById('task-form');
    const submitTaskBtn = document.getElementById('submit-task-btn');
    const nameInput = document.getElementById('name-input');
    const descInput = document.getElementById('desc-input');
    const deadlineInput = document.getElementById('deadline-input');
    const priorityInput = document.getElementById('priority-input');

    addTaskBtn.addEventListener('click', () => {
        taskForm.style.display = 'block';
    });

    submitTaskBtn.addEventListener('click', () => {
        const name = nameInput.value;
        const desc = descInput.value;
        const deadline = deadlineInput.value;
        const priority = priorityInput.value || 1; // Use 1 as the default value if priority is not specified

        // Validate required fields
        const requiredFields = [];
        if (!name) {
            requiredFields.push('Название');
            nameInput.classList.add('required-field');
        } else {
            nameInput.classList.remove('required-field');
        }
        if (!deadline) {
            requiredFields.push('Дедлайн');
            deadlineInput.classList.add('required-field');
        } else {
            deadlineInput.classList.remove('required-field');
        }

        if (requiredFields.length > 0) {
            const fieldNames = requiredFields.join(', ');
            alert(`Please fill in the following required fields: ${fieldNames}`);
            return;
        }

        const taskData = {
            email: "mkdemkov@edu.hse.ru",
            name: name,
            desc: desc,
            deadline: deadline,
            priority: priority
        };

        fetch('http://127.0.0.1:8080/task/new', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(taskData)
        })
            .then(response => response.json())
            .then(data => {
                // Handle the response as needed
                console.log(data);
                // Clear task container
                taskContainer.innerHTML = '';
                // Fetch updated task list
                fetchTasks();
            })
            .catch(error => {
                console.error('Error:', error);
            });
    });

    function createDeleteButton(taskId) {
        const deleteButton = document.createElement('button');
        deleteButton.innerText = 'Delete';
        deleteButton.className = 'delete-button';
        deleteButton.addEventListener('click', () => {
            removeTask(taskId);
        });
        return deleteButton;
    }

    function removeTask(taskId) {
        const url = `http://127.0.0.1:8080/task/remove?id=${taskId}`;

        fetch(url, {method: 'GET'})
            .then(response => response.json())
            .then(data => {
                // Handle the response data if needed
                console.log(data);
                // Remove the task element from the DOM
                const taskElement = document.getElementById(`task-${taskId}`);
                if (taskElement) {
                    taskElement.remove();
                }
            })
            .catch(error => {
                console.error('Error:', error);
            });
    }

    function fetchTasks() {
        fetch(apiUrl)
            .then(response => response.json())
            .then(data => {
                // Render tasks
                for (const taskName in data) {
                    if (data.hasOwnProperty(taskName)) {
                        const task = data[taskName];
                        const taskDiv = document.createElement('div');
                        taskDiv.classList.add('task-div');
                        taskDiv.id = `task-${task.id}`; // Add unique ID to task element
                        taskDiv.innerHTML = `<h3>${task.name}</h3>
                             <p>Deadline: ${task.deadline}</p>
                             <p>ID: ${task.id}</p>`;
                        const deleteButton = createDeleteButton(task.id); // Create delete button for task
                        taskDiv.appendChild(deleteButton); // Add delete button to task element
                        taskContainer.appendChild(taskDiv);
                    }
                }
            })
            .catch(error => {
                console.error('Error:', error);
            });
    }

// Fetch initial task list
    fetchTasks();

    const habitContainer = document.getElementById('habit-container');
    const addHabitBtn = document.getElementById('add-habit-btn');
    const habitForm = document.getElementById('habit-form');
    const submitHabitBtn = document.getElementById('submit-habit-btn');
    const habitNameInput = document.getElementById('habit-name-input');
    const habitDescInput = document.getElementById('habit-desc-input');
    const habitIntervalInput = document.getElementById('habit-interval-input');

    addHabitBtn.addEventListener('click', () => {
        habitForm.style.display = 'block';
    });

    submitHabitBtn.addEventListener('click', () => {
        const name = habitNameInput.value;
        const desc = habitDescInput.value;
        const interval = habitIntervalInput.value;

        // Validate required fields
        const requiredFields = [];
        if (!name) {
            requiredFields.push('Название');
            habitNameInput.classList.add('required-field');
        } else {
            habitNameInput.classList.remove('required-field');
        }
        if (!interval) {
            requiredFields.push('Промежуток');
            habitIntervalInput.classList.add('required-field');
        } else {
            habitIntervalInput.classList.remove('required-field');
        }

        if (requiredFields.length > 0) {
            const fieldNames = requiredFields.join(', ');
            alert(`Please fill in the following required fields: ${fieldNames}`);
            return;
        }

        const habitData = {
            email: 'mkdemkov@edu.hse.ru',
            name: name,
            desc: desc,
            for_time: interval
        };

        fetch('http://127.0.0.1:8080/habit/new', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(habitData)
        })
            .then(response => response.json())
            .then(data => {
                // Handle the response as needed
                console.log(data);
                // Clear habit container
                habitContainer.innerHTML = '';
                // Fetch updated habit list
                fetchHabits();
            })
            .catch(error => {
                console.error('Error:', error);
            });
    });

    function createHabitDeleteButton(habitId) {
        const deleteButton = document.createElement('button');
        deleteButton.innerText = 'Delete';
        deleteButton.className = 'delete-button';
        deleteButton.addEventListener('click', () => {
            removeHabit(habitId);
        });
        return deleteButton;
    }

    function removeHabit(habitId) {
        const url = `http://127.0.0.1:8080/habit/remove?id=${habitId}`;

        fetch(url, {method: 'GET'})
            .then(response => response.json())
            .then(data => {
                // Handle the response data if needed
                console.log(data);
                // Remove the habit element from the DOM
                const habitElement = document.getElementById(`habit-${habitId}`);
                if (habitElement) {
                    habitElement.remove();
                }
            })
            .catch(error => {
                console.error('Error:', error);
            });
    }

    function fetchHabits() {
        const habitUrl = `http://127.0.0.1:8080/habit/list?email=mkdemkov@edu.hse.ru`;

        fetch(habitUrl)
            .then(response => response.json())
            .then(data => {
                // Render habits
                for (const habitName in data) {
                    if (data.hasOwnProperty(habitName)) {
                        const habit = data[habitName];
                        const habitDiv = document.createElement('div');
                        habitDiv.classList.add('task-div');
                        habitDiv.id = `habit-${habit.id}`; // Add unique ID to habit element
                        habitDiv.innerHTML = `<h3>${habit.name}</h3>
                        <p>Промежуток: ${habit.for_time}</p>
                        <p>ID: ${habit.id}</p>`;
                        const deleteButton = createHabitDeleteButton(habit.id); // Create delete button for habit
                        habitDiv.appendChild(deleteButton); // Add delete button to habit element
                        habitContainer.appendChild(habitDiv);
                    }
                }
            })
            .catch(error => {
                console.error('Error:', error);
            });
    }

// Fetch initial habit list
    fetchHabits();

});