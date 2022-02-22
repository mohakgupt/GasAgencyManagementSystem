import mysql.connector

# agency authentication details
# enter to log in by the agency manager
username="laxmiagency"
password="ABcd12%#"

print(
'''
                        +============================================================+
                        |  $$\   $$\ $$$$$$$\         $$$$$$\   $$$$$$\   $$$$$$\    |
			|  $$ |  $$ |$$  __$$\       $$  __$$\ $$  __$$\ $$  __$$\   |
			|  $$ |  $$ |$$ |  $$ |      $$ /  \__|$$ /  $$ |$$ /  \__|  |
			|  $$$$$$$$ |$$$$$$$  |      $$ |$$$$\ $$$$$$$$ |\$$$$$$\    |
			|  $$  __$$ |$$  ____/       $$ |\_$$ |$$  __$$ | \____$$\   |
			|  $$ |  $$ |$$ |            $$ |  $$ |$$ |  $$ |$$\   $$ |  |
			|  $$ |  $$ |$$ |            \$$$$$$  |$$ |  $$ |\$$$$$$  |  |
			|  \__|  \__|\__|             \______/ \__|  \__| \______/   |
			|                                                            |
			|                 "WELCOME TO OUR AGENCY"                    |
			*============================================================*                                                        
              
''')

pwd=input("Enter MYSQL Server password: ")
db=mysql.connector.connect(
    host='localhost',
    user='root',
    password=pwd)
c=db.cursor()

try:
    c.execute("create database HP_GAS_DB")
    print("			[Maximize this window for best experience]")
except:
    pass
c.execute("use HP_GAS_DB")

try:
    c.execute("create table CUSTOMER\
        (Customer_ID integer, \
        Name char(20), \
        Type char(1), \
        Connection_Date date, \
        Address char(50), \
        Pin_Code char(6), \
        Phone_No char(10))")
except:
    pass

try:
    c.execute("create table STOCK\
        (SNo integer, \
        Commercial integer, \
        Domestic integer)")
    c.execute("insert into stock values(1,5650,12630)")
except:
    pass

try:
    c.execute("create table DELIVERY\
        (Customer_ID integer, \
        Date_Booked date, \
        Date_delivered date,\
        Type char(1))")
except:
    pass


try:
    c.execute("create table REQUEST\
        (Customer_ID integer, \
        Date_Booked date, \
        Type char(1))")
except:
    pass

try:
    c.execute("create table PRICE(\
        Type char(1), \
        Price integer)")
    c.execute("insert into PRICE values('C',1200)")
    c.execute("insert into PRICE values('D',650)")
except:
    pass


# functions to get list of all tables at any instant
def cust_list():
    c.execute("select * from customer")
    return c.fetchall()
def stock_list():
    c.execute("select * from stock")
    return c.fetchall()
def deli_list():
    c.execute("select * from delivery")
    return c.fetchall()
def req_list():
    c.execute("select * from request")
    return c.fetchall()
def price_list():
    c.execute("select * from price")
    return c.fetchall()

# function to add a new customer
def add(table,fields,values):
    v=''
    while True:
        for title in fields:
            if title=='Connection_Date':
                print("\nEnter date in yyyy-mm-dd format")
            while v=='':
                v=input('\nEnter ' + title + ': ')
                if title in ("Pin_Code","Phone_No"):
                    if not v.isnumeric():
                        v=''
            else:
                values.append(v)
                v=''
        try:
            c.execute("insert into " + table + " values" + str(tuple(values)))
            db.commit()
            print("SUCCESSFULLY ADDED DATA")
            break
        except:
            print('Error: One or more values passed are incorrect !')
            values=[values[0]]

# function to update data in a field of a table
def update(table,field,id):
    v=''
    while True:
        try:
            if field=='Connection_Date':
                print("Enter date in yyyy-mm-dd format")
            v=input('\nEnter ' + field + ': ')
            if field in ("Name","Type","Address"):
                v="'"+v+"'"
            c.execute("update "+table+" set "+field+"="+v+" where Customer_ID="+id)
            db.commit()
            break
        except:
            print("Invalid value !")

# MAIN PROGRAM LOOP

