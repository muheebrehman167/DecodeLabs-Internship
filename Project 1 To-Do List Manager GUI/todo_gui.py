"""
============================================================
PROJECT 1 (ADVANCED): TO-DO LIST MANAGER - GUI EDITION
============================================================
Organization : DecodeLabs Industrial Training
Batch        : 2026
Developer    : Faraz
Description  : A professional desktop To-Do List application
               built with Tkinter. Features include adding,
               completing, deleting, and editing tasks, task
               counters, persistent storage using JSON, and
               a modern, styled user interface.

Tech Stack   : Python 3.x, Tkinter (standard library),
               JSON (standard library)
============================================================
"""

import json
import os
from datetime import datetime
from tkinter import (
    Tk, Frame, Label, Entry, Button, Listbox, Scrollbar,
    StringVar, messagebox, END, SINGLE, BOTH, LEFT, RIGHT, Y, X,
    TOP, BOTTOM, CENTER
)
from tkinter import font as tkfont


# ------------------------------------------------------------
# CONFIGURATION CONSTANTS
# ------------------------------------------------------------
DATA_FILE = "tasks.json"

COLOR_BG = "#1E1E2E"          # Main background (dark slate)
COLOR_SIDEBAR = "#181825"      # Sidebar / header background
COLOR_CARD = "#2A2A3C"         # Card / list background
COLOR_ACCENT = "#89B4FA"       # Accent blue
COLOR_ACCENT_DARK = "#74A0E0"  # Pressed/hover accent
COLOR_SUCCESS = "#A6E3A1"      # Green for completed tasks
COLOR_DANGER = "#F38BA8"       # Red for delete actions
COLOR_TEXT = "#CDD6F4"         # Primary text
COLOR_TEXT_DIM = "#9399B2"     # Secondary / muted text
COLOR_DONE = "#6C7086"         # Completed task text color

FONT_FAMILY = "Segoe UI"


class TaskManager:
    """
    Handles all task DATA operations (the 'Model' layer).
    Responsible for loading, saving, and modifying the task list.
    Completely independent of the GUI - could be reused with a
    different interface (web, CLI, etc.) without changes.
    """

    def __init__(self, filepath=DATA_FILE):
        self.filepath = filepath
        self.tasks = self._load_tasks()

    def _load_tasks(self):
        """Load tasks from the JSON file. Return an empty list if not found."""
        if os.path.exists(self.filepath):
            try:
                with open(self.filepath, "r", encoding="utf-8") as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                return []
        return []

    def save_tasks(self):
        """Persist the current task list to the JSON file."""
        with open(self.filepath, "w", encoding="utf-8") as f:
            json.dump(self.tasks, f, indent=4)

    def add_task(self, text):
        """Add a new task dictionary to the list and save."""
        task = {
            "text": text,
            "done": False,
            "created": datetime.now().strftime("%Y-%m-%d %H:%M")
        }
        self.tasks.append(task)
        self.save_tasks()

    def toggle_done(self, index):
        """Flip the completion status of a task by its index."""
        if 0 <= index < len(self.tasks):
            self.tasks[index]["done"] = not self.tasks[index]["done"]
            self.save_tasks()

    def edit_task(self, index, new_text):
        """Update the text of an existing task."""
        if 0 <= index < len(self.tasks):
            self.tasks[index]["text"] = new_text
            self.save_tasks()

    def delete_task(self, index):
        """Remove a task from the list by its index."""
        if 0 <= index < len(self.tasks):
            del self.tasks[index]
            self.save_tasks()

    def clear_completed(self):
        """Remove all tasks marked as done."""
        self.tasks = [t for t in self.tasks if not t["done"]]
        self.save_tasks()

    def counts(self):
        """Return (total, completed, pending) counts."""
        total = len(self.tasks)
        completed = sum(1 for t in self.tasks if t["done"])
        pending = total - completed
        return total, completed, pending


