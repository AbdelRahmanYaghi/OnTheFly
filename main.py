from tkinter import *
from tkcalendar import Calendar
import pickle
import numpy as np
from sklearn.preprocessing import LabelEncoder
import pandas as pd
from random import sample

df = pd.read_csv(r"airlines_data_cleaned.csv")
#labels encoder
b = ["Arrival" , "Departure" , "cabin", "traveller_type"]
leArr = LabelEncoder()
leDEP = LabelEncoder()
lecab = LabelEncoder()
letype = LabelEncoder()
df5 = df[b]
df5
df5[b[0]] = leArr.fit_transform(df5[b[0]])
df5[b[1]] = leDEP.fit_transform(df5[b[1]])
df5[b[2]] = lecab.fit_transform(df5[b[2]])
df5[b[3]] = letype.fit_transform(df5[b[3]])


model = pickle.load(open('finalized_model.sav','rb'))
CENT = model.cluster_centers_
root = Tk() # Creating main TKinter obj
root.title("On The Fly") # Setting a title for the app
root.configure(bg='#202020') # Configuring the background color for the entire main window
root.geometry("750x600") # Configuring the size of the main window
root.iconbitmap(r'MyIcon.ico')
# pyglet.font.add_file('Changa-Regular.ttf') # Importing the custom font
root.option_add( "*font", "16" ) # Setting the font as the default font

# Each chunk of the following chunks contains a frame. Each frame for a variable. Did it this way-
# -purely for aesthetic reasons and to make the program look as neat as possible.
  
items = []

TravelerType_frame = Frame(root, bg='#202020') 
TravelerType_frame.pack(fill=X, pady= 15)

TravelerType_text = Label(TravelerType_frame, text = 'Traveler Type', bg='#202020', fg='white')
TravelerType_text.pack( padx=30,side=LEFT)

TravelerType_options = ['Solo Leisure', 'Couple Leisure', 'Business', 'Family Leisure']
TravelerType_Seleceted = StringVar()
TravelerType_dropdown = OptionMenu(TravelerType_frame, TravelerType_Seleceted, *TravelerType_options)
TravelerType_dropdown.config(fg="white", bg="#202020")
TravelerType_dropdown['menu'].config(fg="white", bg="#202020")
TravelerType_dropdown.pack(padx=30, side=RIGHT)


CabinType_frame = Frame(root, bg='#202020')
CabinType_frame.pack(fill=X, pady= 15)

CabinType_text = Label(CabinType_frame, text = 'Cabin Type', bg='#202020', fg='white')
CabinType_text.pack(padx=30, side=LEFT)

CabinType_options = ['Economy Class', 'Business Class', 'First Class','Premium Economy']
CabinType_Seleceted = StringVar()
CabinType_dropdown = OptionMenu(CabinType_frame, CabinType_Seleceted, *CabinType_options)
CabinType_dropdown.config( fg="white", bg="#202020")
CabinType_dropdown['menu'].config( fg="white", bg="#202020")
CabinType_dropdown.pack(padx=30, side=RIGHT)


Departure_frame = Frame(root, bg='#202020')
Departure_frame.pack(fill= X, pady= 15)

Departure_text = Label(Departure_frame, text = 'Departure', bg='#202020', fg='white')
Departure_text.pack(padx=30,side=LEFT)

Departure_options = list(df['Departure'].unique())
Departure_Seleceted = StringVar()
Departure_dropdown = OptionMenu(Departure_frame, Departure_Seleceted, *Departure_options)
Departure_dropdown.config(fg="white", bg="#202020")
Departure_dropdown['menu'].config(fg="white", bg="#202020")
Departure_dropdown.pack(padx=30,side=RIGHT)


Arrival_frame = Frame(root, bg='#202020')
Arrival_frame.pack(fill = X, pady= 15)

Arrival_text = Label(Arrival_frame, text = 'Arrival', bg='#202020', fg='white')
Arrival_text.pack(padx=30, side=LEFT)

Arrival_options = list(df['Arrival'].unique())
Arrival_Seleceted = StringVar()
Arrival_dropdown = OptionMenu(Arrival_frame, Arrival_Seleceted, *Arrival_options)
Arrival_dropdown.config(fg="white", bg="#202020")
Arrival_dropdown['menu'].config(fg="white", bg="#202020")
Arrival_dropdown.pack(padx=30, side=RIGHT)


Date_frame = Frame(root, bg='#202020')
Date_frame.pack(fill= X, pady= 15)

Date_text = Label(Date_frame, text = 'Date', bg='#202020', fg='white')
Date_text.pack(padx=30, side=LEFT)
Date_Selected = StringVar()

DatePop_Button = Button(Date_frame, text = 'Choose Date', fg="white", bg="#202020")    


def chooseDate():
    Date_popWindow = Toplevel(root)
    Date_popWindow.title('Date picker')
    Date_Cal = Calendar(Date_popWindow, selectmode = 'day')
    
    def ConfirmDate():
        Date_Selected = Date_Cal.get_date()
        DatePop_Button.configure(text= Date_Selected)
        Date_popWindow.destroy()
       
    Date_Button = Button(Date_popWindow, text = 'Confirm', command=ConfirmDate)
    Date_Cal.pack()
    Date_Button.pack()
    

DatePop_Button.configure(command= chooseDate)
DatePop_Button.pack(padx=30, side=RIGHT)

Search_frame = Frame(root, bg='#202020')
Search_frame.pack(fill= X, pady= 25)






Search_button = Button(Search_frame, text='Search', width=20)
Search_button.pack()

Suggestions_text = Label(root, text="Suggestions")
Suggestions_text.pack(fill=X, padx=30)

Suggestions_listbox = Listbox(root)
Suggestions_listbox.pack(fill=X, padx=30)



def srch():
    global CENT
    items = []
    items.append(letype.transform([TravelerType_Seleceted.get()])[0])
    items.append(lecab.transform([CabinType_Seleceted.get()])[0])
    items.append(leDEP.transform([Departure_Seleceted.get()])[0])
    items.append(leArr.transform([Arrival_Seleceted.get()])[0])
    

    def dis(CENT, items1):
        Suggestions_listbox.delete(0, END)
        distances = {}
        for idx, i in enumerate(CENT):
            sums = 0
            for j, j1 in zip(i, items1):
                sums += (j-j1)**2
            distances[f'{idx}'] = np.sqrt(sums)
        return distances
    
    d = dis(CENT, items)
    d['4'] = d['4'] * 0.70
    d['2'] = d['2'] * 0.80
    d['1'] = d['1'] * 0.80

            
    dsorted = {k: v for k, v in sorted(d.items(), key=lambda item: item[1])}
    
    
    dkeys =list(dsorted.keys())[-3:]
    print(sample(list(df[model.labels_==int(dkeys[0])]['airline'].unique()[:10]), 3)) # Not enough data for the model to get any results other than (Turkish Airlines, Qatar Airlines, Emirates). So we sample from the top 10 suggestions
    
    for idx,i in enumerate(sample(list(df[model.labels_==int(dkeys[0])]['airline'].unique()[:10]), 3)):
        v = idx+1
        Suggestions_listbox.insert(idx ,f"{v} -  {i}")
    
    
Search_button.configure(command = srch)

root.mainloop()