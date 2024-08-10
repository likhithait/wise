from tkinter import *
from tkinter import messagebox
import sqlite3
import random, os, tempfile,smtplib

def clear():
    bathsoapEntry.delete(0,END)
    facecreamEntry.delete(0,END)
    facewashEntry.delete(0,END)
    hairsprayEntry.delete(0,END)
    hairgelEntry.delete(0,END)
    bodylotionEntry.delete(0,END)

    riceEntry.delete(0,END) 
    oilEntry.delete(0,END) 
    daalEntry.delete(0,END) 
    wheatEntry.delete(0,END) 
    sugarEntry.delete(0,END) 
    teaEntry.delete(0,END)

    maazaEntry.delete(0,END)
    pepsiEntry.delete(0,END)
    spriteEntry.delete(0,END)
    dewEntry.delete(0,END) 
    frootiEntry.delete(0,END)
    cococolaEntry.delete(0,END)



    bathsoapEntry.insert(0,0)
    facecreamEntry.insert(0,0)
    facewashEntry.insert(0,0)
    hairsprayEntry.insert(0,0)
    hairgelEntry.insert(0,0)
    bodylotionEntry.insert(0,0)


    riceEntry.insert(0,0) 
    oilEntry.insert(0,0) 
    daalEntry.insert(0,0) 
    wheatEntry.insert(0,0) 
    sugarEntry.insert(0,0) 
    teaEntry.insert(0,0)


    maazaEntry.insert(0,0)
    pepsiEntry.insert(0,0)
    spriteEntry.insert(0,0)
    dewEntry.insert(0,0) 
    frootiEntry.insert(0,0)
    cococolaEntry.insert(0,0)

    cosmetictaxEntry.delete(0, END)
    grocerytaxEntry.delete(0, END)
    drinktaxEntry.delete(0,END)


    cosmeticpriceEntry.delete(0, END)
    grocerypriceEntry.delete(0, END)
    drinkpriceEntry.delete(0, END)


    nameEntry.delete(0,END)
    phoneEntry.delete(0,END)
    BillnumberEntry.delete(0,END)

    textarea.delete(1.0,END)


def send_email():
    def send_gmail():
        try:
            ob=smtplib.SMTP('smtp.gmail.com',587)
            ob.starttls()
            ob.login(senderEntry.get(), passwordEntry.get())
            message=email_textarea.get(1.0,END)
            ob.sendmail(senderEntry.get(),receiverEntry.get(),message)
            ob.quit()
            messagebox.showinfo('Success','Bill is successfully sent',parent=root1)
            root1.destroy()
        except:
            messagebox.showerror('Error','Something went wrong',parent=root1)


    if textarea.get(1.0, END) == '\n':
        messagebox.showerror('Error', 'Bill is empty')
    else:
        root1 = Toplevel()
        root1.grab_set()
        root1.title('send gmail')
        root1.config(bg='gray20')
        root1.resizable(0, 0)

        senderFrame = LabelFrame(root1, text='SENDER', font=('arial', 16, 'bold'), bd=6, bg='gray20', fg='white')
        senderFrame.grid(row=0, column=0, padx=40, pady=20)

        senderLabel = Label(senderFrame, text="Senders email", font=('arial', 16, 'bold'), bg='gray20', fg='white')
        senderLabel.grid(row=0, column=0, padx=10, pady=8)

        senderEntry = Entry(senderFrame, font=('arial', 16, 'bold'), bd=2, width=23, relief=RIDGE)
        senderEntry.grid(row=0, column=1, padx=10, pady=8)

        passwordLabel = Label(senderFrame, text="password", font=('arial', 16, 'bold'), bg='gray20', fg='white')
        passwordLabel.grid(row=1, column=0, padx=10, pady=8)

        passwordEntry = Entry(senderFrame, font=('arial', 14, 'bold'), bd=2, width=23, relief=RIDGE,show='*')
        passwordEntry.grid(row=1, column=1, padx=10, pady=8)

        recipientFrame = LabelFrame(root1, text='RECIPIENT', font=('arial', 16, 'bold'), bd=6, bg='gray20', fg='white')
        recipientFrame.grid(row=1, column=0, padx=40, pady=20)

        receiverLabel = Label(recipientFrame, text="Email address", font=('arial', 14, 'bold'), bg='gray20', fg='white')
        receiverLabel.grid(row=0, column=0, padx=10, pady=8)

        receiverEntry = Entry(recipientFrame, font=('arial', 14, 'bold'), bd=2, width=23, relief=RIDGE)
        receiverEntry.grid(row=0, column=1, padx=10, pady=8)

        messageLabel = Label(recipientFrame, text="Message", font=('arial', 14, 'bold'), bg='gray20', fg='white')
        messageLabel.grid(row=1, column=0, padx=10, pady=8)

        email_textarea = Text(recipientFrame, font=('arial', 14, 'bold'), bd=2, relief=SUNKEN, width=42, height=11)
        email_textarea.grid(row=2, column=0, columnspan=2)
        email_textarea.delete(1.0, END)
        email_textarea.insert(END, textarea.get(1.0, END).replace('=','').replace('-','').replace('\t\t\t','\t\t'))

        sendButton = Button(root1, text='SEND', font=('arial', 16, 'bold'),width=15,command=send_gmail)
        sendButton.grid(row=2, column=0, pady=20)

        root1.mainloop()

