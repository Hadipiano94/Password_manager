import tkinter as tk
from tkinter import messagebox
from random import choices, randint, shuffle
import json


"""Constants"""


lower_case_letters = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s",
                      "t", "u", "v", "w", "x", "y", "z"]

higher_case_letters = [letter.upper() for letter in lower_case_letters]

numbers = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
symbols = ["!", "@", "#", "$", "%", "&", "*", "(", ")", "+"]


"""Functions"""


def generate():
    low_letters = choices(lower_case_letters, k=randint(4, 6))
    high_letters = choices(higher_case_letters, k=randint(2, 4))
    nums = choices(numbers, k=randint(2, 4))
    syms = choices(symbols, k=randint(1, 3))
    pass_list = low_letters + high_letters + nums + syms
    shuffle(pass_list)
    new_pass = "".join(pass_list)
    e3.delete(0, tk.END)
    e3.insert(0, new_pass)
    return


def save():
    website_text = e1.get().lower().strip()
    username_text = e2.get()
    pass_text = e3.get()
    if website_text.strip() == "" or username_text.strip() == "" or pass_text.strip() == "":

        tk.messagebox.showwarning("Empty Fields", "Please, do not leave any of the fields empty!")
        return

    else:

        pass_data_dict = {
            website_text: {
                "user_name": username_text,
                "password": pass_text,
            }
        }
        try:
            with open("passwords.json", mode="r") as pass_json_file:
                data = json.load(pass_json_file)
                if website_text in data.keys():
                    save_or_update = "Updating"
                else:
                    save_or_update = "Saving"
        except json.decoder.JSONDecodeError:
            save_or_update = "Saving"
        except FileNotFoundError:
            save_or_update = "Saving"

        if tk.messagebox.askyesno(f"{save_or_update} Password",
                                  f"    Website: {website_text}\n    Username: {username_text}\n   "
                                  f" Password: {pass_text}\n\nAre you sure of the information"
                                  f" above?"):
            try:
                with open("passwords.json", mode="r") as pass_json_file:
                    data = json.load(pass_json_file)
                    data.update(pass_data_dict)
            except json.decoder.JSONDecodeError:
                with open("passwords.json", mode="w") as pass_json_file:
                    json.dump(pass_data_dict, pass_json_file, indent=4)
            except FileNotFoundError:
                with open("passwords.json", mode="w") as pass_json_file:
                    json.dump(pass_data_dict, pass_json_file, indent=4)
            else:
                data.update(pass_data_dict)
                with open("passwords.json", mode="w") as pass_json_file:
                    json.dump(data, pass_json_file, indent=4)
            finally:
                tk.messagebox.showwarning("Saved", "Your Password has been successfully saved.")

            reset_form()

        else:
            return

    return


def search():
    search_word = e1.get().strip().lower()
    try:
        with open("passwords.json", mode="r") as pass_json_file:
            data = json.load(pass_json_file)
    except json.decoder.JSONDecodeError:
        tk.messagebox.showerror("Not Found!", "No such Website name found.")
    except FileNotFoundError:
        tk.messagebox.showerror("Not Found!", "No such Website name found.")
    else:
        if search_word in data.keys():
            e2.delete(0, tk.END)
            e2.insert("0", data[search_word]["user_name"])
            e3.delete(0, tk.END)
            e3.insert("0", data[search_word]["password"])
        else:
            tk.messagebox.showerror("Not Found!", "No such Website name found.")


def reset_form():
    e1.delete(0, tk.END)
    e2.delete(0, tk.END)
    e3.delete(0, tk.END)
    e1.focus()
    return


"""UI Setup"""


win = tk.Tk()
win.title("Password Manager")
win.config(padx=40, pady=40, bg="white")

c1 = tk.Canvas(win, width=236, height=236, bg="white", highlightthickness=0)
lock_img = tk.PhotoImage(file="logo.png")
c1.create_image(135, 118, image=lock_img)
c1.grid(column=1, row=0)

l1 = tk.Label(text="    Website:", bg="white", highlightthickness=0)
l1.grid(column=0, row=1)
l2 = tk.Label(text="Username:", bg="white", highlightthickness=0)
l2.grid(column=0, row=2)
l3 = tk.Label(text=" Password:", bg="white", highlightthickness=0)
l3.grid(column=0, row=3)

e1 = tk.Entry(win, bg="white", highlightthickness=0, width=52)
e1.grid(column=1, row=1)
e1.focus()
e2 = tk.Entry(win, bg="white", highlightthickness=0, width=67)
e2.grid(column=1, row=2, columnspan=2)
e3 = tk.Entry(win, bg="white", highlightthickness=0, width=52)
e3.grid(column=1, row=3)

b1 = tk.Button(win, text="Generate Password", font=("Ariel", 7, "normal"), command=generate, highlightthickness=0)
b1.grid(column=2, row=3)
b2 = tk.Button(win, text="Add", font=("Ariel", 7, "bold"), width=66, command=save, highlightthickness=0)
b2.grid(column=1, row=4, columnspan=2)
b3 = tk.Button(win, text="Search", font=("Ariel", 7, "normal"), width=13, command=search, highlightthickness=0)
b3.grid(column=2, row=1)

win.mainloop()
