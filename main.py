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

    loginBtn = Button(bot, text="เข้าสู่ระบบ", fg="white", bg="gray", borderless=1, command=MainPage)
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
                    permission = result[4]
                    MainPage()
                else:
                    messagebox.showerror("Admin:", "ชื่อผู้ใช้งานหรือรหัสผ่านไม่ถูกต้อง กรุณาลองใหม่อีกครั้ง")
                    pwdSpy.set("")
                    usernameSpy.set("")
                    userNameEnt.focus_force()


def MainPage():
    global infoFrame, btnlist, warehouseBtn, supplierManagementBtn, productSearchBtn, intelInvestigateBtn, saveIntelBtn, printReportBtn, purchaseManagementBtn
    mainpageFrame = Frame(root, bg="black")
    mainpageFrame.rowconfigure(0, weight=1)
    mainpageFrame.columnconfigure(0, weight=2)
    mainpageFrame.columnconfigure(1, weight=20)
    mainpageFrame.grid(row=0,rowspan=3, column=0, columnspan=3, sticky="news")

    menuFrame = Frame(mainpageFrame, bg="gray")
    menuFrame.columnconfigure((0,1), weight=1) # type: ignore
    menuFrame.rowconfigure((0,1,2,3,4,5,6,7,8,9), weight=1) # type: ignore
    menuFrame.grid(row=0, column=0, sticky="news")

    infoFrame = Frame(mainpageFrame, bg="white")
    infoFrame.rowconfigure(0, weight=1)
    infoFrame.columnconfigure(0, weight=1)
    infoFrame.grid(row=0, column=1, sticky="news")

    # คลังสินค้า
    warehouseBtn = Button(menuFrame, text="คลังสินค้า", bg="gray", fg="white", borderless=1, command=warehouseClicked)
    warehouseBtn.grid(row=0, column=0, columnspan=2, sticky="news")

    # จัดการผู้ค้าส่ง
    supplierManagementBtn = Button(menuFrame, text="แก้ไข/บันทึกข้อมูลผู้ค้าส่ง", bg="gray", fg="white", borderless=1, command=supplierManagementClicked)
    supplierManagementBtn.grid(row=1, columnspan=2, sticky="news")

    # จัดการข้อมูลการสั่งซื้อ
    purchaseManagementBtn = Button(menuFrame, text="เพิ่ม/แก้ไขข้อมูลการสั่งซื้อ", bg="gray", fg="white", borderless=1, command=purchaseManagementClicked)
    purchaseManagementBtn.grid(row=2, columnspan=2, sticky="news")


    # ค้นหาสินค้า
    productSearchBtn = Button(menuFrame, text="ค้นหาสินค้า", fg="white", bg="gray", command=productsearchClicked, borderless=1)
    productSearchBtn.grid(row=3, column=0, columnspan=2, sticky="news")
    # ตรวจสอบข้อมูล
    intelInvestigateBtn = Button(menuFrame, text="ตรวจสอบข้อมูลการสั่งซื้อ", fg="white", bg="gray", command=intelinvestigateClicked, borderless=1)
    intelInvestigateBtn.grid(row=4, column=0, columnspan=2, sticky="news")
    # บันทึกข้อมูลจัดส่ง
    saveIntelBtn = Button(menuFrame, text="บันทึกข้อมูลการจัดส่ง", fg="white", bg="gray", command=saveintelClicked, borderless=1)
    saveIntelBtn.grid(row=5, column=0, columnspan=2, sticky="news")

    # จัดพิมพ์รายงานเเสดงผลการดำเนินงาน
    printReportBtn = Button(menuFrame, text="จัดพิมพ์รายงาน", fg="white", bg="gray", command=printreportClicked,borderless=1)
    printReportBtn.grid(row=6, column=0, columnspan=2, sticky="news")

    # Logout Button
    Button(menuFrame, text="Log out", bg="white", fg="black", borderless=1, command=mainpageFrame.destroy).grid(row=9, column=0)
    # Exit Button
    Button(menuFrame, text="Exit", bg="red", fg="black", borderless=1, command=exit).grid(row=9, column=1)

    btnlist = [warehouseBtn, supplierManagementBtn, productSearchBtn, intelInvestigateBtn, saveIntelBtn, printReportBtn, purchaseManagementBtn]


def clearInfoFrame():
    for widget in infoFrame.winfo_children():
        widget.destroy()


def resetBtnColor():
    for i in range(len(btnlist)):
        btnlist[i]["fg"] = "white"


def warehouseClicked():
    global warehouseTree
    resetBtnColor()
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

    # Add Button
    Button(middle, text="เพิ่มสินค้า", fg="black", bg="green", borderless=1, command=addProductClicked).grid(row=0, column=0, sticky='ne', padx=60, pady=170)

    # Modify Button
    Button(middle, text="แก้ไขสินค้า", fg="black", bg="yellow", borderless=1, command=modifyProductClicked).grid(row=0, column=0, sticky='se', padx=160, pady=170)

    #Delete Button
    Button(middle, text="ลบสินค้า", fg="black", bg="red", borderless=1, command=deleteProductClicked).grid(row=0, column=0, sticky='se', padx=60, pady=170)
    
    fetchWarehouseTree()
    

def fetchWarehouseTree():
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
            messagebox.showerror("Admin:", "ราคาต้นทุนต้องเป็นจำนวนเต็มบวกเท่านั้น")
            prodCostEnt.focus_force()
        elif prodPriceEnt.get() == "":
            messagebox.showerror("Admin:", "กรุณาใส่ราคาขาย")
            prodPriceEnt.focus_force()
        elif prodPriceEnt.get().replace('.', '',1).isnumeric() == False:
            messagebox.showerror("Admin:", "ราคาขายต้องเป็นจำนวนเต็มบวกเท่านั้น")
            prodPriceEnt.focus_force()
        elif prodQuantityEnt.get() == "":
            messagebox.showerror("Admin:", "กรุณาใส่ปริมาณในคลัง")
            prodQuantityEnt.focus_force()
        elif prodQuantityEnt.get().isnumeric() == False:
            messagebox.showerror("Admin:", "ปริมาณในคลังต้องเป็นตัวเลขจำนวนเต็มบวกเท่านั้นเท่านั้น")
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
                d = today.strftime("%d/%m/%y")
                sql = "INSERT INTO WareHouseTable (productName, cost, price, quantity, date) VALUES (?,?,?,?,?)"
                cursor.execute(sql, [prodnameSpy.get(), prodCostEnt.get(), prodPriceEnt.get(), prodQuantityEnt.get(), d])
                conn.commit()
                messagebox.showinfo("Admin:", "สินค้าใหม่ได้ถูกเพิ่มเข้าคลังแล้ว")
                addProductWindow.destroy()
                fetchWarehouseTree()
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
            fetchWarehouseTree()


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
                d = today.strftime("%d/%m/%y")
                sql = "UPDATE WareHouseTable SET productName = ?, cost = ?, price = ?, quantity = ?, date = ? WHERE productID = ?"
                cursor.execute(sql, [prodnameSpy.get(), prodCostEnt.get(), prodPriceEnt.get(), prodQuantityEnt.get(), d, selectedProd_id])
                conn.commit()
                messagebox.showinfo("Admin:", "แก้ไขสินค้าเรียบร้อยแล้ว")
                modifyWindow.destroy()
                fetchWarehouseTree()
            else:
                prodnameEnt.focus_force()

    if warehouseTree.focus() == "":
        messagebox.showerror("Admin:", "กรุณาเลือกสินค้าที่ต้องการจะแก้ไข")
    else:
        selectedProd = warehouseTree.item(warehouseTree.focus(), "values")
        selectedProd_id = int(selectedProd[0])
        selectedProd_name = selectedProd[1]
        selectedProd_cost = selectedProd[2]
        selectedProd_price = selectedProd[3]
        selectedProd_quantity = selectedProd[4]

        prodnameSpy = StringVar()
        prodnameSpy.set(selectedProd_name)
        w = 500
        h = 500
        modifyWindow = Toplevel(root)
        modifyWindow.title("แก้ไขสินค้า")
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


