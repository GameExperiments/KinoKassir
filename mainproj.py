# Кинокассир
# Проект Ляхницкого Сергея для Лицея Академии Яндекса

import sqlite3 # Библиотека для работы с базой данных
import sys # Библиотека для работы с переменными окружения

from PyQt5.QtCore import * # Библиотека для работы с приложением
from PyQt5.QtGui import * # Библиотека для работы с графикой
from PyQt5.QtWidgets import * # Библиотека для работы с виджетами

from UIs.createUI import Ui_Form as createUI # Импорт интерфейса создания сеанса
from UIs.deleteUI import Ui_Form as deleteUI # Импорт интерфейса удаления сеанса
from UIs.mainpageUI import Ui_Form as mainpageUI # Импорт интерфейса главной страницы
from UIs.returnUI import Ui_Form as returnUI # Импорт интерфейса возврата билетов
from UIs.sellUI import Ui_Form as sellUI # Импорт интерфейса продажи билетов


class mainpage(QMainWindow, mainpageUI): # Главное окно
    def __init__(self): # Параметры окна
        super().__init__()
        self.setupUi(self) # Инициализация интерфейса
        self.setWindowIcon(QIcon('images\icon.png')) # Иконка окна
        self.setWindowTitle("Кинокассир") # Название окна
        self.setWindowFlags(Qt.WindowCloseButtonHint) # Кнопка закрытия окна
        self.setFixedSize(self.size()) # Фиксированный размер окна
        pixmap = QPixmap('images\logo.png') # Логотип
        self.label.setPixmap(pixmap) # Установка логотипа
        self.pushButton.clicked.connect(self.createprocess) # Создание сеанса
        self.pushButton_3.clicked.connect(self.deleteprocess) # Удаление сеанса
        self.pushButton_2.clicked.connect(self.sellprocess) # Продажа билета
        self.pushButton_4.clicked.connect(self.returnprocess) # Возврат билета

    def createprocess(self): # Открытие окна создания сеанса
        self.cams = create() # Создание окна
        self.cams.show() # Открытие окна
        self.close() # Закрытие текущего окна

    def deleteprocess(self): # Открытие окна удаления сеанса
        self.cams = delete() # Создание окна
        self.cams.show() # Открытие окна
        self.close() # Закрытие текущего окна

    def sellprocess(self): # Открытие окна продажи билета
        self.cams = sell() # Создание окна
        self.cams.show() # Открытие окна
        self.close() # Закрытие текущего окна

    def returnprocess(self): # Открытие окна возврата билета
        self.cams = returnpage() # Создание окна
        self.cams.show() # Открытие окна
        self.close() # Закрытие текущего окна


class create(QMainWindow, createUI): # Создание сеанса
    def __init__(self): # Параметры окна
        super().__init__()
        self.setupUi(self) # Инициализация интерфейса
        self.setWindowTitle("Создание сеанса") # Название окна
        self.setWindowFlags(Qt.WindowCloseButtonHint) # Кнопка закрытия окна
        self.setFixedSize(self.size()) # Фиксированный размер окна
        self.setWindowIcon(QIcon('images\icon.png')) # Иконка окна
        self.buttonBox.accepted.connect(self.finish) # Кнопка подтверждения
        self.buttonBox.rejected.connect(self.goMainWindow) # Кнопка отмены
        self.dateEdit.setDateTime(QDateTime.currentDateTime()) # Текущая дата
        self.comboBox.addItems(["Зал 1", "Зал 2", "Зал 3", "Зал 4", "Зал 5", "Зал 6", "Зал 7", "Зал 8", "Зал 9", "Зал 10"]) # Залы
        self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(False) # Отключение кнопки подтверждения
        self.buttonBox.button(QDialogButtonBox.Ok).setText("Создать") # Изменение текста кнопки подтверждения
        self.buttonBox.button(QDialogButtonBox.Cancel).setText("Отмена") # Изменение текста кнопки отмены
        self.dateEdit.dateTimeChanged.connect(self.text_changed) # Отправка сигнала при изменении даты
        self.lineEdit.textChanged.connect(self.text_changed) # Отправка сигнала при изменении времени
        self.comboBox.currentTextChanged.connect(self.text_changed) # Отправка сигнала при изменении зала
    
    def text_changed(self): # Проверка на ввод данных
        sq = sqlite3.connect("allinfo.db") # Подключение к базе данных
        cur = sq.cursor() # Создание курсора
        allmovies = cur.execute(f"SELECT date FROM movies WHERE room_name='{self.comboBox.currentText()}'").fetchall() # Получение всех дат
        allrooms = cur.execute(f"SELECT room_name FROM movies WHERE date='{self.dateEdit.dateTime()}'").fetchall() # Получение всех залов
        if self.lineEdit.text() == "" or self.dateEdit.dateTime() <= QDateTime.currentDateTime(): # Проверка на ввод данных
            self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(False) # Отключение кнопки подтверждения
        elif len(allmovies) != 0 or len(allrooms) != 0: # Проверка на наличие повторов
            self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(False) # Отключение кнопки подтверждения
        else: # Если все введено верно
            self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(True) # Включение кнопки подтверждения
        
    def goMainWindow(self): # Переход на главное окно
        self.cams = mainpage() # Создание окна
        self.cams.show() # Открытие окна
        self.close() # Закрытие текущего окна

    def finish(self): # Создание сеанса
        con = sqlite3.connect("allinfo.db") # Подключение к базе данных
        cur = con.cursor() # Создание курсора
        room = self.comboBox.currentText() # Зал
        cur.execute(f"INSERT INTO movies(name,date,room_name) VALUES('{self.lineEdit.text()}','{self.dateEdit.text()}','{room}')") # Вставка данных
        con.commit() # Сохранение изменений
        self.goMainWindow() # Переход на главное окно


