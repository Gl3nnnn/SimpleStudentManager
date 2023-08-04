from tkinter import *
import tkinter.messagebox as mb
from tkinter import ttk
from tkcalendar import DateEntry
import sqlite3
import datetime
from tkinter import HORIZONTAL, VERTICAL, X, Y, TOP, BOTTOM, BOTH, RIGHT, LEFT, CENTER, NO
import style as style
from tkcalendar import DateEntry
import sqlite3

headlabelfont = ("Helvetica", 16, 'bold')
labelfont = ('Arial', 12)
entryfont = ('Times New Roman', 12)

connector = sqlite3.connect('SchoolManagement.db')
cursor = connector.cursor()
connector.execute(
"CREATE TABLE IF NOT EXISTS SCHOOL_MANAGEMENT (STUDENT_ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, NAME TEXT, EMAIL TEXT, PHONE_NO TEXT, GENDER TEXT, DOB TEXT)"
)

def reset_fields():
   global name_strvar, email_strvar, contact_strvar, gender_strvar, dob
   for i in ['name_strvar', 'email_strvar', 'contact_strvar', 'gender_strvar']:
       exec(f"{i}.set('')")
   dob.set_date(datetime.datetime.now().date())
def reset_form():
   global tree
   tree.delete(*tree.get_children())
   reset_fields()
def display_records():
   tree.delete(*tree.get_children())
   curr = connector.execute('SELECT * FROM SCHOOL_MANAGEMENT')
   data = curr.fetchall()
   for records in data:
       tree.insert('', END, values=records)
def add_record():
   global name_strvar, email_strvar, contact_strvar, gender_strvar, dob
   name = name_strvar.get()
   email = email_strvar.get()
   contact = contact_strvar.get()
   gender = gender_strvar.get()
   DOB = dob.get_date()

   if not name or not email or not contact or not gender or not DOB :
       mb.showerror('Error!', "Please fill all the missing fields!!")
   else:
       try:
           connector.execute(
           'INSERT INTO SCHOOL_MANAGEMENT (NAME, EMAIL, PHONE_NO, GENDER, DOB) VALUES (?,?,?,?,?)', (name, email, contact, gender, DOB)
           )
           connector.commit()
           mb.showinfo('Record added', f"Record of {name} was successfully added")
           reset_fields()
           display_records()
       except:
           mb.showerror('Wrong type', 'The type of the values entered is not accurate. Pls note that the contact field can only contain numbers')
def remove_record():
   if not tree.selection():
       mb.showerror('Error!', 'Please select an item from the database')
   else:
       current_item = tree.focus()
       values = tree.item(current_item)
       selection = values["values"]
       tree.delete(current_item)
       connector.execute('DELETE FROM SCHOOL_MANAGEMENT WHERE STUDENT_ID=%d' % selection[0])
       connector.commit()
       mb.showinfo('Done', 'The record you wanted deleted was successfully deleted.')
       display_records()
def view_record():
   global name_strvar, email_strvar, contact_strvar, gender_strvar, dob
   if not tree.selection():
       mb.showerror('Error!', 'Please select a record to view')
   else:
        current_item = tree.focus()
        values = tree.item(current_item)
        selection = values["values"]

        name_strvar.set(selection[1]); email_strvar.set(selection[2])
        contact_strvar.set(selection[3]); gender_strvar.set(selection[4])
        date = datetime.date(int(selection[5][:4]), int(selection[5][5:7]), int(selection[5][8:]))


def update_treeview():
    tree.delete(*tree.get_children())
    records = cursor.execute('SELECT * FROM SCHOOL_MANAGEMENT').fetchall()
    for record in records:
        tree.insert('', 'end', values=record)


def sort_records(col):
    tree_sort = [(tree.set(child, col), child) for child in tree.get_children('')]
    tree_sort.sort(reverse=False)  # Set to True for descending order
    for index, (val, child) in enumerate(tree_sort):
        tree.move(child, '', index)

# Display message if the database is empty
def check_empty_db():
    if not cursor.execute('SELECT * FROM SCHOOL_MANAGEMENT').fetchone():
        tree.insert('', 'end', values=("No records found", "", "", "", "", "", ""))
        tree.heading('#1', text='', anchor=CENTER)
def display_statistics():
    curr = connector.execute('SELECT GENDER, COUNT(*) FROM SCHOOL_MANAGEMENT GROUP BY GENDER')
    data = curr.fetchall()
    statistics_str = ''
    for gender, count in data:
        statistics_str += f'{gender}: {count}\n'
    mb.showinfo('Statistics', statistics_str)


main = Tk()
main.title('SmartSchool Manager')
main.geometry('1200x800')
main.resizable(0, 0)



lf_bg = '#1E272E'  # Dark Blue-Gray
cf_bg = '#E74C3C'  # Dark Salmon Red
cf_fg = 'white'

name_strvar = StringVar()
email_strvar = StringVar()
contact_strvar = StringVar()
gender_strvar = StringVar()


Label(main, text="SmartSchool Manager System", font=headlabelfont, bg='Blue', foreground='white').pack(side=TOP, fill=X)

left_frame = Frame(main, bg=lf_bg)
left_frame.place(x=0, y=30, relheight=1, relwidth=0.2)

