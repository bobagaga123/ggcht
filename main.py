import keyboard
import threading
import tkinter as tk
import g4f

# Функция для перехвата нажатия клавиш
def hotkey_listener():
    while True:
        # Проверяем, была ли нажата комбинация клавиш
        if keyboard.is_pressed('ctrl+shift+a'):
            print("Была нажата комбинация клавиш Ctrl+Shift+A")
            # При нажатии комбинации клавиш открываем окно с полем для ввода
            show_input_window()
        # Добавляем небольшую задержку, чтобы снизить нагрузку на процессор
        keyboard.wait('ctrl+shift+a', suppress=True)


def generate_and_print(promt):
    response = g4f.ChatCompletion.create(
        model=g4f.models.gpt_35_turbo_16k_0613,
        messages=[{"role": "user", "content": f"Ты - мой помощник. Я тебе пишу свои сообщения, а ты их переделываешь.ПИШИ ТОЛЬКО НА РУССКОМ. Используй очень много MARKDOWN. Пиши только их, и помни, что я пишу в мессенджере, поэтому можешь использовать переходы на другую строку как новое сообщение. Пиши только текст, я отправляю все что ты напишешь автоматически. И помни: ты отвечаешь не мне, а пишешь от моего имени."
                                              f"Вот мой текст: {promt}"}],
        stream=True,
    )

    for message in response:
        try:
            keyboard.write(message)
        except Exception as ex:
            print(message)
            break
    keyboard.press_and_release("enter")



# Функция для отображения окна с полем для ввода
def show_input_window():
    # Создаем окно
    def close_window(event=None):
        data = entry.get()
        print(data)
        window.destroy()
        generate_and_print(data)

    window = tk.Tk()
    window.title("Введите текст")

    # Создаем поле для ввода
    entry = tk.Entry(window)
    entry.pack()

    # Переключаем фокус на поле для ввода текста
    entry.focus_set()

    # Функция для автоматического ввода текста в поле
    def insert_text():
        entry.focus_force()
        entry.icursor(tk.END)

    # Вызываем функцию для автоматического ввода текста
    window.after(100, insert_text)

    window.bind("<Return>", close_window)

    # Функция для обработки события закрытия окна
    def on_closing():
        window.destroy()

    # Назначаем функцию on_closing обработчиком события закрытия окна
    window.protocol("WM_DELETE_WINDOW", on_closing)

    # Запускаем главный цикл обработки событий окна
    window.mainloop()


# Запускаем поток для перехвата нажатия клавиш
threading.Thread(target=hotkey_listener).start()

# Чтобы скрипт продолжал работать, добавим ввод
input("Для выхода нажмите Enter...")