class delete(QMainWindow, deleteUI): # Удаление сеанса
    def __init__(self): # Параметры окна
        super().__init__()
        self.setupUi(self) # Инициализация интерфейса
        self.setWindowTitle("Удаление сеанса") # Заголовок окна
        self.setWindowFlags(Qt.WindowCloseButtonHint) # Кнопка закрытия окна
        self.setFixedSize(self.size()) # Фиксированный размер окна
        self.setWindowIcon(QIcon('images\icon.png')) # Иконка окна
        self.buttonBox.button(QDialogButtonBox.Ok).setText("Удалить") # Изменение текста кнопки подтверждения
        self.buttonBox.button(QDialogButtonBox.Cancel).setText("Отмена") # Изменение текста кнопки отмены
        self.buttonBox.accepted.connect(self.finish) # Отправка сигнала при подтверждении
        self.buttonBox.rejected.connect(self.goMainWindow) # Отправка сигнала при отмене
        self.calendarWidget.clicked.connect(self.calendar_clicked) # Отправка сигнала при выборе даты
        self.comboBox.currentTextChanged.connect(self.calendar_clicked) # Отправка сигнала при изменении зала
        self.listView.clicked.connect(self.list_clicked) # Отправка сигнала при выборе сеанса
        self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(False) # Отключение кнопки подтверждения
        sq = sqlite3.connect("allinfo.db") # Подключение к базе данных
        cur = sq.cursor() # Создание курсора
        allmovies = cur.execute("SELECT name FROM movies") # Получение всех фильмов
        allnames = [] # Список всех названий фильмов
        for i in allmovies.fetchall():
            if i[0] not in allnames: # Проверка на наличие повторов
                allnames.append(i[0]) # Добавление в список
        self.comboBox.addItems(allnames) # Добавление в комбобокс всех названий фильмов
    
    def finish(self): # Удаление сеанса
        con = sqlite3.connect("allinfo.db") # Подключение к базе данных
        cur = con.cursor() # Создание курсора
        chosen_path = self.listView.currentIndex().data() # Получение информации о выбранном сеансе
        room_id = chosen_path.split(";")[1].strip().split()[1] # Получение id зала
        movie_id = cur.execute(f'SELECT id FROM movies WHERE date="{self.calendarWidget.selectedDate().toString("dd.MM.yyyy")}" AND room_name="Зал {room_id}"').fetchall()[0][0] # Получение id фильма
        cur.execute(f"DELETE FROM tickets WHERE movie_id='{movie_id}'") # Удаление билетов
        cur.execute(f"DELETE FROM movies WHERE id='{movie_id}'") # Удаление сеанса
        con.commit() # Сохранение изменений
        self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(False) # Отключение кнопки подтверждения
        self.calendar_clicked() # Обновление списка сеансов

    def calendar_clicked(self): # Нажатие на календарь
        self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(False) # Отключение кнопки подтверждения
        if self.comboBox.currentText() != "" and self.calendarWidget.selectedDate().toString("dd.MM.yyyy") != "": # Проверка на выбор даты и зала
            con = sqlite3.connect("allinfo.db") # Подключение к базе данных
            cur = con.cursor() # Создание курсора
            movie_name = self.comboBox.currentText() # Получение названия фильма
            movie_date = self.calendarWidget.selectedDate().toString("dd.MM.yyyy") # Получение даты
            movie_id = cur.execute(f'SELECT id FROM movies WHERE name="{movie_name}" AND date="{movie_date}"').fetchall() # Получение id фильма
            model_for_list = QStandardItemModel() # Создание модели для списка
            for i in movie_id: # Перебор всех id фильмов
                took_seats = cur.execute(f'SELECT took_seats FROM movies WHERE id="{i[0]}"').fetchall() # Получение занятых мест
                roomname = cur.execute(f'SELECT room_name FROM movies WHERE id="{i[0]}"').fetchall()[0][0] # Получение названия зала
                roomname = roomname.split(" ")[1] # Получение номера зала
                allplaces = 0 # Количество занятых мест
                for j in took_seats: # Перебор всех занятых мест
                    try: # На случай ошибки split
                        for g in j[0].split(): # Перебор всех занятых мест
                            allplaces += 1 # Увеличение количества мест
                    except Exception: # В случае ошибки
                        pass # Пропуск
                model_for_list.appendRow(QStandardItem(f"ID сеанса: {i[0]}; Зал: {roomname}; Занято мест: {allplaces}")) # Добавление в список
            self.listView.setModel(model_for_list) # Установка модели для списка
            self.listView.setEditTriggers(QAbstractItemView.NoEditTriggers) # Отключение редактирования списка
    
    def list_clicked(self): # Нажатие на список
        self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(True) # Включение кнопки подтверждения

    def goMainWindow(self): # Переход на главное окно
        self.cams = mainpage() # Создание объекта главного окна
        self.cams.show() # Показ главного окна
        self.close() # Закрытие текущего окна