def supplierManagementClicked():
    global supplierTree
    resetBtnColor()
    clearInfoFrame()
    supplierManagementBtn["fg"] = "blue"
    supplierManageFrame = Frame(infoFrame, bg="white")
    supplierManageFrame.rowconfigure(0, weight=1) # type: ignore
    supplierManageFrame.rowconfigure(1, weight=5)
    supplierManageFrame.columnconfigure(0, weight=1)
    supplierManageFrame.grid(row=0, column=0, sticky="news")

    top = Frame(supplierManageFrame, bg="white")
    top.rowconfigure(0, weight=1)
    top.columnconfigure(0, weight=1)
    top.grid(row=0, column=0, sticky="news")

    middle = Frame(supplierManageFrame, bg="white")
    middle.rowconfigure(0, weight=1) #type: ignore

    middle.columnconfigure(0, weight=1)
    middle.grid(row=1, column=0, sticky="news")

    #header
    Label(top, text="แก้ไข/บันทึกผู้ค้าส่ง", fg="black", bg="white", font="verdana 35 bold").grid(row=0, column=0, sticky='s')

    supplierTree = ttk.Treeview(middle)
    supplierTree.column("#0", width=0, stretch=NO)
    supplierTree["columns"] = ("รหัสผู้ค้าส่ง","ชื่อร้าน/สวน", "ชื่อผู้ติดต่อ", "เบอร์โทรศัพท์")

    supplierTree.column("รหัสผู้ค้าส่ง", width=100, anchor=CENTER)
    supplierTree.column("ชื่อร้าน/สวน", width=100, anchor=CENTER)
    supplierTree.column("ชื่อผู้ติดต่อ", width=120, anchor=CENTER)
    supplierTree.column("เบอร์โทรศัพท์", width=120, anchor=CENTER)

    supplierTree.heading("รหัสผู้ค้าส่ง", text="รหัสผู้ค้าส่ง")
    supplierTree.heading("ชื่อร้าน/สวน", text="ชื่อร้าน/สวน")
    supplierTree.heading("ชื่อผู้ติดต่อ", text="ชื่อผู้ติดต่อ")
    supplierTree.heading("เบอร์โทรศัพท์", text="เบอร์โทรศัพท์")

    supplierTree.grid(row=0, column=0)

    # Add Button
    Button(middle, text="เพิ่มผู้ค้าส่ง", fg="black", bg="green", borderless=1, command=addSupplierClicked).grid(row=0, column=0, sticky='ne', padx=180, pady=170)

    # Modify Button
    Button(middle, text="แก้ไขผู้ค้าส่ง", fg="black", bg="yellow", borderless=1, command=modifySupperlierClicked).grid(row=0, column=0, sticky='se', padx=280, pady=170)

    #Delete Button
    Button(middle, text="ลบผู้ค้าส่ง", fg="black", bg="red", borderless=1, command=deleteSupplierClicked).grid(row=0, column=0, sticky='se', padx=180, pady=170)
    
    fetchSupplierTree()
    

def fetchSupplierTree():
    supplierTree.delete(*supplierTree.get_children())
    sql = "SELECT * FROM SupplierContactTable"
    cursor.execute(sql)
    res = cursor.fetchall()
    if res:
        for i in range(len(res)):
            supplierTree.insert("",END, values=(res[i][0],res[i][1], res[i][2], res[i][3]))


def addSupplierClicked():
    def AddSupplier():
        if supplierNameEnt.get() == "":
            messagebox.showerror("Admin:", "กรุณาใส่ชื่อร้าน/สวน")
            supplierNameEnt.focus_force()
        elif supplierNameEnt.get().isnumeric() == True:
            messagebox.showerror("Admin:", "ชื่อร้าน/สวนไม่สามารถเป็นตัวเลขได้")
            supplierNameEnt.focus_force()
        elif contactNameEnt.get() == "":
            messagebox.showerror("Admin:", "กรุณาใส่ชื่อผู้ติดต่อ")
            contactNameEnt.focus_force()
        elif contactNameEnt.get().isnumeric() == True:
            messagebox.showerror("Admin:", "ชื่อผู้ติดต่อไม่ถูกต้อง")
            contactNameEnt.focus_force()
        elif phoneEnt.get() == "":
            messagebox.showerror("Admin:", "กรุณาใส่เบอร์โทรศัพท์")
            phoneEnt.focus_force()
        elif phoneEnt.get().replace('-', '').isnumeric() == False or (len(phoneEnt.get().replace('-', '')) != 10 and len(phoneEnt.get().replace('-', '')) != 9):
            messagebox.showerror("Admin:", "เบอร์โทรศัพท์ไม่ถูกต้อง")
            phoneEnt.focus_force()
        else:
            isValid = True
            sql = "SELECT supplierName FROM SupplierContactTable"
            cursor.execute(sql)
            res = cursor.fetchall()
            for i in range(len(res)):
                if res[i][0] == supplierNameEnt.get():
                    messagebox.showerror("Admin:","มีค้าส่งรายนี้ในฐานข้อมูลแล้ว")
                    isValid = False
                    break
            
            if isValid:
                sql = "INSERT INTO SupplierContactTable (supplierName, contactName, phone) VALUES (?,?,?)"
                cursor.execute(sql, [supplierNameEnt.get(), contactNameEnt.get(), phoneEnt.get().replace('-','')])
                conn.commit()
                messagebox.showinfo("Admin:", "ผู้ค้าส่งใหม่ได้ถูกเพิ่มเข้าสู่ฐานระบบแล้ว")
                addSupplierWindow.destroy()
                fetchSupplierTree()
            else:
                supplierNameEnt.focus_force()
    

    w = 500
    h = 500
    addSupplierWindow = Toplevel(root)
    addSupplierWindow.title("เพิ่มผู้ค้าส่งใหม่")
    addSupplierWindow.rowconfigure(0, weight=1)
    addSupplierWindow.columnconfigure(0, weight=1)
    x = root.winfo_screenwidth() / 2 - w / 2
    y = root.winfo_screenheight() / 2 - h / 2
    addSupplierWindow.geometry("%dx%d+%d+%d" %(w, h, x, y))

    addSupplierFrame = Frame(addSupplierWindow, bg="white")
    addSupplierFrame.rowconfigure((0,1,2,3), weight=1) #type: ignore
    addSupplierFrame.columnconfigure((0,1), weight=1)  # type: ignore
    addSupplierFrame.grid(row=0, column=0, sticky="news")

    Label(addSupplierFrame, text="ชื่อร้าน/สวน:", fg="black", bg="white", font="verdana 25").grid(row=0, column=0, sticky='e')
    supplierNameEnt = Entry(addSupplierFrame, width=20)
    supplierNameEnt.grid(row=0, column=1, sticky='w')

    Label(addSupplierFrame, text="ชื่อผู้ติดต่อ:", fg="black", bg="white", font="verdana 25").grid(row=1, column=0, sticky='e')
    contactNameEnt = Entry(addSupplierFrame, width=20)
    contactNameEnt.grid(row=1, column=1, sticky='w')

    Label(addSupplierFrame, text="เบอร์โทรศัพท์ติดต่อ:", fg="black", bg="white", font="verdana 25").grid(row=2, column=0, sticky='e')
    phoneEnt = Entry(addSupplierFrame, width=20)
    phoneEnt.grid(row=2, column=1, sticky='w')

    Button(addSupplierFrame, text="เพิ่มผู้ค้าส่ง", fg="black", bg="green", borderless=1, font="verdana 25 bold", command=AddSupplier).grid(row=3, columnspan=2)


