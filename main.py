import sqlite3
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from tkmacosx import Button
from datetime import date


def ConnectToDatabase():
    global conn, cursor
    conn = sqlite3.connect("database/database.db")
    cursor = conn.cursor()

def CreateWindowsFrame():
    root = Tk()
    root.title("โปรแกรมจัดการคลังสินค้า ร้านโภทิลาษ")
    x = root.winfo_screenwidth() / 2 - w / 2
    y = root.winfo_screenheight() / 2 - h / 2
    root.geometry("%dx%d+%d+%d" %(w, h, x, y))
    root.rowconfigure((0,1,2), weight=1)  # type: ignore
    root.columnconfigure((0,1,2), weight=1) # type: ignore
    root["bg"] = "white"
    
    return root


def LoginPage():
    global userNameEnt, pwdEnt
    loginFrame = Frame(root, bg="gray")
    loginFrame.rowconfigure((0,1,2), weight=1) # type: ignore
    loginFrame.columnconfigure(0, weight=1)
    loginFrame.grid(row=1, column=1, sticky="news")

    top = Frame(loginFrame, bg="white")
    top.rowconfigure(0, weight=1)
    top.columnconfigure(0, weight=1)
    top.grid(row=0 ,column=0, sticky="news")

    header = Label(top, text="เข้าสู่ระบบ", font="verdana 35 bold", bg="white", fg="black")
    header.grid(row=0, column=0)

    middle = Frame(loginFrame, bg="white")
    middle.rowconfigure((0,1,2,3), weight=1) # type: ignore
    middle.columnconfigure(0, weight=1)
    middle.grid(row=1, column=0, sticky="news")

    Label(middle, text="ชื่อผู้ใช้งาน", fg="black", bg="white", font="verdana 25").grid(row=0, column=0)
    userNameEnt = Entry(middle, textvariable=usernameSpy, width=30)
    userNameEnt.grid(row=1, column=0)

    Label(middle, text="รหัสผ่าน", fg="black", bg="white", font="verdana 25").grid(row=2, column=0)
    pwdEnt = Entry(middle, textvariable=pwdSpy, width=30, show="●")
    pwdEnt.grid(row=3, column=0)

    bot = Frame(loginFrame, bg="white")
    bot.rowconfigure(0, weight=1)
    bot.columnconfigure(0, weight=1)
    bot.grid(row=2, column=0, sticky="news")

    loginBtn = Button(bot, text="เข้าสู่ระบบ", fg="white", bg="gray", borderless=1, command=loginclicked)
    loginBtn.grid(row=0, column=0)


def loginclicked():
    if usernameSpy.get() == "":
        messagebox.showwarning("Admin:", "กรุณากรอกชื่อผู้ใช้งานของท่าน")
        userNameEnt.focus_force()
    else:
        if pwdSpy.get() == "":
                messagebox.showwarning("Admin:", "กรุณากรอกรหัสผ่านของท่าน")
                pwdEnt.focus_force()
        else:
                sql = "SELECT * FROM LoginTable WHERE username = ? AND pwd = ?"
                cursor.execute(sql, [usernameSpy.get(), pwdSpy.get()])
                result = cursor.fetchone()
                if result:
                    messagebox.showinfo("Admin:", "เข้าสู่ระบบสำเร็จ")
                    global permission
                    permission = result[3]
                    MainPage()
                else:
                    messagebox.showerror("Admin:", "ชื่อผู้ใช้งานหรือรหัสผ่านไม่ถูกต้อง กรุณาลองใหม่อีกครั้ง")
                    pwdSpy.set("")
                    usernameSpy.set("")
                    userNameEnt.focus_force()