class sell(QMainWindow, sellUI): # продажа билета
    def __init__(self): # Параметры окна
        super().__init__()
        self.setupUi(self) # Инициализация интерфейса
        self.setWindowFlags(Qt.WindowCloseButtonHint) # Кнопка закрытия окна
        self.setFixedSize(self.size()) # Фиксация размера окна
        self.setWindowIcon(QIcon('images\icon.png')) # Иконка окна
        self.setWindowTitle("Продажа билета") # Заголовок окна
        self.selected_seats = [] # Список выбранных мест
        self.num = 0 # Количество выбранных мест
        self.selected_room_name = '' # Название выбранного зала
        self.lineEdit.textChanged.connect(self.text_changed) # Сигнал изменения текста в поле ввода
        self.pushButton_3.clicked.connect(self.click) # Сигнал нажатия на кнопку места
        self.pushButton_4.clicked.connect(self.click) # Сигнал нажатия на кнопку места
        self.pushButton_5.clicked.connect(self.click) # Сигнал нажатия на кнопку места
        self.pushButton_6.clicked.connect(self.click) # Сигнал нажатия на кнопку места
        self.pushButton_7.clicked.connect(self.click) # Сигнал нажатия на кнопку места
        self.pushButton_8.clicked.connect(self.click) # Сигнал нажатия на кнопку места
        self.pushButton_9.clicked.connect(self.click) # Сигнал нажатия на кнопку места
        self.pushButton_10.clicked.connect(self.click) # Сигнал нажатия на кнопку места
        self.pushButton_11.clicked.connect(self.click) # Сигнал нажатия на кнопку места
        self.pushButton_12.clicked.connect(self.click) # Сигнал нажатия на кнопку места
        self.pushButton_13.clicked.connect(self.click) # Сигнал нажатия на кнопку места
        self.pushButton_14.clicked.connect(self.click) # Сигнал нажатия на кнопку места
        self.pushButton_15.clicked.connect(self.click) # Сигнал нажатия на кнопку места
        self.pushButton_16.clicked.connect(self.click) # Сигнал нажатия на кнопку места
        self.pushButton_17.clicked.connect(self.click) # Сигнал нажатия на кнопку места
        self.pushButton_18.clicked.connect(self.click) # Сигнал нажатия на кнопку места
        self.pushButton_19.clicked.connect(self.click) # Сигнал нажатия на кнопку места
        self.pushButton_20.clicked.connect(self.click) # Сигнал нажатия на кнопку места
        self.pushButton_21.clicked.connect(self.click) # Сигнал нажатия на кнопку места
        self.pushButton_22.clicked.connect(self.click) # Сигнал нажатия на кнопку места
        self.pushButton_23.clicked.connect(self.click) # Сигнал нажатия на кнопку места
        self.pushButton_24.clicked.connect(self.click) # Сигнал нажатия на кнопку места
        if True: # Заглушка для возможности скрыть эту часть кода
            self.pushButton_3.setEnabled(False) # Отключение кнопки места
            self.pushButton_3.setStyleSheet("background-color: rgb(255, 255, 255);") # Стиль кнопки места
            self.pushButton_4.setEnabled(False) # Отключение кнопки места
            self.pushButton_4.setStyleSheet("background-color: rgb(255, 255, 255);") # Стиль кнопки места
            self.pushButton_5.setEnabled(False) # Отключение кнопки места
            self.pushButton_5.setStyleSheet("background-color: rgb(255, 255, 255);") # Стиль кнопки места
            self.pushButton_6.setEnabled(False) # Отключение кнопки места
            self.pushButton_6.setStyleSheet("background-color: rgb(255, 255, 255);") # Стиль кнопки места
            self.pushButton_7.setEnabled(False) # Отключение кнопки места
            self.pushButton_7.setStyleSheet("background-color: rgb(255, 255, 255);") # Стиль кнопки места
            self.pushButton_8.setEnabled(False) # Отключение кнопки места
            self.pushButton_8.setStyleSheet("background-color: rgb(255, 255, 255);") # Стиль кнопки места
            self.pushButton_9.setEnabled(False) # Отключение кнопки места
            self.pushButton_9.setStyleSheet("background-color: rgb(255, 255, 255);") # Стиль кнопки места
            self.pushButton_10.setEnabled(False) # Отключение кнопки места
            self.pushButton_10.setStyleSheet("background-color: rgb(255, 255, 255);") # Стиль кнопки места
            self.pushButton_11.setEnabled(False) # Отключение кнопки места
            self.pushButton_11.setStyleSheet("background-color: rgb(255, 255, 255);") # Стиль кнопки места
            self.pushButton_12.setEnabled(False) # Отключение кнопки места
            self.pushButton_12.setStyleSheet("background-color: rgb(255, 255, 255);") # Стиль кнопки места
            self.pushButton_13.setEnabled(False) # Отключение кнопки места
            self.pushButton_13.setStyleSheet("background-color: rgb(255, 255, 255);") # Стиль кнопки места
            self.pushButton_14.setEnabled(False) # Отключение кнопки места
            self.pushButton_14.setStyleSheet("background-color: rgb(255, 255, 255);") # Стиль кнопки места
            self.pushButton_15.setEnabled(False) # Отключение кнопки места
            self.pushButton_15.setStyleSheet("background-color: rgb(255, 255, 255);") # Стиль кнопки места
            self.pushButton_16.setEnabled(False) # Отключение кнопки места
            self.pushButton_16.setStyleSheet("background-color: rgb(255, 255, 255);") # Стиль кнопки места
            self.pushButton_17.setEnabled(False) # Отключение кнопки места
            self.pushButton_17.setStyleSheet("background-color: rgb(255, 255, 255);") # Стиль кнопки места
            self.pushButton_18.setEnabled(False) # Отключение кнопки места
            self.pushButton_18.setStyleSheet("background-color: rgb(255, 255, 255);") # Стиль кнопки места
            self.pushButton_19.setEnabled(False) # Отключение кнопки места
            self.pushButton_19.setStyleSheet("background-color: rgb(255, 255, 255);") # Стиль кнопки места
            self.pushButton_20.setEnabled(False) # Отключение кнопки места
            self.pushButton_20.setStyleSheet("background-color: rgb(255, 255, 255);") # Стиль кнопки места
            self.pushButton_21.setEnabled(False) # Отключение кнопки места
            self.pushButton_21.setStyleSheet("background-color: rgb(255, 255, 255);") # Стиль кнопки места
            self.pushButton_22.setEnabled(False) # Отключение кнопки места
            self.pushButton_22.setStyleSheet("background-color: rgb(255, 255, 255);") # Стиль кнопки места
            self.pushButton_23.setEnabled(False) # Отключение кнопки места
            self.pushButton_23.setStyleSheet("background-color: rgb(255, 255, 255);") # Стиль кнопки места
            self.pushButton_24.setEnabled(False) # Отключение кнопки места
            self.pushButton_24.setStyleSheet("background-color: rgb(255, 255, 255);") # Стиль кнопки места
        self.listView.clicked.connect(self.tabletka) # При нажатии на зал в списке залов
        self.buttonBox.accepted.connect(self.accept) # При нажатии на кнопку подтверждения
        self.buttonBox.rejected.connect(self.goMainWindow) # При нажатии на кнопку отмены
        self.buttonBox.button(QDialogButtonBox.Ok).setText("Продать") # Переименование кнопки подтверждения
        self.buttonBox.button(QDialogButtonBox.Cancel).setText("Отмена") # Переименование кнопки отмены
        self.calendarWidget.clicked.connect(self.calendar_clicked) # При нажатии на календарь
        self.spinBox_2.valueChanged.connect(self.spinBox_value_changed) # При изменении значения спинбокса
        self.selected_movie = self.comboBox.currentText() # Выбранный фильм
        self.calendar_clicked()
        self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(False) # Отключение кнопки подтверждения
        self.spinBox.valueChanged.connect(self.spinBox_value_changed) # При изменении значения спинбокса
        self.comboBox.currentIndexChanged.connect(self.comboBox_current_index_changed) # При изменении выбранного фильма
        sq = sqlite3.connect("allinfo.db") # Подключение к базе данных
        cur = sq.cursor() # Создание курсора
        allmovies = cur.execute("SELECT name FROM movies") # Выбор всех фильмов
        allnames = [] # Список всех названий фильмов
        for i in allmovies.fetchall(): # Перебор всех фильмов
            if i[0] not in allnames: # Если название фильма не в списке
                allnames.append(i[0]) # Добавление названия фильма в список
        self.comboBox.addItems(allnames) # Добавление в список всех названий фильмов
        if self.comboBox.currentText() == '': # Если список пуст
            self.calendarWidget.setEnabled(False) # Отключение календаря

    def spinBox_value_changed(self): # при изменении количества билетов
        if self.num != 0 and self.num == self.spinBox.value() + self.spinBox_2.value() and self.comboBox.currentText() != '' and self.lineEdit.text() != '': # Проверка на совпадение количества билетов
            self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(True) # Включение кнопки подтверждения
        else: # Если не совпадают
            self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(False) # Отключение кнопки подтверждения

    def comboBox_current_index_changed(self): # при изменении фильма в комбобоксе
        self.selected_room_name = '' # Обнуление названия выбранного зала
        self.calendarWidget.setEnabled(True) # Включение календаря
        con = sqlite3.connect("allinfo.db") # Подключение к базе данных
        cur = con.cursor() # Создание курсора
        curDate = self.calendarWidget.selectedDate().toString("dd.MM.yyyy") # Выбранная дата
        cur.execute(f"SELECT * FROM movies WHERE name='{self.comboBox.currentText()}' AND date='{curDate}'") # Выбор всех залов в выбранную дату
        allmovies = cur.fetchall() # Все залы в выбранную дату
        self.model_for_list = QStandardItemModel(len(allmovies), 1) # Создание модели для списка
        self.listView.setModel(self.model_for_list) # Установка модели для списка
        self.listView.setEditTriggers(QAbstractItemView.NoEditTriggers) # Отключение редактирования списка
        if len(allmovies) != 0: # Если есть залы
            for i in range(len(allmovies)): # Перебор всех залов
                self.model_for_list.setItem(i, 0, QStandardItem(allmovies[i][3])) # Добавление названия зала в список
        if True: # Заглушка для возможности скрыть эту часть кода
            self.pushButton_3.setEnabled(False) # Отключение кнопки места
            self.pushButton_3.setStyleSheet("background-color: rgb(255, 255, 255);") # Сброс цвета кнопки
            self.pushButton_3.setText('14') # Сброс названия кнопки
            self.pushButton_4.setEnabled(False) # Отключение кнопки места
            self.pushButton_4.setStyleSheet("background-color: rgb(255, 255, 255);") # Сброс цвета кнопки
            self.pushButton_4.setText('13') # Сброс названия кнопки
            self.pushButton_5.setEnabled(False) # Отключение кнопки места
            self.pushButton_5.setStyleSheet("background-color: rgb(255, 255, 255);") # Сброс цвета кнопки
            self.pushButton_5.setText('1') # Сброс названия кнопки
            self.pushButton_6.setEnabled(False) # Отключение кнопки места
            self.pushButton_6.setStyleSheet("background-color: rgb(255, 255, 255);") # Сброс цвета кнопки
            self.pushButton_6.setText('2') # Сброс названия кнопки
            self.pushButton_7.setEnabled(False) # Отключение кнопки места
            self.pushButton_7.setStyleSheet("background-color: rgb(255, 255, 255);") # Сброс цвета кнопки
            self.pushButton_7.setText('3') # Сброс названия кнопки
            self.pushButton_8.setEnabled(False) # Отключение кнопки места
            self.pushButton_8.setStyleSheet("background-color: rgb(255, 255, 255);") # Сброс цвета кнопки
            self.pushButton_8.setText('12') # Сброс названия кнопки
            self.pushButton_9.setEnabled(False) # Отключение кнопки места
            self.pushButton_9.setStyleSheet("background-color: rgb(255, 255, 255);") # Сброс цвета кнопки
            self.pushButton_9.setText('6') # Сброс названия кнопки
            self.pushButton_10.setEnabled(False) # Отключение кнопки места
            self.pushButton_10.setStyleSheet("background-color: rgb(255, 255, 255);") # Сброс цвета кнопки
            self.pushButton_10.setText('5') # Сброс названия кнопки
            self.pushButton_11.setEnabled(False) # Отключение кнопки места
            self.pushButton_11.setStyleSheet("background-color: rgb(255, 255, 255);") # Сброс цвета кнопки
            self.pushButton_11.setText('4') # Сброс названия кнопки
            self.pushButton_12.setEnabled(False) # Отключение кнопки места
            self.pushButton_12.setStyleSheet("background-color: rgb(255, 255, 255);") # Сброс цвета кнопки
            self.pushButton_12.setText('11') # Сброс названия кнопки
            self.pushButton_13.setEnabled(False) # Отключение кнопки места
            self.pushButton_13.setStyleSheet("background-color: rgb(255, 255, 255);") # Сброс цвета кнопки
            self.pushButton_13.setText('7') # Сброс названия кнопки
            self.pushButton_14.setEnabled(False) # Отключение кнопки места
            self.pushButton_14.setStyleSheet("background-color: rgb(255, 255, 255);") # Сброс цвета кнопки
            self.pushButton_14.setText('8') # Сброс названия кнопки
            self.pushButton_15.setEnabled(False) # Отключение кнопки места
            self.pushButton_15.setStyleSheet("background-color: rgb(255, 255, 255);") # Сброс цвета кнопки
            self.pushButton_15.setText('10') # Сброс названия кнопки
            self.pushButton_16.setEnabled(False) # Отключение кнопки места
            self.pushButton_16.setStyleSheet("background-color: rgb(255, 255, 255);") # Сброс цвета кнопки
            self.pushButton_16.setText('19') # Сброс названия кнопки
            self.pushButton_17.setEnabled(False) # Отключение кнопки места
            self.pushButton_17.setStyleSheet("background-color: rgb(255, 255, 255);") # Сброс цвета кнопки
            self.pushButton_17.setText('18') # Сброс названия кнопки
            self.pushButton_18.setEnabled(False) # Отключение кнопки места
            self.pushButton_18.setStyleSheet("background-color: rgb(255, 255, 255);") # Сброс цвета кнопки
            self.pushButton_18.setText('17') # Сброс названия кнопки
            self.pushButton_19.setEnabled(False) # Отключение кнопки места
            self.pushButton_19.setStyleSheet("background-color: rgb(255, 255, 255);") # Сброс цвета кнопки
            self.pushButton_19.setText('9') # Сброс названия кнопки
            self.pushButton_20.setEnabled(False) # Отключение кнопки места
            self.pushButton_20.setStyleSheet("background-color: rgb(255, 255, 255);") # Сброс цвета кнопки
            self.pushButton_20.setText('15') # Сброс названия кнопки
            self.pushButton_21.setEnabled(False) # Отключение кнопки места
            self.pushButton_21.setStyleSheet("background-color: rgb(255, 255, 255);") # Сброс цвета кнопки
            self.pushButton_21.setText('16') # Сброс названия кнопки
            self.pushButton_22.setEnabled(False) # Отключение кнопки места
            self.pushButton_22.setStyleSheet("background-color: rgb(255, 255, 255);") # Сброс цвета кнопки
            self.pushButton_22.setText('20') # Сброс названия кнопки
            self.pushButton_23.setEnabled(False) # Отключение кнопки места
            self.pushButton_23.setStyleSheet("background-color: rgb(255, 255, 255);") # Сброс цвета кнопки
            self.pushButton_23.setText('21') # Сброс названия кнопки
            self.pushButton_24.setEnabled(False) # Отключение кнопки места
            self.pushButton_24.setStyleSheet("background-color: rgb(255, 255, 255);") # Сброс цвета кнопки
            self.pushButton_24.setText('22') # Сброс названия кнопки

    def calendar_clicked(self): # при нажатии на календарь
        self.selected_room_name = '' # Сброс названия комнаты
        if self.comboBox.currentText() != '': # Если выбрана комната
            con = sqlite3.connect("allinfo.db") # Подключение к базе данных
            cur = con.cursor() # Создание курсора
            curDate = self.calendarWidget.selectedDate().toString("dd.MM.yyyy") # Получение даты из календаря
            cur.execute(f"SELECT * FROM movies WHERE name='{self.comboBox.currentText()}' AND date='{curDate}'") # Выбор из базы данных всех фильмов выбранной комнаты на выбранную дату
            alldates = cur.fetchall() # Получение всех данных из базы данных
            self.model_for_list = QStandardItemModel(len(alldates), 1) # Создание модели для списка
            self.model_for_list.setHorizontalHeaderLabels(['Информация']) # Заголовок списка
            self.listView.setModel(self.model_for_list) # Установка модели для списка
            self.listView.setEditTriggers(QAbstractItemView.NoEditTriggers) # Запрет на редактирование списка
            if len(alldates) != 0: # Если есть данные в базе данных
                for i in range(len(alldates)): # Цикл по всем данным из базы данных
                    self.model_for_list.setItem(i, 0, QStandardItem(alldates[i][3])) # Заполнение списка данными из базы данных
        if True: # Заглушка для возможности скрыть эту часть кода
            self.pushButton_3.setEnabled(False) # Отключение кнопки места
            self.pushButton_3.setStyleSheet("background-color: rgb(255, 255, 255);") # Сброс цвета кнопки
            self.pushButton_3.setText('14') # Сброс названия кнопки
            self.pushButton_4.setEnabled(False) # Отключение кнопки места
            self.pushButton_4.setStyleSheet("background-color: rgb(255, 255, 255);") # Сброс цвета кнопки
            self.pushButton_4.setText('13') # Сброс названия кнопки
            self.pushButton_5.setEnabled(False) # Отключение кнопки места
            self.pushButton_5.setStyleSheet("background-color: rgb(255, 255, 255);") # Сброс цвета кнопки
            self.pushButton_5.setText('1') # Сброс названия кнопки
            self.pushButton_6.setEnabled(False) # Отключение кнопки места
            self.pushButton_6.setStyleSheet("background-color: rgb(255, 255, 255);") # Сброс цвета кнопки
            self.pushButton_6.setText('2') # Сброс названия кнопки
            self.pushButton_7.setEnabled(False) # Отключение кнопки места
            self.pushButton_7.setStyleSheet("background-color: rgb(255, 255, 255);") # Сброс цвета кнопки
            self.pushButton_7.setText('3') # Сброс названия кнопки
            self.pushButton_8.setEnabled(False) # Отключение кнопки места
            self.pushButton_8.setStyleSheet("background-color: rgb(255, 255, 255);") # Сброс цвета кнопки
            self.pushButton_8.setText('12') # Сброс названия кнопки
            self.pushButton_9.setEnabled(False) # Отключение кнопки места
            self.pushButton_9.setStyleSheet("background-color: rgb(255, 255, 255);") # Сброс цвета кнопки
            self.pushButton_9.setText('6') # Сброс названия кнопки
            self.pushButton_10.setEnabled(False) # Отключение кнопки места
            self.pushButton_10.setStyleSheet("background-color: rgb(255, 255, 255);") # Сброс цвета кнопки
            self.pushButton_10.setText('5') # Сброс названия кнопки
            self.pushButton_11.setEnabled(False) # Отключение кнопки места
            self.pushButton_11.setStyleSheet("background-color: rgb(255, 255, 255);") # Сброс цвета кнопки
            self.pushButton_11.setText('4') # Сброс названия кнопки
            self.pushButton_12.setEnabled(False) # Отключение кнопки места
            self.pushButton_12.setStyleSheet("background-color: rgb(255, 255, 255);") # Сброс цвета кнопки
            self.pushButton_12.setText('11') # Сброс названия кнопки
            self.pushButton_13.setEnabled(False) # Отключение кнопки места
            self.pushButton_13.setStyleSheet("background-color: rgb(255, 255, 255);") # Сброс цвета кнопки
            self.pushButton_13.setText('7') # Сброс названия кнопки
            self.pushButton_14.setEnabled(False) # Отключение кнопки места
            self.pushButton_14.setStyleSheet("background-color: rgb(255, 255, 255);") # Сброс цвета кнопки
            self.pushButton_14.setText('8') # Сброс названия кнопки
            self.pushButton_15.setEnabled(False) # Отключение кнопки места
            self.pushButton_15.setStyleSheet("background-color: rgb(255, 255, 255);") # Сброс цвета кнопки
            self.pushButton_15.setText('10') # Сброс названия кнопки
            self.pushButton_16.setEnabled(False) # Отключение кнопки места
            self.pushButton_16.setStyleSheet("background-color: rgb(255, 255, 255);") # Сброс цвета кнопки
            self.pushButton_16.setText('19') # Сброс названия кнопки
            self.pushButton_17.setEnabled(False) # Отключение кнопки места
            self.pushButton_17.setStyleSheet("background-color: rgb(255, 255, 255);") # Сброс цвета кнопки
            self.pushButton_17.setText('18') # Сброс названия кнопки
            self.pushButton_18.setEnabled(False) # Отключение кнопки места
            self.pushButton_18.setStyleSheet("background-color: rgb(255, 255, 255);") # Сброс цвета кнопки
            self.pushButton_18.setText('17') # Сброс названия кнопки
            self.pushButton_19.setEnabled(False) # Отключение кнопки места
            self.pushButton_19.setStyleSheet("background-color: rgb(255, 255, 255);") # Сброс цвета кнопки
            self.pushButton_19.setText('9') # Сброс названия кнопки
            self.pushButton_20.setEnabled(False) # Отключение кнопки места
            self.pushButton_20.setStyleSheet("background-color: rgb(255, 255, 255);") # Сброс цвета кнопки
            self.pushButton_20.setText('15') # Сброс названия кнопки
            self.pushButton_21.setEnabled(False) # Отключение кнопки места
            self.pushButton_21.setStyleSheet("background-color: rgb(255, 255, 255);") # Сброс цвета кнопки
            self.pushButton_21.setText('16') # Сброс названия кнопки
            self.pushButton_22.setEnabled(False) # Отключение кнопки места
            self.pushButton_22.setStyleSheet("background-color: rgb(255, 255, 255);") # Сброс цвета кнопки
            self.pushButton_22.setText('20') # Сброс названия кнопки
            self.pushButton_23.setEnabled(False) # Отключение кнопки места
            self.pushButton_23.setStyleSheet("background-color: rgb(255, 255, 255);") # Сброс цвета кнопки
            self.pushButton_23.setText('21') # Сброс названия кнопки
            self.pushButton_24.setEnabled(False) # Отключение кнопки места
            self.pushButton_24.setStyleSheet("background-color: rgb(255, 255, 255);") # Сброс цвета кнопки
            self.pushButton_24.setText('22') # Сброс названия кнопки

    def click(self): # кнопки выбора мест
        if self.sender().text() != 'v': # если не выбрано место
            self.selected_seats.append(self.sender().text()) # добавление выбранного места в список
            self.sender().setText("v") # выбраннно место
            self.sender().setStyleSheet("background-color: rgb(0, 255, 0);") # зеленый цвет кнопки
            self.num += 1 # увеличение количества выбранных мест
        else:
            self.sender().setText("DDLC") # Заглушка для отмены выбора места
            self.sender().setStyleSheet("background-color: rgb(255, 255, 255);") # Сброс цвета кнопки
            self.num -= 1 # уменьшение количества выбранных мест
        if (self.num != 0 and self.num == self.spinBox.value() + self.spinBox_2.value()) and self.lineEdit.text() != '':
            self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(True) # включение кнопки оформления заказа
        else:
            self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(False) # отключение кнопки оформления заказа
        if True: # Заглушка для возможности скрыть эту часть кода
            if self.pushButton_3.text() == 'DDLC': # если активна заглушка
                self.pushButton_3.setText('14') # замена заглушки на номер места
                self.selected_seats.remove('14') # удаление места из списка выбранных мест
            if self.pushButton_4.text() == 'DDLC': # Мне надоело писать одно и то же.
                self.pushButton_4.setText('13')
                self.selected_seats.remove('13')
            if self.pushButton_5.text() == 'DDLC':
                self.pushButton_5.setText('1')
                self.selected_seats.remove('1')
            if self.pushButton_6.text() == 'DDLC':
                self.pushButton_6.setText('2')
                self.selected_seats.remove('2')
            if self.pushButton_7.text() == 'DDLC':
                self.pushButton_7.setText('3')
                self.selected_seats.remove('3')
            if self.pushButton_8.text() == 'DDLC':
                self.pushButton_8.setText('12')
                self.selected_seats.remove('12')
            if self.pushButton_9.text() == 'DDLC':
                self.pushButton_9.setText('6')
                self.selected_seats.remove('6')
            if self.pushButton_10.text() == 'DDLC':
                self.pushButton_10.setText('5')
                self.selected_seats.remove('5')
            if self.pushButton_11.text() == 'DDLC':
                self.pushButton_11.setText('4')
                self.selected_seats.remove('4')
            if self.pushButton_12.text() == 'DDLC':
                self.pushButton_12.setText('11')
                self.selected_seats.remove('11')
            if self.pushButton_13.text() == 'DDLC':
                self.pushButton_13.setText('7')
                self.selected_seats.remove('7')
            if self.pushButton_14.text() == 'DDLC':
                self.pushButton_14.setText('8')
                self.selected_seats.remove('8')
            if self.pushButton_15.text() == 'DDLC':
                self.pushButton_15.setText('10')
                self.selected_seats.remove('10')
            if self.pushButton_16.text() == 'DDLC':
                self.pushButton_16.setText('19')
                self.selected_seats.remove('19')
            if self.pushButton_17.text() == 'DDLC':
                self.pushButton_17.setText('18')
                self.selected_seats.remove('18')
            if self.pushButton_18.text() == 'DDLC':
                self.pushButton_18.setText('17')
                self.selected_seats.remove('17')
            if self.pushButton_19.text() == 'DDLC':
                self.pushButton_19.setText('9')
                self.selected_seats.remove('9')
            if self.pushButton_20.text() == 'DDLC':
                self.pushButton_20.setText('15')
                self.selected_seats.remove('15')
            if self.pushButton_21.text() == 'DDLC':
                self.pushButton_21.setText('16')
                self.selected_seats.remove('16')
            if self.pushButton_22.text() == 'DDLC':
                self.pushButton_22.setText('20')
                self.selected_seats.remove('20')
            if self.pushButton_23.text() == 'DDLC':
                self.pushButton_23.setText('21')
                self.selected_seats.remove('21')
            if self.pushButton_24.text() == 'DDLC':
                self.pushButton_24.setText('22')
                self.selected_seats.remove('22')
    
    def tabletka(self): # при выборе сеанса в таблице
        self.selected_seats = [] # очистка списка выбранных мест
        self.num = 0
        self.spinBox.setValue(0) # сброс количества выбранных мест
        self.spinBox_2.setValue(0) # сброс количества выбранных мест
        self.selected_room_name = self.listView.currentIndex().data() # получение названия выбранного сеанса
        con = sqlite3.connect("allinfo.db") # подключение к базе данных
        cur = con.cursor() # создание курсора
        curDate = self.calendarWidget.selectedDate().toString("dd.MM.yyyy") # получение даты выбранного сеанса
        try: # на случай ошибки
            seats_took = cur.execute(f"SELECT took_seats FROM movies WHERE room_name='{self.selected_room_name}' AND date='{curDate}'").fetchall()[0][0].split()
        except Exception: # в случае ошибки
            seats_took = [] # пустой список
        if True is True: # Заглушка для возможности скрыть эту часть кода
            if '14' not in seats_took: # если места нет
                self.pushButton_3.setEnabled(True) # включение кнопки
                self.pushButton_3.setText('14') # сброс названия места
                self.pushButton_3.setStyleSheet("background-color: rgb(255, 255, 255);") # сброс цвета кнопки
            else: # если место есть
                self.pushButton_3.setText('X') # запись в кнопку знака "места занято"
                self.pushButton_3.setEnabled(False) # отключение кнопки
                self.pushButton_3.setStyleSheet("background-color: rgb(255, 0, 0); color: rgb(255, 255, 255);") # изменение цвета кнопки
            if '13' not in seats_took: # даже не просите повторять
                self.pushButton_4.setEnabled(True)
                self.pushButton_4.setText('13')
                self.pushButton_4.setStyleSheet("background-color: rgb(255, 255, 255);")
            else:
                self.pushButton_4.setText('X')
                self.pushButton_4.setEnabled(False)
                self.pushButton_4.setStyleSheet("background-color: rgb(255, 0, 0); color: rgb(255, 255, 255);")
            if '1' not in seats_took:
                self.pushButton_5.setEnabled(True)
                self.pushButton_5.setText('1')
                self.pushButton_5.setStyleSheet("background-color: rgb(255, 255, 255);")
            else:
                self.pushButton_5.setText('X')
                self.pushButton_5.setEnabled(False)
                self.pushButton_5.setStyleSheet("background-color: rgb(255, 0, 0); color: rgb(255, 255, 255);")
            if '2' not in seats_took:
                self.pushButton_6.setEnabled(True)
                self.pushButton_6.setText('2')
                self.pushButton_6.setStyleSheet("background-color: rgb(255, 255, 255);")
            else:
                self.pushButton_6.setText('X')
                self.pushButton_6.setEnabled(False)
                self.pushButton_6.setStyleSheet("background-color: rgb(255, 0, 0); color: rgb(255, 255, 255);")
            if '3' not in seats_took:
                self.pushButton_7.setEnabled(True)
                self.pushButton_7.setText('3')
                self.pushButton_7.setStyleSheet("background-color: rgb(255, 255, 255);")
            else:
                self.pushButton_7.setText('X')
                self.pushButton_7.setEnabled(False)
                self.pushButton_7.setStyleSheet("background-color: rgb(255, 0, 0); color: rgb(255, 255, 255);")
            if '12' not in seats_took:
                self.pushButton_8.setEnabled(True)
                self.pushButton_8.setText('12')
                self.pushButton_8.setStyleSheet("background-color: rgb(255, 255, 255);")
            else:
                self.pushButton_8.setText('X')
                self.pushButton_8.setEnabled(False)
                self.pushButton_8.setStyleSheet("background-color: rgb(255, 0, 0); color: rgb(255, 255, 255);")
            if '6' not in seats_took:
                self.pushButton_9.setEnabled(True)
                self.pushButton_9.setText('6')
                self.pushButton_9.setStyleSheet("background-color: rgb(255, 255, 255);")
            else:
                self.pushButton_9.setText('X')
                self.pushButton_9.setEnabled(False)
                self.pushButton_9.setStyleSheet("background-color: rgb(255, 0, 0); color: rgb(255, 255, 255);")
            if '5' not in seats_took:
                self.pushButton_10.setEnabled(True)
                self.pushButton_10.setText('5')
                self.pushButton_10.setStyleSheet("background-color: rgb(255, 255, 255);")
            else:
                self.pushButton_10.setText('X')
                self.pushButton_10.setEnabled(False)
                self.pushButton_10.setStyleSheet("background-color: rgb(255, 0, 0); color: rgb(255, 255, 255);")
            if '4' not in seats_took:
                self.pushButton_11.setEnabled(True)
                self.pushButton_11.setText('4')
                self.pushButton_11.setStyleSheet("background-color: rgb(255, 255, 255);")
            else:
                self.pushButton_11.setText('X')
                self.pushButton_11.setEnabled(False)
                self.pushButton_11.setStyleSheet("background-color: rgb(255, 0, 0); color: rgb(255, 255, 255);")
            if '11' not in seats_took:
                self.pushButton_12.setEnabled(True)
                self.pushButton_12.setText('11')
                self.pushButton_12.setStyleSheet("background-color: rgb(255, 255, 255);")
            else:
                self.pushButton_12.setText('X')
                self.pushButton_12.setEnabled(False)
                self.pushButton_12.setStyleSheet("background-color: rgb(255, 0, 0); color: rgb(255, 255, 255);")
            if '7' not in seats_took:
                self.pushButton_13.setEnabled(True)
                self.pushButton_13.setText('7')
                self.pushButton_13.setStyleSheet("background-color: rgb(255, 255, 255);")
            else:
                self.pushButton_13.setText('X')
                self.pushButton_13.setEnabled(False)
                self.pushButton_13.setStyleSheet("background-color: rgb(255, 0, 0); color: rgb(255, 255, 255);")
            if '8' not in seats_took:
                self.pushButton_14.setEnabled(True)
                self.pushButton_14.setText('8')
                self.pushButton_14.setStyleSheet("background-color: rgb(255, 255, 255);")
            else:
                self.pushButton_14.setText('X')
                self.pushButton_14.setEnabled(False)
                self.pushButton_14.setStyleSheet("background-color: rgb(255, 0, 0); color: rgb(255, 255, 255);")
            if '10' not in seats_took:
                self.pushButton_15.setEnabled(True)
                self.pushButton_15.setText('10')
                self.pushButton_15.setStyleSheet("background-color: rgb(255, 255, 255);")
            else:
                self.pushButton_15.setText('X')
                self.pushButton_15.setEnabled(False)
                self.pushButton_15.setStyleSheet("background-color: rgb(255, 0, 0); color: rgb(255, 255, 255);")
            if '19' not in seats_took:
                self.pushButton_16.setEnabled(True)
                self.pushButton_16.setText('19')
                self.pushButton_16.setStyleSheet("background-color: rgb(255, 255, 255);")
            else:
                self.pushButton_16.setText('X')
                self.pushButton_16.setEnabled(False)
                self.pushButton_16.setStyleSheet("background-color: rgb(255, 0, 0); color: rgb(255, 255, 255);")
            if '18' not in seats_took:
                self.pushButton_17.setEnabled(True)
                self.pushButton_17.setText('18')
                self.pushButton_17.setStyleSheet("background-color: rgb(255, 255, 255);")
            else:
                self.pushButton_17.setText('X')
                self.pushButton_17.setEnabled(False)
                self.pushButton_17.setStyleSheet("background-color: rgb(255, 0, 0); color: rgb(255, 255, 255);")
            if '17' not in seats_took:
                self.pushButton_18.setEnabled(True)
                self.pushButton_18.setText('17')
                self.pushButton_18.setStyleSheet("background-color: rgb(255, 255, 255);")
            else:
                self.pushButton_18.setText('X')
                self.pushButton_18.setEnabled(False)
                self.pushButton_18.setStyleSheet("background-color: rgb(255, 0, 0); color: rgb(255, 255, 255);")
            if '9' not in seats_took:
                self.pushButton_19.setEnabled(True)
                self.pushButton_19.setText('9')
                self.pushButton_19.setStyleSheet("background-color: rgb(255, 255, 255);")
            else:
                self.pushButton_19.setText('X')
                self.pushButton_19.setEnabled(False)
                self.pushButton_19.setStyleSheet("background-color: rgb(255, 0, 0); color: rgb(255, 255, 255);")
            if '15' not in seats_took:
                self.pushButton_20.setEnabled(True)
                self.pushButton_20.setText('15')
                self.pushButton_20.setStyleSheet("background-color: rgb(255, 255, 255);")
            else:
                self.pushButton_20.setText('X')
                self.pushButton_20.setEnabled(False)
                self.pushButton_20.setStyleSheet("background-color: rgb(255, 0, 0); color: rgb(255, 255, 255);")
            if '16' not in seats_took:
                self.pushButton_21.setEnabled(True)
                self.pushButton_21.setText('16')
                self.pushButton_21.setStyleSheet("background-color: rgb(255, 255, 255);")
            else:
                self.pushButton_21.setText('X')
                self.pushButton_21.setEnabled(False)
                self.pushButton_21.setStyleSheet("background-color: rgb(255, 0, 0); color: rgb(255, 255, 255);")
            if '20' not in seats_took:
                self.pushButton_22.setEnabled(True)
                self.pushButton_22.setText('20')
                self.pushButton_22.setStyleSheet("background-color: rgb(255, 255, 255);")
            else:
                self.pushButton_22.setText('X')
                self.pushButton_22.setEnabled(False)
                self.pushButton_22.setStyleSheet("background-color: rgb(255, 0, 0); color: rgb(255, 255, 255);")
            if '21' not in seats_took:
                self.pushButton_23.setEnabled(True)
                self.pushButton_23.setText('21')
                self.pushButton_23.setStyleSheet("background-color: rgb(255, 255, 255);")
            else:
                self.pushButton_23.setText('X')
                self.pushButton_23.setEnabled(False)
                self.pushButton_23.setStyleSheet("background-color: rgb(255, 0, 0); color: rgb(255, 255, 255);")
            if '22' not in seats_took:
                self.pushButton_24.setEnabled(True)
                self.pushButton_24.setText('22')
                self.pushButton_24.setStyleSheet("background-color: rgb(255, 255, 255);")
            else:
                self.pushButton_24.setText('X')
                self.pushButton_24.setEnabled(False)
                self.pushButton_24.setStyleSheet("background-color: rgb(255, 0, 0); color: rgb(255, 255, 255);")
    
    def accept(self): # продажа билетов
        con = sqlite3.connect("allinfo.db") # подключение к базе данных
        cur = con.cursor() # создание курсора
        movieid = cur.execute(f"SELECT id FROM movies WHERE date='{self.calendarWidget.selectedDate().toString('dd.MM.yyyy')}' AND room_name='{self.selected_room_name}'").fetchall()[0][0] # получение id фильма
        sts = ' '.join(self.selected_seats) # преобразование списка в строку
        cur.execute(f'INSERT INTO tickets(name,movie_id,seat_number) VALUES("{self.lineEdit.text()}","{movieid}","{sts}")') # добавление данных в таблицу
        try: # на случай ошибки
            alreadytookseats = cur.execute(f"SELECT took_seats FROM movies WHERE date='{self.calendarWidget.selectedDate().toString('dd.MM.yyyy')}' AND room_name='{self.selected_room_name}'").fetchall()[0][0].split() # получение списка занятых мест
        except Exception: # в случае ошибки
            alreadytookseats = [] # пустой список
        try: # на случай ошибки
            for seat in alreadytookseats: # перебор занятых мест
                self.selected_seats.append(seat) # добавление занятых мест в список выбранных мест
        except Exception: # в случае ошибки
            pass # пропуск
        self.selected_seats = ' '.join(self.selected_seats) # преобразование списка в строку
        cur.execute(f'UPDATE movies SET took_seats="{self.selected_seats}" WHERE id="{movieid}"') # обновление данных в таблице
        con.commit() # подтверждение изменений
        self.goMainWindow() # переход на главное окно

    def text_changed(self): # при изменении текста в поле ввода имени
        if (self.num != 0 and self.num == self.spinBox.value() + self.spinBox_2.value()) and self.lineEdit.text() != '': # если выбрано место и введено имя
            self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(True) # включение кнопки подтверждения
    
    def goMainWindow(self): # Возвращает на главную страницу
        self.cams = mainpage() # создание окна
        self.cams.show() # открытие окна
        self.close() # закрытие текущего окна