def modifySupperlierClicked():
    def ModifySupplier():
        if supplierNameEnt.get() == "":
            messagebox.showerror("Admin:", "กรุณาใส่ชื่อร้าน/สวน")
            supplierNameEnt.focus_force()
        elif supplierNameEnt.get().isnumeric() == True:
            messagebox.showerror("Admin:", "ชื่อสินค้าร้าน/สวน ไม่ถูกต้อง")
            supplierNameEnt.focus_force()
        elif contactNameEnt.get() == "":
            messagebox.showerror("Admin:", "กรุณาใส่ชื่อผู้ติดต่อ")
            contactNameEnt.focus_force()
        elif contactNameEnt.get().isnumeric() == True:
            messagebox.showerror("Admin:", "ชื่อผู้ติดต่อไม่ถูกต้อง")
            contactNameEnt.focus_force()
        elif phoneEnt.get() == "":
            messagebox.showerror("Admin:", "กรุณาใส่เบอร์โทรศัพท์ติดต่อ")
            phoneEnt.focus_force()
        elif phoneEnt.get().replace('-', '').isnumeric() == False or (len(phoneEnt.get().replace('-', '')) != 10 and len(phoneEnt.get().replace('-', '')) != 9):
            messagebox.showerror("Admin:", "เบอร์โทรศัพท์ไม่ถูกต้อง")
            phoneEnt.focus_force()
        else:
            isValid = True
            sql = "SELECT supplierName, supplierID FROM SupplierContactTable"
            cursor.execute(sql)
            res = cursor.fetchall()
            for i in range(len(res)):
                if res[i][0] == supplierNameEnt.get() and res[i][1] != selectedSupp_id:
                    messagebox.showerror("Admin:","มีผู้ค้าส่งนี้อยู่ในฐานระบบแล้ว")
                    isValid = False
                    break
            
            if isValid:
                sql = "UPDATE SupplierContactTable SET supplierName = ?, contactName = ?, phone = ? WHERE supplierID = ?"
                cursor.execute(sql, [supplierNameEnt.get(), contactNameEnt.get(), phoneEnt.get().replace('-',''), selectedSupp_id])
                conn.commit()
                messagebox.showinfo("Admin:", "แก้ไขผู้ค้าส่งเรียบร้อยแล้ว")
                modifyWindow.destroy()
                fetchSupplierTree()
            else:
                supplierNameEnt.focus_force()

    if supplierTree.focus() == "":
        messagebox.showerror("Admin:", "กรุณาเลือกผู้ค้าส่งที่ต้องการจะแก้ไข")
    else:
        selectedSupp = supplierTree.item(supplierTree.focus(), "values")
        selectedSupp_id = int(selectedSupp[0])
        selectedSupp_name = selectedSupp[1]
        selectedSupp_contact = selectedSupp[2]
        selectedSupp_phone = selectedSupp[3]

        w = 500
        h = 500
        modifyWindow = Toplevel(root)
        modifyWindow.title("แก้ไขผู้ค้าส่ง")
        modifyWindow.rowconfigure(0, weight=1)
        modifyWindow.columnconfigure(0, weight=1)
        x = root.winfo_screenwidth() / 2 - w / 2
        y = root.winfo_screenheight() / 2 - h / 2
        modifyWindow.geometry("%dx%d+%d+%d" %(w, h, x, y))

        modifyFrame = Frame(modifyWindow, bg="white")
        modifyFrame.rowconfigure((0,1,2,3), weight=1) #type: ignore
        modifyFrame.columnconfigure((0,1), weight=1)  # type: ignore
        modifyFrame.grid(row=0, column=0, sticky="news")

        Label(modifyFrame, text="ชื่อร้าน/สวน:", fg="black", bg="white", font="verdana 25").grid(row=0, column=0, sticky='e')
        supplierNameEnt = Entry(modifyFrame, width=20)
        supplierNameEnt.insert(END, selectedSupp_name)
        supplierNameEnt.grid(row=0, column=1, sticky='w')

        Label(modifyFrame, text="ชื่อผู้ติดต่อ:", fg="black", bg="white", font="verdana 25").grid(row=1, column=0, sticky='e')
        contactNameEnt = Entry(modifyFrame, width=20)
        contactNameEnt.insert(END, selectedSupp_contact)
        contactNameEnt.grid(row=1, column=1, sticky='w')

        Label(modifyFrame, text="เบอร์โทรศัพท์:", fg="black", bg="white", font="verdana 25").grid(row=2, column=0, sticky='e')
        phoneEnt = Entry(modifyFrame, width=20)
        phoneEnt.insert(END, selectedSupp_phone)
        phoneEnt.grid(row=2, column=1, sticky='w')

        Button(modifyFrame, text="แก้ไขผู้ค้าส่ง", fg="black", bg="yellow", borderless=1, font="verdana 25 bold", command=ModifySupplier).grid(row=3, columnspan=2)


def deleteSupplierClicked():
    if supplierTree.focus() == "":
        messagebox.showerror("Admin:", "กรุณาเลือกผู้ค้าส่งที่ต้องการจะลบที่ต้องการจะลบ")
    else:
        msg = messagebox.askquestion("Delete", "ต้องการจะลบผู้ค้าส่งนี้หรือไม่นี้หรือไม่", icon="warning")
        if msg == "yes":
            selectedSupp = supplierTree.item(supplierTree.focus(), "values")
            selectedSupp_id= selectedSupp[0]
            sql = '''DELETE FROM SupplierContactTable
                        WHERE supplierID = ?'''
            cursor.execute(sql, [selectedSupp_id])
            conn.commit()
            messagebox.showinfo("Admin:", "ผู้ค้าส่งถูกลบออกจากฐานข้อมูลเรียบร้อยแล้ว")
            fetchSupplierTree()


def productsearchClicked() :
    global prodSearchFrame, searchBar
    resetBtnColor()
    clearInfoFrame()
    productSearchBtn["fg"] = "blue"
    prodSearchFrame = Frame(infoFrame, bg="yellow")
    prodSearchFrame.rowconfigure(0, weight=1)
    prodSearchFrame.rowconfigure(1, weight=3)
    prodSearchFrame.columnconfigure(0, weight=3)
    prodSearchFrame.columnconfigure(1, weight=1)
    prodSearchFrame.grid(row=0, column=0, sticky="news")
    # head
    searchBar = Entry(prodSearchFrame, width=70)
    searchBar.grid(row=0, column=0)
    searchBtn = Button(prodSearchFrame, text="ค้นหา", command=createProdSearchTree)
    searchBtn.grid(row=0, column=1)


def createProdSearchTree() :
    global prodserachedTree
    prodserachedTree = ttk.Treeview(prodSearchFrame)
    prodserachedTree.column("#0", width=0, stretch=NO)
    prodserachedTree["columns"] = ("ชื่อสินค้า", "จำนวน", "ราคา/หน่วย", "วันที่สั่ง")

    prodserachedTree.column("ชื่อสินค้า", width=120, anchor=E)
    prodserachedTree.column("จำนวน", width=120, anchor=CENTER)
    prodserachedTree.column("ราคา/หน่วย", width=120, anchor=CENTER)
    prodserachedTree.column("วันที่สั่ง", width=120, anchor=CENTER)

    prodserachedTree.heading("ชื่อสินค้า", text="ชื่อสินค้า")
    prodserachedTree.heading("จำนวน", text="จำนวน")
    prodserachedTree.heading("ราคา/หน่วย", text="ราคา/หน่วย")
    prodserachedTree.heading("วันที่สั่ง", text="วันที่สั่ง")

    prodserachedTree.grid(row=1, column=0, columnspan=2)
    fetchProdSearchedTree()


def fetchProdSearchedTree():
    prodserachedTree.delete(*prodserachedTree.get_children())
    sql = "SELECT * FROM WareHouseTable"
    cursor.execute(sql)
    res = cursor.fetchall()
    if res:
        for i in range(len(res)):
            if searchBar.get() in res[i][1] :
                prodserachedTree.insert("",END, values=(res[i][1],res[i][4], res[i][3], res[i][5]))


def intelinvestigateClicked() :
    resetBtnColor()
    clearInfoFrame()
    intelInvestigateBtn["fg"] = "blue"
    intelinvestigateFrame = Frame(infoFrame, bg="gray")
    intelinvestigateFrame.rowconfigure((0, 1), weight=1)
    intelinvestigateFrame.columnconfigure((0, 1), weight=1)
    intelinvestigateFrame.grid(row=0, column=0, sticky="news")
    # head 
    Label(intelinvestigateFrame, text="ตรวจสอบข้อมูลการสั่งสินค้า", fg="black", bg="white").grid(row=0, column=0)
    # middle
    intelInvestigateTree = ttk.Treeview(intelinvestigateFrame)
    intelInvestigateTree.column("#0", width=0, stretch=NO)
    intelInvestigateTree["columns"] = ("ชื่อสินค้า", "จำนวน", "ราคา/หน่วย", "วันที่สั่ง", "ผู้ค้าส่ง")

    intelInvestigateTree.column("ชื่อสินค้า", width=120, anchor=E)
    intelInvestigateTree.column("จำนวน", width=120, anchor=CENTER)
    intelInvestigateTree.column("ราคา/หน่วย", width=120, anchor=CENTER)
    intelInvestigateTree.column("วันที่สั่ง", width=120, anchor=CENTER)
    intelInvestigateTree.column("ผู้ค้าส่ง", width=120, anchor=CENTER)

    intelInvestigateTree.heading("ชื่อสินค้า", text="ชื่อสินค้า")
    intelInvestigateTree.heading("จำนวน", text="จำนวน")
    intelInvestigateTree.heading("ราคา/หน่วย", text="ราคา/หน่วย")
    intelInvestigateTree.heading("วันที่สั่ง", text="วันที่สั่ง")
    intelInvestigateTree.heading("ผู้ค้าส่ง", text="ผู้ค้าส่ง")

    intelInvestigateTree.grid(row=1, column=0, columnspan=2)

    intelInvestigateTree.delete(*intelInvestigateTree.get_children())
    sql = "SELECT * FROM TableName"
    cursor.execute(sql)
    res = cursor.fetchall()
    if res:
        for i in range(len(res)):
            prodserachedTree.insert("",END, values=(res[i][1],res[i][4], res[i][3], res[i][5]))


