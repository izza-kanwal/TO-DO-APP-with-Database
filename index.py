import flet as ft
import sqlite3

def main(page: ft.Page):
    conn = sqlite3.connect("TODO.db")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS tasks (id INTEGER PRIMARY KEY AUTOINCREMENT, name VARCHAR(700), status BOOL)")
    conn.commit()
    page.window_width = 370

    page.auto_scroll="TRUE"
    
    
    page.horizontal_alignment="center"
    def add(task):
        print("called")
        conn = sqlite3.connect("TODO.db")
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS tasks (id INTEGER PRIMARY KEY AUTOINCREMENT, name VARCHAR(700), status BOOL)")
        conn.commit()
        
        task_value = task.value
        if task.value == "":
            task.helper_text = "Error: Task cannot be empty"
        else:
            cursor.execute("INSERT INTO tasks (name, status) VALUES (?, ?)", (task_value, False))
            conn.commit()
            task.helper_text = "Submitted"
            task.value = ""
       
        conn.close()
        fetch(box1)  # Refresh the list after adding a task
        page.update()

    def fetch(box1):
        conn = sqlite3.connect("TODO.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tasks")
        data = cursor.fetchall()
        box1.controls.clear()  # Clear existing tasks in the box
        for row in data:
            task_id = row[0]
            task_name = row[1]
            task_status = row[2]
            print(f"Data = {row[2]}")
            temp = "test"
            if task_status == 1:
                temp = "True"
            if task_status == 0:
                temp = "False"  
                page.update()  
            print(temp)    
            task_row = ft.Container(
                content=ft.Row([
                ft.Checkbox(value=temp, on_change=lambda e, task_id=task_id: toggle_status(task_id, e.control.value)),
                #print(f"Check Value = {row[2]}")
                ft.Text(value=task_name),
                ft.IconButton(icon=ft.icons.DELETE, on_click=lambda e, task_id=task_id: delete(task_id))
            ],alignment=ft.MainAxisAlignment.SPACE_BETWEEN
            ),bgcolor="lightblue",border_radius=10,width=300
            )
            box1.controls.append(task_row)
        conn.close()
        page.update()

    def delete(task_id):
        conn = sqlite3.connect("TODO.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM tasks WHERE id=?", (task_id,))
        conn.commit()
        conn.close()
        fetch(box1)  # Refresh the list after deleting a task
        page.update()

    def toggle_status(task_id, new_status):
        conn = sqlite3.connect("TODO.db")
        cursor = conn.cursor()
        cursor.execute("UPDATE tasks SET status=? WHERE id=?", (new_status, task_id))
        new_status=True
        conn.commit()
        conn.close()
        fetch(box1)  # Refresh the list after toggling status
        page.update()

    text = ft.Text(value="TO DO LIST",size=20)
    task = ft.TextField(label="ADD TASK" ,helper_text="",width=250,border_width=2,border_color="black",border_radius=10)
    btn = ft.IconButton(icon=ft.icons.ADD, on_click=lambda _: add(task))
    
    box1 = ft.Column([])

    box = ft.Container(
        content=ft.Row(
            [
                task, btn
            ],
        ),padding=1,border_radius=5 ,width=300
     
    )
    
    box2 = ft.Container(
        content=box1,
    )
    
    fetch(box1)  #Fetch tasks when the application starts
    
    page.add(text, box, box2)

ft.app(target=main)