def MainPage():
    global infoFrame, warehouseBtn
    mainpageFrame = Frame(root, bg="black")
    mainpageFrame.rowconfigure(0, weight=1)
    mainpageFrame.columnconfigure(0, weight=1)
    mainpageFrame.columnconfigure(1, weight=5)
    mainpageFrame.grid(row=0,rowspan=3, column=0, columnspan=3, sticky="news")

    menuFrame = Frame(mainpageFrame, bg="gray")
    menuFrame.columnconfigure((0,1), weight=1) # type: ignore
    menuFrame.rowconfigure((0,1,2,3,4,5,6,7,8,9), weight=1) # type: ignore
    menuFrame.grid(row=0, column=0, sticky="news")

    infoFrame = Frame(mainpageFrame, bg="green")
    infoFrame.rowconfigure(0, weight=1)
    infoFrame.columnconfigure(0, weight=1)
    infoFrame.grid(row=0, column=1, sticky="news")

    # คลังสินค้า
    warehouseBtn = Button(menuFrame, text="คลังสินค้า", bg="gray", fg="white", borderless=1, command=warehouseClicked)
    warehouseBtn.grid(row=0, column=0, columnspan=2, sticky="news")
    # Logout Button
    Button(menuFrame, text="Log out", bg="white", fg="black", borderless=1, command=mainpageFrame.destroy).grid(row=9, column=0)
    # Exit Button
    Button(menuFrame, text="Exit", bg="red", fg="black", borderless=1, command=exit).grid(row=9, column=1)


def clearInfoFrame():
    for widget in infoFrame.winfo_children():
        widget.destroy()


def warehouseClicked():
    global warehouseTree
    clearInfoFrame()
    warehouseBtn["fg"] = "blue"
    warehouseFrame = Frame(infoFrame, bg="white")
    warehouseFrame.rowconfigure(0, weight=1) # type: ignore
    warehouseFrame.rowconfigure(1, weight=5)
    warehouseFrame.columnconfigure(0, weight=1)
    warehouseFrame.grid(row=0, column=0, sticky="news")

    top = Frame(warehouseFrame, bg="white")
    top.rowconfigure(0, weight=1)
    top.columnconfigure(0, weight=1)
    top.grid(row=0, column=0, sticky="news")

    middle = Frame(warehouseFrame, bg="white")
    middle.rowconfigure(0, weight=1) #type: ignore

    middle.columnconfigure(0, weight=1)
    middle.grid(row=1, column=0, sticky="news")

    #header
    Label(top, text="คลังสินค้า", fg="black", bg="white", font="verdana 35 bold").grid(row=0, column=0, sticky='s')

    warehouseTree = ttk.Treeview(middle)
    warehouseTree.column("#0", width=0, stretch=NO)
    warehouseTree["columns"] = ("รหัสสินค้า","ชื่อสินค้า", "ราคาต้นทุนต่อหน่วย", "ราคาขายต่อหน่วย", "ปริมาณคงเหลือ", "วันที่บันทึกล่าสุด")

    warehouseTree.column("รหัสสินค้า", width=100, anchor=CENTER)
    warehouseTree.column("ชื่อสินค้า", width=100, anchor=CENTER)
    warehouseTree.column("ราคาต้นทุนต่อหน่วย", width=120, anchor=E)
    warehouseTree.column("ราคาขายต่อหน่วย", width=120, anchor=E)
    warehouseTree.column("ปริมาณคงเหลือ", width=120, anchor=E)
    warehouseTree.column("วันที่บันทึกล่าสุด", width=120, anchor=E)

    warehouseTree.heading("รหัสสินค้า", text="รหัสสินค้า")
    warehouseTree.heading("ชื่อสินค้า", text="ชื่อสินค้า")
    warehouseTree.heading("ราคาต้นทุนต่อหน่วย", text="ราคาต้นทุนต่อหน่วย")
    warehouseTree.heading("ราคาขายต่อหน่วย", text="ราคาขายต่อหน่วย")
    warehouseTree.heading("ปริมาณคงเหลือ", text="ปริมาณคงเหลือ")
    warehouseTree.heading("วันที่บันทึกล่าสุด", text="วันที่บันทึกล่าสุด")


    warehouseTree.grid(row=0, column=0)
    fetchTree()

    # Add Button
    Button(middle, text="เพิ่มสินค้า", fg="black", bg="green", borderless=1, command=addProductClicked).grid(row=0, column=0, sticky='ne', padx=60, pady=170)

    # Modify Button
    Button(middle, text="แก้ไขสินค้า", fg="black", bg="yellow", borderless=1, command=modifyProductClicked).grid(row=0, column=0, sticky='se', padx=160, pady=170)

    #Delete Button
    Button(middle, text="ลบสินค้า", fg="black", bg="red", borderless=1, command=deleteProductClicked).grid(row=0, column=0, sticky='se', padx=60, pady=170)
    

