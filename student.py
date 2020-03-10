from tkinter import *  
from PIL import ImageTk,Image
import time
import bs4
import requests 
from io import BytesIO
import socket
from tkinter import messagebox
from tkinter import scrolledtext
import cx_Oracle
import datetime


# main screen
root = Tk()
root.title("WooooooooW")
root.geometry("500x500+300+200")


# splash screen 
sph = Toplevel(root)
sph.title("Splash")
sph.geometry("1200x700+0+0")
sph.withdraw()


# getting img info
res1 = requests.get("https://www.brainyquote.com/quote_of_the_day.html")
soup =  bs4.BeautifulSoup(res1.text,"lxml")
quote = soup.find('img',{"class":"p-qotd"})

# forming the url
s1 = "https://www.brainyquote.com"
s2 = str(quote['data-img-url'])
s = s1 + s2


# getting current City
res2 = requests.get("https://ipinfo.io/")
data = res2.json()
city = data['city']

# Displaying City
lblcity = Label(sph,text ='City  =  ' + city)
lblcity.config(font=('Courier', 20,'bold'))

# API address 
api_address = "http://api.openweathermap.org/data/2.5/weather?units=metric"+"&q="+city+"&appid=159655bb4e04fb16e92fbb7d1678c733"

# getting current Temperature
res2 = requests.get(api_address)
wdata = res2.json()
temp = wdata['main']['temp']

# Displaying Temperature
lbltemp = Label(sph,text ='Temp  =  ' + str(temp))
lbltemp.config(font=('Courier', 20,'bold'))

# getting the image
response = requests.get(s)
img = Image.open(BytesIO(response.content))

# attaching img to GUI
canvas = Canvas(sph, width = 1200, height = 500)      
canvas.pack()  
img = ImageTk.PhotoImage(img) 
canvas.create_image(600,300,anchor=CENTER,image=img)

lblcity.place(x = 250,y = 550)
lbltemp.place(x = 750, y = 550)


# open close operations of splash and main screen
root.withdraw()	
sph.deiconify()
sph.update()
time.sleep(8)
sph.withdraw()
root.deiconify()



# View Screen
vist = Toplevel(root)
vist.title("View Student")
vist.geometry("500x500+300+200")
vist.withdraw()


stViewData = scrolledtext.ScrolledText(vist,width=30,height=10)

# ViewBack Button
def f4():
	root.deiconify()
	vist.withdraw()
	stViewData.config(state='normal')
	stViewData.delete('1.0',END)
btnViewBack = Button(vist,text="Back",command=f4)

# Packing on view Screen
stViewData.pack()
btnViewBack.pack()


# Add Screen 
adst = Toplevel(root)
adst.title("Add Student")
adst.geometry("500x500+300+200")
adst.withdraw()

# Add  screen Form
lblRno = Label(adst,text="Enter rno")
entRno = Entry(adst,bd=5)
lblname = Label(adst,text="Enter name")
entName = Entry(adst,bd=7)


# Add Button
def f5():
	con = None
	cursor = None
	try:		
		con = cx_Oracle.connect("system/abc123")
		cursor  = con.cursor()
		stViewData.config(state='normal')
		sql = "insert into student values ('%d','%s')"
		rno = int(entRno.get())
		name = entName.get()


		# Validation on Inserting students
		if type(name)==str and len(name)!=0 and name.isalpha() :
			
			args=(rno,name)
			cursor.execute(sql % args)
			con.commit()
			messagebox.showinfo("Success",str(cursor.rowcount)+"records inserted")
			entRno.delete(0,'end')
			entName.delete(0,'end')
			
		else:
			messagebox.showerror("Failure","Name should be string")

	except cx_Oracle.DatabaseError as e:
		con.rollback()
		messagebox.showerror("Failure","issue : "+str(e))
	except ValueError:
		messagebox.showerror("Failure","Rno should contains interger only")
	finally:
		if cursor is not None:
			cursor.close()
		if con is not None:
			con.close()

btnAddSave = Button(adst,text="Save",command=f5)

# AddBack button
def f2():
	root.deiconify()
	adst.withdraw()

btnAddBack = Button(adst,text="Back",command=f2)

lblRno.pack(pady=10)
entRno.pack(pady=10)
lblname.pack(pady=10)
entName.pack(pady=10)
btnAddSave.pack(pady=10)
btnAddBack.pack(pady=10)


# Add Button
def f1():
	adst.deiconify()
	root.withdraw()
btnAdd = Button(root,text="Add",width=10,command=f1)


