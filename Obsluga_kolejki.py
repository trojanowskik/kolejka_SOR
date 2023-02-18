import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
from my_priority_queue import PriorityQueue
import time


class SOR(tk.Frame, tk.Entry):
    
    def __init__(self, root, fcolor, *args, **kwargs):
        super().__init__(root, *args, **kwargs)
        self.bind('<FocusIn>', self.zmiana_koloru_in)
        self.bind('<FocusOut>', self.zmiana_koloru_out)
        self.fcolor = fcolor
        self.tlo = self.cget('bg')
        
        self.lista = []
        self.lista_wypisanych = []
        self.kolejka = PriorityQueue()
        self.i = 0
        self.korzen = root
        self.utworz_menu()
        
        self.imie = tk.StringVar()
        self.nazwisko = tk.StringVar()
        self.pesel = tk.StringVar()
        self.triaz = tk.StringVar()
        self.wyszukiwarka = tk.StringVar()
        
        self.etykieta_nr_wpisu = tk.Label(self)
        self.etykieta_nr_wpisu.grid(row = 0, column = 2, columnspan = 2, sticky = tk.W + tk.E)
        
        self.etykieta_enter = tk.Label(self, text = '', background = 'light blue')
        self.etykieta_enter.grid(row = 1, column = 0, columnspan = 7, sticky = tk.W + tk.E)
        
        self.etykieta_imie = tk.Label(self, text = 'Imię: ')
        self.etykieta_imie.grid(row = 2, column = 0, sticky = tk.W + tk.E)
        
        self.pole_imie = tk.Entry(self, width = 30, textvariable = self.imie)
        self.pole_imie.grid(row = 2, column = 1, columnspan = 3, sticky = tk.W + tk.E)

        self.etykieta_nazwisko = tk.Label(self, text = 'Nazwisko: ')
        self.etykieta_nazwisko.grid(row = 3, column = 0, sticky = tk.W + tk.E)
        
        self.pole_nazwisko = tk.Entry(self, width = 30, textvariable = self.nazwisko)
        self.pole_nazwisko.grid(row = 3, column = 1, columnspan = 3,  sticky = tk.W + tk.E)
        
        self.etykieta_pesel = tk.Label(self, text = 'PESEL: ')
        self.etykieta_pesel.grid(row = 4, column = 0, sticky = tk.W + tk.E)
        
        self.pole_pesel = tk.Entry(self, width = 30, textvariable = self.pesel)
        self.pole_pesel.grid(row = 4, column = 1, columnspan = 3, sticky = tk.W + tk.E)
        
        self.etykieta_kodu = tk.Label(self, text = 'KOD TRIAŻU: ')
        self.etykieta_kodu.grid(row = 5, column = 0, sticky = tk.W + tk.E)
        
        kody_triazu = ttk.Combobox(self, width = 27, textvariable = self.triaz)
        kody_triazu['values'] = ('zielony', 'żółty', 'czerwony') 
        kody_triazu['state'] = 'readonly'
        kody_triazu.grid(row = 5, column = 1, columnspan = 3)
        
        self.informacja = tk.Button(self, text = '?', command = self.wyswietl_informacje)
        self.informacja.grid(column = 4, row = 5, sticky = tk.E+tk.W)
        
        self.dodaj = tk.Button(self, text='Dodaj pacjenta do kolejki', command = self.dodaj)
        self.dodaj.grid(column = 0, row = 6, columnspan = 4, sticky = tk.E+tk.W)
    
        self.przycisk_do_poczatku = tk.Button(self, text = '|<-', command = self.do_poczatku)
        self.przycisk_do_poczatku.grid(row = 7, column = 0, sticky = tk.W + tk.E)
        self.przycisk_do_poczatku['state'] = tk.DISABLED
        
        self.przycisk_poprzedni = tk.Button(self, text = '<-', command = self.poprzedni)
        self.przycisk_poprzedni.grid(row = 7, column = 1, sticky = tk.W + tk.E)
        self.przycisk_poprzedni['state'] = tk.DISABLED
        
        self.przycisk_nastepny = tk.Button(self, text = '->', command = self.nastepny)
        self.przycisk_nastepny.grid(row = 7, column = 2, sticky = tk.W + tk.E)
        self.przycisk_nastepny['state'] = tk.DISABLED
        
        self.przycisk_do_konca = tk.Button(self, text = '->|', command = self.do_konca)
        self.przycisk_do_konca.grid(row = 7, column = 3, sticky = tk.W + tk.E)
        self.przycisk_do_konca['state'] = tk.DISABLED
        
        self.wyswietl = tk.Button(self, text = 'Wyświetl pacjentów', command = self.wyswietl_pacjentow)
        self.wyswietl.grid(row=8, column = 0, columnspan = 4, sticky = tk.W + tk.E)
       
        self.etykieta_enter2 = tk.Label(self, text = '                                       ', background = "light blue")
        self.etykieta_enter2.grid(row = 9, column = 0, columnspan = 7, sticky = tk.W + tk.E)
         
        self.etykieta_wyszukiwarka = tk.Label(self, text = 'Wyszukaj osobę po PESELU: ')
        self.etykieta_wyszukiwarka.grid(row = 10, column = 0, columnspan = 3)
        
        self.pole_wyszukiwarka = tk.Entry(self, width = 30, textvariable = self.wyszukiwarka)
        self.pole_wyszukiwarka.grid(row = 10, column = 3, columnspan = 3, sticky = tk.W + tk.E)
                
        self.przycisk_wyszukiwarka = tk.Button(self, text = 'Szukaj', command = self.szukaj, background = 'blue')
        self.przycisk_wyszukiwarka.grid(row = 11, column = 2, columnspan = 2, sticky = tk.W + tk.E)
        
        self.przycisk_usun = tk.Button(self, text = 'Przyjęty na oddział', command = self.przyjety, foreground = 'blue')
        self.przycisk_usun.grid(row = 2, column = 6, columnspan = 2,  sticky = tk.W + tk.E)
        self.przycisk_usun['state'] = tk.DISABLED
        
        self.przycisk_zatwierdz = tk.Button(self, text = 'Wypis', command = self.wypis, foreground = 'blue')
        self.przycisk_zatwierdz.grid(row = 3, column = 6, columnspan = 2,  sticky = tk.W + tk.E)
        self.przycisk_zatwierdz['state'] = tk.DISABLED
        
        self.przycisk_nowy = tk.Button(self, text = 'Smierć', command = self.smierc, foreground = 'blue')
        self.przycisk_nowy.grid(row = 4, column = 6, columnspan = 2,  sticky = tk.W + tk.E)
        self.przycisk_nowy['state'] = tk.DISABLED
        
        if tk.messagebox.askokcancel(title = None, message = 'Chcesz otworzyć plik?'):
            self.otworz_plik()
    
    
    def wyswietl_informacje(self):
        ## kod triażu jest uniwersalnym kodem stosowanym na SOR-ze
        ## jest to metoda segregacji pacjentów - okręla on kolejnosć pacjentów biorąc pod uwagę ich stan zdrowia i zagrożenie życia
        ## informacje o poszczególnych kodach znajdują się w oknie komunikatu
        komunikat = 'CZERWONY – bezpośrednie zagrożenie życia lub zdrowia – pomoc musi być udzielona natychmiast;\n\nŻÓŁTY – przypadek pilny – pacjent powinien być przyjęty jak najszybciej;\n\nZIELONY – przypadek stabilny – nie ma zagrożenia życia lub poważnego uszczerbku na zdrowiu – pacjent zostanie przyjęty po pacjentach z kodem czerwonym i żółtym.'
        messagebox.showinfo('Informacje o kodach', komunikat)
        
    
    def dodaj(self):
        ## dodawanie elementów do listy (nie kolejki priotytetowej)
        imie2 = self.pole_imie.get()
        nazwisko2 = self.pole_nazwisko.get()
        pesel2 = self.pesel.get()
        triaz2 = self.triaz.get()      
        
        ## sprawdzanie poprawnosci numeru PESEL
        if len(pesel2) != 11:
            komunikat = 'niepoprawny numer PESEL!'
            messagebox.showinfo('Informacje o kodach', komunikat)
        #i = 0
        #while i < len(self.lista):
        #    pesel = self.lista[i][2]
        #    if pesel2 == pesel:
        #        komunikat = 'w bazie jest już taki numer PESEL!'
        #        messagebox.showinfo('Informacje o kodach', komunikat)
        #        i += 1  
        pesel2 = self.pesel.get()
        
        self.lista.append([imie2, nazwisko2, pesel2, triaz2])
        self.i = len(self.lista) - 1

        self.imie.set(self.lista[self.i][0])
        self.nazwisko.set(self.lista[self.i][1])
        self.pesel.set(self.lista[self.i][2])
    
        self.etykieta_nr_wpisu.config(text = 'Wpis nr {} (z {})'.format(int(self.i + 1), len(self.lista)))
        self.przycisk_nastepny['state'] = tk.DISABLED
        self.przycisk_do_konca['state'] = tk.DISABLED
        
        if len(self.lista) == 1:
            self.przycisk_usun['state'] = tk.NORMAL
            self.przycisk_zatwierdz['state'] = tk.NORMAL
            
        elif len(self.lista) > 1:
            self.przycisk_do_poczatku['state'] = tk.NORMAL
            self.przycisk_poprzedni['state'] = tk.NORMAL
            
        else:
            self.przycisk_do_poczatku['state'] = tk.DISABLED
            self.przycisk_poprzedni['state'] = tk.DISABLED
            
            
    def wyswietl_pacjentow(self):
        ## funkcja wywietla pacjentów według kolejnosci z kolejki priorytetowej
        ## wywietlanie pacjentów jest możliwe po dodaniu ich do listy
        komunikat = ''
        self.i = 0
        i = 0
        while i < len(self.lista):
            self.lista = sorted(self.lista, key = lambda e: e[2])
            nazwisko = self.lista[i][0]
            imie = self.lista[i][1]
            pesel = self.lista[i][2]
            kod = self.lista[i][3]
            kod.rstrip()
            kod.lstrip()
            kod2 = str(kod)

            if kod2 == 'ĹĽĂłĹ‚ty\n' or kod2 == 'żółty':
                pri = 2
            elif kod2 == 'czerwony\n' or kod2 == 'czerwony':
                pri = 3
            elif kod2 == 'zielony\n' or kod2 == 'zielony':
                pri = 1
            self.lista = sorted(self.lista, key = lambda e: e[2])    
            self.kolejka.attach((nazwisko, imie, pesel), pri)
            i +=1
        
        while self.kolejka.is_empty() == False:
            item = self.kolejka.detach()
            komunikat = komunikat + "pacjent: " + str(item[0][0]) + " " + str(item[0][1]) + ", numer PESEL: " + str(item[0][2]) + ", priorytet: " + str(item[1]) + '\n'

        messagebox.showinfo('Kolejka przyjmowania pacjentów: ', komunikat) 
        
        
    
    def do_poczatku(self):
        self.i = 0
        self.etykieta_nr_wpisu.config(text = 'Osoba nr {} (z {})'.format(int(self.i + 1), len(self.lista)))
        
        self.imie.set(self.lista[self.i][0])
        self.nazwisko.set(self.lista[self.i][1])
        self.pesel.set(self.lista[self.i][2])
        self.triaz.set(self.lista[self.i][3])
        self.przycisk_do_poczatku['state'] = tk.DISABLED
        self.przycisk_poprzedni['state'] = tk.DISABLED
        
        if len(self.lista) > 1:
            self.przycisk_nastepny['state'] = tk.NORMAL
            self.przycisk_do_konca['state'] = tk.NORMAL


    def poprzedni(self):
        self.i = self.i - 1
        self.etykieta_nr_wpisu.config(text = 'Osoba nr {} (z {})'.format(int(self.i + 1), len(self.lista)))
        
        self.imie.set(self.lista[self.i][0])
        self.nazwisko.set(self.lista[self.i][1])
        self.pesel.set(self.lista[self.i][2])
        self.triaz.set(self.lista[self.i][3])
        
        if len(self.lista) > 1:
            self.przycisk_nastepny['state'] = tk.NORMAL
            self.przycisk_do_konca['state'] = tk.NORMAL
        
        if self.i == 0:
            self.przycisk_poprzedni['state'] = tk.DISABLED
            self.przycisk_do_poczatku['state'] = tk.DISABLED
            
    
    def nastepny(self):
        self.i = self.i + 1
        self.etykieta_nr_wpisu.config(text = 'Osoba nr {} (z {})'.format(int(self.i + 1), len(self.lista)))
        
        self.imie.set(self.lista[self.i][0])
        self.nazwisko.set(self.lista[self.i][1])
        self.pesel.set(self.lista[self.i][2])
        self.triaz.set(self.lista[self.i][3])
        self.przycisk_do_poczatku['state'] = tk.NORMAL
        self.przycisk_poprzedni['state'] = tk.NORMAL
        
        if self.i == len(self.lista) - 1:
            self.przycisk_nastepny['state'] = tk.DISABLED
            self.przycisk_do_konca['state'] = tk.DISABLED
            
    
    def do_konca(self):
        self.i = len(self.lista) - 1
        self.etykieta_nr_wpisu.config(text = 'Osoba nr {} (z {})'.format(int(self.i + 1), len(self.lista)))
        
        self.imie.set(self.lista[self.i][0])
        self.nazwisko.set(self.lista[self.i][1])
        self.pesel.set(self.lista[self.i][2])
        self.triaz.set(self.lista[self.i][3])
        
        self.przycisk_do_konca['state'] = tk.DISABLED
        self.przycisk_nastepny['state'] = tk.DISABLED
        self.przycisk_do_poczatku['state'] = tk.NORMAL
        self.przycisk_poprzedni['state'] = tk.NORMAL
        

    def przyjety(self):
        ## funkcja przechowuje informacje o pacjentach, którzy zostali przyjęci na dowolny oddział szpitala
        self.i = 0
        if len(self.lista) > 0:
            komunikat = [self.lista[self.i][0], self.lista[self.i][1], (self.lista[self.i][2]), str("pacjent przyjęty na oddział: " ) + str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))]
            print(komunikat)
            self.lista_wypisanych.append(komunikat)
            if self.i == 0:
                del self.lista[self.i]
                if len(self.lista) > 0:
                    self.imie.set(self.lista[self.i][0])
                    self.nazwisko.set(self.lista[self.i][1])
                    self.pesel.set(self.lista[self.i][2])
                    self.i = 0
                    self.etykieta_nr_wpisu.config(text = 'Osoba nr {} (z {})'.format(int(self.i + 1), len(self.lista)))
            else:
                del self.lista[self.i]
                if self.i - 1 != 0:
                    self.i -= 1
                    self.imie.set(self.lista[self.i][0])
                    self.nazwisko.set(self.lista[self.i][1])
                    self.pesel.set(self.lista[self.i][2])
                    
                    self.etykieta_nr_wpisu.config(text = 'Osoba nr {} (z {})'.format(int(self.i), len(self.lista)))
                else:
                    self.i -= 1
                    self.imie.set(self.lista[self.i][0])
                    self.nazwisko.set(self.lista[self.i][1])
                    self.pesel.set(self.lista[self.i][2])
                    
                    self.etykieta_nr_wpisu.config(text = 'Osoba nr {} (z {})'.format(int(self.i + 1), len(self.lista)))
                    
                    self.przycisk_poprzedni['state'] = tk.DISABLED
                    self.przycisk_do_poczatku['state'] = tk.DISABLED
            self.lista.pop(self.i)
        else:
            self.imie.set('')
            self.nazwisko.set('')
            self.pesel.set('')
            self.i = 0
            self.etykieta_nr_wpisu.config(text = 'Osoba nr {} (z {})'.format(int(self.i + 1), len(self.lista)))
                    


    def wypis(self):
        ## funkcja przechowuje informacje o pacjentach, którzy zostali wypisani z SOR-u
        self.i = 0
        if len(self.lista) > 0:
            komunikat = [self.lista[self.i][0], self.lista[self.i][1], (self.lista[self.i][2]), str("wypis do domu: " ) + str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))]
            print(komunikat)
            self.lista_wypisanych.append(komunikat)
            if self.i == 0:
                del self.lista[self.i]
                if len(self.lista) > 0:
                    self.imie.set(self.lista[self.i][0])
                    self.nazwisko.set(self.lista[self.i][1])
                    self.pesel.set(self.lista[self.i][2])
                    self.i = 0
                    self.etykieta_nr_wpisu.config(text = 'Osoba nr {} (z {})'.format(int(self.i + 1), len(self.lista)))
            else:
                del self.lista[self.i]
                if self.i - 1 != 0:
                    self.i -= 1
                    self.imie.set(self.lista[self.i][0])
                    self.nazwisko.set(self.lista[self.i][1])
                    self.pesel.set(self.lista[self.i][2])
                    
                    self.etykieta_nr_wpisu.config(text = 'Osoba nr {} (z {})'.format(int(self.i), len(self.lista)))
                else:
                    self.i -= 1
                    self.imie.set(self.lista[self.i][0])
                    self.nazwisko.set(self.lista[self.i][1])
                    self.pesel.set(self.lista[self.i][2])
                    
                    self.etykieta_nr_wpisu.config(text = 'Osoba nr {} (z {})'.format(int(self.i + 1), len(self.lista)))
                    
                    self.przycisk_poprzedni['state'] = tk.DISABLED
                    self.przycisk_do_poczatku['state'] = tk.DISABLED
            self.lista.pop(self.i)
        else:
            self.imie.set('')
            self.nazwisko.set('')
            self.pesel.set('')
            self.i = 0
            self.etykieta_nr_wpisu.config(text = 'Osoba nr {} (z {})'.format(int(self.i + 1), len(self.lista)))
      
        
         
    def smierc(self):
        ## funkcja przechowuje informacje o pacjentach, którzy zmarli w czasie pobytu na SOR-ze
        self.i = 0
        if len(self.lista) > 0:
            komunikat = [self.lista[self.i][0], self.lista[self.i][1], (self.lista[self.i][2]), str("pacjent zmarł: " ) + str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))]
            print(komunikat)
            self.lista_wypisanych.append(komunikat)
            if self.i == 0:
                del self.lista[self.i]
                if len(self.lista) > 0:
                    self.imie.set(self.lista[self.i][0])
                    self.nazwisko.set(self.lista[self.i][1])
                    self.pesel.set(self.lista[self.i][2])
                    self.i = 0
                    self.etykieta_nr_wpisu.config(text = 'Osoba nr {} (z {})'.format(int(self.i + 1), len(self.lista)))
            else:
                del self.lista[self.i]
                if self.i - 1 != 0:
                    self.i -= 1
                    self.imie.set(self.lista[self.i][0])
                    self.nazwisko.set(self.lista[self.i][1])
                    self.pesel.set(self.lista[self.i][2])
                    
                    self.etykieta_nr_wpisu.config(text = 'Osoba nr {} (z {})'.format(int(self.i), len(self.lista)))
                else:
                    self.i -= 1
                    self.imie.set(self.lista[self.i][0])
                    self.nazwisko.set(self.lista[self.i][1])
                    self.pesel.set(self.lista[self.i][2])
                    
                    self.etykieta_nr_wpisu.config(text = 'Osoba nr {} (z {})'.format(int(self.i + 1), len(self.lista)))
                    
                    self.przycisk_poprzedni['state'] = tk.DISABLED
                    self.przycisk_do_poczatku['state'] = tk.DISABLED
            self.lista.pop(self.i)
        else:
            self.imie.set('')
            self.nazwisko.set('')
            self.pesel.set('')
            self.i = 0
            self.etykieta_nr_wpisu.config(text = 'Osoba nr {} (z {})'.format(int(self.i + 1), len(self.lista)))
      
    
    def utworz_menu(self):
        menu = tk.Menu(self.korzen)
        menu_plik = tk.Menu(menu, tearoff = 0)
        menu_plik.add_command(label = 'Otwórz plik', command = self.otworz_plik)
        menu_plik.add_command(label = 'Zapisz plik', command = self.zapisz_plik)
        menu_plik.add_command(label = 'Utwórz plik', command = self.utworz_plik)
        menu.add_cascade(label = 'Plik', menu = menu_plik)
        self.korzen['menu'] = menu   
    
    
    def otworz_plik(self):
        try:
            with filedialog.askopenfile(filetypes = [('pliki tekstowe', '*.txt')]) as plik:
                for linia in plik:
                    linia.strip('\n')
                    try:
                        imie1, nazwisko1, pesel1, triaz1 = linia.split(' ')
                        self.lista.append([imie1, nazwisko1, pesel1, triaz1])
                        self.imie.set(self.lista[self.i][0])
                        self.nazwisko.set(self.lista[self.i][1])
                        self.pesel.set(self.lista[self.i][2])
                        self.triaz.set(self.lista[self.i][3])
                        
                    except ValueError:
                        pass
                    
            if len(self.lista) > 1:
                self.przycisk_nastepny['state'] = tk.NORMAL
                self.przycisk_do_konca['state'] = tk.NORMAL
                self.przycisk_usun['state'] = tk.NORMAL
                self.przycisk_zatwierdz['state'] = tk.NORMAL
                self.przycisk_nowy['state'] = tk.NORMAL
                
            elif len(self.lista) == 1:
                self.przycisk_usun['state'] = tk.NORMAL
                self.przycisk_zatwierdz['state'] = tk.NORMAL
                self.przycisk_nowy['state'] = tk.NORMAL
            
            else:
                raise ValueError("Pusty plik!")
                
            self.etykieta_nr_wpisu.config(text = 'Osoba nr {} (z {})'.format(int(self.i + 1), len(self.lista)))
            
        except AttributeError:
                pass
    
    
    def zapisz_plik(self):
        gotowy = ''
        
        for element in self.lista:
            for czlon in element:
                if '\n' in czlon:
                    gotowy += czlon
                else:
                    gotowy += czlon + ' '

        print(gotowy[:len(gotowy)-2], file = filedialog.asksaveasfile())
        
    
    def utworz_plik(self):
        self.lista = []
        self.imie.set('')
        self.nazwisko.set('')
        self.pesel.set('')
        self.triaz.set('')
        self.i = 0
        
        self.etykieta_nr_wpisu.config(text = 'Osoba nr {} (z {})'.format(int(self.i + 1), len(self.lista)))
        
        if self.i > 1:
            self.przycisk_nastepny['state'] = tk.NORMAL
            self.przycisk_do_konca['state'] = tk.NORMAL
            self.przycisk_przyjety['state'] = tk.NORMAL
            self.przycisk_wypis['state'] = tk.NORMAL
            self.przycisk_smierc['state'] = tk.NORMAL
            self.przycisk_do_poczatku['state'] = tk.NORMAL
            self.przycisk_poprzedni['state'] = tk.NORMAL
                
        elif self.i == 1:
            self.przycisk_przyjety['state'] = tk.NORMAL
            self.przycisk_wypis['state'] = tk.NORMAL
            self.przycisk_smierc['state'] = tk.NORMAL
        
        elif self.i == 0:
            self.przycisk_nowy['state'] = tk.NORMAL
            self.przycisk_do_poczatku['state'] = tk.DISABLED
            self.przycisk_poprzedni['state'] = tk.DISABLED
            self.przycisk_nastepny['state'] = tk.DISABLED
            self.przycisk_do_konca['state'] = tk.DISABLED
            
            
    def szukaj(self):
        ## funkcja wyszukuje pacjentów, którzy znajdują się na SORze, a informacje o nich są przechowywane w Tkinterze
        ## po uruchomieniu funkcji menu przewija się do pacjenta o zadanym numerze PESEL
        ## w przypadku wypisu/przyjęciu na oddział/smierci - zwraca informację co się stało z pacjentem
        szukany_pesel = self.pole_wyszukiwarka.get()
        self.i = 0
        ilosc_wystapien = 0
        for element in self.lista:
            for czlon in element:
                if czlon == szukany_pesel: 
                    self.imie.set(element[0])
                    self.nazwisko.set(element[1])
                    self.pesel.set(element[2])
                    self.triaz.set(element[3])
                    self.etykieta_nr_wpisu.config(text = 'Osoba nr {} (z {})'.format(self.i + 1, len(self.lista)))
                    ilosc_wystapien += 1
            self.i += 1
            
        if ilosc_wystapien == 0:
            i = 0
            komunikat = 'brak danych o osobie o takim numerze PESEL'
            while i < len(self.lista_wypisanych):
                nazwisko = self.lista_wypisanych[i][0]
                imie = self.lista_wypisanych[i][1]
                pesel = self.lista_wypisanych[i][2]
                komentarz = self.lista_wypisanych[i][3]
                if pesel == szukany_pesel:
                    komunikat = (imie + " " + nazwisko + "\n" + "numer PESEL: " + pesel + "\n"+ komentarz)
                i += 1
            messagebox.showinfo('Informacje o pacjencie: ', komunikat)
            
        
        if self.i > 1:
            self.przycisk_nastepny['state'] = tk.NORMAL
            self.przycisk_do_konca['state'] = tk.NORMAL
            self.przycisk_usun['state'] = tk.NORMAL
            self.przycisk_zatwierdz['state'] = tk.NORMAL
            self.przycisk_nowy['state'] = tk.NORMAL
            self.przycisk_do_poczatku['state'] = tk.NORMAL
            self.przycisk_poprzedni['state'] = tk.NORMAL
                
        elif self.i == 1:
            self.przycisk_usun['state'] = tk.NORMAL
            self.przycisk_zatwierdz['state'] = tk.NORMAL
            self.przycisk_nowy['state'] = tk.NORMAL
            
        elif self.i == 0:
            self.przycisk_nowy['state'] = tk.NORMAL
            self.przycisk_do_poczatku['state'] = tk.DISABLED
            self.przycisk_poprzedni['state'] = tk.DISABLED
            if len(self.lista) > 1:
                self.przycisk_nastepny['state'] = tk.NORMAL
                self.przycisk_do_konca['state'] = tk.NORMAL
            else:
                self.przycisk_nastepny['state'] = tk.DISABLED
                self.przycisk_do_konca['state'] = tk.DISABLED


    def zmiana_koloru_in(self, event):
        self['bg'] = self.fcolor 
    
    
    def zmiana_koloru_out(self, event):
        self['bg'] = self.tlo 
        
        
def main():
    okno_glowne = tk.Tk() 
    okno_glowne.title('SOR')  
    ramka = SOR(okno_glowne, fcolor = 'light blue', background = 'light blue') 
    ramka.pack()
    okno_glowne.mainloop()
    
    
main()