def fetchTree():
    warehouseTree.delete(*warehouseTree.get_children())
    sql = "SELECT * FROM WareHouseTable"
    cursor.execute(sql)
    res = cursor.fetchall()
    if res:
        for i in range(len(res)):
            warehouseTree.insert("",END, values=(res[i][0],res[i][1], res[i][2], res[i][3], res[i][4], res[i][5]))


def addProductClicked():
    def AddProduct():
        if prodnameSpy.get() == "":
            messagebox.showerror("Admin:", "กรุณาใส่ชื่อสินค้า")
            prodnameEnt.focus_force()
        elif prodnameSpy.get().isnumeric() == True:
            messagebox.showerror("Admin:", "ชื่อสินค้าไม่สามารถเป็นตัวเลขได้")
            prodnameEnt.focus_force()
        elif prodCostEnt.get() == "":
            messagebox.showerror("Admin:", "กรุณาใส่ราคาต้นทุน")
            prodCostEnt.focus_force()
        elif prodCostEnt.get().replace('.', '',1).isnumeric() == False:
            messagebox.showerror("Admin:", "ราคาต้นทุนต้องเป็นตัวเลขเท่านั้น")
            prodCostEnt.focus_force()
        elif prodPriceEnt.get() == "":
            messagebox.showerror("Admin:", "กรุณาใส่ราคาขาย")
            prodPriceEnt.focus_force()
        elif prodPriceEnt.get().replace('.', '',1).isnumeric() == False:
            messagebox.showerror("Admin:", "ราคาขายต้องเป็นตัวเลขเท่านั้น")
            prodPriceEnt.focus_force()
        elif prodQuantityEnt.get() == "":
            messagebox.showerror("Admin:", "กรุณาใส่ปริมาณในคลัง")
            prodQuantityEnt.focus_force()
        elif prodQuantityEnt.get().isnumeric() == False:
            messagebox.showerror("Admin:", "ปริมาณในคลังต้องเป็นตัวเลขจำนวนเต็มเท่านั้นเท่านั้น")
            prodQuantityEnt.focus_force()
        else:
            isValid = True
            sql = "SELECT productName FROM WareHouseTable"
            cursor.execute(sql)
            res = cursor.fetchall()
            for i in range(len(res)):
                if res[i][0] == prodnameSpy.get():
                    messagebox.showerror("Admin:","สินค้าประเภทนี้มีอยู่ในคลังอยู่แล้ว")
                    isValid = False
                    break
            
            if isValid:
                today = date.today()
                d = today.strftime("%m/%d/%y")
                sql = "INSERT INTO WareHouseTable (productName, cost, price, quantity, date) VALUES (?,?,?,?,?)"
                cursor.execute(sql, [prodnameSpy.get(), prodCostEnt.get(), prodPriceEnt.get(), prodQuantityEnt.get(), d])
                conn.commit()
                messagebox.showinfo("Admin:", "สินค้าใหม่ได้ถูกเพิ่มเข้าคลังแล้ว")
                addProductWindow.destroy()
                fetchTree()
            else:
                prodnameEnt.focus_force()

    prodnameSpy = StringVar()

    w = 500
    h = 500
    addProductWindow = Toplevel(root)
    addProductWindow.title("เพิ่มสินค้าใหม่")
    addProductWindow.rowconfigure(0, weight=1)
    addProductWindow.columnconfigure(0, weight=1)
    x = root.winfo_screenwidth() / 2 - w / 2
    y = root.winfo_screenheight() / 2 - h / 2
    addProductWindow.geometry("%dx%d+%d+%d" %(w, h, x, y))

    addProductFrame = Frame(addProductWindow, bg="white")
    addProductFrame.rowconfigure((0,1,2,3,4), weight=1) #type: ignore
    addProductFrame.columnconfigure((0,1), weight=1)  # type: ignore
    addProductFrame.grid(row=0, column=0, sticky="news")

    Label(addProductFrame, text="ชื่อสินค้า:", fg="black", bg="white", font="verdana 25").grid(row=0, column=0, sticky='e')
    prodnameEnt = Entry(addProductFrame, textvariable=prodnameSpy, width=20)
    prodnameEnt.grid(row=0, column=1, sticky='w')

    Label(addProductFrame, text="ราคาต้นทุน:", fg="black", bg="white", font="verdana 25").grid(row=1, column=0, sticky='e')
    prodCostEnt = Entry(addProductFrame, width=20)
    prodCostEnt.grid(row=1, column=1, sticky='w')

    Label(addProductFrame, text="ราคาขาย:", fg="black", bg="white", font="verdana 25").grid(row=2, column=0, sticky='e')
    prodPriceEnt = Entry(addProductFrame, width=20)
    prodPriceEnt.grid(row=2, column=1, sticky='w')

    Label(addProductFrame, text="ปริมาณในคลัง:", fg="black", bg="white", font="verdana 25").grid(row=3, column=0, sticky='e')
    prodQuantityEnt = Entry(addProductFrame, width=20)
    prodQuantityEnt.grid(row=3, column=1, sticky='w')

    Button(addProductFrame, text="เพิ่มสินค้า", fg="black", bg="green", borderless=1, font="verdana 25 bold", command=AddProduct).grid(row=4, columnspan=2)