class returnpage(QMainWindow, returnUI): # возврат билета
    def __init__(self): # Параметры окна
        super().__init__()
        self.setupUi(self) # инициализация окна
        self.setWindowTitle("Возврат билета") # заголовок окна
        self.setWindowFlags(Qt.WindowCloseButtonHint) # кнопка закрытия окна
        self.setFixedSize(self.size()) # запрет на изменение размера окна
        self.setWindowIcon(QIcon('images\icon.png')) # иконка окна
        self.buttonBox.accepted.connect(self.return_ticket) # при нажатии на кнопку подтверждения
        self.buttonBox.rejected.connect(self.goMainWindow) # при нажатии на кнопку отмены
        self.buttonBox.button(QDialogButtonBox.Ok).setText("Возврат") # изменение названия кнопки подтверждения
        self.buttonBox.button(QDialogButtonBox.Cancel).setText("Отмена") # изменение названия кнопки отмены
        self.calendarWidget.clicked.connect(self.show_tickets) # при нажатии на дату
        self.listView.clicked.connect(self.select_ticket) # при нажатии на билет
        self.comboBox.currentTextChanged.connect(self.show_tickets) # при изменении выбранного элемента в выпадающем списке
        self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(False) # запрет на нажатие кнопки подтверждения
        con = sqlite3.connect("allinfo.db") # подключение к базе данных
        cur = con.cursor() # создание курсора
        allmovies = cur.execute("SELECT name FROM movies") # выбор из таблицы всех фильмов
        allnames = [] # пустой список
        for i in allmovies.fetchall(): # перебор всех фильмов
            if i[0] not in allnames: # если нет в списке
                allnames.append(i[0]) # добавление в список
        self.comboBox.addItems(allnames) # добавление в выпадающий список всех фильмов
        if self.comboBox.currentText() == '': # если нет названий фильмов
            self.calendarWidget.setEnabled(False) # запрет на выбор даты
    
    def show_tickets(self): # Показывает билеты на выбранную дату
        if self.calendarWidget.selectedDate().toString("dd.MM.yyyy") != '' and self.comboBox.currentText() != '': # если выбрана дата и выбран фильм
            self.selected_movie_name = self.comboBox.currentText() # выбранный фильм
            self.model_for_list = QStandardItemModel() # создание модели для списка
            con = sqlite3.connect("allinfo.db") # подключение к базе данных
            cur = con.cursor() # создание курсора
            selected_date = self.calendarWidget.selectedDate().toString("dd.MM.yyyy") # выбранная дата
            movie_id = con.execute(f"SELECT id FROM movies WHERE name='{self.selected_movie_name}' AND date='{selected_date}'").fetchall() # получение id фильма из таблицы на выбранную дату
            for i in movie_id: # перебор всех id
                for g in i: # перебор всех id
                    movie_id = g # выбранный id
                    for j in cur.execute(f"SELECT * FROM tickets WHERE movie_id='{movie_id}'").fetchall(): # получение всех билетов на выбранную дату
                        room = cur.execute(f"SELECT room_name FROM movies WHERE id='{movie_id}'").fetchall()[0][0].split()[1] # получение номера зала
                        try: # на случай ошибки
                            seats = ', '.join(j[3].split()) # получение мест
                        except Exception: # в случае ошибки
                            seats = j[3] # берем все разом
                        self.model_for_list.setItem(self.model_for_list.rowCount(), 0, QStandardItem(f'Имя: {j[1]}; Места: {seats}; Зал: {room}')) # добавление в список
            self.model_for_list.setHorizontalHeaderLabels(['Билеты']) # добавление заголовков
            self.listView.setModel(self.model_for_list) # добавление модели в список
            self.listView.setEditTriggers(QAbstractItemView.NoEditTriggers) # запрет на редактирование списка
        else:
            self.model_for_list = QStandardItemModel() # создание модели для списка
            self.listView.setModel(self.model_for_list) # добавление модели в список
            self.listView.setEditTriggers(QAbstractItemView.NoEditTriggers) # запрет на редактирование списка
    
    def select_ticket(self): # Выбор билета
        self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(True) # включение кнопки ОК
    
    def return_ticket(self): # Возврат билета
        self.selected_ticket = self.listView.currentIndex().data() # выбранный билет
        self.user_name = self.selected_ticket.split(';')[0].split(':')[1] # имя покупателя
        self.user_name = self.user_name.strip() # удаление пробела в начале
        self.user_place = self.selected_ticket.split(';')[1].split(':')[1] # места покупателя
        self.user_place = self.user_place.strip() # удаление пробела в начале
        self.user_place = ' '.join(self.user_place.split(', ')) # строка с местами покупателя
        self.user_place_list = self.user_place.split() # список мест покупателя
        self.user_room = self.selected_ticket.split(';')[2].split(':')[1] # зал покупателя
        self.user_room = self.user_room.strip() # удаление пробела в начале
        self.selected_movie_name = self.comboBox.currentText() # выбранный фильм
        self.selected_date = self.calendarWidget.selectedDate().toString("dd.MM.yyyy") # выбранная дата
        con = sqlite3.connect("allinfo.db") # подключение к базе данных
        cur = con.cursor() # создание курсора
        movie_id = cur.execute(f"SELECT id FROM movies WHERE name='{self.selected_movie_name}' AND date='{self.selected_date}' AND room_name='Зал {self.user_room}'").fetchall()[0][0] # получение id фильма из таблицы на выбранную дату и зал
        movie_places = cur.execute(f"SELECT took_seats FROM movies WHERE id='{movie_id}'").fetchall()[0][0] # получение мест на выбранную дату и зал
        movie_places = movie_places.split() # список мест на выбранную дату и зал
        for i in self.user_place_list: # проверка на наличие мест в списке мест покупателя
            movie_places.remove(i) # удаление мест из списка мест на выбранную дату и зал
        movie_places = ' '.join(movie_places) # строка с местами на выбранную дату и зал
        cur.execute(f"DELETE from tickets WHERE name='{self.user_name}' AND movie_id='{movie_id}' AND seat_number='{self.user_place}'") # удаление билета из таблицы билетов
        cur.execute(f"UPDATE movies SET took_seats='{movie_places}' WHERE id='{movie_id}'") # обновление мест на выбранную дату и зал
        con.commit() # подтверждение изменений
        self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(False) # отключение кнопки ОК
        self.show_tickets() # обновление списка билетов
    
    def goMainWindow(self): # Возвращает на главную страницу
        self.cams = mainpage() # создание окна
        self.cams.show() # открытие окна
        self.close() # закрытие текущего окна


if __name__ == '__main__': # Запуск программы
    app = QApplication(sys.argv)
    ex = mainpage() # создание окна
    ex.show() # открытие окна
    sys.exit(app.exec_())