# MAIN MENU
while True:
    print('''
---------------------------- MENU ----------------------------
0. EXIT
1. CUSTOMER
2. AGENCY
3. ABOUT US''')
    choice=int(input("\nEnter your choice: "))
    
    # CUSTOMER===============================================================
    if choice==1:
        while True:

            # BEFORE LOGIN
            logged=False
            print('''
0. <-- BACK
1. Login
2. Create New Account''')
            cchoice=int(input("Enter your choice: "))

            # 1. LOGIN FOR CUSTOMER
            if cchoice==1:
                print('---------------------------- LOGIN ----------------------------')
                nameinput=int(input('\nEnter Customer ID: '))
                for rec in cust_list():
                    if rec[0]==nameinput:
                        cust=rec
                        cust_id=str(rec[0])
                        logged=True
                        break
                else:
                    print('NO DATA FOUND')

            # 2. CREATE NEW ACC
            if cchoice==2:
                print('--------------- CREATE NEW ACCOUNT ---------------')
                add('customer',('Name','Type','Connection_Date','Address','Pin_Code','Phone_No'),[len(cust_list())+1])
                cust=cust_list()[len(cust_list())-1]
                cust_id=str(cust[0])
                logged=True
            
            # 3. EXIT
            if cchoice==0:
                break

            
            # AFTER LOGIN
            if logged==True:
                print("\n------------------- LOGGED IN --------------------\n")
                print("\nYour Account Details:")
                print("Customer_ID:\t",cust[0])
                print("Name:\t\t",cust[1])
                print("Type:\t\t",cust[2])
                print("Connection_Date:",cust[3])
                print("Address:\t",cust[4])
                print("Pin_Code:\t",cust[5])
                print("Phone_No:\t",cust[6],"\n\n")
                while True:
                    print('''
0. <-- BACK
1. Edit Account
2. Book Cylinder
3. Get Delivery Receipt
4. Check Purchase History''')
                    cchoice=int(input("Enter your choice: "))

                    # EDIT ACCOUNT
                    if cchoice==1:
                        print('\n----------------- EDIT ACCOUNT -----------------')
                        print("\nNote: Please type correct field name from above list.")
                        while True:
                            field=input("\nWhich field to update: ")
                            try:
                                update('customer',field,cust_id)
                            except:
                                print("Invalid field name typed")
                            ans=input("\nEdit more fields? (Y/N): ")
                            if ans=='N':
                                break
                        cust=cust_list()[cust[0]-1]
                        print("\nUpdated profile:")
                        print("Customer_ID:\t",cust[0])
                        print("Name:\t\t",cust[1])
                        print("Type:\t\t",cust[2])
                        print("Connection_Date:",cust[3])
                        print("Address:\t",cust[4])
                        print("Pin_Code:\t",cust[5])
                        print("Phone_No:\t",cust[6],"\n\n")

                    # BOOK CYLINDER
                    if cchoice==2:
                        print('\n--------------- BOOK CYLINDER ---------------')
                        add('request',('Date_Booked','Type'),[cust_id])
                        if req_list()[-1][2]=="C":
                            amt=price_list()[0][1]
                        elif req_list()[-1][2]=="D":
                            amt=price_list()[1][1]
                        print("Your request for 1 cylinder has been registered")
                        print("\nTOTAL CHARGES: ",amt)

                    # GET DELIVERY RECEIPT
                    if cchoice==3:
                        print('\n--------------- GET DELIVERY RECEIPT ---------------')
                        b=input("Date of booking (yyyy-mm-dd): ")
                        d=input("Type: ")
                        e=input("Enter date of delivery (yyyy-mm-dd): ")
                        count=0
                        for rec in req_list():
                            if rec[0]==int(cust_id) and str(rec[1])==b and rec[2]==d:
                                tup=(cust_id,b,e,d)
                                c.execute("insert into delivery values" + str(tup))
                                db.commit()
                                count+=1
                            else:
                                pass
                        if count==0:
                            print("NO SUCH DELIVERY REQUEST WAS FOUND !")
                        if count!=0:
                            print("+====================== DELIVERY RECEIPT =====================+")
                            print("\n\tCustomer ID:",cust[0])
                            print("\n\tName:",cust[1])
                            print("\n\tType:",cust[2])
                            print("\n\tDate Booked:")
                            for rec in deli_list():
                                if rec[0]==int(cust_id) and str(rec[1])==b:
                                    print('\t',rec[1])
                            print("\n\tDate Delivered:")
                            for rec in deli_list():
                                if rec[0]==int(cust_id) and str(rec[2])==e:
                                    print('\t',rec[2])
                            if cust[2]=="C":
                                amt=price_list()[0][1] * count
                            elif cust[2]=="D":
                                amt=price_list()[1][1] * count
                            print("\n\tAMOUNT PAID: ",amt)
                            print("\n\t\tTHANK YOU,  WE HOPE TO SEE YOU AGAIN!")



                    # CHECK PURCHASE HISTORY
                    if cchoice==4:
                        print('\n--------------- PURCHASE HISTORY ---------------')
                        print("Date_Booked\tDate_Delivered\tType")
                        for rec in deli_list():
                            if rec[0]==int(cust_id):
                                print(rec[1],"\t",rec[2],"\t",rec[3],"\t")

                    if cchoice==0:
                        break


    # AGENCY=======================================================
    if choice==2:
        logged=False   # variable to check login status
        # LOGIN
        print('------------------ LOGIN ------------------')
        while logged==False:
            a=input("\nUsername:\t")
            b=input("\nPassword:\t")
            if a==username and b==password:
                print("LOGGED IN")
                logged=True
            else:
                print("Invalid credentials !")
        
        while True:
            print('''
0. <-- BACK
1. View/Update Price
2. Add Stock Record
3. Stock Report
4. Customer Report
5. Request Report
6. Delivery Report''')
            achoice=int(input("Enter your choice: "))
        
            # VIEW/UPDATE PRICE
            if achoice==1:
                print('\n--------------- STOCK PRICES ---------------')
                print("\nCurrent Price:")
                print("Type\tPrice")
                for rec in price_list():
                    print(rec[0],"\t",rec[1])
                print("\n1. Update\n2. Exit")
                choice2=int(input("Enter your choice: "))
                if choice2==1:
                    cp=input("Enter Commercial price (CP): ")
                    dp=input("Enter Domestic Price (DP): ")
                    c.execute("update price set price="+cp+" where Type='C'")
                    c.execute("update price set price="+dp+" where Type='D'")
                    db.commit()
                    print("Price updated successfully")
            

            # ADD STOCK RECORD
            if achoice==2:
                print('\n--------------- ADD STOCK RECORD ---------------')
                cp=''
                dp=''
                while cp=='':
                    cp=input("Enter commercial stock amount: ")
                while dp=='':
                    dp=input("Enter domestic stock amount: ")
                stockno=str(len(stock_list())+1)
                c.execute("insert into stock values(" + stockno + "," + cp+ "," + dp + ")")
                db.commit()
                print("Stock updated successfully")

            # STOCK REPORT
            if achoice==3:
                print('\n--------------- VIEW STOCK REPORT ---------------')
                print("\n\t\tSTOCK REPORT")
                print("S No\tCommercial\tDomestic")
                ctotal=0
                dtotal=0
                for rec in stock_list():
                    print(rec[0],"\t",rec[1],"\t\t",rec[2])
                    ctotal+=rec[1]
                    dtotal+=rec[2]
                print("\nTotal\t",ctotal,"\t\t",dtotal)
            
            # CUSTOMER REPORT
            if achoice==4:
                print('\n--------------- VIEW CUSTOMER REPORT ---------------')
                print("\n\t\t\tCUSTOMER REPORT")
                print("Customer ID\tName\t\tType\tConnection Date\t\tAddress\t\tPincode     Phone No.")
                for rec in cust_list():
                    print(rec[0],"\t     ",rec[1],"\t\t",rec[2],"\t",rec[3],"\t      ",rec[4],"\t",rec[5],"     ",rec[6])
            
            # REQUEST REPORT
            if achoice==5:
                print('\n--------------- VIEW REQUEST REPORT ---------------')
                print("\n\t\tREQUEST REPORT")
                print("Customer ID\tName\t\tDate Booked\tType")
                for rec in req_list():
                    print(rec[0],"\t\t",cust_list()[rec[0]-1][1],"\t",rec[1],"\t",rec[2])
            
            # DELIVERY REPORT
            if achoice==6:
                print('\n--------------- VIEW DELIVERY REPORT ---------------')
                print("\n\t\tDELIVERY REPORT")
                print ("Customer ID\tDate Booked\tDate Delivered\tType")
                for rec in deli_list():
                    print(rec[0],"\t\t",rec[1],"\t",rec[2],"\t",rec[3])

            # EXIT
            if achoice==0:
                break
    

    # ABOUT US ==========================
    if choice==3:
        print('''
                    <-- ENTER KEY to go back

                    +================== ABOUT THE DEVELOPERS ================+
                    |                                                        |
                    |                Hindustan Petroleum Gas                 |
                    |                Management Application                  |
                    |                                                        |
                    |     Developed by :-                                    |
                    |     > MOHAK GUPTA                                      |
                    |     > PRAKHAR SHUKLA                                   |
                    |     > OM DEV YADAV                                     |
                    |                                                        |
                    |     Who are the students of:-                          |
                    |     > Class : XII-A                                    |
                    |     > School: Assisi Convent School Etah               |
                    |                                                        |
                    ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++''')
        input()


    # EXIT===============================================
    if choice==0:
        print("Quitting program !")
        db.close()
        break