# AddView Button
def f3():
	vist.deiconify()
	adst.withdraw()	
	con = None
	cursor = None
	try:
		con = cx_Oracle.connect("system/abc123")
		cursor = con.cursor()
		stViewData.config(state='normal')
		sql = "select * from student order by rno"
		cursor.execute(sql)
		data = cursor.fetchall()
		info=""
		for d in data:
			info =info+" rno "+ str(d[0])+" name "+d[1]+"\n" 
		
		stViewData.insert(INSERT ,info)
		stViewData.config(state='disabled')
	except cx_Oracle.DatabaseError as e:
		con.rollback()
		messagebox.showerror("Failure", "Issue : " + str(e))
	finally:
		if cursor is not None:
			cursor.close()
		if con is not None:
			con.close()


btnView = Button(root,text="View",width=10,command=f3)
btnAdd.pack(pady=20)
btnView.pack(pady=20)

upst = Toplevel(root)
upst.title("Update Student")
upst.geometry("400x400+300+200")
upst.withdraw()


def f7():
	root.withdraw()
	upst.deiconify()

btnUpdate = Button(root,text="Update",width=10,command=f7)
btnUpdate.pack(pady=20)

def f6():
	con = None
	cursor = None
	try:		
		con = cx_Oracle.connect("system/abc123")
		cursor  = con.cursor()
		stViewData.config(state='normal')
		sql = "update student set name='%s' Where rno ='%d'"
		rno = int(entUpdateRno.get())
		name = entUpdateName.get()
		
		if type(name)==str and len(name)!=0 and name.isalpha() :
			args=(name,rno)			
			cursor.execute(sql % args)
			con.commit()
			messagebox.showinfo("Success",str(cursor.rowcount)+"records updated")
			entUpdateName.delete(0,'end')
			entUpdateRno.delete(0,'end')
			
		else :
			messagebox.showerror("Failure", "Name should be string")
	except cx_Oracle.DatabaseError as e:
		con.rollback()
		messagebox.showerror("Failure","issue : "+str(e))
	except ValueError:
		messagebox.showerror("Failure","Rno should be integer only")
	finally:
		if cursor is not None:
			cursor.close()
		if con is not None:
			con.close()


btnUpdateUpdate = Button(upst,text="Update",width=10,command=f6)
entUpdateName = Entry(upst,bd=5)
entUpdateRno = Entry(upst,bd=5)
lblUpdateRno = Label(upst,text="Enter rno")
lblUpdateName = Label(upst,text="Enter updated Name")
lblUpdateRno.pack(pady=10)
entUpdateRno.pack(pady=10)
lblUpdateName.pack(pady=10)
entUpdateName.pack(pady=10)
btnUpdateUpdate.pack(pady=10)
def f8():
	upst.withdraw()
	root.deiconify()

btnUpdateBack = Button(upst,text="Back",width=10,command=f8)
btnUpdateBack.pack(pady=10)

dest = Toplevel(root)
dest.title("Delete Student")
dest.geometry("400x400+300+200")
dest.withdraw()

def f9():
	root.withdraw()
	dest.deiconify()
btnDelete = Button(root,text="Delete",width=10,command=f9)
btnDelete.pack(pady=20)

def f10():
	dest.withdraw()
	root.deiconify()
btnDeleteBack = Button(dest,text='Back',width=10,command=f10)

def f11():
	con = None
	cursor = None
	try:		
		con = cx_Oracle.connect("system/abc123")
		cursor  = con.cursor()
		stViewData.config(state='normal')
		sql = "delete student Where rno ='%d'"
		rno = int(entDeleteRno.get())
		args=(rno)			
		cursor.execute(sql % args)
		con.commit()
		messagebox.showinfo("Success",str(cursor.rowcount)+"records deleted")
		entDeleteRno.delete(0,'end')
		
	except cx_Oracle.DatabaseError as e:
		con.rollback()
		messagebox.showerror("Failure","issue : "+str(e))
	except ValueError:
		messagebox.showerror("Failure","Rno should be integer only")
	finally:
		if cursor is not None:
			cursor.close()
		if con is not None:
			con.close()
btnDeleteDelete = Button(dest,text='Delete',width=10,command=f11)
lblDeleteRno = Label(dest,text='Enter Rno')
lblDeleteRno.pack(pady=10)
entDeleteRno = Entry(dest,bd=5)
entDeleteRno.pack(pady=10)
btnDeleteDelete.pack(pady=10)
btnDeleteBack.pack(pady=10)
	

root.mainloop()    