import sqlite3
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
# from tkmacosx import Button


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

    # loginBtn = Button(bot, text="เข้าสู่ระบบ", fg="white", bg="gray", borderless=1, command=loginclicked)
    loginBtn = Button(bot, text="เข้าสู่ระบบ", fg="white", bg="gray", border=1, command=MainPage)
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
    global infoFrame
    mainpageFrame = Frame(root, bg="black")
    mainpageFrame.rowconfigure(0, weight=1)
    mainpageFrame.columnconfigure(0, weight=1)
    mainpageFrame.columnconfigure(1, weight=3)
    mainpageFrame.grid(row=0,rowspan=3, column=0, columnspan=3, sticky="news")

    menuFrame = Frame(mainpageFrame, bg="white")
    menuFrame.columnconfigure((0,1), weight=1) # type: ignore
    menuFrame.rowconfigure((0,1,2,3,4,5,6,7,8,9), weight=1) # type: ignore
    menuFrame.grid(row=0, column=0, sticky="news")

    infoFrame = Frame(mainpageFrame, bg="green")
    infoFrame.rowconfigure(0, weight=1)
    infoFrame.columnconfigure(0, weight=1)
    infoFrame.grid(row=0, column=1, sticky="news")

    # ค้นหาสินค้า
    productSearchBtn = Button(menuFrame, text="ค้นหาสินค้า", fg="black", bg="white", command=productsearchClicked)
    productSearchBtn.grid(row=3, column=0, columnspan=2, sticky="news")
    # ตรวจสอบข้อมูล
    intelInvestigateBtn = Button(menuFrame, text="ตรวจสอบข้อมูลการสั่งซื้อ", fg="black", bg="white", command=intelinvestigateClicked)
    intelInvestigateBtn.grid(row=4, column=0, columnspan=2, sticky="news")
    # บันทึกข้อมูลจัดส่ง
    saveIntelBtn = Button(menuFrame, text="บันทึกข้อมูลการจัดส่ง", fg="black", bg="white", command=saveintelClicked)
    saveIntelBtn.grid(row=5, column=0, columnspan=2, sticky="news")
    # จัดพิมพ์รายงานเเสดงผลการดำเนินงาน
    printReportBtn = Button(menuFrame, text="ค้นหาสินค้า", fg="black", bg="white", command=printreportClicked)
    printReportBtn.grid(row=6, column=0, columnspan=2, sticky="news")
    # Logout Button
    Button(menuFrame, text="Log out", bg="white", fg="black", border=1, command=mainpageFrame.destroy).grid(row=9, column=0)
    # Exit Button
    Button(menuFrame, text="Exit", bg="red", fg="black", border=1, command=exit).grid(row=9, column=1)


def productsearchClicked() :
    global prodSearchFrame, searchBar
    clearInfoFrame()
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
    clearInfoFrame()
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
    clearInfoFrame()
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
    clearInfoFrame()
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


def clearInfoFrame() :
    for child in infoFrame.winfo_children() :
        child.destroy()


def printClicked() :
    return


w = 1024
h = 720

root = CreateWindowsFrame()
ConnectToDatabase()

# Login Spies
usernameSpy = StringVar()
pwdSpy = StringVar()

LoginPage()
root.mainloop()
