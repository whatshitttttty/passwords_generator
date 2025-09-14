from tkinter import *
from tkinter import messagebox
from random import randint,shuffle,choice
import pyperclip
import json
def generate():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']


    password_letters = [choice(letters) for _ in range(randint(8, 10))]
    password_symbols = [choice(symbols) for _ in range(randint(2, 4))]
    password_numbers = [choice(numbers) for _ in range(randint(2, 4))]
    password_list = password_letters+password_symbols+password_numbers

    shuffle(password_list)

    password = "".join(password_list)
    password_entry.insert(0,f"{password}")
    pyperclip.copy(password)




window = Tk()
window.title("Password Manager")
window.configure(bg="white", padx=50, pady=50)

def save():
    website = website_entry.get().strip()
    email = email_entry.get().strip()
    password = password_entry.get().strip()
    new_data = {
        website: {
            "email": email,
            "password": password
        }
    }

    if len(website) == 0 or len(email) == 0 or len(password) == 0:
        messagebox.showerror(title="Error", message="Please enter all the details")

    else:
        #is_ok = messagebox.askokcancel(title=website, message=f"There are the details entered: \n"
                                                  #f"Email: {email}\nPassword: {password}\n It is ok to save")
        #if is_ok:
        try:
            with open("password.json", "r", encoding="utf-8") as f:
                data=json.load(f)
        except FileNotFoundError:
            with open("password.json", "w", encoding="utf-8") as f:
                json.dump(new_data,f,indent=4)
        else:
            data.update(new_data)
            with open("password.json", "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)
        finally:
            website_entry.delete(0, END)
            password_entry.delete(0, END)


def search():
    website = website_entry.get().strip()
    try:
        with open("password.json", "r", encoding="utf-8") as f:
            data=json.load(f)
    except FileNotFoundError:
        messagebox.showerror(title="Error", message="No Data File Found")
    else:
        if website in data:
            email = data[website]["email"]
            password = data[website]["password"]
            messagebox.showinfo(title=website, message=f"Email:{email}\nPassword:{password}")
        else:
            messagebox.showerror(title="Error", message="No details for the website exists")

# 用一个 Frame 管住布局更好调
frm = Frame(window, bg="white")
frm.grid()

# 让第1、2列可拉伸（Entry/按钮所在列）
frm.columnconfigure(1, weight=1)
frm.columnconfigure(2, weight=1)

# 顶部 Logo
canvas = Canvas(frm, width=200, height=200, bg="white",
                highlightthickness=4, highlightbackground="black")
canvas.grid(row=0, column=0, columnspan=3, pady=(10, 20))
lock = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=lock)
canvas.image = lock

# 第1行：Website
Label(frm, text="Website:", bg="white").grid(row=1, column=0, sticky="e", padx=(0, 8), pady=4)
website_entry = Entry(frm)
website_entry.grid(row=1, column=1, sticky="we", pady=4)
website_entry.focus()

# 第2行：Email/Username
Label(frm, text="Email/Username:", bg="white").grid(row=2, column=0, sticky="e", padx=(0, 8), pady=4)
email_entry = Entry(frm)
email_entry.grid(row=2, column=1, columnspan=2, sticky="we", pady=4)
email_entry.insert(0, "gj4668045@gmail.com")

# 第3行：Password + 生成按钮
Label(frm, text="Password:", bg="white").grid(row=3, column=0, sticky="e", padx=(0, 8), pady=4)
password_entry = Entry(frm)
password_entry.grid(row=3, column=1, sticky="we", pady=4)
Button(frm, text="Generate Password",command=generate).grid(row=3, column=2, sticky="w", padx=(8, 0), pady=4)
Button(frm, text="Search",command=search,width=14).grid(row=1, column=2, sticky="w", padx=(8, 0), pady=4)

# 第4行：Add（跨两列）
Button(frm, text="Add",command=save).grid(row=4, column=1, columnspan=2, sticky="we", pady=(10, 0))


window.mainloop()
