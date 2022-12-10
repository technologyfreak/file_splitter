#!/usr/bin/env python3

from sys import maxsize
from threading import Thread
from tkinter import *
from tkinter import filedialog, ttk

from handlers import HANDLERS


class Splitter:
    def __init__(self, root) -> None:
        # Set the title of the root window
        root.title("File Splitter")

        # Create a mainframe widget
        mainframe = ttk.Frame(root, padding="6 6 24 24")
        mainframe.grid(column=0, row=0, sticky=(N, W, E, S))

        # Configure the root window
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)

        # Create a label for the filename
        filename_lbl = ttk.Label(mainframe, text="Filename:")
        filename_lbl.grid(column=1, row=1, sticky=W)

        # Create a string variable for the filename
        self.filename = StringVar()

        # Create an entry widget for the filename
        filename_entry = ttk.Entry(mainframe, textvariable=self.filename)
        filename_entry.grid(column=2, row=1, sticky=(W, E))

        # Create a button for opening the file
        open_btn = ttk.Button(mainframe, text="Open",
                              command=self.get_filename)
        open_btn.grid(column=3, row=1, sticky=W)

        # Create a label for the chunk size
        chunksize_lbl = ttk.Label(mainframe, text="Chunk Size:")
        chunksize_lbl.grid(column=1, row=2, sticky=W)

        # Create an integer variable for the chunk size
        self.chunksize = IntVar()
        self.chunksize.set(1)

        # Create a spinbox for the chunk size
        chunksize_entry = ttk.Spinbox(
            mainframe, from_=1, to=maxsize, textvariable=self.chunksize)
        chunksize_entry.grid(column=2, row=2, sticky=(W, E))

        # Create a dictionary for storing the active handlers
        self.handlers_active: dict[str, IntVar] = {}

        # Create a counter for the number of handlers
        self.handlers_count = 0

        # Loop through the handlers
        for self.handlers_count, key in enumerate(HANDLERS, start=3):
            # Create an integer variable for each handler
            self.handlers_active[key] = IntVar()

            # Create a checkbox for each handler
            chk_btn = ttk.Checkbutton(mainframe, text=key,
                                      variable=self.handlers_active[key],
                                      command=self.toggle_handler)
            chk_btn.grid(column=1, row=self.handlers_count, sticky=W)

        # Create a button for splitting the file
        self.split_btn = ttk.Button(mainframe, text="Split",
                                    command=self.run_handlers,
                                    state=DISABLED)
        self.split_btn.grid(column=1, row=self.handlers_count+1, sticky=W)

        # Create a progress bar for showing the progress of the file splitting
        self.progress = ttk.Progressbar(mainframe, orient=HORIZONTAL, maximum=len(
            self.handlers_active.items()),
            mode="determinate",
            length=100)
        self.progress.grid(column=2, row=self.handlers_count+1, sticky=(W, E))

        # Loop through all the child widgets of the mainframe
        for child in mainframe.winfo_children():
            # Configure the padding for each child widget
            child.grid_configure(padx=5, pady=5)

    def get_filename(self) -> None:
        # Create a new thread for opening the file
        thread = Thread(target=self.open_file)

        # Start the thread
        thread.start()

    def open_file(self) -> None:
        self.reset_progress()

        # Open the file selection dialog and store the selected filename in the self.filename variable
        self.filename.set(filedialog.askopenfilename())

    def reset_progress(self) -> None:
        self.progress["value"] = 0
        self.progress.update_idletasks()

    def run_handlers(self) -> None:
        self.reset_progress()
        chunksize = self.chunksize.get()

        # call the appropriate handlers
        for key, value in self.handlers_active.items():
            if value.get():
                HANDLERS[key](self.filename.get(), chunksize)
                self.step_progression()

    def step_progression(self) -> None:
        self.progress["value"] += self.chunksize.get()
        self.progress.update_idletasks()

    def toggle_handler(self) -> None:
        for value in self.handlers_active.values():
            if value.get():
                self.split_btn["state"] = NORMAL
                return
        else:
            self.split_btn["state"] = DISABLED


if __name__ == "__main__":
    root = Tk()
    Splitter(root)
    root.mainloop()