def print_bill(user_name, phone_number, bill_number):
    if textarea.get(1.0, END) == '\n':
        messagebox.showerror('Error', 'Bill is empty')
    else:
        # Generate a temporary text file
        file = tempfile.mktemp('.txt')
        file_content = textarea.get(1.0, END)

        # content to the text file
        with open(file, 'w') as f:
            f.write(file_content)

        # Connecting to the SQLite database
        conn = sqlite3.connect('example.db')
        c = conn.cursor()

        # Create a table to store user information and bills if it doesn't exist
        c.execute('''CREATE TABLE IF NOT EXISTS UserBills
                     (bill_number INTEGER PRIMARY KEY,
                     user_name TEXT,
                     phone_number TEXT,
                     file_content TEXT)''')

        # Insert user information and bill content into the database
        c.execute("INSERT INTO UserBills (bill_number, user_name, phone_number, file_content) VALUES (?, ?, ?, ?)",
                  (bill_number, user_name, phone_number, file_content))

        # Commit changes
        conn.commit()

        # Close the connection
        conn.close()

        
        os.startfile(file, 'print')

def search_bill():
    for i in os.listdir('bills/'):
        if i.split('.')[0]==BillnumberEntry.get():
            f=open(f'bills/{i}','r')
            textarea.delete(1.0,END)
            for data in f:
                textarea.insert(END,data)
            f.close()
            break
    
    else:
        messagebox.showerror('Error','Invalid Bill Number')



if not os.path.exists('bills'):
    os.mkdir('bills')




def bill_content(bill_content_text, bill_number): 
    file_path = f'bills/{bill_number}.txt'
    with open(file_path, 'w') as file:
        file.write(bill_content_text)
    messagebox.showinfo('Success', f'Bill {bill_number} is saved successfully')
    return file_path

def save_bill(bill_content_text, bill_number, user_name, phone_number):

    # Connect to the SQLite database
    conn = sqlite3.connect('customer_details.db')
    c = conn.cursor()

    # Create a table to store user information and bills if it doesn't exist
    c.execute('''CREATE TABLE IF NOT EXISTS UserBills
                 (bill_number INTEGER PRIMARY KEY,
                 user_name TEXT,
                 phone_number TEXT,
                 file_content TEXT)''')

    # Insert user information and bill content into the database
    c.execute("INSERT INTO UserBills (bill_number, user_name, phone_number, file_content) VALUES (?, ?, ?, ?)",
              (bill_number, user_name, phone_number, bill_content_text))

    # Commit changes
    conn.commit()

    # Close the connection
    conn.close()


