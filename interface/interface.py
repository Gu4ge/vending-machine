import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showwarning
from datetime import date, datetime
from matplotlib.figure import Figure
import pandas as pd
from pandastable import Table
import csv
from pyowm import OWM
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# считывание влажности и температуры в городе
def get_temp_moisture():
    owm = OWM('0a070c6851d842137f5087b8422bacf4')
    mgr = owm.weather_manager()
    observation = mgr.weather_at_place('Moscow, RU')
    w = observation.weather
    return [round(w.temperature('celsius')['temp']), w.humidity]

DF_ADMIN = pd.read_excel("data/data.xlsx", index_col="index")  # датафрейм для админа
information = list()
TEMP_MOISTURE = get_temp_moisture()

    
    
class admin:
    
    #создание окна администратора
    def click_admin_button(self):
        self.window_admin = tk.Tk()
        self.window_admin.grab_set()
        self.window_admin.title("админ")
        self.window_admin.geometry("440x240")
        
        ttk.Label(self.window_admin, text=f"дата: {date.today()}").pack()
        
        self.df_weather = pd.read_csv('data/weather.csv', delimiter=',')
        
        t = TEMP_MOISTURE[0] + self.df_weather["temp"][0]
        m = TEMP_MOISTURE[1] + self.df_weather["moisture"][0]
        
        self.label1 = ttk.Label(self.window_admin, text=f"{t}°C")
        self.label1.pack()
        self.label2 = ttk.Label(self.window_admin, text=f"{m}%")
        self.label2.pack()
        
        self.btn_statistics = tk.Button(self.window_admin, text="посмотреть статистику", command=self.get_statistics)
        self.btn_statistics.pack()
        self.btn_change = tk.Button(self.window_admin, text="внести изменения", command=self.change_products)
        self.btn_change.pack()
        
        scale_temp = ttk.Scale(self.window_admin, from_=-10, to=10, value=self.df_weather["temp"][0], command=self.change_temp)
        scale_temp.pack()
        scale_moisture = ttk.Scale(self.window_admin, from_=-10, to=10, value=self.df_weather["moisture"][0], command=self.change_moisture)
        scale_moisture.pack()
        self.btn_destroy_wadmin = tk.Button(self.window_admin, text="назад", command=self.window_admin.destroy)
        self.btn_destroy_wadmin.pack()
        
        # вывод предупреждений
        if t < 10:
            showwarning(title="Предупреждение", message="температура ниже 10°C")
        elif t > 30:
            showwarning(title="Предупреждение", message="температура выше 30°C")
        
        if m < 45:
            showwarning(title="Предупреждение", message="влажнотсь ниже 45%")
        elif m > 65:
            showwarning(title="Предупреждение", message="влажность выше 65%")
        
        lst = list()
        tmp_index = 1   
        for i in DF_ADMIN['срок хранения']:
            tmp = str(i).split()
            d = datetime(int(tmp[2]), int(tmp[1]), int(tmp[0]))
            if d <= datetime.now():
                lst.append(tmp_index)
            tmp_index += 1
        
        if len(lst) != 0:
            showwarning(title="Предупреждение", message=f"истек срок годности в ячейках: {lst}")
        
        lst1 = list()
        tmp_index1 = 1   
        for i in DF_ADMIN['количество']:
            if i == 0:
                lst1.append(tmp_index1)
            tmp_index1 += 1
        
        if len(lst1) != 0:
            showwarning(title="Предупреждение", message=f"кончился товар в ячейках: {lst1}")
    
    # изменение температуры
    def change_temp(self, value):
        self.label1.config(text=f"{TEMP_MOISTURE[0] + round(float(value))}°C")
        self.df_weather['temp'] = round(float(value))
        self.df_weather.to_csv('data/weather.csv', index=False)
        
    # изменение влажности
    def change_moisture(self, value):
        self.label2.config(text=f"{TEMP_MOISTURE[1] + round(float(value))}%")
        self.df_weather['moisture'] = round(float(value))
        self.df_weather.to_csv('data/weather.csv', index=False)
    
    # вывод окна статистики
    def get_statistics(self):
        self.window_statics = tk.Tk()
        self.window_statics.title("статистика")
        self.window_statics.geometry("440x340")
        df_stat_bill = pd.read_csv("data/bill.csv", delimiter='\t')
        
        frame = tk.Frame(self.window_statics)
        frame.pack(anchor='nw', side="left")
        
        df1 = df_stat_bill["название"].value_counts()# самый популярный товар
        df1 = df1.reset_index()
        ttk.Label(frame, text="популярный товар").pack()
        
        df2 = df_stat_bill["тип"].value_counts() # самый популярный тип товара
        df2 = df2.reset_index()
        ttk.Label(frame, text="популярный тип товара").pack()
        
        df4 = df_stat_bill["цена"].sum() 
        ttk.Label(frame, text="заработано").pack() # сколько заработано
        
        frame1 = tk.Frame(self.window_statics)
        frame1.pack(anchor='n', side="top")
        ttk.Label(frame1, text=df1["название"][0]).pack()
        ttk.Label(frame1, text=df2["тип"][0]).pack()
        ttk.Label(frame1, text=df4).pack()

        self.btn_clear = tk.Button(self.window_statics, text="очистить", command=self.clear_stat).pack()
        
        # вывод графика количества купленных товаров
        fig = Figure(figsize=(6, 4))
        ax = fig.add_subplot(111)
        df_stat_bill["название"].value_counts().plot(kind='bar', ax=ax)
        ax.set_title("Количество товаров")
        ax.set_xlabel("Товар")
        ax.set_ylabel("Количество")

        canvas = FigureCanvasTkAgg(fig, master=self.window_statics)
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        canvas.draw()
        
        
        
    # очистить статистику    
    def clear_stat(self):
        df = pd.DataFrame(columns=['ячейка','тип','название','цена'])
        df.to_csv("data/bill.csv", sep='\t', index=False, encoding='utf-8')
    
    # изменение определенного продукта
    def change_data(self):
        DF_ADMIN.loc[int(self.information[0])-1] = [self.information[0], self.information[1], self.information[2], self.information[3], self.information[4], self.information[5]]
        DF_ADMIN.to_excel("data/data.xlsx")

    # сбор данных на на изменение продукта
    def append_data(self, event):
        self.information = []
        self.information.append(int(self.combobox.get()))
        self.information.append(self.combobox1.get())
        self.information.append(self.productname.get())
        self.information.append(self.storagelif.get())
        self.information.append(int(self.combobox2.get()))
        self.information.append(int(self.productprice.get()))
        
    # функция изменения параметров продукта
    def selected(self, event):
        self.textinformation = ["тип продукта", "название", "срок годности", "количество", "цена"]
        self.cellproduct = str(self.combobox.get())
        
        self.window_select = tk.Tk()
        self.window_select.title("изменение")
        self.window_select.geometry('400x200')
        
        self.frame1 = tk.Frame(self.window_select)
        self.frame1.pack(anchor='nw', side="left")
        for i in range(5):
            self.labeltmp = ttk.Label(self.frame1, text=self.textinformation[i])
            self.labeltmp.pack()
        
        self.frame2 = tk.Frame(self.window_select)
        self.frame2.pack(anchor='n', side="top")
        
        self.typeofproduct = ["еда", "напиток"]
        self.combobox1 = ttk.Combobox(self.frame2, values=self.typeofproduct, state="readonly")
        self.combobox1.set(DF_ADMIN.loc[int(self.cellproduct)-1, "тип"])
        self.combobox1.pack()
        
        self.combobox1.bind("<<ComboboxSelected>>", self.append_data)
        
        self.productname = ttk.Entry(self.frame2)
        self.productname.insert(0, DF_ADMIN.loc[int(self.cellproduct)-1, "название"])
        self.productname.pack()
        self.productname.bind("<Leave>", self.append_data)
        
        self.storagelif = ttk.Entry(self.frame2)
        self.storagelif.insert(0, DF_ADMIN.loc[int(self.cellproduct)-1, "срок хранения"])
        self.storagelif.pack()
        self.storagelif.bind("<Leave>", self.append_data)
        
        
        self.productcount = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "0"]
        self.combobox2 = ttk.Combobox(self.frame2, values=self.productcount, state="readonly")
        self.combobox2.set(DF_ADMIN.loc[int(self.cellproduct)-1, "количество"])
        self.combobox2.pack()
        self.combobox2.bind("<<ComboboxSelected>>", self.append_data)
        
        self.productprice = ttk.Entry(self.frame2)
        self.productprice.insert(0, DF_ADMIN.loc[int(self.cellproduct)-1, "цена"])
        self.productprice.pack()
        self.productprice.bind("<Leave>", self.append_data)
        
        tk.Button(self.frame2, text="изменить", command=self.change_data).pack()
    
    # создания окна изменения продукта
    def change_products(self):
        self.window_change = tk.Tk()
        self.window_change.title("предварительная сводка")
        self.frame = tk.Frame(self.window_change)
        self.frame.pack()
        self.pt = Table(self.frame, dataframe=DF_ADMIN, height=440, width=550)
        self.pt.show()
        
        self.label = ttk.Label(self.window_change, text="выберите номер ячейки")
        self.label.pack()
        
        self.colls = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20"]
        self.combobox = ttk.Combobox(self.window_change, values=self.colls, state="readonly")
        self.combobox.pack()
        self.combobox.bind("<<ComboboxSelected>>", self.selected)
        self.btn_destroy_wchange = tk.Button(self.window_change, text="назад", command=self.window_change.destroy)
        self.btn_destroy_wchange.pack()
        
    
    