def saveintelClicked() :
    resetBtnColor()
    clearInfoFrame()
    saveIntelBtn["fg"] = "blue"
    saveIntelFrame = Frame(infoFrame, bg="cyan")
    saveIntelFrame.columnconfigure((0, 1, 2), weight=1)
    saveIntelFrame.rowconfigure((0, 2), weight=1)
    saveIntelFrame.rowconfigure(1, weight=8)
    saveIntelFrame.grid(row=0, column=0, sticky="news")
    # header
    Label(saveIntelFrame, text="บันทึกข้อมูลการจัดส่ง", fg="black", bg="cyan", font="verdana 25").grid(row=0, column=0)
    #middle
    intelFrame = Frame(saveIntelFrame, bg="white")
    intelFrame.columnconfigure((0, 1, 2), weight=1)
    intelFrame.rowconfigure((0, 1, 2, 3, 4, 5, 6, 7), weight=1)
    intelFrame.grid(row=1, column=0, columnspan=3, sticky="news")

    Label(intelFrame, text="หมายเลขสินค้า", fg="black", bg="white", justify=RIGHT).grid(row=0, column=0, sticky="e")
    product = Entry(intelFrame, width=70)
    product.grid(row=0, column=1, columnspan=2, sticky="w")

    Label(intelFrame, text="ชื่อลูกค้า", fg="black", bg="white", justify=RIGHT).grid(row=1, column=0, sticky="e")
    clientName = Entry(intelFrame, width=70)
    clientName.grid(row=1, column=1, columnspan=2, sticky="w")

    Label(intelFrame, text="เบอร์โทรศัพท์", fg="black", bg="white", justify=RIGHT).grid(row=2, column=0, sticky="e")
    telNumber = Entry(intelFrame, width=70)
    telNumber.grid(row=2, column=1, columnspan=2, sticky="w")

    Label(intelFrame, text="รูปแบบจัดส่ง", fg="black", bg="white", justify=RIGHT).grid(row=3, column=0, sticky="e")
    deliverForm = ttk.Combobox(intelFrame, width=35, values=["ส่งเองเก่งพอ", "ขี้เกียจส่งให้หน่อย"])
    deliverForm.grid(row=3, column=1, columnspan=2, sticky="w")
    
    Label(intelFrame, text="ชื่อบริษัทขนส่ง", fg="black", bg="white", justify=RIGHT).grid(row=4, column=0, sticky="e")
    transportName = Entry(intelFrame, width=70)
    transportName.grid(row=4, column=1, columnspan=2, sticky="w")

    Label(intelFrame, text="หมายเลขพัสดุ", fg="black", bg="white", justify=RIGHT).grid(row=5, column=0, sticky="e")
    prodID = Entry(intelFrame, width=70)
    prodID.grid(row=5, column=1, columnspan=2, sticky="w")

    Label(intelFrame, text="ที่อยู่จัดส่ง", fg="black", bg="white", justify=RIGHT).grid(row=6, column=0, sticky="e")
    clientAddress = Text(intelFrame, width=70, height=3) # .get ได้เลย
    clientAddress.grid(row=7, column=0, columnspan=3,sticky="n")
    # bottom
    saveBtn = Button(saveIntelFrame, text="บันทึก", fg="black", bg="lime", width=20, height=5, command=saveClicked)
    saveBtn.grid(row=2, column=2)


def printreportClicked() :
    resetBtnColor()
    clearInfoFrame()
    printReportBtn["fg"] = "blue"
    printReportFrame = Frame(infoFrame, bg="lime")
    printReportFrame.rowconfigure((0, 2), weight=1)
    printReportFrame.rowconfigure(1, weight=3)
    printReportFrame.columnconfigure((0, 1), weight=1)
    printReportFrame.grid(row=0, column=0, sticky="news")
    # head
    headFrame = Frame(printReportFrame, bg="white")
    headFrame.rowconfigure((0, 1), weight=1)
    headFrame.columnconfigure((0, 1), weight=1)
    headFrame.grid(row=0, column=0, columnspan=2, sticky="news")
    # middle
    middleFrame = Frame(printReportFrame, bg="orange")
    middleFrame.rowconfigure(0, weight=1)
    middleFrame.rowconfigure(1, weight=3)
    middleFrame.columnconfigure(0, weight=1)
    middleFrame.grid(row=1, column=0, columnspan=2, sticky="news")
    # bottom
    printBtn = Button(printReportFrame, text="พิมพ์", fg="black", bg="yellow", command=printClicked, width=20, height=5)
    printBtn.grid(row=2, column=1, sticky="e", padx=10)
    # head buttons
    purchaseReportBtn = Button(headFrame, text="รายงานสรุปข้อมูลการสั่งซื้อ", fg="black", bg="white", command=lambda:reportChange("purchase", middleFrame))
    purchaseReportBtn.grid(row=0, column=0, sticky="news", padx=10)
    sellingReportBtn = Button(headFrame, text="รายงานสรุปข้อมูลการขาย", fg="black", bg="white", command=lambda:reportChange("selling", middleFrame))
    sellingReportBtn.grid(row=0, column=1, sticky="news", padx=10)
    sumReportBtn = Button(headFrame, text="รายงานสรุปรายรับ-รายจ่าย", fg="black", bg="white", command=lambda:reportChange("sum", middleFrame))
    sumReportBtn.grid(row=1, column=0, columnspan=2, sticky="news", pady=3, padx=40)


def reportChange(name, frame) :
    for child in frame.winfo_children() :
        child.destroy()
    if name == "purchase" :
        Label(frame, text="รายงานสรุปข้อมูลการสั่งซื้อ", fg="black", bg="white").grid(row=0, column=0, sticky="w")
    elif name == "selling" :
        Label(frame, text="รายงานสรุปข้อมูลการขาย", fg="black", bg="white").grid(row=0, column=0, sticky="w")
    elif name == "sum" :
        Label(frame, text="รายงานสรุปรายรับ-รายจ่าย", fg="black", bg="white").grid(row=0, column=0, sticky="w")


def saveClicked() :
    return


def printClicked() :
    return


def purchaseManagementClicked():
    global purchaseTree
    resetBtnColor()
    clearInfoFrame()
    purchaseManagementBtn["fg"] = "blue"
    purchaseMangementFrame = Frame(infoFrame, bg="white")
    purchaseMangementFrame.grid(row=0, column=0, sticky="news")

    purchaseMangementFrame.rowconfigure(0, weight=1) # type: ignore
    purchaseMangementFrame.rowconfigure(1, weight=5)
    purchaseMangementFrame.columnconfigure(0, weight=1)
    purchaseMangementFrame.grid(row=0, column=0, sticky="news")

    top = Frame(purchaseMangementFrame, bg="white")
    top.rowconfigure(0, weight=1)
    top.columnconfigure(0, weight=1)
    top.grid(row=0, column=0, sticky="news")

    middle = Frame(purchaseMangementFrame, bg="white")
    middle.rowconfigure(0, weight=1) #type: ignore

    middle.columnconfigure(0, weight=1)
    middle.grid(row=1, column=0, sticky="news")

    #header
    Label(top, text="เพิ่ม/แก้ไขข้อมูลการสั่งซื้อ", fg="black", bg="white", font="verdana 35 bold").grid(row=0, column=0, sticky='s')

    purchaseTree = ttk.Treeview(middle)
    purchaseTree.column("#0", width=0, stretch=NO)
    purchaseTree["columns"] = ("รหัสสั่งซื้อ","วันที่สั่งซื้อ", "ชื่อผู้สั่งซื้อ", "ชื่อผู้ค้าส่ง", "รายการสินค้า", "ปริมาณการสั่งซื้อ", "ราคาซื้อต่อหน่วย", "ค่าใช้จ่าย", "สถานะ")

    purchaseTree.column("รหัสสั่งซื้อ", width=90, anchor=CENTER)
    purchaseTree.column("วันที่สั่งซื้อ", width=90, anchor=CENTER)
    purchaseTree.column("ชื่อผู้สั่งซื้อ", width=90, anchor=CENTER)
    purchaseTree.column("ชื่อผู้ค้าส่ง", width=90, anchor=CENTER)
    purchaseTree.column("รายการสินค้า", width=90, anchor=E)
    purchaseTree.column("ปริมาณการสั่งซื้อ", width=90, anchor=E)
    purchaseTree.column("ราคาซื้อต่อหน่วย", width=90, anchor=E)
    purchaseTree.column("ค่าใช้จ่าย", width=90, anchor=CENTER)
    purchaseTree.column("สถานะ", width=90, anchor=CENTER)

    purchaseTree.heading("รหัสสั่งซื้อ", text="รหัสสั่งซื้อ")
    purchaseTree.heading("วันที่สั่งซื้อ", text="วันที่สั่งซื้อ")
    purchaseTree.heading("ชื่อผู้สั่งซื้อ", text="ชื่อผู้สั่งซื้อ")
    purchaseTree.heading("ชื่อผู้ค้าส่ง", text="ชื่อผู้ค้าส่ง")
    purchaseTree.heading("รายการสินค้า", text="รายการสินค้า")
    purchaseTree.heading("ปริมาณการสั่งซื้อ", text="ปริมาณการสั่งซื้อ")
    purchaseTree.heading("ราคาซื้อต่อหน่วย", text="ราคาซื้อต่อหน่วย")
    purchaseTree.heading("ค่าใช้จ่าย", text="ค่าใช้จ่าย")
    purchaseTree.heading("สถานะ", text="สถานะ")

    purchaseTree.grid(row=0, column=0)

    # Add Button
    Button(middle, text="สร้างรายการสั่งซื้อใหม่", fg="black", bg="green", borderless=1, command=addPurchaseClicked).grid(row=0, column=0, sticky='ne', padx=15, pady=170)

    # Modify Button
    Button(middle, text="แก้ไขคำสั่งซื้อ", fg="black", bg="yellow", borderless=1, command=modifyPurchaseClicked).grid(row=0, column=0, sticky='se', padx=160, pady=170)

    # Confirm Button
    Button(middle, text="ยืนยันคำสั่งซื้อ", fg="black", bg="green", borderless=1, command=confrimPurchaseClicked).grid(row=0, column=0, sticky='se', padx=280, pady=170)

    #Delete Button
    Button(middle, text="ลบ/ยกเลิกคำสั่งซื้อ", fg="black", bg="red", borderless=1, command=deletePurchaseClicked).grid(row=0, column=0, sticky='se', padx=15, pady=170)
    

    fetchPurchaseTree()