def bill_area():
    if nameEntry.get() == '' or phoneEntry.get() == '':
        messagebox.showerror('Error','Customer Details are required')
    elif cosmeticpriceEntry.get() == '' and grocerypriceEntry.get() == '' and drinkpriceEntry.get() == '':
        messagebox.showerror('Error', 'No Products are selected')
    elif cosmeticpriceEntry.get() == '0 Rs' and grocerypriceEntry.get() == '0 Rs' and drinkpriceEntry.get() == '0 Rs': 
        messagebox.showerror('Error', 'No Products are selected')
    else:
        if textarea.get("1.0", "end-1c") == "":
            messagebox.showerror("Error", "No items to bill.")
            return

        # Generate a random bill number
        bill_number = random.randint(500, 1000)

        
        # Call bill_content function to get the bill content
        bill_content_result = bill_content(textarea.get("1.0", "end"), bill_number)

        # Ask for confirmation to save the bill
        result = messagebox.askyesno("Confirm", "Do you want to save the bill?")
        if result:
            save_bill(bill_content_result, bill_number, nameEntry.get(), phoneEntry.get())

        # Clear the bill area
        textarea.delete("1.0", END)

        # Display the bill details
        textarea.insert(END, bill_content_result)

        # Display the bill details
        textarea.insert(END, '\t\t*Welcome Customer*\n')
        textarea.insert(END, f'\nBill Number: {bill_number}\n')
        textarea.insert(END, f'\nCustomer Name: {nameEntry.get()}\n')
        textarea.insert(END, f'\nCustomer Phone Number: {phoneEntry.get()}\n')
        textarea.insert(END, '\n=======================================================\n')
        textarea.insert(END, 'Product\t\t\tQuantity\t\t\tPrice\n')
        textarea.insert(END, '=======================================================\n')

        # Insert code to display the products and their prices here

        # Display taxes
        textarea.insert(END, '-------------------------------------------------------\n')
        textarea.insert(END, f'Cosmetic Tax\t\t\t\t{cosmetictaxEntry.get()}\n')
        textarea.insert(END, f'Grocery Tax\t\t\t\t{grocerytaxEntry.get()}\n')
        textarea.insert(END, f'Drink Tax\t\t\t\t{drinktaxEntry.get()}\n')
        textarea.insert(END, '-------------------------------------------------------\n')
        textarea.insert(END, f'\nTotal Bill \t\t\t\t{totalbill} Rs\n')




        if bathsoapEntry.get() != '0':
            textarea.insert(END, f'\nBath Soap\t\t\t{bathsoapEntry.get()}\t\t\t{soapprice} Rs')
        if hairsprayEntry.get() != '0':
            textarea.insert(END, f'\nHair Spray\t\t\t{hairsprayEntry.get()}\t\t\t{hairsprayprice} Rs')
        if hairgelEntry.get() != '0':
            textarea.insert(END, f'\nHair Gel\t\t\t{hairgelEntry.get()}\t\t\t{hairgelprice} Rs')
        if facecreamEntry.get() != '0':
            textarea.insert(END, f'\nFace cream\t\t\t{facecreamEntry.get()}\t\t\t{facecreamprice} Rs')
        if facewashEntry.get() != '0':
            textarea.insert(END, f'\nFace wash\t\t\t{facewashEntry.get()}\t\t\t{facewashprice} Rs')
        if bodylotionEntry.get() != '0':
            textarea.insert(END, f'\nBody lotion\t\t\t{bodylotionEntry.get()}\t\t\t{bodylotionprice} Rs')


        if riceEntry.get() != '0':
            textarea.insert(END, f'\nRice\t\t\t{riceEntry.get()}\t\t\t{riceprice} Rs')
        if daalEntry.get() != '0':
            textarea.insert(END, f'\nDaal\t\t\t{daalEntry.get()}\t\t\t{daalprice} Rs')
        if oilEntry.get() != '0':
            textarea.insert(END, f'\nOil\t\t\t{oilEntry.get()}\t\t\t{oilprice} Rs')
        if sugarEntry.get() != '0':
            textarea.insert(END, f'\nSugar\t\t\t{sugarEntry.get()}\t\t\t{sugarprice} Rs')
        if wheatEntry.get() != '0':
            textarea.insert(END, f'\nWheat\t\t\t{wheatEntry.get()}\t\t\t{wheatprice} Rs')
        if teaEntry.get() != '0':
            textarea.insert(END, f'\nTea\t\t\t{teaEntry.get()}\t\t\t{teaprice} Rs')

        if frootiEntry.get() != '0':
            textarea.insert(END, f'\nFrooti\t\t\t{frootiEntry.get()}\t\t\t{frootiprice} Rs')
        if dewEntry != '0':
            textarea.insert(END, f'\nDew\t\t\t{dewEntry.get()}\t\t\t{dewprice} Rs')
        if pepsiprice.get() != '0':
            textarea.insert(END, f'\nPepsi\t\t\t{pepsiEntry.get()}\t\t\t{pepsiprice} Rs')
        if spriteEntry.get() != '0':
            textarea.insert(END, f'\nSprite\t\t\t{spriteEntry.get()}\t\t\t{spriteprice} Rs')
        if cococolaEntry.get() != '0':
            textarea.insert(END, f'\nCococola\t\t\t{cococolaEntry.get()}\t\t\t{cococolaprice} Rs')

        textarea.insert(END, '\n----------------------------------------------------------------')

        if cosmetictaxEntry.get() != '0.0 Rs':
            textarea.insert(END, f'\nCosmetic Tax\t\t\t\t{cosmetictaxEntry.get()}')
        if grocerytaxEntry.get() != '0.0 Rs':
            textarea.insert(END, f'\nGrocery Tax\t\t\t\t{grocerytaxEntry.get()}')
        if drinktaxEntry.get() != '0.0 Rs':
            textarea.insert(END, f'\nDrink Tax\t\t\t\t{drinktaxEntry.get()}')

        textarea.insert(END, f'\n\nTotal Bill \t\t\t\t{totalbill}')

        textarea.insert(END, '\n----------------------------------------------------------------')

        save_bill()



