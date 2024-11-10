
# Task Manager

This Task Manager is a simple, GUI-based application for personal task organization, developed in Python. It uses customtkinter for a modern interface and integrates with MySQL to store tasks persistently.


## Features

- Adding tasks with due dates
- Marking tasks as complete
- Removing tasks from the list
- Showing/hiding completed tasks
- Calendar integration for date selection

Each task is saved in a MySQL database, allowing easy access to your task history. The app provides a straightforward way to stay on top of daily to-dos with a clean, intuitive interface.


## Dependencies

The application uses the following Python libraries:

- The application uses the following Python libraries:

- [customtkinter](https://github.com/TomSchimansky/CustomTkinter): A custom extension of Tkinter for building modern, responsive, and attractive GUIs.
- [Pillow](https://python-pillow.org/): Python Imaging Library, used for handling and displaying images within the application.
- [PyMySQL](https://pypi.org/project/PyMySQL/): A Python library for connecting and interacting with MySQL databases.
- [tkcalendar](https://pypi.org/project/tkcalendar/): A widget library for easy calendar and date entry integration.


## Installation

1. Clone the repository:

```bash
  https://github.com/Anjana-05/Task-Manager.git
```
2. Navigate to the project directory:

```bash
  cd task-manager
```
3. Install the dependencies:

```bash
  pip install -r requirements.txt
```
4. Download and set up [MySQL](https://www.mysql.com/).

5. Edit database connection credentials in main.py

6. Run the application:

```bash
 python main.py
```

## Usage

The application provides a simple GUI for managing tasks:

- Add tasks by typing a description, selecting a due date, and clicking ADD.
- Mark tasks as completed by checking the box next to each task.
- Show or hide completed tasks using the Hide Completed checkbox.
- Delete tasks individually by clicking the trash can icon.
- Tasks are saved automatically to the database.
## Screenshots

![Screenshot 2024-11-07 101259](https://github.com/user-attachments/assets/fc8281dd-4cc1-48f8-8477-f2fc26560f10)

![Screenshot 2024-11-07 101502](https://github.com/user-attachments/assets/e92a768c-d2d5-40e9-829b-af4d92772863)

![Screenshot 2024-11-07 101735](https://github.com/user-attachments/assets/f1b9bfe5-0a78-4796-a4b0-3b69497cc18c)

![Screenshot 2024-11-07 103023](https://github.com/user-attachments/assets/af3533ec-1191-4187-bd73-2dc91d734834)

![Screenshot 2024-11-07 103040](https://github.com/user-attachments/assets/cbc3d315-bca7-4d87-afe9-8db0f5a3be62)