def fetchPurchaseTree():
    purchaseTree.delete(*purchaseTree.get_children())
    sql = "SELECT * FROM PurchaseOrderTable"
    cursor.execute(sql)
    res = cursor.fetchall()
    if res:
        for i in range(len(res)):
            status = "กำลังดำเนินการ"
            if res[i][8] == 1:
                status = "สมบูรณ์"
            purchaseTree.insert("",END, values=(res[i][0],res[i][1], res[i][2], res[i][3], res[i][4], res[i][5], res[i][6], res[i][7], status))


def deletePurchaseClicked():
    if purchaseTree.focus() == "":
        messagebox.showerror("Admin:", "กรุณาเลือกคำสั่งซื้อที่ต้องการจะลบหรือยกเลิก")
    elif purchaseTree.item(purchaseTree.focus(), "values")[8] == "สมบูรณ์":
        messagebox.showerror("Admin:", "รายการสั่งซื้อดำเนินการเสร็จสมบูรณ์แล้ว ไม่สามารถยกเลิก/ลบได้")
    else:
        msg = messagebox.askquestion("Delete", "ต้องการลบ/ยกเลิกคำสั่งซื้อนี้หรือไม่", icon="warning")
        if msg == "yes":
            selectedProd = purchaseTree.item(purchaseTree.focus(), "values")
            
            selectedProd_id = selectedProd[0]
            sql = '''DELETE FROM PurchaseOrderTable
                        WHERE orderID = ?'''
            cursor.execute(sql, [selectedProd_id])
            conn.commit()
            messagebox.showinfo("Admin:", "คำสั่งซื้อถูกลบ/ยกเลิกเรียบร้อยแล้ว")
            fetchPurchaseTree()


def getOrdererNames():
    returnlist = []
    sql = "SELECT name FROM LoginTable WHERE permission = 0"
    cursor.execute(sql)
    res = cursor.fetchall()
    if res:
        for i in range(len(res)):
            returnlist.append(res[i][0])
    return returnlist


def getSupplier():
    returnlist = []
    sql = "SELECT supplierName FROM SupplierContactTable"
    cursor.execute(sql)
    res = cursor.fetchall()
    if res:
        for i in range(len(res)):
            returnlist.append(res[i][0])
    return returnlist

def getProduct():
    sql = "SELECT * FROM WareHouseTable"
    cursor.execute(sql)
    res = cursor.fetchall()
    if res:
        return res
    

def getTotalCost(list):
    total = 0.00
    for i in range(len(list)):
        cost = float(list[i][2]) * float(list[i][3])
        total += cost
    return total