def deleteProductClicked():
    if warehouseTree.focus() == "":
        messagebox.showerror("Admin:", "กรุณาเลือกสินค้าที่ต้องการจะลบ")
    else:
        msg = messagebox.askquestion("Delete", "ต้องการลบสินค้านี้หรือไม่", icon="warning")
        if msg == "yes":
            selectedProd = warehouseTree.item(warehouseTree.focus(), "values")
            selectedProd_id = selectedProd[0]
            sql = '''DELETE FROM WareHouseTable
                        WHERE productID = ?'''
            cursor.execute(sql, [selectedProd_id])
            conn.commit()
            messagebox.showinfo("Admin:", "สินค้าถูกลบออกจากคลังเรียบร้อยแล้ว")
            fetchTree()


def modifyProductClicked():
    def ModifyProduct():
        if prodnameSpy.get() == "":
            messagebox.showerror("Admin:", "กรุณาใส่ชื่อสินค้า")
            prodnameEnt.focus_force()
        elif prodnameSpy.get().isnumeric() == True:
            messagebox.showerror("Admin:", "ชื่อสินค้าไม่สามารถเป็นตัวเลขได้")
            prodnameEnt.focus_force()
        elif prodCostEnt.get() == "":
            messagebox.showerror("Admin:", "กรุณาใส่ราคาต้นทุน")
            prodCostEnt.focus_force()
        elif prodCostEnt.get().replace('.', '',1).isnumeric() == False:
            messagebox.showerror("Admin:", "ราคาต้นทุนต้องเป็นตัวเลขเท่านั้น")
            prodCostEnt.focus_force()
        elif prodPriceEnt.get() == "":
            messagebox.showerror("Admin:", "กรุณาใส่ราคาขาย")
            prodPriceEnt.focus_force()
        elif prodPriceEnt.get().replace('.', '',1).isnumeric() == False:
            messagebox.showerror("Admin:", "ราคาขายต้องเป็นตัวเลขเท่านั้น")
            prodPriceEnt.focus_force()
        elif prodQuantityEnt.get() == "":
            messagebox.showerror("Admin:", "กรุณาใส่ปริมาณในคลัง")
            prodQuantityEnt.focus_force()
        elif prodQuantityEnt.get().isnumeric() == False:
            messagebox.showerror("Admin:", "ปริมาณในคลังต้องเป็นตัวเลขจำนวนเต็มเท่านั้นเท่านั้น")
            prodQuantityEnt.focus_force()
        else:
            isValid = True
            sql = "SELECT productName, productID FROM WareHouseTable"
            cursor.execute(sql)
            res = cursor.fetchall()
            for i in range(len(res)):
                if res[i][0] == prodnameSpy.get() and res[i][1] != selectedProd_id:
                    messagebox.showerror("Admin:","สินค้าประเภทนี้มีอยู่ในคลังอยู่แล้ว")
                    isValid = False
                    break
            
            if isValid:
                today = date.today()
                d = today.strftime("%m/%d/%y")
                sql = "UPDATE WareHouseTable SET productName = ?, cost = ?, price = ?, quantity = ?, date = ? WHERE productID = ?"
                cursor.execute(sql, [prodnameSpy.get(), prodCostEnt.get(), prodPriceEnt.get(), prodQuantityEnt.get(), d, selectedProd_id])
                conn.commit()
                messagebox.showinfo("Admin:", "แก้ไขสินค้าเรียบร้อยแล้ว")
                modifyWindow.destroy()
                fetchTree()
            else:
                prodnameEnt.focus_force()

    if warehouseTree.focus() == "":
        messagebox.showerror("Admin:", "กรุณาเลือกสินค้าที่ต้องการจะแก้ไข")
    else:
        selectedProd = warehouseTree.item(warehouseTree.focus(), "values")
        selectedProd_id = selectedProd[0]
        selectedProd_name = selectedProd[1]
        selectedProd_cost = selectedProd[2]
        selectedProd_price = selectedProd[3]
        selectedProd_quantity = selectedProd[4]

        prodnameSpy = StringVar()
        prodnameSpy.set(selectedProd_name)
        w = 500
        h = 500
        modifyWindow = Toplevel(root)
        modifyWindow.title("เพิ่มสินค้าใหม่")
        modifyWindow.rowconfigure(0, weight=1)
        modifyWindow.columnconfigure(0, weight=1)
        x = root.winfo_screenwidth() / 2 - w / 2
        y = root.winfo_screenheight() / 2 - h / 2
        modifyWindow.geometry("%dx%d+%d+%d" %(w, h, x, y))

        modifyFrame = Frame(modifyWindow, bg="white")
        modifyFrame.rowconfigure((0,1,2,3,4), weight=1) #type: ignore
        modifyFrame.columnconfigure((0,1), weight=1)  # type: ignore
        modifyFrame.grid(row=0, column=0, sticky="news")

        Label(modifyFrame, text="ชื่อสินค้า:", fg="black", bg="white", font="verdana 25").grid(row=0, column=0, sticky='e')
        prodnameEnt = Entry(modifyFrame, textvariable=prodnameSpy, width=20)
        prodnameEnt.grid(row=0, column=1, sticky='w')

        Label(modifyFrame, text="ราคาต้นทุน:", fg="black", bg="white", font="verdana 25").grid(row=1, column=0, sticky='e')
        prodCostEnt = Entry(modifyFrame, width=20)
        prodCostEnt.insert(END, selectedProd_cost)
        prodCostEnt.grid(row=1, column=1, sticky='w')

        Label(modifyFrame, text="ราคาขาย:", fg="black", bg="white", font="verdana 25").grid(row=2, column=0, sticky='e')
        prodPriceEnt = Entry(modifyFrame, width=20)
        prodPriceEnt.insert(END, selectedProd_price)
        prodPriceEnt.grid(row=2, column=1, sticky='w')

        Label(modifyFrame, text="ปริมาณในคลัง:", fg="black", bg="white", font="verdana 25").grid(row=3, column=0, sticky='e')
        prodQuantityEnt = Entry(modifyFrame, width=20)
        prodQuantityEnt.insert(END, selectedProd_quantity)
        prodQuantityEnt.grid(row=3, column=1, sticky='w')

        Button(modifyFrame, text="แก้ไขสินค้า", fg="black", bg="yellow", borderless=1, font="verdana 25 bold", command=ModifyProduct).grid(row=4, columnspan=2)


w = 1024
h = 720

root = CreateWindowsFrame()
ConnectToDatabase()

# Login Spies
usernameSpy = StringVar()
pwdSpy = StringVar()

warehouseIsopen = False

LoginPage()
root.mainloop()