
import openpyxl
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter.messagebox import showinfo
from tkinter import *
import pandas as pd
import sys
import os
import pandas as pd


#Window setup
root = tk.Tk()
root.title("Fotocodering m.b.v EAN code")


#setting window size
width=755
height=371
screenwidth = root.winfo_screenwidth()
screenheight = root.winfo_screenheight()

root.geometry('700x200')
root.iconbitmap('ico LS.ico')


global locatie
locatie = []

# Ask the user to select a single file name.
def openfile():


    file = filedialog.askopenfilename(parent=root,
                                    initialdir="S:\SMS verdeling\SMS Verdeling",
                                    title="Selecteer SMS lijst:",
                                    filetypes=[ ('Excel', '.xlsx') ,('all files', '.*')])
    locatie.append(file)
    #for adres in locatie:
    label = tk.Label(LFrame, text= file)
    label.pack()

def directory():
    #for widget in frame.winfo_children():
        #widget.destroy()

    mapfoto = filedialog.askdirectory(parent=root,
                                    initialdir="S:\SMS verdeling\SMS Verdeling",
                                    title="Selecteer map:")
    locatie.append(mapfoto)
    label = tk.Label(RFrame, text= mapfoto)

    label.pack()

def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        root.destroy()

def done():
    if messagebox.askokcancel("Done", "Klaar is kees!"):
        root.destroy()

#def clear():
    locatie.clear()
    LFrame.destroy()
    RFrame.destroy()

def codeer():
    # Formule maken om de afbeeldingen uit te pakken
    #even voor de test
    smslocatie = locatie[0]
    directory= locatie[1]
    # lege dataframe maken
    df= []
    for subdir, dirs, files in os.walk(directory):
        for file in files:
            #print(os.path.join(subdir, file))
            if file.endswith(".png"):
                df.append(file)

    # een ean lisjt maken van de afbeeldingen
    lijst_EAN = [i.split("_",1) for i in df]
    df_lijst_EAN = pd.DataFrame(lijst_EAN, columns=['barcode','soort'])


    #een SMS lijst inladen
    sms = pd.read_excel(smslocatie,  engine='openpyxl')
    if 'barcode' in sms.columns:
        sms['barcode']= pd.to_numeric(sms['barcode'], errors= 'coerce')
        ## hierzijn indien iets veranderd moet worden aan de benaming# num maken
        sms = sms[['barcode', 'ProductID','Product','Color']] # alleen nodige kolommen Indien andere toevoegingen hier doen
        df_lijst_EAN['barcode']= pd.to_numeric(df_lijst_EAN['barcode'], errors= 'coerce')

        #het samenvoegen met een left join op de eanlijst. op de barcode
        result= pd.merge(left= df_lijst_EAN,right= sms, how='left', left_on='barcode', right_on='barcode') #.fillna(0)
        #warning
        if result.empty:
            messagebox.showerror(title= 'Error',message='Kan geen EAN van de foto koppelen met de SMSlijst.')

        #resultaat in een colom zetten en een list maken
        result['newname']= result['ProductID']+'_'+result['Product']+'_'+result['Color']+'_'+result['soort']
        newname = result['newname'].tolist()

        #het renamen van de afbeeldingen in de juiste mappen
        for subdir, dirs, files in os.walk(directory):
            for file in files:
                newfilename = newname[files.index(file)]

                #shutil.copy(os.path.join(subdir, file),os.path.join(subdir, newfilename)) #kopier
                os.rename(os.path.join(subdir, file),os.path.join(subdir, newfilename) ) #hernoemen
    else:
        messagebox.showerror(title= 'Error',message='Let op! De Excel file klopt niet. Kan geen Barcode kolom vinden in SMS lijst'
                                                    ' of je hebt een verkeerd bestand geopend. Probeer opnieuw.')








# Frame and its contents
LFrame = Frame(root)
LFrame.grid(row = 0, column = 1, sticky = W, pady = 2)

RFrame = Frame(root)
RFrame.grid(row = 1, column = 1, sticky = W, pady = 2)


#Buttons
b1 = tk.Button(root, text="Open SMS lijst", command= openfile, padx=10, pady=5, bg='grey')
b1.grid(row = 0, column = 0, sticky = E, pady = 2)
#but folder
b2 = tk.Button(root, text='Locatiemap Fotos',command= directory, padx=10, pady=5, bg= 'grey')
b2.grid(row = 1, column = 0, sticky = E, pady = 2)
#but codeer
b3 = tk.Button(root, text='Codeer' , command=lambda:[codeer(),done()],padx=10, pady=5, bg= 'green')
b3.grid(row = 3, column = 0, sticky = E, pady = 2)
#but opnieuw
#b4 = tk.Button(root, text='refresh' ,command= clear, padx=10, pady=5,bg= 'yellow')
#b4.grid(row = 4, column = 0, sticky = E, pady = 2)



# Afsluiten applicatie
root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()






