const todoListElement = document.getElementById("todo-list");


function displayTodos(todos) {

    todoListElement.innerHTML = "";


    todos.forEach((todo) => {

        const taskElement = document.createElement("div");

        taskElement.classList.add("todo-item");


        if (todo.completed) {
            taskElement.classList.add("completed");
        } else {
            taskElement.classList.add("incomplete");
        }


        const contentElement = document.createElement("div");

        contentElement.classList.add("todo-content");


        const titleElement = document.createElement("h2");

        titleElement.classList.add("todo-title");

        titleElement.textContent = todo.title;


        const descriptionElement = document.createElement("p");

        descriptionElement.classList.add("todo-description");

        descriptionElement.textContent = todo.description;


        contentElement.appendChild(titleElement);

        contentElement.appendChild(descriptionElement);


        const statusElement = document.createElement("div");

        statusElement.classList.add("todo-status");


        if (todo.completed) {

            statusElement.textContent = "Completed";

            statusElement.classList.add("completed-status");

        } else {

            statusElement.textContent = "Incomplete";

            statusElement.classList.add("incomplete-status");
        }


        taskElement.appendChild(contentElement);

        taskElement.appendChild(statusElement);


        todoListElement.appendChild(taskElement);
    });
}


function loadTodos() {

fetch("http://127.0.0.1:8000/todos")

        .then((response) => {

            if (!response.ok) {
                throw new Error("Failed to fetch todos");
            }

            return response.json();
        })

        .then((todos) => {

            displayTodos(todos);

        })

        .catch((error) => {

            console.error("Error loading todos:", error);

            todoListElement.innerHTML =
                "<p>Unable to load todos. Please make sure the backend is running.</p>";
        });
}


loadTodos();