def total():
    global soapprice,hairsprayprice,hairgelprice,facecreamprice,facewashprice,bodylotionprice
    global riceprice,daalprice,oilprice,sugarprice,wheatprice,teaprice
    global frootiprice,dewprice,pepsiprice,spriteprice,cococolaprice
    global totalbill


    soapprice=int(bathsoapEntry.get())*20
    facecreamprice=int(facecreamEntry.get())*50
    facewashprice =int (facewashEntry.get()) * 100
    hairsprayprice = int(hairsprayEntry.get()) * 150
    hairgelprice = int(hairgelEntry.get()) * 80
    bodylotionprice =int(bodylotionEntry.get()) * 60
     
  
      

    totalcosmeticprice=soapprice+facewashprice+facecreamprice+hairgelprice 
    cosmeticpriceEntry.delete(0, END)
    cosmeticpriceEntry.insert(0, f'{totalcosmeticprice} Rs')
    cosmtictax=totalcosmeticprice*0.12
    cosmetictaxEntry.delete(0,END)
    cosmetictaxEntry.insert(0,str(cosmtictax) +' Rs')
      




    riceprice=int(riceEntry.get())*30
    daalprice=int(daalEntry.get())*100
    oilprice=int(oilEntry.get())*120
    sugarprice=int(sugarEntry.get())*50
    teaprice=int(teaEntry.get())*140
    wheatprice=int(wheatEntry.get())*80



    totalgroceryprice=riceprice+daalprice+oilprice+sugarprice+teaprice+wheatprice
    grocerypriceEntry.delete(0,END)
    grocerypriceEntry.insert(0,str (totalgroceryprice)+' Rs')
    grocerytax = totalgroceryprice * 0.05
    grocerytaxEntry.delete(0,END)
    grocerytaxEntry.insert(0, str(cosmtictax)+ 'Rs')




    maazaprice = int (maazaEntry.get()) * 50
    frootiprice = int(frootiEntry.get()) * 20
    dewprice = int (dewEntry.get()) * 30
    pepsiprice = int (pepsiEntry.get()) * 20
    spriteprice = int(spriteEntry.get()) * 45
    cococolaprice = int(cococolaEntry.get()) * 90



    totaldrinksprice=maazaprice+frootiprice+dewprice+pepsiprice+spriteprice+cococolaprice
    drinkpriceEntry.delete(0,END)
    drinkpriceEntry.insert(0,str (totaldrinksprice)+' Rs')
    drinktax = totaldrinksprice * 0.12
    drinktaxEntry.delete(0,END)
    drinktaxEntry.insert(0, str(drinktax)+ 'Rs')


    totalbill= totalcosmeticprice+ totalgroceryprice+ totaldrinksprice+ cosmtictax+ grocerytax+ drinktax

    

    totalcosmeticprice = soapprice + facewashprice + facecreamprice + hairgelprice + bodylotionprice
    cosmtictax = totalcosmeticprice * 0.12

    
    totalgroceryprice = riceprice + daalprice + oilprice + sugarprice + wheatprice + teaprice
    grocerytax = totalgroceryprice * 0.05

    
    totaldrinksprice = maazaprice + frootiprice + dewprice + pepsiprice + spriteprice + cococolaprice
    drinktax = totaldrinksprice * 0.12

    
    totalbill = totalcosmeticprice + totalgroceryprice + totaldrinksprice + cosmtictax + grocerytax + drinktax

    textarea.delete(1.0, END)
    textarea.insert(END, '\t\t*Welcome Customer*\n')
    textarea.insert(END, f'\nBill Number: {BillnumberEntry}\n')
    textarea.insert(END, f'\nCustomer Name: {nameEntry.get()}\n')

    textarea.insert(END, f'\nCustomer Phone Number: {phoneEntry.get()}\n')
    textarea.insert(END, '\n=======================================================\n')
    textarea.insert(END, 'Product\t\t\tQuantity\t\t\tPrice\n')
    textarea.insert(END, '=======================================================\n')

    # Display cosmetic items
    cosmetic_items = {
        "Bath Soap": bathsoapEntry.get(),
        "Face Cream": facecreamEntry.get(),
        "Face Wash": facewashEntry.get(),
        "Hair Spray": hairsprayEntry.get(),
        "Hair Gel": hairgelEntry.get(),
        "Body Lotion": bodylotionEntry.get()
    }
    for item, quantity in cosmetic_items.items():
        if int(quantity) > 0:
            price = eval(f"{item.lower().replace(' ', '')}price")
            textarea.insert(END, f'{item}\t\t\t{quantity}\t\t\t{int(quantity) * price} Rs\n')

    # Display grocery items
    grocery_items = {
        "Rice": riceEntry.get(),
        "Daal": daalEntry.get(),
        "Oil": oilEntry.get(),
        "Sugar": sugarEntry.get(),
        "Wheat": wheatEntry.get(),
        "Tea": teaEntry.get()
    }
    for item, quantity in grocery_items.items():
        if int(quantity) > 0:
            price = eval(f"{item.lower()}price")
            textarea.insert(END, f'{item}\t\t\t{quantity}\t\t\t{int(quantity) * price} Rs\n')

    # Display drink items
    drink_items = {
        "Maaza": maazaEntry.get(),
        "Frooti": frootiEntry.get(),
        "Dew": dewEntry.get(),
        "Pepsi": pepsiEntry.get(),
        "Sprite": spriteEntry.get(),
        "Coco Cola": cococolaEntry.get()
    }
    for item, quantity in drink_items.items():
        if int(quantity) > 0 :
            price = eval(f"{item.lower()}price")
            textarea.insert(END, f'{item}\t\t\t{quantity}\t\t\t{int(quantity) * price} Rs\n')

    # Display taxes
    textarea.insert(END, '-------------------------------------------------------\n')
    textarea.insert(END, f'Cosmetic Tax\t\t\t\t{cosmtictax} Rs\n')
    textarea.insert(END, f'Grocery Tax\t\t\t\t{grocerytax} Rs\n')
    textarea.insert(END, f'Drink Tax\t\t\t\t{drinktax} Rs\n')
    textarea.insert(END, '-------------------------------------------------------\n')
    textarea.insert(END, f'\nTotal Bill \t\t\t\t{totalbill} Rs\n')