class user:
    # создание окна пользователся
    def click_user_button(self):
        # датафрейм с нормальным сроком годности и количеством > 0
        DF_USER = DF_ADMIN[(DF_ADMIN["количество"] != 0) & (DF_ADMIN['срок хранения'].apply(self.check_date) == True)]
        DF_USER = DF_USER[["ячейка", "название", "цена"]]
                
        self.window_user = tk.Tk()
        self.window_user.title("покупатель")
        self.window_user.geometry("340x440")
        self.frame = tk.Frame(self.window_user)
        self.frame.pack(fill="both", expand=True)
        
        self.pt = Table(self.frame, dataframe=DF_USER)
        self.pt.show()
        
        self.btn_user = tk.Button(self.window_user, text="купить товар", command=self.buy_product)
        self.btn_user.pack()
        self.btn_destroy_wuser = tk.Button(self.window_user, text="назад", command=self.window_user.destroy)
        self.btn_destroy_wuser.pack()
    
    # проверка на срок годности
    def check_date(self, date):
        d = datetime.strptime(date, '%d %m %Y')
        return d >= datetime.now()
        
    # создание окна покупки
    def buy_product(self):
        self.window_buying = tk.Tk()
        self.window_buying.title("покупка")
        self.window_buying.geometry("240x140")
        self.label = ttk.Label(self.window_buying, text="выберите номер ячейки")
        self.label.pack()
        
        df = DF_ADMIN[(DF_ADMIN["количество"] != 0) & (DF_ADMIN['срок хранения'].apply(self.check_date) == True)]
        df = df["ячейка"].to_string(index=False)
        
        # выбор ячейки
        self.colls = df[5:]
        self.combobox = ttk.Combobox(self.window_buying, values=self.colls, state="readonly")
        self.combobox.pack()
        self.combobox.bind("<<ComboboxSelected>>", self.selected)
    
    # создание окна определенной ячейки для покупки
    def selected(self, event):
        id_product = self.combobox.get()
        
        DF_ADMIN.loc[int(id_product)-1, "количество"] -= 1
        DF_ADMIN.to_excel("data/data.xlsx")
        
        # запись покупки для дальнейшей статистики
        with open("data/bill.csv", mode="a", encoding="utf-8") as f:
            file_writer = csv.writer(f, delimiter = "\t")
            file_writer.writerow([id_product, DF_ADMIN.loc[int(id_product)-1, "тип"], DF_ADMIN.loc[int(id_product)-1, "название"], DF_ADMIN.loc[int(id_product)-1, "цена"]])
        
        # подтверждение оплаты
        ttk.Label(self.window_buying, text="успешно!").pack()
    
# главное меню    
administrator = admin()
person = user() 

window = tk.Tk()
window.title("главное окно")
window.geometry("240x140")

btn_admin = tk.Button(window, text="войти как администратор", command=administrator.click_admin_button)
btn_user = tk.Button(window, text="войти как пользователь", command=person.click_user_button)
btn_exit = tk.Button(window, text="выйти", command=window.destroy)
btn_admin.pack()
btn_user.pack()
btn_exit.pack()

window.mainloop()