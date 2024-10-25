from tkinter import *
from tkinter import filedialog, simpledialog, ttk
import ctypes
import re
import os
import psutil
from pypresence import Presence
import time

# Increase Dots Per inch so it looks sharper
ctypes.windll.shcore.SetProcessDpiAwareness(True)

# Setup Tkinter
root = Tk()
img = PhotoImage(file='icon.png')
root.iconphoto(False, img)
root.title("NexCode")
root.geometry('800x600')

# Setup Notebook (tab container)
notebook = ttk.Notebook(root)
notebook.pack(fill=BOTH, expand=1)

# Placeholder for the currently focused tab's text widget
current_text_widget = None

# Load the logo image with an absolute path
try:
    logo = PhotoImage(file='logo.png')  # Change this to your actual path
    print("Logo loaded successfully")
except Exception as e:
    print(f"Error loading logo: {e}")

# Function to create a new tab with a text editor
def create_new_tab():
    global current_text_widget

    # Create a frame for the tab
    tab_frame = Frame(notebook)
    notebook.add(tab_frame, text="Untitled")

    # Create a new text widget in the tab
    text_widget = Text(tab_frame, background=background, foreground=normal, 
                       insertbackground=normal, relief=FLAT, borderwidth=30, font=font, undo=True)
    text_widget.pack(fill=BOTH, expand=1)
    text_widget.bind('<KeyRelease>', changes)

    # Insert logo and introductory text
    text_widget.image_create(END, image=logo)
    text_widget.insert('end', "\n\n")  # Adding some space after the logo
    intro_text = """
# Made By Ahmed Belmehnouf
# Catch me on: 
# Github: https://github.com/Untitled-Master
# Instagram: https://www.instagram.com/untitledmaster



# Note:
# Clear the page to start programming.
# To run the program press CTRL + R
# To save the program press CTRL + S
# To open a program press CTRL + O
# To copy text press CTRL + C
# To paste text press CTRL + V
# To cut text press CTRL + X
# To undo press CTRL + Z
# To redo press CTRL + Y
# To select all text press CTRL + A
# To search press CTRL + F
# To insert a print statement press CTRL + P

"""
    text_widget.insert('end', intro_text)

    # Apply green color to the introductory text
    text_widget.tag_add("intro", "1.0", "end")
    text_widget.tag_config("intro", foreground=comments)

    # Set this new text widget as the current one
    notebook.select(tab_frame)
    current_text_widget = text_widget

# Execute the Program
def execute(event=None):
    # Write the Content to the Temporary File
    with open('run.py', 'w', encoding='utf-8') as f:
        f.write(current_text_widget.get('1.0', END))

    # Start the File in a new CMD Window
    os.system('start cmd /K "python run.py"')

# Save the content to a file
def save_file(event=None):
    file_path = filedialog.asksaveasfilename(defaultextension=".py", 
                                             filetypes=[("Python Files", "*.py"), ("All Files", "*.*")])
    if file_path:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(current_text_widget.get('1.0', END))

# Open a file and load its content into a new tab
def open_file(event=None):
    file_path = filedialog.askopenfilename(filetypes=[("Python Files", "*.py"), ("All Files", "*.*")])
    if file_path:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            create_new_tab()  # Create a new tab for the opened file
            current_text_widget.delete('1.0', END)
            current_text_widget.insert('1.0', content)

# Undo the last action
def undo():
    try:
        current_text_widget.edit_undo()
    except TclError:
        pass  # Ignore if nothing to undo

# Redo the last undone action
def redo():
    try:
        current_text_widget.edit_redo()
    except TclError:
        pass  # Ignore if nothing to redo

# Select all text
def select_all(event=None):
    current_text_widget.tag_add("sel", "1.0", "end")

# Search for text
def search(event=None):
    search_term = simpledialog.askstring("Search", "Enter text to search:")
    if search_term:
        highlight_occurrences(search_term)

def highlight_occurrences(search_term):
    # Remove previous highlights
    for tag in current_text_widget.tag_names():
        current_text_widget.tag_remove(tag, "1.0", "end")
    
    # Create a pattern to search for
    pattern = re.escape(search_term)
    start_idx = '1.0'
    
    while True:
        start_idx = current_text_widget.search(pattern, start_idx, stopindex=END)
        if not start_idx:
            break
        end_idx = f"{start_idx}+{len(search_term)}c"
        current_text_widget.tag_add("highlight", start_idx, end_idx)
        start_idx = end_idx

    # Configure the highlight tag
    current_text_widget.tag_config("highlight", foreground="red")

