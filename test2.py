import subprocess
import openai
import tkinter as tk
from tkinter import simpledialog, scrolledtext, Label, messagebox
import os
import getpass
from PIL import Image, ImageTk

# Ensure the global reference for the image is set outside of any function
logo_image = None

def add_logo_to_gui(window, logo_path):
    global logo_image
    # Load the image
    image = Image.open(logo_path)
    # Resize the image if it's too large; you can skip this if the image size is suitable
    image = image.resize((100, 100), Image.Resampling.LANCZOS)
    # Convert the image to a PhotoImage
    logo_image = ImageTk.PhotoImage(image)
    # Create a label to display the image
    logo_label = Label(window, image=logo_image)
    # Keep a reference, to prevent it from being garbage collected
    logo_label.image = logo_image
    # Place the label on the GUI
    logo_label.pack(side='top', pady=10)

def run_command(command, sudo_password=''):
    try:
        if 'sudo' in command and sudo_password:
            command = f"echo {sudo_password} | sudo -S " + command
        command = os.path.expanduser(command)
        result = subprocess.run(command, shell=True, text=True, capture_output=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        return e.output

def send_to_gpt(api_key, objective, command_output, is_error=False, first_call=False):
    openai.api_key = api_key
    prompt = f"{objective} Please suggest a valid command to achieve this. " \
             f"You have access to a Kali machine with all the tools that it comes with " \
             f"Previous output: '{command_output}'\n"
    if is_error or first_call:
        prompt += "Note: An error was encountered or this is the first command. Please provide a valid command."
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=50
        )
        return response.choices[0].text.strip()
    except Exception as e:
        return f"Error in GPT response: {str(e)}"

def append_to_gui(output_window, text):
    output_window['state'] = 'normal'
    output_window.insert(tk.END, text + '\n')
    output_window['state'] = 'disabled'
    output_window.see(tk.END)

def ask_api_key(root):
    while True:
        api_key = simpledialog.askstring("OpenAI API Key", "Enter your OpenAI API key:", parent=root)
        if api_key is not None:
            return api_key
        else:
            if messagebox.askyesno("Exit", "Are you sure you want to exit?"):
                root.destroy()
                exit()
            else:
                continue

def ask_sudo_password(root):
    while True:
        sudo_password = simpledialog.askstring("Sudo Password", "Enter your sudo password:", show='*', parent=root)
        if sudo_password is not None:
            return sudo_password
        else:
            if messagebox.askyesno("Exit", "Are you sure you want to exit?"):
                root.destroy()
                exit()
            else:
                continue

def on_close(root):
    if messagebox.askokcancel("Exit", "Are you sure you want to exit?"):
        root.destroy()  # This forcefully closes the Tkinter application


def main(api_key, objective, sudo_password, output_window):
    current_command = "ls"
    while True:
        append_to_gui(output_window, f"Next command to be executed: {current_command}")
        output_window.update_idletasks()

        output = run_command(current_command, sudo_password)
        is_error = "command not found" in output or "No such file or directory" in output

        append_to_gui(output_window, f"Executed: {current_command}\nOutput:\n{output}\nError:\n{is_error}\n")
        output_window.update_idletasks()

        next_command = send_to_gpt(api_key, objective, output, is_error)
        if next_command.lower() in ["exit", "quit", "stop", ""]:
            append_to_gui(output_window, "Stopping as per GPT suggestion or no command provided.")
            break

        current_command = next_command

if __name__ == "__main__":
    root = tk.Tk()
    root.title("☠︎₦Ɇ₮ⱤɄ₦₦ɆⱤ V1☠︎")

    root.protocol("WM_DELETE_WINDOW", lambda: on_close(root))


    output_window = scrolledtext.ScrolledText(root, state='disabled', height=20, width=100)
    output_window.pack(padx=10, pady=10)

    root.attributes('-topmost', True)
    root.update()
    root.attributes('-topmost', False)



    api_key = ask_api_key(root)  # Pass the 'root' argument to the function
    if not api_key:
        messagebox.showerror("Error", "No API Key provided.")
        root.destroy()
        exit()

    objective = simpledialog.askstring("Objective", "What is your objective?", parent=root)  # Add the 'parent=root' argument
    if not objective:
        messagebox.showerror("Error", "No objective provided.")
        root.destroy()
        exit()


    sudo_password = ask_sudo_password(root)  # Pass the 'root' argument to the function
    if not sudo_password:
        messagebox.showerror("Error", "No sudo password provided.")
        root.destroy()
        exit()
    script_dir = os.path.dirname(__file__)
    logo_path = os.path.join(script_dir, 'RainRain.png')

    if os.path.exists(logo_path):
        image = Image.open(logo_path)
        # Replace Image.ANTIALIAS with Image.Resampling.LANCZOS or other available resampling filter
        image = image.resize((100, 100), Image.Resampling.LANCZOS)
        logo_image = ImageTk.PhotoImage(image)
        logo_label = tk.Label(root, image=logo_image)
        logo_label.image = logo_image  # keep a reference
        logo_label.pack()
    else:
        messagebox.showerror("Error", "The logo file was not found.")
        root.destroy()

    # Call the main function to start the command loop
    main(api_key, objective, sudo_password, output_window)

    # Start the GUI event loopAI test
    root.mainloop()
