from customtkinter import (
    CTk,
    CTkFrame,
    CTkButton,
    CTkCheckBox,
    CTkEntry,
    CTkScrollableFrame,
    CTkImage,
    CTkToplevel,
    CTkLabel,
    set_appearance_mode,
)
from tkinter import END, IntVar
from PIL import Image
import pymysql
from tkcalendar import DateEntry

# Database connection credentials
sqlCred = {
    "host": "localhost",
    "user": "root",
    "password": "Python",
    "database": None,
    "port": 3306,
}

# Database Initialization
with pymysql.connect(
    host=sqlCred["host"],
    user=sqlCred["user"],
    password=sqlCred["password"],
    port=sqlCred["port"],
) as connection:
    with connection.cursor() as cursor:
        cursor.execute("CREATE DATABASE IF NOT EXISTS taskManager;")
        sqlCred["database"] = "taskManager"

# Connecting to the database
connection = pymysql.connect(
    host=sqlCred["host"],
    user=sqlCred["user"],
    password=sqlCred["password"],
    database=sqlCred["database"],
    port=sqlCred["port"],
)

cursor = connection.cursor()

# Recreate taskTable with the correct columns
cursor.execute("DROP TABLE IF EXISTS taskTable;")  # Drop the table if it exists
cursor.execute(
    """
    CREATE TABLE taskTable(
        taskString TEXT,
        dueDate DATE,
        status INTEGER
    );
    """
)
connection.commit()

# Load the bin icon image (update the path if necessary)
bin_icon = CTkImage(Image.open("./images/bin.png"))

# Class for managing tasks
class TaskManager:
    def __init__(self, masterFrame: CTkScrollableFrame):
        self.taskList = dict()
        self.master = masterFrame
        self.hideCompleted = False

    def addTask(self, taskString: str, dueDate: str, taskStatus: int = 0, initialize: bool = False):
        if not len(taskString.strip()):
            return
        
        if not initialize:
            taskInput.delete(0, END)
            dateEntry.delete(0, END)

        # Check if task already exists in self.taskList
        for task_id, task_data in list(self.taskList.items()):
            if task_data[2] == taskString and task_data[3] == dueDate:
                task_data[0].destroy()
                del self.taskList[task_id]

        if len(taskString) > 26:
            taskItem = CTkScrollableFrame(master=self.master, orientation="horizontal", height=40)
        else:
            taskItem = CTkFrame(master=self.master)

        checkbox_var = IntVar()
        checkbox_var.set(taskStatus)

        taskCheck = CTkCheckBox(
            master=taskItem,
            text=f"{taskString} (Due: {dueDate})",
            font=("monospace", 15),
            variable=checkbox_var
        )
        
        self.taskList[taskCheck.__hash__()] = [taskItem, taskCheck, taskString, dueDate]
        
        taskCheck.configure(
            command=lambda: self.update(self.taskList[taskCheck.__hash__()])
        )

        taskCheck.anchor("w")
        taskCheck.grid(row=0, column=0, padx=10, pady=10)

        deleteIconButton = CTkButton(
            master=taskItem,
            text=None, 
            image=bin_icon,
            width=20,  
            height=20,  
            command=lambda: self.deleteTask(taskCheck.__hash__())
        )
        deleteIconButton.grid(row=0, column=1, padx=10, pady=10)

        # Only show the task if it shouldn't be hidden
        if not (self.hideCompleted and taskStatus == 1):
            taskItem.pack(padx=10, pady=10, fill="x")
        
        if not initialize:
            cursor.execute("INSERT INTO taskTable (taskString, dueDate, status) VALUES (%s, %s, %s);", 
                         (taskString, dueDate, taskStatus))
            connection.commit()

    def deleteTask(self, task_id):
        taskItem = self.taskList[task_id]
        cursor.execute("DELETE FROM taskTable WHERE taskString = %s AND dueDate = %s;", 
                      (taskItem[2], taskItem[3]))
        connection.commit()
        taskItem[0].destroy()
        del self.taskList[task_id]

    def update(self, taskItem):
        # Update database
        cursor.execute(
            "UPDATE taskTable SET status=%s WHERE taskString=%s AND dueDate=%s;",
            (taskItem[1].get(), taskItem[2], taskItem[3])
        )
        connection.commit()
        
        # Handle visibility based on hideCompleted setting
        if self.hideCompleted and taskItem[1].get() == 1:
            taskItem[0].pack_forget()
        elif not self.hideCompleted:
            taskItem[0].pack(padx=10, pady=10, fill="x")

    def showOrHideCompleted(self, status: bool):
        self.hideCompleted = status
        # Clear all tasks from view
        for task_data in self.taskList.values():
            task_data[0].pack_forget()
        
        # Repack tasks based on their completion status
        for task_data in self.taskList.values():
            if not (self.hideCompleted and task_data[1].get() == 1):
                task_data[0].pack(padx=10, pady=10, fill="x")

def displayDB():
    # Clear existing tasks from UI
    for task_data in taskManager.taskList.values():
        task_data[0].destroy()
    taskManager.taskList.clear()
    
    # Fetch and display tasks from database
    cursor.execute("SELECT * FROM taskTable;")
    tableRows = cursor.fetchall()
    for row in tableRows:
        taskManager.addTask(row[0], row[1], row[2], initialize=True)
        
def displayDB():
    # Fetch tasks from the database and add them to the UI
    cursor.execute("SELECT * FROM taskTable;")
    tableRows = cursor.fetchall()
    for row in tableRows:
        taskManager.addTask(row[0], row[1], row[2], initialize=True)  # Add task to the UI

def close_connection():
    cursor.close()
    connection.commit()  # Commit any final changes before closing
    connection.close()
    app.destroy()

# UI Definition

set_appearance_mode("dark")

app = CTk()
app.title("Personal Task Manager")
app.geometry("800x600")
app.minsize(370, 550)
app.resizable(False, True)
app.iconbitmap("./images/taskManagerIcon.ico")
app.configure(bg="black")

mainFrame = CTkFrame(master=app)
mainFrame.pack(padx=10, pady=10, expand=True, fill="both")

taskManagerFrame = CTkFrame(master=mainFrame)
taskManagerFrame.pack(padx=10, pady=10, fill="x")

taskInput = CTkEntry(master=taskManagerFrame, width=225)
taskInput.grid(row=0, column=0, padx=30, pady=30)

dateEntry = DateEntry(master=taskManagerFrame, width=20, background='darkblue', foreground='white', borderwidth=2)
dateEntry.grid(row=0, column=1, padx=30, pady=30)

taskListFrame = CTkScrollableFrame(master=mainFrame)
taskListFrame.pack(padx=10, pady=10, expand=True, fill="both")

taskManager = TaskManager(taskListFrame)

displayDB()  # Fetch and display tasks when the app starts

addTaskButton = CTkButton(
    master=taskManagerFrame,
    text="ADD",
    width=60,
    command=lambda: taskManager.addTask(taskInput.get(), dateEntry.get_date()),  
)
addTaskButton.grid(row=0, column=2, padx=10, pady=10)

hideCompletedCheck = CTkCheckBox(
    master=taskManagerFrame, text="Hide Completed", font=("monospace", 15)
)
hideCompletedCheck.configure(
    command=lambda: taskManager.showOrHideCompleted(hideCompletedCheck.get())
)
hideCompletedCheck.grid(row=1, column=0, padx=10, pady=10)


# Application close protocol
app.protocol("WM_DELETE_WINDOW", close_connection)

# Start the main event loop
app.mainloop()
