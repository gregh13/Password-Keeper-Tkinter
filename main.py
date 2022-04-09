from tkinter import *
from tkinter import messagebox
import random
import pyperclip
import json

FILE_NAME = "password_manager.json"

DIGITS = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
LO_CASE_CHARACTERS = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h',
                      'i', 'j', 'k', 'm', 'n', 'o', 'p', 'q',
                      'r', 's', 't', 'u', 'v', 'w', 'x', 'y',
                      'z']

UP_CASE_CHARACTERS = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H',
                      'I', 'J', 'K', 'M', 'N', 'O', 'P', 'Q',
                      'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y',
                      'Z']

SYMBOLS = ['@', '#', '$', '%', '=', ':', '?', '.', '/', '|', '~', '>',
           '*', '(', ')', '<']

# combines all the character arrays above to form one array
COMBINED_LIST = DIGITS + UP_CASE_CHARACTERS + LO_CASE_CHARACTERS + SYMBOLS


# ------------------------ Retrieve Passwords ------------------------------#
def get_file_info():
    file_info = Tk()
    file_info.minsize(200, 100)
    file_info.config(padx=10, pady=10)
    file_info.title("File Info")
    printout = ""
    with open(FILE_NAME, mode="r") as manager_file:
        user_data = json.load(manager_file)
    for key in user_data:
        printout += f"Website: {key}\n" \
                  f"Email/Username: {user_data[key]['email/username']}\n" \
                  f"Password:  {user_data[key]['password']}\n\n"
    file_info_label = Label(file_info, text=printout)
    file_info_label.grid(sticky="W", column=1, row=1)
    done_button = Button(file_info, text="Done", width=10, command=file_info.destroy)
    done_button.grid(column=1, row=2)


def search():
    website_search = website_entry.get()
    try:
        with open(FILE_NAME, mode="r") as manager_file:
            user_data = json.load(manager_file)
    except FileNotFoundError:
        messagebox.showerror(title="Error", message="File not found, save a new password to create a file")

    else:
        if website_search in user_data:
            results = f"Email/Username: {user_data[website_search]['email/username']}\n" \
                      f"Password:  {user_data[website_search]['password']}"
            messagebox.showinfo(title=website_search, message=results)
        else:
            not_found = f"Sorry, no data available for '{website_search}'"
            messagebox.showinfo(title=website_search, message=not_found)


# ------------------------ Password Generator ------------------------------#
def generate_password():
    password = ""
    password_entry.delete(0, END)
    for char in range(random.randint(10, 14)):
        password += random.choice(COMBINED_LIST)
    password_entry.insert(END, string=password)
    pyperclip.copy(password)


# -------------------------- Saving Password ----------------------------#
def error_popup():

    messagebox.showerror(title="Uh-oh", message="Blank field detected!\n\nPlease fill everything in.", )


    # Just one line of code above does the same as the 15 lines below. Messagebox for the win!!

    # def popup_destory():
    #     add_password_button.config(state="normal")
    #     error_window.destroy()

    # error_window = Tk()
    # error_window.minsize(200, 100)
    # error_window.config(padx=10, pady=10)
    # error_window.title("Blank fields!")
    #
    # error_message_label = Label(error_window, text="Blank field detected!\n\nPlease fill everything in.",
    #                             font=("Courier", 14, "normal"))
    # error_message_label.config(pady=20)
    # error_message_label.grid(column=1, row=1)
    #
    # error_button = Button(error_window, text="OK", command=popup_destory)
    # error_button.grid(column=1, row=2)


