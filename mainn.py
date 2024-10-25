from tkinter import *
from tkinter import filedialog, simpledialog
import ctypes
import re
import os
from pypresence import Presence
import time

# Increase Dots Per inch so it looks sharper
ctypes.windll.shcore.SetProcessDpiAwareness(True)

# Setup Tkinter
root = Tk()
img = PhotoImage(file='icon.png')
root.iconphoto(False, img)
root.title("NexCode")
root.geometry('500x500')


# Load the logo image with an absolute path
try:
    logo = PhotoImage(file='logo.png')  # Change this to your actual path
    print("Logo loaded successfully")
except Exception as e:
    print(f"Error loading logo: {e}")

# Execute the Program
def execute(event=None):
    # Write the Content to the Temporary File
    with open('run.py', 'w', encoding='utf-8') as f:
        f.write(editArea.get('1.0', END))

    # Start the File in a new CMD Window
    os.system('start cmd /K "python run.py"')

# Save the content to a file
def save_file(event=None):
    file_path = filedialog.asksaveasfilename(defaultextension=".py", 
                                               filetypes=[("Python Files", "*.py"), ("All Files", "*.*")])
    if file_path:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(editArea.get('1.0', END))

# Open a file and load its content into the editor
def open_file(event=None):
    file_path = filedialog.askopenfilename(filetypes=[("Python Files", "*.py"), ("All Files", "*.*")])
    if file_path:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            editArea.delete('1.0', END)  # Clear the current content
            editArea.insert('1.0', content)  # Insert the new content

# Copy selected text
def copy_text(event=None):
    root.clipboard_clear()  # Clear the clipboard
    text = editArea.get(SEL_FIRST, SEL_LAST)  # Get selected text
    root.clipboard_append(text)  # Append to clipboard

# Paste text from the clipboard
def paste_text(event=None):
    try:
        text = root.clipboard_get()  # Get text from clipboard
        editArea.insert(INSERT, text)  # Insert text at the current cursor position
    except TclError:
        pass  # If there's nothing in the clipboard, ignore

# Cut selected text
def cut_text(event=None):
    copy_text()  # Copy the selected text first
    editArea.delete(SEL_FIRST, SEL_LAST)  # Delete the selected text

# Undo the last action
def undo():
    try:
        editArea.edit_undo()
    except TclError:
        pass  # Ignore if nothing to undo

# Redo the last undone action
def redo():
    try:
        editArea.edit_redo()
    except TclError:
        pass  # Ignore if nothing to redo

# Select all text
def select_all(event=None):
    editArea.tag_add("sel", "1.0", "end")

# Search for text
def search(event=None):
    search_term = simpledialog.askstring("Search", "Enter text to search:")
    if search_term:
        highlight_occurrences(search_term)

def highlight_occurrences(search_term):
    # Remove previous highlights
    for tag in editArea.tag_names():
        editArea.tag_remove(tag, "1.0", "end")
    
    # Create a pattern to search for
    pattern = re.escape(search_term)  # Escape special characters
    start_idx = '1.0'
    
    while True:
        start_idx = editArea.search(pattern, start_idx, stopindex=END)
        if not start_idx:
            break
        end_idx = f"{start_idx}+{len(search_term)}c"
        editArea.tag_add("highlight", start_idx, end_idx)
        start_idx = end_idx  # Move to the end of the last found match

    # Configure the highlight tag
    editArea.tag_config("highlight", foreground="red")

# Register Changes made to the Editor Content
def changes(event=None):
    global previousText

    # If actually no changes have been made stop / return the function
    if editArea.get('1.0', END) == previousText:
        return

    # Remove all tags so they can be redrawn
    for tag in editArea.tag_names():
        editArea.tag_remove(tag, "1.0", "end")

    # Add tags where the search_re function found the pattern
    i = 0
    for pattern, color in repl:
        for start, end in search_re(pattern, editArea.get('1.0', END)):
            editArea.tag_add(f'{i}', start, end)
            editArea.tag_config(f'{i}', foreground=color)
            i += 1

    previousText = editArea.get('1.0', END)

