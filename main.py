from tkinter import *
from tkinter import messagebox
import os
import secrets
import string
import json
# import pyperclip

directory = os.path.dirname(os.path.realpath(__file__))

# ---------------------------- PASSWORD GENERATOR ------------------------------- #


def generate_random_password():
    symbols = ["*", "%"]

    password = ""

    for _ in range(6):
        password += secrets.choice(string.ascii_lowercase)
        password += secrets.choice(string.ascii_uppercase)
        password += secrets.choice(string.digits)
        password += secrets.choice(symbols)

    password_entry.delete(0, END)
    password_entry.insert(0, password)

    # pyperclip.copy(password)

# ---------------------------- SAVE PASSWORD ------------------------------- #


def save():
    website = website_entry.get()
    email = email_entry.get()
    password = password_entry.get()

    if len(website) == 0 or len(password) == 0:
        messagebox.showinfo(
            title="Error", message="site and password are required..")
        return

    confirm = messagebox.askokcancel(
        title=website, message=f"site:{website}\nemail:{email}\npassword:{password}\nsave?")

    if confirm:
        new_data = {website: {
            "email": email,
            "password": password
        }}
        try:
            with open(f"{directory}/data/data.json", "r") as file:
                # reading previous content from file
                content = json.load(file)

                # updates content
                content.update(new_data)

            with open(f"{directory}/data/data.json", "w") as file:
                # now save the updated content
                json.dump(content, file, indent=4)

                # file.write(f"{website}, {email}, {password}\n")

        except FileNotFoundError or json.decoder.JSONDecodeError:
            with open(f"{directory}/data/data.json", "w") as file:
                json.dump(new_data, file, indent=4)

        finally:
            website_entry.delete(0, END)
            password_entry.delete(0, END)


def search():
    website = website_entry.get()

    try:
        with open(f"{directory}/data/data.json", "r") as data:
            content = json.load(data)

            if website in content:
                searched_website = content[website]
                email = searched_website["email"]
                password = searched_website["password"]

                messagebox.showinfo(
                    title=website, message=f"email: {email}\npassword: {password}")
            else:
                messagebox.showwarning(title=website,
                                       message=f"Not able to find \"{website}\" site")

    except FileNotFoundError:
        messagebox.showwarning(title="Error", message="File does not exist.")

# ---------------------------- UI SETUP ------------------------------- #


window = Tk()
window.title("Password Manager")
window.config(bg="#ffffff", padx=40, pady=40)

canvas = Canvas(height=200, width=200)
logo_img = PhotoImage(file=f"{directory}/images/logo.png")
canvas.create_image(100, 100, image=logo_img)
canvas.grid(row=0, column=1)
canvas.config(bg="#ffffff", highlightthickness=0)

# --------- labels ------------ #
website_label = Label(text="Site")
website_label.grid(row=1, column=0)

email_label = Label(text="Email/Username")
email_label.grid(row=2, column=0)

password_label = Label(text="password")
password_label.grid(row=3, column=0)

# --------- entries ---------- #
website_entry = Entry(width=40)
website_entry.grid(row=1, column=1, columnspan=1)
website_entry.focus()

email_entry = Entry(width=40)
email_entry.grid(row=2, column=1, columnspan=1)
email_entry.insert(0, "commonemail@email.com")

password_entry = Entry(width=40)
password_entry.grid(row=3, column=1, columnspan=1)

# --------- buttons ---------- #
search_button = Button(
    text="Search", width=15, command=search
)
search_button.grid(row=1, column=2)

generate_password_button = Button(
    text="Generate Password", command=generate_random_password)
generate_password_button.grid(row=3, column=2)

add_button = Button(text="Add", width=50, command=save)
add_button.grid(row=4, column=1, columnspan=2)


window.mainloop()