root=Tk()
root.title('Payment Reciept')
root.geometry('1270x685')

headingLabel=Label(root,text='Payment Receipt',font=('times new roman',30,'bold'),bg='gray20',fg='gold',bd=12,relief=GROOVE)
headingLabel.pack(fill=X)

font=('times new roman',15,'bold')

customer_details_frame=LabelFrame(root,text='Customer Details',font=('times new roman',15,'bold'),bd=8,relief=GROOVE,bg='gray20')
customer_details_frame.pack(fill=X)

nameLabel=Label(customer_details_frame,text='Name',font=('times new roman',15,'bold'),bg='gray20',fg='white')
nameLabel.grid(row=0,column=0,padx=20,pady=2)

nameEntry=Entry(customer_details_frame,font=('arial',15),bd=7,width=18)
nameEntry.grid(row=0,column=1,padx=8)
               
phoneLabel=Label(customer_details_frame,text='phone',font=('times new roman',15,'bold'),bg='gray20',fg='white')
phoneLabel.grid(row=0,column=2,padx=20,pady=2)

phoneEntry=Entry(customer_details_frame,font=('arial',15),bd=7,width=18)
phoneEntry.grid(row=0,column=3,padx=8)

BillnumberLabel=Label(customer_details_frame,text='Bill Number',font=('times new roman',15,'bold'),bg='gray20',fg='white')
BillnumberLabel.grid(row=0,column=4,padx=20,pady=2)

BillnumberEntry=Entry(customer_details_frame,font=('arial',15),bd=7,width=18)
BillnumberEntry.grid(row=0,column=5,padx=8)

searchButton=Button(customer_details_frame,text='SEARCH',command=search_bill)
searchButton.grid(row=0,column=6,padx=20,pady=8)

productsFrame=Frame(root)
productsFrame.pack()

cosmeticsFrame=LabelFrame(productsFrame,text='Cosmetics',font=('times new roman',15,'bold'),fg='gold',bd=8,relief=GROOVE,bg='gray20')
cosmeticsFrame.grid(row=0,column=0)