# Track Changes in the Text Widget Content
def changes(event=None):
    global previousText

    # If no changes have been made, stop/return the function
    if current_text_widget.get('1.0', END) == previousText:
        return

    # Remove all tags to redraw them
    for tag in current_text_widget.tag_names():
        current_text_widget.tag_remove(tag, "1.0", "end")

    # Add tags where the search_re function found the pattern
    i = 0
    for pattern, color in repl:
        for start, end in search_re(pattern, current_text_widget.get('1.0', END)):
            current_text_widget.tag_add(f'{i}', start, end)
            current_text_widget.tag_config(f'{i}', foreground=color)
            i += 1

    previousText = current_text_widget.get('1.0', END)
# Function to insert a print statement
def insert_print_statement(event=None):  # Accept event argument
    current_text_widget.insert(INSERT, 'print("")')
    current_text_widget.mark_set(INSERT, 'insert-2c')  # Move cursor inside the quotes

# Function to insert a flask starter code
def insert_flask_code(event=None):
    current_text_widget.insert(INSERT, '''from flask import Flask
app = Flask(__name__)

@app.route('/')
def home():
    return "Hello, Flask!"

if __name__ == '__main__':
    app.run(debug=True)
    ''')


def search_re(pattern, text, groupid=0):
    matches = []
    text = text.splitlines()
    for i, line in enumerate(text):
        for match in re.finditer(pattern, line):
            matches.append(
                (f"{i + 1}.{match.start()}", f"{i + 1}.{match.end()}")
            )
    return matches

# Function to toggle between tabs
def toggle_tabs(event=None):
    current_tab = notebook.index(notebook.select())
    next_tab = (current_tab + 1) % notebook.index("end")
    notebook.select(next_tab)

# Function to handle tab changes and set the current text widget
def on_tab_change(event):
    global current_text_widget
    current_tab = notebook.nametowidget(notebook.select())
    current_text_widget = current_tab.winfo_children()[0]

# Define color scheme and font
def rgb(rgb):
    return "#%02x%02x%02x" % rgb

previousText = ''
normal = rgb((234, 234, 234))
keywords = rgb((118, 228, 148))
comments = rgb((155, 243, 179))
string = rgb((234, 162, 95))
function = rgb((95, 211, 234))
background = rgb((32, 32, 32))
font = 'Consolas 15'

# Define Regex Patterns with Colors
repl = [
    ['(^| )(False|None|True|and|as|assert|async|await|break|class|continue|def|del|elif|else|except|finally|for|from|global|if|import|in|is|lambda|nonlocal|not|or|pass|raise|return|try|while|with|yield)($| )', keywords],
    ['".*?"', string],
    ['\'.*?\'', string],
    ['#.*?$', comments],
]

# Bindings for shortcuts
root.bind('<Control-r>', execute)
root.bind('<Control-s>', save_file)
root.bind('<Control-o>', open_file)
root.bind('<Control-f>', search)
root.bind('<Control-z>', undo)
root.bind('<Control-y>', redo)
root.bind('<Control-a>', select_all)
root.bind('<Control-t>', lambda event: create_new_tab())
root.bind('<Control-Tab>', toggle_tabs)
notebook.bind("<<NotebookTabChanged>>", on_tab_change)
root.bind('<Control-p>', insert_print_statement)  # Bind Ctrl + P to insert a print statement
root.bind('<Control-/>', insert_flask_code)

# Check if Discord is running
def is_discord_open():
    for process in psutil.process_iter(attrs=['name']):
        if process.info['name'] == 'Discord.exe':
            return True
    return False

# Initialize Discord presence if Discord is open
client_id = '1287482407460540486'
RPC = None
if is_discord_open():
    RPC = Presence(client_id)
    RPC.connect()
    start_time = int(time.time())
    RPC.update(
        state="NexoCode",
        details="Programming",
        start=start_time,
        large_image="nexo1",
        large_text="NexoCode",
        small_text="made by ahmed bl",
    )
else:
    print("Discord is not open. Presence not updated.")

# Open initial tab and start main loop
create_new_tab()
try:
    root.mainloop()
finally:
    if RPC:
        RPC.close()