def confirm_popup():

    def confirm_okay():
        def finish():
            password_entry.delete(0, END)
            website_entry.delete(0, END)
            email_user_entry.delete(0, END)
            confirm_window.destroy()
            save_success.destroy()

        new_entry = {
            saved_website: {
                "email/username": saved_email_user,
                "password": saved_password,
            }
        }

        try:
            with open(FILE_NAME, mode="r") as manager_file:
                file = json.load(manager_file)
                file.update(new_entry)
        except FileNotFoundError:
            with open(FILE_NAME, mode="w") as manager_file:
                json.dump(new_entry, manager_file, indent=4)
        else:
            with open(FILE_NAME, mode="w") as manager_file:
                json.dump(file, manager_file, indent=4)

        save_success = Tk()
        save_success.minsize(200, 100)
        save_success.config(padx=20, pady=20)
        save_success.title("Information Saved!")

        save_success_label = Label(save_success, text=f"Your information has been saved to {FILE_NAME}.")
        save_success_button = Button(save_success, text="Okay", command=finish)
        save_success_label.config(pady=10)
        save_success_label.grid(column=1, row=1)
        save_success_button.grid(column=1, row=2)

    def confirm_cancel():
        add_password_button.config(state="normal")
        confirm_window.destroy()

    saved_website = website_entry.get()
    saved_email_user = email_user_entry.get()
    saved_password = password_entry.get()

    confirm_window = Tk()
    confirm_window.minsize(300, 150)
    confirm_window.config(padx=20, pady=20)
    confirm_window.title("Confirm Your Information")

    confirm_web_label = Label(confirm_window, text="Website:", font=("Courier", 15, "normal"))
    confirm_email_label = Label(confirm_window, text="Email/Username:", font=("Courier", 15, "normal"))
    confirm_pass_label = Label(confirm_window, text="Password:", font=("Courier", 15, "normal"))
    confirm_web_info = Label(confirm_window, text=saved_website, font=("Courier", 15, "bold"))
    confirm_email_info = Label(confirm_window, text=saved_email_user, font=("Courier", 15, "bold"))
    confirm_pass_info = Label(confirm_window, text=saved_password, font=("Courier", 15, "bold"))
    confirm_web_label.grid(sticky="E", column=1, row=1)
    confirm_web_info.grid(sticky="W", column=2, row=1)
    confirm_email_label.grid(sticky="E", column=1, row=2)
    confirm_email_info.grid(sticky="W", column=2, row=2)
    confirm_pass_label.grid(sticky="E", column=1, row=3)
    confirm_pass_info.grid(sticky="W", column=2, row=3)

    confirm_message_label = Label(confirm_window, text="\nIf this information is correct,\nclick 'Okay'",
                                  font=("Courier", 15, "normal"))
    confirm_message_label.config(pady=10)
    confirm_message_label.grid(columnspan=2, column=1, row=4)

    confirm_button_okay = Button(confirm_window, width=4, text="Okay", command=confirm_okay)
    confirm_button_okay.grid(sticky="W", column=1, row=5)

    confirm_button_cancel = Button(confirm_window, width=4, text="Cancel", command=confirm_cancel)
    confirm_button_cancel.grid(sticky="E", column=2, row=5)


def add_entry():
    saved_website = website_entry.get()
    saved_email_user = email_user_entry.get()
    saved_password = password_entry.get()
    if saved_website == "" or saved_email_user == "" or saved_password == "":
        error_popup()
    else:
        confirm_popup()


# ---------------------------- UI Setup --------------------------------#

window = Tk()
window.minsize(400, 300)
window.title("Password Manager")
window.config(padx=50, pady=0)

canvas = Canvas(width=100, height=200)
lock_image = PhotoImage(file="lock_graphic_small.png")
canvas.create_image(53, 100, image=lock_image)
canvas.grid(column=2, row=1)

adjustment_label = Label(text="    ")
adjustment_label.grid(column=0, row=1)

title1_label = Label(text="My", font=("Courier", 30, "normal"))
title1_label.grid(sticky="E", column=1, row=1, )

title2_label = Label(text="Pass", font=("Courier", 30, "normal"))
title2_label.grid(sticky="W", column=3, row=1)

website_label = Label(text="Website")
website_label.grid(sticky="E", column=1, row=2)

email_user_label = Label(text="Email/Username")
email_user_label.grid(sticky="E", column=1, row=3)

password_label = Label(text="Password")
password_label.grid(sticky="E", column=1, row=4)

website_entry = Entry(width=19)
website_entry.focus()
website_entry.grid(sticky="W", columnspan=2, column=2, row=2)

email_user_entry = Entry(width=33)
email_user_entry.grid(sticky="W", columnspan=2, column=2, row=3)

password_entry = Entry(width=19)
password_entry.grid(sticky="W", columnspan=2, column=2, row=4)

password_gen_button = Button(text="Generate", width=10, command=generate_password)
password_gen_button.grid(sticky="E", column=3, row=4)

search_button = Button(text="Search", width=10, command=search)
search_button.grid(sticky="E", column=3, row=2)

add_password_button = Button(text="Add", width=45, command=add_entry)
add_password_button.grid(pady=20, columnspan=3, column=1, row=5)

retrieve_pass_button = Button(text="Retrieve My Passwords", width=30, command=get_file_info)
retrieve_pass_button.grid(pady=10, columnspan=3, column=1, row=0)

window.mainloop()