bathsoapLabel=Label(cosmeticsFrame,text='Bath Soap',font=('times new roman',15,'bold'),bg='gray20',fg='white')
bathsoapLabel.grid(row=0,column=0,pady=9,padx=10,sticky='w')

bathsoapEntry=Entry(cosmeticsFrame,font=('times new roman',15,'bold'),width=10,bd=5)
bathsoapEntry.grid(row=0,column=1,pady=9,padx=10)
bathsoapEntry.insert(0,0)

facecreamLabel=Label(cosmeticsFrame,text='Face Cream',font=('times new roman',15,'bold'),bg='gray20',fg='white')
facecreamLabel.grid(row=1,column=0,pady=9,padx=10,sticky='w')

facecreamEntry=Entry(cosmeticsFrame,font=('times new roman',15,'bold'),width=10,bd=5)
facecreamEntry.grid(row=1,column=1,pady=9,padx=10)
facecreamEntry.insert(0,0)


facewashLabel=Label(cosmeticsFrame,text='Face Wash',font=('times new roman',15,'bold'),bg='gray20',fg='white')
facewashLabel.grid(row=2,column=0,pady=9,padx=10,sticky='w')

facewashEntry=Entry(cosmeticsFrame,font=('times new roman',15,'bold'),width=10,bd=5)
facewashEntry.grid(row=2,column=1,pady=9,padx=10)
facewashEntry.insert(0,0)

hairsprayLabel=Label(cosmeticsFrame,text='Hair Spray',font=('times new roman',15,'bold'),bg='gray20',fg='white')
hairsprayLabel.grid(row=3,column=0,pady=9,padx=10,sticky='w')

hairsprayEntry=Entry(cosmeticsFrame,font=('times new roman',15,'bold'),width=10,bd=5)
hairsprayEntry.grid(row=3,column=1,pady=9,padx=10)
hairsprayEntry.insert(0,0)

hairgelLabel=Label(cosmeticsFrame,text='Hair Gel',font=('times new roman',15,'bold'),bg='gray20',fg='white')
hairgelLabel.grid(row=4,column=0,pady=9,padx=10,sticky='w')

hairgelEntry=Entry(cosmeticsFrame,font=('times new roman',15,'bold'),width=10,bd=5)
hairgelEntry.grid(row=4,column=1,pady=9,padx=10)
hairgelEntry.insert(0,0)

bodylotionLabel=Label(cosmeticsFrame,text='Body Lotion',font=('times new roman',15,'bold'),bg='gray20',fg='white')
bodylotionLabel.grid(row=5,column=0,pady=9,padx=10,sticky='w')

bodylotionEntry=Entry(cosmeticsFrame,font=('times new roman',15,'bold'),width=10,bd=5)
bodylotionEntry.grid(row=5,column=1,pady=9,padx=10)
bodylotionEntry.insert(0,0)

groceryFrame=LabelFrame(productsFrame,text='Grocery',font=('times new roman',15,'bold'),fg='gold',bd=8,relief=GROOVE,bg='gray20')
groceryFrame.grid(row=0,column=1)

riceLabel=Label(groceryFrame,text='Rice',font=('times new roman',15,'bold'),bg='gray20',fg='white')
riceLabel.grid(row=0,column=0,pady=9,padx=10,sticky='w')

riceEntry=Entry(groceryFrame,font=('times new roman',15,'bold'),width=10,bd=5)
riceEntry.grid(row=0,column=1,pady=9,padx=10)
riceEntry.insert(0,0)

oilLabel=Label(groceryFrame,text='Oil',font=('times new roman',15,'bold'),bg='gray20',fg='white')
oilLabel.grid(row=1,column=0,pady=9,padx=10,sticky='w')

oilEntry=Entry(groceryFrame,font=('times new roman',15,'bold'),width=10,bd=5)
oilEntry.grid(row=1,column=1,pady=9,padx=10)
oilEntry.insert(0,0)

daalLabel=Label(groceryFrame,text='Daal',font=('times new roman',15,'bold'),bg='gray20',fg='white')
daalLabel.grid(row=2,column=0,pady=9,padx=10,sticky='w')

daalEntry=Entry(groceryFrame,font=('times new roman',15,'bold'),width=10,bd=5)
daalEntry.grid(row=2,column=1,pady=9,padx=10)
daalEntry.insert(0,0)