def addPurchaseClicked():
    def AddPurchaseOrder():
        if ordererNameCombo.get() == "":
            messagebox.showerror("Admin:", "กรุณาเลือกผู้สั่งซื้อ")
            ordererNameCombo.focus_force()
        elif supplierCombo.get() == "":
            messagebox.showerror("Admin:", "กรุณาเลือกผู้ค้าส่ง")
            supplierCombo.focus_force()
        elif infoTree.get_children() == ():
            messagebox.showerror("Admin:", "ไม่มีรายการสินค้าที่ต้องการจะสั่งซื้อ")
        else:
            sql = '''INSERT INTO PurchaseOrderTable (date, ordererName, supplierName, productList, quantities, costPerUnit, totalCost, status)
                     VALUES (?,?,?,?,?,?,?,?)'''
            date = "%d/%d/%d" %(daySpy.get(), monthSpy.get(), yearSpy.get())
            ordererName = ordererNameCombo.get()
            supplierName = supplierCombo.get()
            productList = ""
            quantities = ""
            costPerUnit = ""
            for i in range(len(orderProdlist)):
                if i == len(orderProdlist) - 1:
                    productList += orderProdlist[i][1]
                    quantities += orderProdlist[i][3]
                    costPerUnit += orderProdlist[i][2]
                else:
                    productList += orderProdlist[i][1] + "\n"
                    quantities += orderProdlist[i][3] + "\n"
                    costPerUnit += orderProdlist[i][2] + "\n"
            totalCost = getTotalCost(orderProdlist)
            status = 0
            cursor.execute(sql, [date, ordererName, supplierName, productList, quantities, costPerUnit, totalCost, status])
            conn.commit()
            fetchPurchaseTree()
            messagebox.showinfo("Admin:", "เพิ่มรายการสั่งซื้อดังกล่าวแล้ว")
            addPurchaseWindow.destroy()
        
    
    def fetchinfoTree():
        infoTree.delete(*infoTree.get_children())
        for i in range(len(orderProdlist)):
            infoTree.insert("",END, values=(orderProdlist[i][0],orderProdlist[i][1],orderProdlist[i][2],orderProdlist[i][3]))
    

    def updateTotalLabel():
        totalLabel["text"] = "ค่าใช้จ่าย %.2f บาท"  %getTotalCost(orderProdlist) 
        

    def addProductlist():
        def fetchWarehouseTree():
            alreadyAddedId = [int(orderProdlist[i][0]) for i in range(len(orderProdlist))]
            warehouseTree.delete(*warehouseTree.get_children())
            sql = "SELECT * FROM WareHouseTable"
            cursor.execute(sql)
            res = cursor.fetchall()
            if res:
                for i in range(len(res)):
                    if res[i][0] not in alreadyAddedId:
                        warehouseTree.insert("",END, values=(res[i][0],res[i][1], res[i][2], res[i][4]))
        
        
        def warehouseTreeclicked(event):
            selected_prod = warehouseTree.item(warehouseTree.focus(), "values")
            costEnt.delete(0, END)
            costEnt.insert(END, selected_prod[2])


        def addToProductListClicked():
            if warehouseTree.focus() == "":
                messagebox.showerror("Admin:", "เลือกสินค้าที่ต้องการเพิ่มลงในรายการสั่งซื้อ")
            elif costEnt.get() == "" or costEnt.get().replace('.', '',1).isnumeric() == False:
                messagebox.showerror("Admin:", "ราคาซื้อต่อหน่วยต้องเป็นจำนวนจริงเท่านั้น")
                costEnt.focus_force()
            elif orderQuantityEnt.get() == "" or orderQuantityEnt.get().isnumeric() == False:
                messagebox.showerror("Admin:", "ปริมาณสั่งซื้อต้องเป็นจำนวนเต็มบวกเท่านั้น")
                orderQuantityEnt.focus_force()
            else:
                selected_prod = warehouseTree.item(warehouseTree.focus(), "values")
                info = (selected_prod[0], selected_prod[1], costEnt.get(), orderQuantityEnt.get())
                info = tuple(info)
                orderProdlist.append(info)
                warehouseTree.delete(warehouseTree.focus())
                costEnt.delete(0, END)
                orderQuantityEnt.delete(0, END)
                updateTotalLabel()
                messagebox.showinfo("Admin:", "เพิ่มสินค้าดังกล่าวลงในรายการสั่งซื้อแล้ว")
        
        
        def confirmClicked():
            addProductlistWindow.destroy()
            fetchinfoTree()
        
        w = 600
        h = 500
        addProductlistWindow = Toplevel(root)
        addProductlistWindow.title("รายการสินค้า")
        addProductlistWindow.rowconfigure(0, weight=1)
        addProductlistWindow.columnconfigure(0, weight=1)
        x = root.winfo_screenwidth() / 2 - w / 2
        y = root.winfo_screenheight() / 2 - h / 2
        addProductlistWindow.geometry("%dx%d+%d+%d" %(w, h, x, y))
        
        addProductListFrame = Frame(addProductlistWindow, bg="white")
        addProductListFrame.columnconfigure(0, weight=1)
        addProductListFrame.rowconfigure((0,1), weight=1) # type: ignore
        addProductListFrame.grid(row=0, column=0, sticky="news")

        top = Frame(addProductListFrame, bg="white")
        top.rowconfigure((0,1), weight=1) # type: ignore
        top.columnconfigure((0,1), weight=1) # type: ignore
        top.grid(row=0, column=0, sticky="news")
        
        bot = Frame(addProductListFrame, bg="white")
        bot.rowconfigure((0,1), weight=1) # type: ignore
        bot.columnconfigure(0, weight=1)
        bot.grid(row=1, column=0, sticky="news")

        Label(top, text="ราคาซื้อต่อหน่วย:", fg="black", bg="white", font="verdana 25").grid(row=0, column=0, sticky='e')
        costEnt = Entry(top, width=20)
        costEnt.grid(row=0, column=1, sticky='w')

        Label(top, text="ปริมาณที่สั่งซื้อ:", fg="black", bg="white", font="verdana 25").grid(row=1, column=0, sticky='e')
        orderQuantityEnt = Entry(top, width=20)
        orderQuantityEnt.grid(row=1, column=1, sticky='w')

        warehouseTree = ttk.Treeview(bot)
        warehouseTree.column("#0", width=0, stretch=NO)
        warehouseTree["columns"] = ("รหัสสินค้า","ชื่อสินค้า", "ราคาต้นทุนต่อหน่วย", "ปริมาณคงเหลือ")

        warehouseTree.column("รหัสสินค้า", width=100, anchor=CENTER)
        warehouseTree.column("ชื่อสินค้า", width=100, anchor=CENTER)
        warehouseTree.column("ราคาต้นทุนต่อหน่วย", width=120, anchor=CENTER)
        warehouseTree.column("ปริมาณคงเหลือ", width=120, anchor=CENTER)

        warehouseTree.heading("รหัสสินค้า", text="รหัสสินค้า")
        warehouseTree.heading("ชื่อสินค้า", text="ชื่อสินค้า")
        warehouseTree.heading("ราคาต้นทุนต่อหน่วย", text="ราคาต้นทุนต่อหน่วย")
        warehouseTree.heading("ปริมาณคงเหลือ", text="ปริมาณคงเหลือ")
        warehouseTree.grid(row=0, column=0)

        warehouseTree.bind('<Double-1>', warehouseTreeclicked)

        fetchWarehouseTree()

        Button(bot, text="เพิ่มรายการสินค้า", fg="black", bg="green", borderless=1, command=addToProductListClicked).grid(row=1, column=0, sticky='e', padx=120)
        
        Button(bot, text="ยืนยัน", fg="black", bg="green", borderless=1, command=confirmClicked).grid(row=1, column=0, sticky='e', padx=20)


    orderProdlist = []

    w = 500
    h = 500
    addPurchaseWindow = Toplevel(root)
    addPurchaseWindow.title("สร้างรายการสั่งซื้อใหม่")
    addPurchaseWindow.rowconfigure(0, weight=1)
    addPurchaseWindow.columnconfigure(0, weight=1)
    x = root.winfo_screenwidth() / 2 - w / 2
    y = root.winfo_screenheight() / 2 - h / 2
    addPurchaseWindow.geometry("%dx%d+%d+%d" %(w, h, x, y))

    addPurchaseFrame = Frame(addPurchaseWindow, bg="white")
    addPurchaseFrame.rowconfigure((0,1,2,3,4,5,6), weight=1) #type: ignore
    addPurchaseFrame.columnconfigure((0,1), weight=1)  # type: ignore
    addPurchaseFrame.grid(row=0, column=0, sticky="news")

    names = getOrdererNames()
    suppliers = getSupplier()


    Label(addPurchaseFrame, text="วันที่สั่งซื้อ", fg="black", bg="white", font="verdana 25").grid(row=0, column=0, sticky='e')
    tmpFrame = Frame(addPurchaseFrame, bg="white")
    tmpFrame.rowconfigure(0, weight=1)
    tmpFrame.columnconfigure((0,1,2), weight=1) # type: ignore
    tmpFrame.grid(row=0, column=1, sticky="news")

    days = [x for x in range(1, 32)]
    months = [x for x in range(1, 13)]
    years = [x for x in range(2023, 2033)]

    daySpy = IntVar()
    daySpy.set(days[0])

    monthSpy = IntVar()
    monthSpy.set(months[0])

    yearSpy = IntVar()
    yearSpy.set(years[0])
    
    OptionMenu(tmpFrame, daySpy, *days).grid(row=0, column=0) #type: ignore
    OptionMenu(tmpFrame, monthSpy, *months).grid(row=0, column=1) #type: ignore
    OptionMenu(tmpFrame, yearSpy, *years).grid(row=0, column=2) #type: ignore



    Label(addPurchaseFrame, text="ผู้สั่งซื้อ:", fg="black", bg="white", font="verdana 25").grid(row=1, column=0, sticky='e')
    ordererNameCombo = ttk.Combobox(addPurchaseFrame, values=names, state="readonly")
    ordererNameCombo.grid(row=1, column=1, sticky='w')

    Label(addPurchaseFrame, text="ผู้ค้าส่ง:", fg="black", bg="white", font="verdana 25").grid(row=2, column=0, sticky='e')
    supplierCombo = ttk.Combobox(addPurchaseFrame, values=suppliers, state="readonly")
    supplierCombo.grid(row=2, column=1, sticky='w')

    Label(addPurchaseFrame, text="รายการสินค้า:", fg="black", bg="white", font="verdana 25").grid(row=3, column=0, sticky='e')
    Button(addPurchaseFrame, text="เลือกรายการสินค้า", fg="white", bg="gray", font="verdana 15", borderless=1, command=addProductlist).grid(row=3, column=1, sticky='w', padx=5)

    infoTree = ttk.Treeview(addPurchaseFrame)
    infoTree.column("#0", width=0, stretch=NO)
    infoTree["columns"] = ("รหัสสินค้า","ชื่อสินค้า", "ราคาซื้อต่อหน่วย", "ปริมาณสั่งซื้อ")

    infoTree.column("รหัสสินค้า", width=100, anchor=CENTER)
    infoTree.column("ชื่อสินค้า", width=100, anchor=CENTER)
    infoTree.column("ราคาซื้อต่อหน่วย", width=120, anchor=CENTER)
    infoTree.column("ปริมาณสั่งซื้อ", width=120, anchor=CENTER)

    infoTree.heading("รหัสสินค้า", text="รหัสสินค้า")
    infoTree.heading("ชื่อสินค้า", text="ชื่อสินค้า")
    infoTree.heading("ราคาซื้อต่อหน่วย", text="ราคาซื้อต่อหน่วย")
    infoTree.heading("ปริมาณสั่งซื้อ", text="ปริมาณสั่งซื้อ")
    infoTree.grid(row=4, columnspan=2)

    fetchinfoTree()
    totalCost = getTotalCost(orderProdlist)

    totalLabel = Label(addPurchaseFrame, text="ค่าใช้จ่าย: " + str(totalCost) + " บาท", fg="red", bg="white", font="verdana 20 bold")
    totalLabel.grid(row=5, columnspan=2)


    Button(addPurchaseFrame, text="เพิ่มรายการสั่งซื้อ", fg="black", bg="green", borderless=1, font="verdana 25 bold", command=AddPurchaseOrder).grid(row=6, columnspan=2)