def insert_print_statement(event=None):
    editArea.insert(INSERT, 'print(" ")')
    editArea.mark_set(INSERT, 'insert-3c')  # Move cursor inside the quotes


def search_re(pattern, text, groupid=0):
    matches = []
    text = text.splitlines()
    for i, line in enumerate(text):
        for match in re.finditer(pattern, line):
            matches.append(
                (f"{i + 1}.{match.start()}", f"{i + 1}.{match.end()}")
            )
    return matches

def rgb(rgb):
    return "#%02x%02x%02x" % rgb

previousText = ''

# Define colors for the various types of tokens
normal = rgb((234, 234, 234))
keywords = rgb((118, 228, 148))
comments = rgb((155, 243, 179))
string = rgb((234, 162, 95))
function = rgb((95, 211, 234))
background = rgb((32, 32, 32))
font = 'Consolas 15'

# Define a list of Regex Patterns that should be colored in a certain way
repl = [
    ['(^| )(False|None|True|and|as|assert|async|await|break|class|continue|def|del|elif|else|except|finally|for|from|global|if|import|in|is|lambda|nonlocal|not|or|pass|raise|return|try|while|with|yield)($| )', keywords],
    ['".*?"', string],
    ['\'.*?\'', string],
    ['#.*?$', comments],
]

# Make the Text Widget with undo enabled
editArea = Text(
    root,
    background=background,
    foreground=normal,
    insertbackground=normal,
    relief=FLAT,
    borderwidth=30,
    font=font,
    undo=True  # Enable undo
)

# Place the Edit Area with the pack method
editArea.pack(
    fill=BOTH,
    expand=1
)

# Insert the logo image into the editArea
editArea.image_create(END, image=logo)

# Insert some Standard Text into the Edit Area
editArea.insert('end', "\n\n")  # Adding some space after the logo
editArea.insert('end', """# Made By Ahmed Belmehnouf
# Catch me on: 
#   Github: https://github.com/Untitled-Master
#   Instagram: https://www.instagram.com/untitledmaster



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

""")

# Bind the KeyRelease to the Changes Function
editArea.bind('<KeyRelease>', changes)

# Function to auto-close delimiters
def auto_close(event=None):
    char = event.char
    closing_pairs = {
        'print(': ')',
        '(': ')',
        '{': '}',
        '[': ']',
        '"': '"',
        "'": "'"
    }
    if char in closing_pairs:
        editArea.insert(INSERT, closing_pairs[char])
        editArea.mark_set("insert", "end-1c")  # Move the cursor back

# Bind the auto-close function to the KeyRelease event
editArea.bind('<KeyRelease>', auto_close, add='+')  # Use add='+' to add this handler

# Bind shortcuts
root.bind('<Control-r>', execute)
root.bind('<Control-s>', save_file)
root.bind('<Control-o>', open_file)
root.bind('<Control-c>', copy_text)
root.bind('<Control-v>', paste_text)
root.bind('<Control-x>', cut_text)
root.bind('<Control-f>', search)  # Bind Ctrl + F to the search function
root.bind('<Control-z>', undo)     # Bind Ctrl + Z to undo
root.bind('<Control-y>', redo)     # Bind Ctrl + Y to redo
root.bind('<Control-a>', select_all) # Bind Ctrl + A to select all text
root.bind('<Control-p>', insert_print_statement)  # Bind Ctrl + P to insert a print statement

changes()

# Replace with your Discord application's Client ID
client_id = ''
RPC = Presence(client_id)
RPC.connect()

# Convert start and end timestamps (e.g., current time for demo purposes)
start_time = int(time.time())

# Update the presence with the equivalent fields from your C code example
RPC.update(
    state="NexoCode",  # State
    details="Programming",  # Details
    start=start_time,  # Start timestamp
    large_image="nexo1",  # Update with your large image key
    large_text="NexoCode",           # Large image hover text
    small_text="made by ahmed bl", # Small image hover text
)

# Keep the presence alive
try:
    while True:
        root.mainloop()
        time.sleep(15)  # Keep the connection alive
except KeyboardInterrupt:
    print("Disconnecting...")
    RPC.close()  # Gracefully close the connection