wheatLabel=Label(groceryFrame,text='Wheat',font=('times new roman',15,'bold'),bg='gray20',fg='white')
wheatLabel.grid(row=3,column=0,pady=9,padx=10,sticky='w')

wheatEntry=Entry(groceryFrame,font=('times new roman',15,'bold'),width=10,bd=5)
wheatEntry.grid(row=3,column=1,pady=9,padx=10)
wheatEntry.insert(0,0)

sugarLabel=Label(groceryFrame,text='Sugar',font=('times new roman',15,'bold'),bg='gray20',fg='white')
sugarLabel.grid(row=4,column=0,pady=9,padx=10,sticky='w')

sugarEntry=Entry(groceryFrame,font=('times new roman',15,'bold'),width=10,bd=5)
sugarEntry.grid(row=4,column=1,pady=9,padx=10)
sugarEntry.insert(0,0)

teaLabel=Label(groceryFrame,text='Tea',font=('times new roman',15,'bold'),bg='gray20',fg='white')
teaLabel.grid(row=5,column=0,pady=9,padx=10,sticky='w')

teaEntry=Entry(groceryFrame,font=('times new roman',15,'bold'),width=10,bd=5)
teaEntry.grid(row=5,column=1,pady=9,padx=10)
teaEntry.insert(0,0)

drinksFrame=LabelFrame(productsFrame,text='Cold Drinks',font=('times new roman',15,'bold'),fg='gold',bd=8,relief=GROOVE,bg='gray20')
drinksFrame.grid(row=0,column=2)

maazaLabel=Label(drinksFrame,text='Maaza',font=('times new roman',15,'bold'),bg='gray20',fg='white')
maazaLabel.grid(row=0,column=0,pady=9,padx=10,sticky='w')

maazaEntry=Entry(drinksFrame,font=('times new roman',15,'bold'),width=10,bd=5)
maazaEntry.grid(row=0,column=1,pady=9,padx=10)
maazaEntry.insert(0,0)

pepsiLabel=Label(drinksFrame,text='Pepsi',font=('times new roman',15,'bold'),bg='gray20',fg='white')
pepsiLabel.grid(row=1,column=0,pady=9,padx=10,sticky='w')

pepsiEntry=Entry(drinksFrame,font=('times new roman',15,'bold'),width=10,bd=5)
pepsiEntry.grid(row=1,column=1,pady=9,padx=10)
pepsiEntry.insert(0,0)

spriteLabel=Label(drinksFrame,text='Sprite',font=('times new roman',15,'bold'),bg='gray20',fg='white')
spriteLabel.grid(row=2,column=0,pady=9,padx=10,sticky='w')

spriteEntry=Entry(drinksFrame,font=('times new roman',15,'bold'),width=10,bd=5)
spriteEntry.grid(row=2,column=1,pady=9,padx=10)
spriteEntry.insert(0,0)

dewLabel=Label(drinksFrame,text='Dew',font=('times new roman',15,'bold'),bg='gray20',fg='white')
dewLabel.grid(row=3,column=0,pady=9,padx=10,sticky='w')

dewEntry=Entry(drinksFrame,font=('times new roman',15,'bold'),width=10,bd=5)
dewEntry.grid(row=3,column=1,pady=9,padx=10)
dewEntry.insert(0,0)

frootiLabel=Label(drinksFrame,text='Frooti',font=('times new roman',15,'bold'),bg='gray20',fg='white')
frootiLabel.grid(row=4,column=0,pady=9,padx=10,sticky='w')

frootiEntry=Entry(drinksFrame,font=('times new roman',15,'bold'),width=10,bd=5)
frootiEntry.grid(row=4,column=1,pady=9,padx=10)
frootiEntry.insert(0,0)

cococolaLabel=Label(drinksFrame,text='Coco Cola',font=('times new roman',15,'bold'),bg='gray20',fg='white')
cococolaLabel.grid(row=5,column=0,pady=9,padx=10,sticky='w')

cococolaEntry=Entry(drinksFrame,font=('times new roman',15,'bold'),width=10,bd=5)
cococolaEntry.grid(row=5,column=1,pady=9,padx=10)
cococolaEntry.insert(0,0)

billframe=Frame(productsFrame,bd=8,relief=GROOVE)
billframe.grid(row=0,column=3,padx=10)

billareaLabel=Label(billframe,text='Bill Area',font=('times new roman',15,'bold'),bd=7,relief=GROOVE)
billareaLabel.pack(fill=X)