def modifyPurchaseClicked():
    def ModifyPurchaseOrder():
        if infoTree.get_children() == ():
            messagebox.showerror("ไม่มีรายการสินค้า")
        else:
            sql = '''UPDATE PurchaseOrderTable
                    set date = ?, ordererName = ?, supplierName = ?, productList = ?, quantities = ?, costPerUnit = ?, totalCost = ?
                    WHERE orderID = ?'''
            date = "%d/%d/%d" %(daySpy.get(), monthSpy.get(), yearSpy.get())
            ordererName = ordererNameCombo.get()
            supplierName = supplierCombo.get()
            productList = ""
            quantitiesStr = ""
            costPerUnit = ""
            for i in range(len(productsName)):
                if i == len(productsName) - 1:
                    productList += productsName[i]
                    quantitiesStr += quantities[i]
                    costPerUnit += costs[i]
                else:
                    productList += productsName[i] + "\n"
                    quantitiesStr += quantities[i] + "\n"
                    costPerUnit += costs[i] + "\n"
            totalCost = getTotal()
            cursor.execute(sql, [date, ordererName, supplierName, productList, quantitiesStr, costPerUnit, totalCost, oldPurchase[0]])
            conn.commit()
            fetchPurchaseTree()
            messagebox.showinfo("Admin:", "แก้ไขรายการสั่งซื้อดังกล่าวแล้ว")
            modifyPurchaseWindow.destroy()
            
    def updateTotalLabel():
        totalLabel["text"] = "ค่าใช้จ่าย %.2f บาท"  %getTotal() 
    def addProductlist():
        def fetchWarehouseTree():
            alreadyAddedId = [int(getProductID(productsName[i])) for i in range(len(productsName))]
            warehouseTree.delete(*warehouseTree.get_children())
            sql = "SELECT * FROM WareHouseTable"
            cursor.execute(sql)
            res = cursor.fetchall()
            if res:
                for i in range(len(res)):
                    if res[i][0] not in alreadyAddedId:
                        warehouseTree.insert("",END, values=(res[i][0],res[i][1], res[i][2], res[i][4]))
        
        
        def warehouseTreeclicked(event):
            selected_prod = warehouseTree.item(warehouseTree.focus(), "values")
            costEnt.delete(0, END)
            costEnt.insert(END, selected_prod[2])


        def addToProductListClicked():
            if warehouseTree.focus() == "":
                messagebox.showerror("Admin:", "เลือกสินค้าที่ต้องการเพิ่มลงในรายการสั่งซื้อ")
            elif costEnt.get() == "" or costEnt.get().replace('.', '',1).isnumeric() == False:
                messagebox.showerror("Admin:", "ราคาซื้อต่อหน่วยต้องเป็นจำนวนจริงเท่านั้น")
                costEnt.focus_force()
            elif orderQuantityEnt.get() == "" or orderQuantityEnt.get().isnumeric() == False:
                messagebox.showerror("Admin:", "ปริมาณสั่งซื้อต้องเป็นจำนวนเต็มบวกเท่านั้น")
                orderQuantityEnt.focus_force()
            else:
                selected_prod = warehouseTree.item(warehouseTree.focus(), "values")
                productsName.append(selected_prod[1])
                costs.append(selected_prod[2])
                quantities.append(selected_prod[3])
                warehouseTree.delete(warehouseTree.focus())
                costEnt.delete(0, END)
                orderQuantityEnt.delete(0, END)
                updateTotalLabel()
                messagebox.showinfo("Admin:", "เพิ่มสินค้าดังกล่าวลงในรายการสั่งซื้อแล้ว")
        
        
        def confirmClicked():
            addProductlistWindow.destroy()
            fetchinfoTree()
        
        w = 600
        h = 500
        addProductlistWindow = Toplevel(root)
        addProductlistWindow.title("รายการสินค้า")
        addProductlistWindow.rowconfigure(0, weight=1)
        addProductlistWindow.columnconfigure(0, weight=1)
        x = root.winfo_screenwidth() / 2 - w / 2
        y = root.winfo_screenheight() / 2 - h / 2
        addProductlistWindow.geometry("%dx%d+%d+%d" %(w, h, x, y))
        
        addProductListFrame = Frame(addProductlistWindow, bg="white")
        addProductListFrame.columnconfigure(0, weight=1)
        addProductListFrame.rowconfigure((0,1), weight=1) # type: ignore
        addProductListFrame.grid(row=0, column=0, sticky="news")

        top = Frame(addProductListFrame, bg="white")
        top.rowconfigure((0,1), weight=1) # type: ignore
        top.columnconfigure((0,1), weight=1) # type: ignore
        top.grid(row=0, column=0, sticky="news")
        
        bot = Frame(addProductListFrame, bg="white")
        bot.rowconfigure((0,1), weight=1) # type: ignore
        bot.columnconfigure(0, weight=1)
        bot.grid(row=1, column=0, sticky="news")

        Label(top, text="ราคาซื้อต่อหน่วย:", fg="black", bg="white", font="verdana 25").grid(row=0, column=0, sticky='e')
        costEnt = Entry(top, width=20)
        costEnt.grid(row=0, column=1, sticky='w')

        Label(top, text="ปริมาณที่สั่งซื้อ:", fg="black", bg="white", font="verdana 25").grid(row=1, column=0, sticky='e')
        orderQuantityEnt = Entry(top, width=20)
        orderQuantityEnt.grid(row=1, column=1, sticky='w')

        warehouseTree = ttk.Treeview(bot)
        warehouseTree.column("#0", width=0, stretch=NO)
        warehouseTree["columns"] = ("รหัสสินค้า","ชื่อสินค้า", "ราคาต้นทุนต่อหน่วย", "ปริมาณคงเหลือ")

        warehouseTree.column("รหัสสินค้า", width=100, anchor=CENTER)
        warehouseTree.column("ชื่อสินค้า", width=100, anchor=CENTER)
        warehouseTree.column("ราคาต้นทุนต่อหน่วย", width=120, anchor=CENTER)
        warehouseTree.column("ปริมาณคงเหลือ", width=120, anchor=CENTER)

        warehouseTree.heading("รหัสสินค้า", text="รหัสสินค้า")
        warehouseTree.heading("ชื่อสินค้า", text="ชื่อสินค้า")
        warehouseTree.heading("ราคาต้นทุนต่อหน่วย", text="ราคาต้นทุนต่อหน่วย")
        warehouseTree.heading("ปริมาณคงเหลือ", text="ปริมาณคงเหลือ")
        warehouseTree.grid(row=0, column=0)

        warehouseTree.bind('<Double-1>', warehouseTreeclicked)

        fetchWarehouseTree()

        Button(bot, text="เพิ่มรายการสินค้า", fg="black", bg="green", borderless=1, command=addToProductListClicked).grid(row=1, column=0, sticky='e', padx=120)
        
        Button(bot, text="ยืนยัน", fg="black", bg="green", borderless=1, command=confirmClicked).grid(row=1, column=0, sticky='e', padx=20)


    def modifyProductlist():
        if infoTree.focus() == "":
            messagebox.showerror("Admin:", "กรุณาเลือกสินค้าที่ต้องการจะแก้ไข")
        else:
            def modifyProductListClicked():
                if costEnt.get() == "" or costEnt.get().replace('.', '',1).isnumeric() == False:
                    messagebox.showerror("Admin:", "ราคาซื้อต่อหน่วยต้องเป็นจำนวนจริงเท่านั้น")
                    costEnt.focus_force()
                elif orderQuantityEnt.get() == "" or orderQuantityEnt.get().isnumeric() == False:
                    messagebox.showerror("Admin:", "ปริมาณสั่งซื้อต้องเป็นจำนวนเต็มบวกเท่านั้น")
                    orderQuantityEnt.focus_force()
                else:
                    for i in range(len(productsName)):
                        if productsName[i] == selectedProd[1]:
                            costs[i] = costEnt.get()
                            quantities[i] = orderQuantityEnt.get()
                    fetchinfoTree()
                    modifyProductlistWindow.destroy()
                    updateTotalLabel()
            
            
            def deleteProductListClicked():
                for i in range(len(productsName)):
                    if productsName[i] == selectedProd[1]:
                        costs.pop(productsName.index(productsName[i]))
                        quantities.pop(productsName.index(productsName[i]))
                        productsName.remove(productsName[i])
                        break
                fetchinfoTree()
                modifyProductlistWindow.destroy()
                updateTotalLabel()


            w = 600
            h = 500
            selectedProd = infoTree.item(infoTree.focus(), "values")
            selectedcost = selectedProd[2]
            selectedquan = selectedProd[3]
            modifyProductlistWindow = Toplevel(root)
            modifyProductlistWindow.title("แก้ไขรายการสินค้า")
            modifyProductlistWindow.rowconfigure(0, weight=1)
            modifyProductlistWindow.columnconfigure(0, weight=1)
            x = root.winfo_screenwidth() / 2 - w / 2
            y = root.winfo_screenheight() / 2 - h / 2
            modifyProductlistWindow.geometry("%dx%d+%d+%d" %(w, h, x, y))
            
            modifyProductListFrame = Frame(modifyProductlistWindow, bg="white")
            modifyProductListFrame.columnconfigure((0,1), weight=1) # type: ignore
            modifyProductListFrame.rowconfigure((0,1,2), weight=1) # type: ignore
            modifyProductListFrame.grid(row=0, column=0, sticky="news")


            Label(modifyProductListFrame, text="ราคาซื้อต่อหน่วย:", fg="black", bg="white", font="verdana 25").grid(row=0, column=0, sticky='e')
            costEnt = Entry(modifyProductListFrame, width=20)
            costEnt.insert(END, selectedcost)
            costEnt.grid(row=0, column=1, sticky='w')

            Label(modifyProductListFrame, text="ปริมาณที่สั่งซื้อ:", fg="black", bg="white", font="verdana 25").grid(row=1, column=0, sticky='e')
            orderQuantityEnt = Entry(modifyProductListFrame, width=20)
            orderQuantityEnt.insert(END, selectedquan)
            orderQuantityEnt.grid(row=1, column=1, sticky='w')


            Button(modifyProductListFrame, text="แก้ไขรายการสินค้า", fg="black", bg="green", borderless=1, command=modifyProductListClicked).grid(row=2, columnspan=2, sticky='e', padx=120)
            
            Button(modifyProductListFrame, text="ลบสินค้า", fg="black", bg="green", borderless=1, command=deleteProductListClicked).grid(row=2, columnspan=2, sticky='e', padx=20)


    def fetchinfoTree():
        infoTree.delete(*infoTree.get_children())
        for i in range(len(productsName)):
            infoTree.insert("",END, values=(getProductID(productsName[i]),productsName[i],costs[i],quantities[i]))


    def getProductID(name):
        sql = "SELECT productID FROM WareHouseTable WHERE productName = ?"
        cursor.execute(sql, [name])
        res = cursor.fetchone()
        return res[0]
    
    def getTotal():
        total = 0.0
        for i in range(len(quantities)):
            total += float(quantities[i]) * float(costs[i])
        return total

    if purchaseTree.focus() == "":
        messagebox.showerror("Admin:", "กรุณาเลือกคำสั่งซื้อที่ต้องการจะแก้ไข")
    elif purchaseTree.item(purchaseTree.focus(), "values")[8] == "สมบูรณ์":
        messagebox.showerror("Admin:", "รายการสั่งซื้อดำเนินการเสร็จสมบูรณ์แล้ว ไม่สามารถแก้ไขได้")
    else:
        oldPurchase = purchaseTree.item(purchaseTree.focus(), "values")
        date = oldPurchase[1].split("/")
        productsName = oldPurchase[4].split("\n")
        quantities = oldPurchase[5].split("\n")
        costs = oldPurchase[6].split("\n")
        totalCost = oldPurchase[7]

        w = 500
        h = 500
        modifyPurchaseWindow = Toplevel(root)
        modifyPurchaseWindow.title("แก้ไขรายการสั่งซื้อ")
        modifyPurchaseWindow.rowconfigure(0, weight=1)
        modifyPurchaseWindow.columnconfigure(0, weight=1)
        x = root.winfo_screenwidth() / 2 - w / 2
        y = root.winfo_screenheight() / 2 - h / 2
        modifyPurchaseWindow.geometry("%dx%d+%d+%d" %(w, h, x, y))

        modifyPurchaseFrame = Frame(modifyPurchaseWindow, bg="white")
        modifyPurchaseFrame.rowconfigure((0,1,2,3,4,5,6), weight=1) #type: ignore
        modifyPurchaseFrame.columnconfigure((0,1), weight=1)  # type: ignore
        modifyPurchaseFrame.grid(row=0, column=0, sticky="news")

        names = getOrdererNames()
        suppliers = getSupplier()


        Label(modifyPurchaseFrame, text="วันที่สั่งซื้อ", fg="black", bg="white", font="verdana 25").grid(row=0, column=0, sticky='e')
        tmpFrame = Frame(modifyPurchaseFrame, bg="white")
        tmpFrame.rowconfigure(0, weight=1)
        tmpFrame.columnconfigure((0,1,2), weight=1) # type: ignore
        tmpFrame.grid(row=0, column=1, sticky="news")

        days = [x for x in range(1, 32)]
        months = [x for x in range(1, 13)]
        years = [x for x in range(2023, 2033)]

        daySpy = IntVar()
        daySpy.set(int(date[0]))

        monthSpy = IntVar()
        monthSpy.set(int(date[1]))

        yearSpy = IntVar()
        yearSpy.set(int(date[2]))
        
        OptionMenu(tmpFrame, daySpy, *days).grid(row=0, column=0) #type: ignore
        OptionMenu(tmpFrame, monthSpy, *months).grid(row=0, column=1) #type: ignore
        OptionMenu(tmpFrame, yearSpy, *years).grid(row=0, column=2) #type: ignore

        Label(modifyPurchaseFrame, text="ผู้สั่งซื้อ:", fg="black", bg="white", font="verdana 25").grid(row=1, column=0, sticky='e')
        ordererNameCombo = ttk.Combobox(modifyPurchaseFrame, values=names, state="readonly")
        ordererNameCombo.current(names.index(oldPurchase[2]))
        ordererNameCombo.grid(row=1, column=1, sticky='w')

        Label(modifyPurchaseFrame, text="ผู้ค้าส่ง:", fg="black", bg="white", font="verdana 25").grid(row=2, column=0, sticky='e')
        supplierCombo = ttk.Combobox(modifyPurchaseFrame, values=suppliers, state="readonly")
        supplierCombo.current(suppliers.index(oldPurchase[3]))
        supplierCombo.grid(row=2, column=1, sticky='w')

        Label(modifyPurchaseFrame, text="รายการสินค้า:", fg="black", bg="white", font="verdana 25").grid(row=3, column=0, sticky='e')
        Button(modifyPurchaseFrame, text="เพิ่มรายการสินค้า", fg="white", bg="gray", font="verdana 15", borderless=1, command=addProductlist).grid(row=3, column=1, sticky='w', padx=5)
        Button(modifyPurchaseFrame, text="แก้ไขสินค้า", fg="white", bg="gray", font="verdana 15", borderless=1, command=modifyProductlist).grid(row=3, column=1, sticky='e', padx=10)


        infoTree = ttk.Treeview(modifyPurchaseFrame)
        infoTree.column("#0", width=0, stretch=NO)
        infoTree["columns"] = ("รหัสสินค้า","ชื่อสินค้า", "ราคาซื้อต่อหน่วย", "ปริมาณสั่งซื้อ")

        infoTree.column("รหัสสินค้า", width=100, anchor=CENTER)
        infoTree.column("ชื่อสินค้า", width=100, anchor=CENTER)
        infoTree.column("ราคาซื้อต่อหน่วย", width=120, anchor=CENTER)
        infoTree.column("ปริมาณสั่งซื้อ", width=120, anchor=CENTER)

        infoTree.heading("รหัสสินค้า", text="รหัสสินค้า")
        infoTree.heading("ชื่อสินค้า", text="ชื่อสินค้า")
        infoTree.heading("ราคาซื้อต่อหน่วย", text="ราคาซื้อต่อหน่วย")
        infoTree.heading("ปริมาณสั่งซื้อ", text="ปริมาณสั่งซื้อ")
        infoTree.grid(row=4, columnspan=2)

        fetchinfoTree()
        totalCost = getTotal()

        totalLabel = Label(modifyPurchaseFrame, text="ค่าใช้จ่าย: " + str(totalCost) + " บาท", fg="red", bg="white", font="verdana 20 bold")
        totalLabel.grid(row=5, columnspan=2)


        Button(modifyPurchaseFrame, text="แก้ไขรายการสั่งซื้อ", fg="black", bg="green", borderless=1, font="verdana 25 bold", command=ModifyPurchaseOrder).grid(row=6, columnspan=2)



