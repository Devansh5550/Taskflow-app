import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

tasks = []

# LOAD TASKS
try:
    with open("tasks.txt", "r") as f:
        for line in f:
            tasks.append(line.strip().split("|"))
except:
    pass


# ---------------- FUNCTIONS ----------------

def refresh_list():
    listbox.delete(0, tk.END)

    for t in tasks:
        text, priority, due, done = t

        display = f"{text}   [{priority}]   {due}"
        listbox.insert(tk.END, display)

        index = tk.END

        if done == "1":
            listbox.itemconfig(index, fg="#777")

        if priority == "HIGH":
            listbox.itemconfig(index, fg="#ff5252")
        elif priority == "MED":
            listbox.itemconfig(index, fg="#ffc107")
        elif priority == "LOW":
            listbox.itemconfig(index, fg="#00e676")

    update_progress()
    check_due_alerts()


def add_task(event=None):
    text = entry.get().strip()
    if not text:
        return

    priority = priority_box.get()
    due = due_entry.get()

    tasks.append([text, priority, due, "0"])
    entry.delete(0, tk.END)
    refresh_list()


def toggle_complete(event):
    i = listbox.curselection()
    if i:
        tasks[i[0]][3] = "0" if tasks[i[0]][3] == "1" else "1"
        refresh_list()


def delete_task():
    i = listbox.curselection()
    if i:
        tasks.pop(i[0])
        refresh_list()


def move_up(event):
    i = listbox.curselection()
    if i and i[0] > 0:
        tasks[i[0]], tasks[i[0]-1] = tasks[i[0]-1], tasks[i[0]]
        refresh_list()
        listbox.select_set(i[0]-1)


def move_down(event):
    i = listbox.curselection()
    if i and i[0] < len(tasks)-1:
        tasks[i[0]], tasks[i[0]+1] = tasks[i[0]+1], tasks[i[0]]
        refresh_list()
        listbox.select_set(i[0]+1)


def update_progress():
    if not tasks:
        progress['value'] = 0
        counter.config(text="0 Tasks")
        return

    done = sum(1 for t in tasks if t[3] == "1")
    percent = (done / len(tasks)) * 100
    progress['value'] = percent
    counter.config(text=f"{done}/{len(tasks)} Completed")


def search_tasks(event):
    q = search.get().lower()
    listbox.delete(0, tk.END)

    for t in tasks:
        if q in t[0].lower():
            listbox.insert(tk.END, f"{t[0]} [{t[1]}] {t[2]}")


def check_due_alerts():
    today = datetime.now().strftime("%d/%m")
    for t in tasks:
        if t[2] == today and t[3] == "0":
            root.title("⚠ Task Due Today!")


def save_tasks():
    with open("tasks.txt", "w") as f:
        for t in tasks:
            f.write("|".join(t) + "\n")


def export_tasks():
    with open("exported_tasks.txt", "w") as f:
        for t in tasks:
            f.write(f"{t[0]} | {t[1]} | {t[2]} | Done:{t[3]}\n")
    messagebox.showinfo("Exported", "Tasks exported!")


def update_clock():
    clock.config(text=datetime.now().strftime("%I:%M %p"))
    root.after(1000, update_clock)


def on_close():
    save_tasks()
    root.destroy()


# ---------------- WINDOW ----------------

root = tk.Tk()
root.title("TASKFLOW GOD MODE")
root.geometry("500x740")
root.configure(bg="#0a0a0a")

title = tk.Label(root, text="TASKFLOW", font=("Segoe UI", 24, "bold"),
                 fg="#00e5ff", bg="#0a0a0a")
title.pack(pady=(10,0))

clock = tk.Label(root, fg="#aaa", bg="#0a0a0a")
clock.pack()
update_clock()

search = tk.Entry(root, font=("Segoe UI", 11),
                  bg="#1f1f1f", fg="white",
                  insertbackground="white")
search.pack(padx=20, pady=10, fill="x")
search.insert(0, "Search...")
search.bind("<KeyRelease>", search_tasks)

card = tk.Frame(root, bg="#141414")
card.pack(padx=20, pady=10, fill="both", expand=True)

entry = tk.Entry(card, font=("Segoe UI", 12),
                 bg="#262626", fg="white",
                 insertbackground="white")
entry.pack(padx=15, pady=10, fill="x", ipady=6)
entry.focus()

sub = tk.Frame(card, bg="#141414")
sub.pack()

priority_box = ttk.Combobox(sub, values=["LOW","MED","HIGH"], width=6)
priority_box.set("MED")
priority_box.grid(row=0,column=0,padx=5)

due_entry = tk.Entry(sub, width=10)
due_entry.insert(0, datetime.now().strftime("%d/%m"))
due_entry.grid(row=0,column=1,padx=5)

btn_frame = tk.Frame(card, bg="#141414")
btn_frame.pack(pady=5)

def btn(txt, cmd, color):
    return tk.Button(btn_frame, text=txt, command=cmd,
                     bg=color, fg="black", bd=0,
                     font=("Segoe UI",9,"bold"),
                     padx=10, pady=6, cursor="hand2")

btn("ADD", add_task, "#00e676").grid(row=0,column=0,padx=4)
btn("DELETE", delete_task, "#ff5252").grid(row=0,column=1,padx=4)
btn("EXPORT", export_tasks, "#00e5ff").grid(row=0,column=2,padx=4)

listbox = tk.Listbox(card,
                     font=("Segoe UI", 11),
                     bg="#1f1f1f",
                     fg="white",
                     selectbackground="#00e5ff",
                     selectforeground="black",
                     activestyle="none")
listbox.pack(padx=15, pady=15, fill="both", expand=True)

listbox.bind("<Double-Button-1>", toggle_complete)
root.bind("<Control-Up>", move_up)
root.bind("<Control-Down>", move_down)
entry.bind("<Return>", add_task)

progress = ttk.Progressbar(root, length=380)
progress.pack(pady=5)

counter = tk.Label(root, fg="#888", bg="#0a0a0a")
counter.pack()

refresh_list()

root.protocol("WM_DELETE_WINDOW", on_close)
root.mainloop()