center_frame = Frame(main, bg=cf_bg)
center_frame.place(relx=0.2, y=30, relheight=1, relwidth=0.2)

right_frame = Frame(main, bg="Gray")
right_frame.place(relx=0.4, y=30, relheight=1, relwidth=0.6)

Label(left_frame, text="Name:", font=labelfont, bg=lf_bg, fg=cf_fg).place(relx=0.375, rely=0.05)
Label(left_frame, text="Contact Number:", font=labelfont, bg=lf_bg, fg=cf_fg).place(relx=0.175, rely=0.18)
Label(left_frame, text="Email Address:", font=labelfont, bg=lf_bg, fg=cf_fg).place(relx=0.2, rely=0.31)
Label(left_frame, text="Gender:", font=labelfont, bg=lf_bg, fg=cf_fg).place(relx=0.3, rely=0.44)
Label(left_frame, text="Date of Birth (DOB):", font=labelfont, bg=lf_bg, fg=cf_fg).place(relx=0.1, rely=0.57)





Entry(left_frame, width=19, textvariable=name_strvar, font=entryfont).place(x=20, rely=0.1)
Entry(left_frame, width=19, textvariable=contact_strvar, font=entryfont).place(x=20, rely=0.23)
Entry(left_frame, width=19, textvariable=email_strvar, font=entryfont).place(x=20, rely=0.36)


OptionMenu(left_frame, gender_strvar, 'Male', "Female").place(x=45, rely=0.49, relwidth=0.5)
dob = DateEntry(left_frame, font=("Arial", 12), width=15)
dob.place(x=20, rely=0.62)
Button(left_frame, text='Submit and Add Record', font=labelfont, bg=cf_bg, fg=cf_fg, command=add_record).place(relx=0.025, rely=0.85)





Label(right_frame, text='Students Records', font=headlabelfont, bg='red', foreground='white').pack(side=TOP, fill=BOTH)

tree = ttk.Treeview(right_frame, height=100, selectmode=BROWSE,
                    columns=('Student ID', "Name", "Email Address", "Contact Number", "Gender", "Date of Birth"),
                    displaycolumns='#all')

style = ttk.Style()
style.configure('Treeview', font=('Arial', 12), background='gray', foreground='black')
style.configure('Treeview.Heading', font=('Arial', 12, 'bold'))


X_scroller = Scrollbar(tree, orient=HORIZONTAL, command=tree.xview)
Y_scroller = Scrollbar(tree, orient=VERTICAL, command=tree.yview)
X_scroller.pack(side=BOTTOM, fill=X)
Y_scroller.pack(side=RIGHT, fill=Y)
tree.config(yscrollcommand=Y_scroller.set, xscrollcommand=X_scroller.set)
style.configure('Treeview', font=('Arial', 12), background='light gray', foreground='black')
tree.heading('Student ID', text='ID', anchor=CENTER)
tree.heading('Name', text='Name', anchor=CENTER)
tree.heading('Email Address', text='Email ID', anchor=CENTER)
tree.heading('Contact Number', text='Phone Number', anchor=CENTER)
tree.heading('Gender', text='Gender', anchor=CENTER)
tree.heading('Date of Birth', text='Date Of Birth', anchor=CENTER)


tree.column('#0', width=0, stretch=NO)
tree.column('#1', width=40, stretch=NO)
tree.column('#2', width=140, stretch=NO)
tree.column('#3', width=200, stretch=NO)
tree.column('#4', width=80, stretch=NO)
tree.column('#5', width=80, stretch=NO)
tree.column('#6', width=80, stretch=NO)

tree.place(y=30, relwidth=1, relheight=0.9, relx=0)
tree.tag_configure('TreeHeading', font=('Arial', 12, 'bold'), background='light gray', foreground='black')
tree.tag_configure('TreeRow', font=('Arial', 12), background='white', foreground='black')

# Apply the style to headings and rows
tree.tag_configure('TreeHeading', font=('Arial', 12, 'bold'), background='light gray', foreground='black')
tree.tag_configure('TreeRow', font=('Arial', 12), background='white', foreground='black')

# Bind the focus_set() method to the treeview and sorting method to the column headings
tree.tag_bind('Treeview', '<Button-1>', lambda e: tree.focus_set())
tree.tag_bind('TreeHeading', '<Button-1>', lambda e: sort_records(tree.identify_column(e.x)))

ttk.Button(center_frame, text='Delete Record', style='CenterButton.TButton', command=remove_record, width=15).pack(pady=5)
ttk.Button(center_frame, text='View Record', style='CenterButton.TButton', command=view_record, width=15).pack(pady=5)
ttk.Button(center_frame, text='Reset Fields', style='CenterButton.TButton', command=reset_fields, width=15).pack(pady=5)
ttk.Button(center_frame, text='Delete Database', style='CenterButton.TButton', command=reset_form, width=15).pack(pady=5)
ttk.Button(center_frame, text='View Records', style='CenterButton.TButton', command=view_record, width=15).pack(pady=5)
ttk.Button(center_frame, text='Display Statistics', style='CenterButton.TButton', command=display_statistics, width=15).pack(pady=5)

display_records()
tree_frame = Frame(right_frame)




main.update()
main.mainloop()
