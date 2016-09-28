#!/usr/bin/python
import os
import getpass
import subprocess

import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

# Static Variables
ENTER = 65293
TAB = 65289

# Initialize new builder
builder = Gtk.Builder()
# Specifiy the glade file to load
builder.add_from_file("./terminal.glade")

# Create a new window object from the builder
window = builder.get_object("applicationwindow1")
# Destroy the window and exit this script when the window is closed
window.connect('destroy', Gtk.main_quit)
# Show all the widgets in the window
window.show_all()

# Define the textview objects
Input = builder.get_object("Input")
Output = builder.get_object("Output")

# Initialize variables and home directory
return_code = 0
user = getpass.getuser()
directory = os.path.expanduser("~")
output_text = ""
os.chdir(directory)


# Send the output of a command to the scroll view
def output(text):
    global output_text
    # get the Output text view buffer
    buffer = Output.get_buffer()
    # Print text to buffer
    output_text = text + "\n" + output_text
    buffer.set_text(output_text)
    return


# Parse the input string
# This is where you can add commands.
# Please add them where they belong alphabetically
# TODO save the command in a history file
def parse_input(spell):
    # print the command to output
    output(spell)
    # Using the globally defined directory
    global directory
    # The return code
    success = 0
    # split the text into an array of arguments
    args = spell.split()
    # If enter is pressed alone then add a new line
    if len(args) == 0:
        output("")
    # floo = cd
    elif "Avada Kedavra" in spell:
        os.system("gksudo xkill")
    elif "floo" in spell:
        if len(args) > 1:
            if len(args) > 1:
                directory = args[1]
            else:
                directory = os.path.expanduser("~")
        os.chdir(directory)
        directory = os.getcwd()
        output(directory)
    elif "exit" in spell:
        exit(0)
    else:
        i = 0
        for arg in args:
            if "sudo" in arg:
                args[i] = "gksudo"
            i += 1
        # Run as shell command if it isn't a spell first
        return_code = shell(args)
        success == return_code

    return success


def tab_autocomplete():
    print("This feature hasn't been added yet")
    # end_iter = Input.get_end_iter()
    # Output.insert(end_iter, "The text to append")


# When the enter key is pressed in the input field
def enter_pressed(widget, event):
    if event.keyval == ENTER:
        # Get the buffer from the Input view
        details = Input.get_buffer()
        # assign the text in the buffer to a string
        text = details.get_text(details.get_start_iter(), details.get_end_iter(), False)
        # Remove all the text in the buffer
        details.set_text("")
        # Parse the input
        return parse_input(text)
    elif event.keyval == TAB:
        tab_autocomplete()

# Function to execute commands using the shell
#TODO Make the output asynchronous
def shell(command):
    popen = subprocess.Popen(command, stdout=subprocess.PIPE,bufsize=1)
    lines_iterator = iter(popen.stdout.readline, b"")
    while popen.poll() is None:
        for line in lines_iterator:
	    output(line.rstrip())



# Connect the textView input to a function
Input.connect('key-press-event', enter_pressed)

# Run the main program
Gtk.main()