class TodoApp:
    """
    The main GUI application (the 'View' + 'Controller' layer).
    Builds the window, widgets, and connects user actions to the
    TaskManager (Model).
    """

    def __init__(self, root):
        self.root = root
        self.manager = TaskManager()

        self._configure_window()
        self._configure_fonts()
        self._build_layout()
        self.refresh_task_list()

    # ------------------------------------------------------------
    # WINDOW SETUP
    # ------------------------------------------------------------
    def _configure_window(self):
        self.root.title("DecodeLabs To-Do List Manager")
        self.root.geometry("520x640")
        self.root.minsize(440, 520)
        self.root.configure(bg=COLOR_BG)

    def _configure_fonts(self):
        self.font_title = tkfont.Font(family=FONT_FAMILY, size=20, weight="bold")
        self.font_subtitle = tkfont.Font(family=FONT_FAMILY, size=10)
        self.font_normal = tkfont.Font(family=FONT_FAMILY, size=12)
        self.font_small = tkfont.Font(family=FONT_FAMILY, size=9)
        self.font_button = tkfont.Font(family=FONT_FAMILY, size=11, weight="bold")

    # ------------------------------------------------------------
    # LAYOUT CONSTRUCTION
    # ------------------------------------------------------------
    def _build_layout(self):
        self._build_header()
        self._build_input_area()
        self._build_task_list_area()
        self._build_footer()

    def _build_header(self):
        header = Frame(self.root, bg=COLOR_SIDEBAR, height=90)
        header.pack(fill=X, side=TOP)

        title = Label(
            header, text="DecodeLabs To-Do List",
            font=self.font_title, fg=COLOR_TEXT, bg=COLOR_SIDEBAR
        )
        title.pack(pady=(18, 0))

        subtitle = Label(
            header, text="Python Internship  |  Batch 2026  |  Project 1 (Advanced)",
            font=self.font_subtitle, fg=COLOR_TEXT_DIM, bg=COLOR_SIDEBAR
        )
        subtitle.pack(pady=(2, 14))

    def _build_input_area(self):
        input_frame = Frame(self.root, bg=COLOR_BG)
        input_frame.pack(fill=X, padx=20, pady=(18, 10))

        self.entry_var = StringVar()
        self.entry = Entry(
            input_frame, textvariable=self.entry_var,
            font=self.font_normal, bg=COLOR_CARD, fg=COLOR_TEXT,
            insertbackground=COLOR_TEXT, relief="flat", bd=0
        )
        self.entry.pack(side=LEFT, fill=X, expand=True, ipady=8, padx=(0, 10))
        self.entry.bind("<Return>", lambda event: self.on_add_task())
        self.entry.focus_set()

        add_btn = Button(
            input_frame, text="+ Add Task", font=self.font_button,
            bg=COLOR_ACCENT, fg=COLOR_SIDEBAR, activebackground=COLOR_ACCENT_DARK,
            relief="flat", bd=0, padx=16, cursor="hand2",
            command=self.on_add_task
        )
        add_btn.pack(side=RIGHT, ipady=6)

    def _build_task_list_area(self):
        list_frame = Frame(self.root, bg=COLOR_BG)
        list_frame.pack(fill=BOTH, expand=True, padx=20, pady=(0, 10))

        scrollbar = Scrollbar(list_frame, bg=COLOR_BG)
        scrollbar.pack(side=RIGHT, fill=Y)

        self.listbox = Listbox(
            list_frame, font=self.font_normal, bg=COLOR_CARD, fg=COLOR_TEXT,
            selectbackground=COLOR_ACCENT, selectforeground=COLOR_SIDEBAR,
            activestyle="none", relief="flat", bd=0,
            yscrollcommand=scrollbar.set, highlightthickness=0
        )
        self.listbox.pack(side=LEFT, fill=BOTH, expand=True)
        scrollbar.config(command=self.listbox.yview)

        self.listbox.bind("<Double-Button-1>", lambda event: self.on_toggle_done())

        action_frame = Frame(self.root, bg=COLOR_BG)
        action_frame.pack(fill=X, padx=20, pady=(0, 10))

        self._action_button(action_frame, "Mark Done / Undo", self.on_toggle_done, COLOR_SUCCESS)
        self._action_button(action_frame, "Edit", self.on_edit_task, COLOR_ACCENT)
        self._action_button(action_frame, "Delete", self.on_delete_task, COLOR_DANGER)
        self._action_button(action_frame, "Clear Completed", self.on_clear_completed, COLOR_TEXT_DIM)

    def _action_button(self, parent, text, command, color):
        btn = Button(
            parent, text=text, font=self.font_small, bg=COLOR_CARD, fg=color,
            activebackground=COLOR_SIDEBAR, relief="flat", bd=0,
            padx=10, pady=6, cursor="hand2", command=command
        )
        btn.pack(side=LEFT, expand=True, fill=X, padx=4)
        return btn

    def _build_footer(self):
        footer = Frame(self.root, bg=COLOR_SIDEBAR, height=40)
        footer.pack(fill=X, side=BOTTOM)

        self.status_var = StringVar()
        status_label = Label(
            footer, textvariable=self.status_var, font=self.font_small,
            fg=COLOR_TEXT_DIM, bg=COLOR_SIDEBAR
        )
        status_label.pack(pady=10)

    # ------------------------------------------------------------
    # EVENT HANDLERS (CONTROLLER LOGIC)
    # ------------------------------------------------------------
    def on_add_task(self):
        """Read text from the entry box and add it as a new task."""
        text = self.entry_var.get().strip()

        if not text:
            messagebox.showwarning("Empty Task", "Please type a task before adding it.")
            return

        self.manager.add_task(text)
        self.entry_var.set("")
        self.refresh_task_list()

    def on_toggle_done(self):
        """Toggle the completed status of the selected task."""
        index = self._get_selected_index()
        if index is None:
            return
        self.manager.toggle_done(index)
        self.refresh_task_list()

    def on_edit_task(self):
        """Edit the text of the selected task using a simple input dialog."""
        index = self._get_selected_index()
        if index is None:
            return

        current_text = self.manager.tasks[index]["text"]
        new_text = self._prompt_edit_dialog(current_text)

        if new_text is not None:
            new_text = new_text.strip()
            if new_text:
                self.manager.edit_task(index, new_text)
                self.refresh_task_list()
            else:
                messagebox.showwarning("Empty Task", "Task text cannot be empty.")

    def on_delete_task(self):
        """Delete the selected task after confirmation."""
        index = self._get_selected_index()
        if index is None:
            return

        task_text = self.manager.tasks[index]["text"]
        confirm = messagebox.askyesno(
            "Confirm Delete",
            f"Delete this task?\n\n\"{task_text}\""
        )
        if confirm:
            self.manager.delete_task(index)
            self.refresh_task_list()

    def on_clear_completed(self):
        """Remove all completed tasks after confirmation."""
        _, completed, _ = self.manager.counts()
        if completed == 0:
            messagebox.showinfo("Nothing to Clear", "There are no completed tasks to clear.")
            return

        confirm = messagebox.askyesno(
            "Clear Completed Tasks",
            f"Remove all {completed} completed task(s)?"
        )
        if confirm:
            self.manager.clear_completed()
            self.refresh_task_list()

    # ------------------------------------------------------------
    # HELPER METHODS
    # ------------------------------------------------------------
    def _get_selected_index(self):
        """Return the index of the selected listbox item, or None."""
        selection = self.listbox.curselection()
        if not selection:
            messagebox.showinfo("No Task Selected", "Please select a task first.")
            return None
        return selection[0]

    def _prompt_edit_dialog(self, current_text):
        """
        A small custom dialog window for editing a task,
        since tkinter has no built-in text input dialog with
        pre-filled content that matches our theme.
        """
        from tkinter import simpledialog
        return simpledialog.askstring(
            "Edit Task", "Update task text:", initialvalue=current_text
        )

    def refresh_task_list(self):
        """
        Redraw the entire listbox based on the current state
        of self.manager.tasks. Also updates the status bar.
        """
        self.listbox.delete(0, END)

        for task in self.manager.tasks:
            prefix = "[x] " if task["done"] else "[ ] "
            display_text = f"{prefix}{task['text']}"
            self.listbox.insert(END, display_text)

            # Color completed tasks differently
            index = self.listbox.size() - 1
            if task["done"]:
                self.listbox.itemconfig(index, fg=COLOR_DONE)
            else:
                self.listbox.itemconfig(index, fg=COLOR_TEXT)

        self._update_status()

    def _update_status(self):
        total, completed, pending = self.manager.counts()
        self.status_var.set(
            f"Total: {total}   |   Pending: {pending}   |   Completed: {completed}"
            f"   |   Double-click a task to mark done/undo"
        )


def main():
    """Application entry point."""
    root = Tk()
    app = TodoApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