def confrimPurchaseClicked():
    if purchaseTree.focus() == "":
        messagebox.showerror("Admin:", "กรุณาเลือกคำสั่งซื้อที่ต้องการจะยืนยัน")
    elif purchaseTree.item(purchaseTree.focus(), "values")[8] == "สมบูรณ์":
        messagebox.showerror("Admin:", "รายการสั่งซื้อดำเนินการเสร็จสมบูรณ์แล้ว")
    else:
        msg = messagebox.askquestion("Confirm", "ต้องการยืนยันคำสั่งซื้อนี้หรือไม่", icon="warning")
        if msg == "yes":
            selectedProd = purchaseTree.item(purchaseTree.focus(), "values")
            selectedProd_id = selectedProd[0]
            sql = "UPDATE PurchaseOrderTable SET status = 1 WHERE orderID = ?"
            cursor.execute(sql, [selectedProd_id])
            conn.commit()
            fetchPurchaseTree()

            today = date.today()
            d = today.strftime("%d/%m/%y")
            prodNames = selectedProd[4].split("\n")
            prodQuan = selectedProd[5].split("\n")
            prodCost = selectedProd[6].split("\n")
            for i in range(len(prodNames)):
                sql = "SELECT quantity FROM WareHouseTable WHERE productName = ?"
                cursor.execute(sql, [prodNames[i]])
                originalQuan = cursor.fetchone()
                originalQuan = originalQuan[0]
                sql = "UPDATE WareHouseTable SET cost = ?, quantity = ?, date = ? WHERE productName = ?"
                cursor.execute(sql, [prodCost[i], int(prodQuan[i]) + originalQuan, d, prodNames[i]])
                conn.commit()
            messagebox.showinfo("Admin:", "รายการสั่งซื้อได้รับการยืนยันแล้ว รายการสินค้าจะถูกเพิ่มเข้าคลังอัตโนมัติ")

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