scrollbar=Scrollbar(billframe,orient=VERTICAL)
scrollbar.pack(side=RIGHT,fill=Y)

textarea=Text(billframe,height=18,width=55,yscrollcommand=scrollbar.set)
textarea.pack()

scrollbar.config(command=textarea.yview)

billmenuFrame=LabelFrame(root,text='Bill Menu',font=('times new roman',16,'bold'),fg='gold',bd=8,relief=GROOVE,bg='gray20')
billmenuFrame.pack()

cosmeticpriceLabel=Label(billmenuFrame,text='Cosmetic Price',font=('times new roman',12,'bold'),bg='gray20',fg='white')
cosmeticpriceLabel.grid(row=0,column=0,pady=3,padx=5,sticky='w')
cosmeticpriceEntry=Entry(billmenuFrame,font=('times new roman',12,'bold'),width=8,bd=3)
cosmeticpriceEntry.grid(row=0,column=1,pady=3,padx=5)

grocerypriceLabel=Label(billmenuFrame,text='Grocery Price',font=('times new roman',12,'bold'),bg='gray20',fg='white')
grocerypriceLabel.grid(row=1,column=0,pady=3,padx=5,sticky='w')
grocerypriceEntry=Entry(billmenuFrame,font=('times new roman',12,'bold'),width=8,bd=3)
grocerypriceEntry.grid(row=1,column=1,pady=3,padx=5)

drinkpriceLabel=Label(billmenuFrame,text='Cold Drink Price',font=('times new roman',11,'bold'),bg='gray20',fg='white')
drinkpriceLabel.grid(row=2,column=0,pady=3,padx=5,sticky='w')
drinkpriceEntry=Entry(billmenuFrame,font=('times new roman',11,'bold'),width=8,bd=3)
drinkpriceEntry.grid(row=2,column=1,pady=3,padx=5)

cosmetictaxLabel=Label(billmenuFrame,text='Cosmetic Tax',font=('times new roman',12,'bold'),bg='gray20',fg='white')
cosmetictaxLabel.grid(row=0,column=2,pady=3,padx=5,sticky='w')
cosmetictaxEntry=Entry(billmenuFrame,font=('times new roman',12,'bold'),width=8,bd=3)
cosmetictaxEntry.grid(row=0,column=3,pady=3,padx=5)

grocerytaxLabel=Label(billmenuFrame,text='Grocery Tax',font=('times new roman',12,'bold'),bg='gray20',fg='white')
grocerytaxLabel.grid(row=1,column=2,pady=3,padx=5,sticky='w')
grocerytaxEntry=Entry(billmenuFrame,font=('times new roman',12,'bold'),width=8,bd=3)
grocerytaxEntry.grid(row=1,column=3,pady=3,padx=5)

drinktaxLabel=Label(billmenuFrame,text='Cool Drink Tax',font=('times new roman',11,'bold'),bg='gray20',fg='white')
drinktaxLabel.grid(row=2,column=2,pady=3,padx=5,sticky='w')
drinktaxEntry=Entry(billmenuFrame,font=('times new roman',11,'bold'),width=8,bd=3)
drinktaxEntry.grid(row=2,column=3,pady=3,padx=5)

buttonFrame=Frame(billmenuFrame,bd=8,relief=GROOVE)
buttonFrame.grid(row=0,column=4,rowspan=3)

totalButton=Button(buttonFrame,text='Total',font=('arial',16,'bold'),bg='gray20',fg='white',bd=5,width=8,pady=10,command=total)
totalButton.grid(row=0,column=0,pady=20,padx=5)

billButton=Button(buttonFrame,text='Bill',font=('arial',16,'bold'),bg='gray20',fg='white',bd=5,width=8,pady=10,command=bill_area)
billButton.grid(row=0,column=1,pady=20,padx=5)

emailButton=Button(buttonFrame,text='Email',font=('arial',16,'bold'),bg='gray20',fg='white',bd=5,width=8,pady=10,command=send_email)
emailButton.grid(row=0,column=2,pady=20,padx=5)

printButton=Button(buttonFrame,text='Print',font=('arial',16,'bold'),bg='gray20',fg='white',bd=5,width=8,pady=10)
printButton.grid(row=0,column=3,pady=20,padx=5)

clearButton=Button(buttonFrame,text='Clear',font=('arial',16,'bold'),bg='gray20',fg='white',bd=5,width=8,pady=10,command=clear)
clearButton.grid(row=0,column=4,pady=20,padx=5)

root.mainloop()