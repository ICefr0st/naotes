#начни тут создавать приложение с умными заметками
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
        QApplication, QWidget, 
        QHBoxLayout, QVBoxLayout, 
        QGroupBox, QButtonGroup, QRadioButton,  
        QPushButton, QLabel, QListWidget,QLineEdit,QTextEdit,
        QInputDialog,QFormLayout,QInputDialog)
import json 
app =QApplication([])


"""Создание главного окна приложения"""
notes_win = QWidget()
notes_win.setWindowTitle('Умные заметки')
notes_win.resize(950, 650)

#Создание виджетов окна

list_notes = QListWidget()
list_notes_label =QLabel('Ваши заметки')

button_note_create = QPushButton('Создать заметку')
button_note_delete = QPushButton('Удалить заметку')
button_note_save = QPushButton('Сохранить заметку')

field_tag = QLineEdit('')
field_tag.setPlaceholderText('добавьте тег..')
field_text = QTextEdit ()

button_tag_create = QPushButton('Добавить тег к заметке')
button_tag_delete = QPushButton('Удалить тег от заметки')
button_tag_reserch =QPushButton('Искать заметку по тегу')

list_tag = QListWidget()
list_tag_label = QLabel('Список тегов')

"""Создание лейаутов"""

layouts_notes = QHBoxLayout()
nomer_1 =QVBoxLayout()
nomer_1.addWidget(field_text)


nomer_2 = QVBoxLayout()
nomer_2.addWidget(list_notes_label)
nomer_2.addWidget(list_notes)

bot_1 = QHBoxLayout()
bot_1.addWidget(button_note_create)
bot_1.addWidget(button_note_delete)
bot_2 = QHBoxLayout()
bot_2.addWidget(button_note_save)
nomer_2.addLayout(bot_1)
nomer_2.addLayout(bot_2)

nomer_2.addWidget(list_tag_label)
nomer_2.addWidget(list_tag)
nomer_2.addWidget(field_tag)


bot_3 = QHBoxLayout()
bot_3.addWidget(button_tag_create)
bot_3.addWidget(button_tag_delete)

bot_4 = QHBoxLayout()
bot_4.addWidget(button_tag_reserch)

nomer_2.addLayout(bot_3)
nomer_2.addLayout(bot_4)

layouts_notes.addLayout(nomer_1,stretch= 3)
layouts_notes.addLayout(nomer_2,stretch= 1)

notes_win.setLayout(layouts_notes)




def add_note():
    note_name, ok = QInputDialog.getText(notes_win,'Добавить заметку','Название заметки:')
    if ok and note_name != '':
        notes[note_name]={'текст':'','теги':[]}
        list_notes.addItem(note_name)
        #list_tag.addItems(notes[note_name]['теги'])
def show_note():
    
    key = list_notes.selectedItems()[0].text()
    print(key)
    field_text.setText(notes[key]["текст"])
    list_tag.clear()
    list_tag.addItems(notes[key]["теги"])


def save_note():
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        notes[key]["текст"] = field_text.toPlainText()
        with open("notes_data.json", "w") as file:
            json.dump(notes, file, sort_keys=True, ensure_ascii=False)
        print(notes)
    else:
        print("Заметка для сохранения не выбрана!")

def del_notes():
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        del notes[key]
        list_notes.clear()
        list_tag.clear()
        field_text.clear()
        list_notes.addItems(notes)
        with open ('notes_data.json','w') as file:
            json.dump(notes,file,sort_keys =True, ensure_ascii = False)
        print(notes)
    
def add_tag():
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        tag = field_tag.text()
        if not tag in notes[key]["теги"]:
            notes[key]["теги"].append(tag)
            list_tag.addItem(tag)
            field_tag.clear()
        with open("notes_data.json", "w") as file:
            json.dump(notes, file, sort_keys=True)
    else:
        print("Заметка для добавления тега не выбрана!")

def del_tag():
    if list_tag.selectedItems():
        key = list_notes.selectedItems()[0].text()
        tag = list_tag.selectedItems()[0].text()
        notes[key]["теги"].remove(tag)
        list_tag.clear()
        list_tag.addItems(notes[key]["теги"])
        with open("notes_data.json", "w") as file:
            json.dump(notes, file, sort_keys=True, ensure_ascii=False)
    else:
        print("Тег для удаления не выбран!")


def search_tag():
    
    tag = field_tag.text()
    if button_tag_reserch.text() == "Искать заметку по тегу" and tag:
        print(tag)
        notes_filtered = {} 
        for note in notes:
            if tag in notes[note]["теги"]: 
                notes_filtered[note]=notes[note]
        button_tag_reserch.setText("Сбросить поиск")
        list_notes.clear()
        list_tag.clear()
        list_notes.addItems(notes_filtered)
       
    elif button_tag_reserch.text() == "Сбросить поиск":
        field_tag.clear()
        list_notes.clear()
        list_tag.clear()
        list_notes.addItems(notes)
        button_tag_reserch.setText("Искать заметки по тегу")
        
    else:
        pass

notes_win.show()
list_notes.itemClicked.connect(show_note)
button_note_create.clicked.connect(add_note)
button_note_save.clicked.connect(save_note)
button_note_delete.clicked.connect(del_notes)
button_tag_create.clicked.connect(add_tag)
button_tag_delete.clicked.connect(del_tag)
button_tag_reserch.clicked.connect(search_tag)
with open("notes_data.json", "r") as file:
    notes = json.load(file)
list_notes.addItems(notes)


app.exec_()
