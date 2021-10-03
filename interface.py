from tkinter import *
from tkinter import ttk
from prediction import Predict
from converter import Converter


class App:
    def __init__(self):
        self.cur_obj = Predict()
        self.converter_obj = Converter()

        self.list_cur = self.cur_obj.currencies()
        self.list_cur_converter = self.converter_obj.list_currencies()

        self.window = Tk()
        self.window.geometry('1000x500')

        self.info_label = Label(self.window, text='Выбери валюту для предсказания', padx=100)
        self.lb = Listbox(width=30, selectmode='SINGLE')
        self.lb_predict = Listbox(height=1, width=30)

        self.show_cur_button = Button(self.window, width=20, text="Показать валюты", command=self.show_predict_list)
        self.hide_cur_button = Button(self.window, width=20, text="Скрыть валюты", command=self.hide_predict_list)
        self.predict_cur_button = Button(self.window, width=20, text="предсказать валюту", command=self.predict_cur)
        self.label_of_predict = Label(self.window, text='Ожидаемый курс на завтра:')

        self.label_of_volume = Label(self.window, text='Объём валюты:')
        self.label_of_choose_first = Label(self.window, text='Из какой валюты:')
        self.label_of_choose_second = Label(self.window, text='В какую валюту:')
        self.volume = Entry(self.window)
        self.comboExample_first = ttk.Combobox(self.window,
                                               values=self.list_cur_converter)
        self.comboExample_second = ttk.Combobox(self.window,
                                                values=self.list_cur_converter)
        self.print_result = Button(self.window, width=20, text="Конвертировать", command=self.converter)

        self.label_of_predict.grid(column=1, row=5)
        self.info_label.grid(column=1, row=0, columnspan=2)
        self.show_cur_button.grid(column=1, row=1, columnspan=2)
        self.hide_cur_button.grid(column=1, row=2, columnspan=2)
        self.lb.grid(column=1, row=3, columnspan=2)
        self.predict_cur_button.grid(column=1, row=4, columnspan=2)
        self.lb_predict.grid(column=2, row=5)
        self.label_of_volume.grid(column=3, row=0)
        self.label_of_choose_first.grid(column=3, row=1)
        self.label_of_choose_second.grid(column=3, row=2)
        self.volume.grid(column=4, row=0)
        self.comboExample_first.grid(column=4, row=1)
        self.comboExample_second.grid(column=4, row=2)
        self.print_result.grid(column=5, row=0)

        self.window.mainloop()

    def converter(self):
        volume = self.volume.get()
        from_cur = self.comboExample_first.get()
        to_cur = self.comboExample_second.get()
        self.label_result = Label(self.window, text=self.converter_obj.convert_cur(volume, from_cur, to_cur))
        self.label_result.grid(column=5, row=1)

    def show_predict_list(self):
        for cur in self.list_cur:
            self.lb.insert(END, cur)

    def hide_predict_list(self):
        self.lb.delete(0, END)

    def predict_cur(self):
        self.lb_predict.delete(0, END)
        select_cur = self.lb.curselection()
        try:
            get_select = self.lb.get(select_cur)
        except TclError:
            return

        try:
            predict_cur_result = self.cur_obj.get_prediction(get_select)
        except ValueError:
            self.lb_predict.insert(END, "Нет информации о валюте")
            return
        self.lb_predict.insert(END, str(predict_cur_result))


test = App()
