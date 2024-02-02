# DayZRadioAddonCreator

## [RUS]

Это программа для авто создания аддонов на модификации от Yuki и FoX добавляющие радио.
**!Версия для мода Yuki не будет обнавлена!**
Программа для FoX - это полностью переписанная и переделанная программа, в ней есть GUI (Если говорить о .exe версии), генератор текстур и т.д.\

Для использования программы требуется DayZTools.

### Процесс установки
Шаг 1: Зайдите на сайт https://github.com/igorir3/DayZRadioAddonCreator и скачайте архив как Zip-файл.\
Шаг 2: Создайте папку для установки программы и перенесите туда `FoXRadioRecorder.exe`, папку `datapack`, а также все три файла из папки `ffmpeg-n4.4-latest-win64-gpl-4.4`. ВНИМАНИЕ! НУЖНО ПЕРЕНЕСТИ ФАЙЛ **ИЗ** ПАПКИ, А НЕ САМУ ПАПКУ.

### Процесс создания мода
Шаг 8: Запустите файл **FoXRadioRecorder.exe**\
Шаг 9: Нажмите на кнопку настроек и введите путь к папке DayZTools в поле `DayZTools Path`, нажмите на кнопку "Agree" и закройте окно, можете заново открыть окно, что бы проверить сохранились ли настройки.\
Шаг 10: **СКОПИРУЙТЕ** MP3 (должен содержать метаданные, если вы хотите использовать режим ввода по метаданным) или OGG в новую папку **input**, эти файлы будут преобразованы и перемещены в конечный результат.\
Шаг 10.5: Если вы хотите создать плейлист, то просто создайте папку с названием плейлиста и переместите туда файлы песен (.mp3 и .ogg), которые войдут в плейлист
Шаг 11: Нажмите на кнопку обновить и проверьте все ли файлы есть в списке по середине.\
Шаг 12: Выберите режим **Режим ввода** нажав на поле правее "Information input mode" и выберете нужный режим.\
Automatic = Использует имена файлов\
Manual = Ручной ввод (Каждый раз будет спрашивать, а как записать ту или иную песню)\
Data from mp3 = Использует метаданные Mp3\
Шаг 13: Если вы хотите включить генератор текстур нажмите на кнопку правее от Texture Generatore mode\
Шаг 14: Нажмите "Process" и дождитесь окончания процесса (об этом будет написано в текстовом поле снизу окна). ВНИМАНИЕ! Во время работы программы будет открываться большое кол-во консольных окон, ПРОСТО НЕ ТРОГАЙТЕ ИХ!.

### Конечный результат
Ваш мод будет полностью создан и помещен в папку **output**, готов к публикации в мастерской или перепаковке в серверный пакет (включая файл Types).\
Во время работы программа для оптимизации времени и места, программа будет пользоваться уже созданными файлами (Если - это возможно). Для обычного пользователя - это значит две вещи:\
1. Моды весят меньше\
2. В определённых случаях значительно ускоряет работу программы

### Параметры
Это описание всех пунктов в окне параметров:\
DayZTools Path = Путь к папке DayZTools\
Lang = Язык (ВРЕМЕННО ВЫРЕЗАНО)\
Count of Stickers = Количество стикеров на кассете\
Blank Texture = Изначальная текстура кассеты (Таже текстура кассеты, но без текста или же стикеров). В формате .png!\
Font = Путь к файлу шрифта в формате .tff, который используется для создания текстур кассет


### Поддержка
Я работаю над этим и другими проектами буквально за бесплатно, а выжить на зарплату в 10 000, когда ты студент-мехатроник проблематично, поэтому буду рад, если вы поддержите меня: **https://boosty.to/igorir3**
If this system is not available to you, I will be glad to donate to WebMoney: https://pay.web.money/d/t4rp

## [ENG]
This is a program for auto creation of addons for mods from Yuki and FoX that add radio.
**!The version for the Yuki mod will not be updated!**
The FoX program is a completely rewritten and redesigned program, it has a GUI (If we talk about the .exe version), texture generator, etc.\

To use the program requires DayZTools.

### Installation Process
Step 1: Go to https://github.com/igorir3/DayZRadioAddonCreator and download the archive as a Zip file.\.
Step 2: Create a folder to install the program and move `FoXRadioRecorder.exe`, `datapack` folder and all three files from `ffmpeg-n4.4-latest-win64-gpl-4.4` folder there. ATTENTION! YOU NEED TO MOVE THE FILE **FROM** FOLDER, NOT THE FOLDER ITSELF.

### Mod Creation Process
Step 8: Run the file **FoXRadioRecorder.exe**\.
Step 9: Click on the settings button and enter the path to the DayZTools folder in the `DayZTools Path` field, click on the "Agree" button and close the window, you can reopen the window to check if the settings are saved.\
Step 10: **COPIRE** MP3 (must contain metadata if you want to use metadata input mode) or OGG to a new **input** folder, these files will be converted and moved to the final result.\
Step 10.5: If you want to create a playlist, simply create a folder with the same name as the playlist and move the song files (.mp3 and .ogg) that will be part of the playlist to it.\
Step 11: Click the refresh button and check if all the files are in the middle of the list.
Step 12: Select **Input mode** by clicking the box to the right of "Information input mode" and select the desired mode.\
Automatic = Uses filenames.\
Manual = Manual input (Every time it will ask you how to record this or that song).\
Data from mp3 = Uses Mp3 metadata.\
Step 13: If you want to enable the texture generator, click on the button to the right of Texture Generatore mode.
Step 14: Click "Process" and wait for the process to finish (it will be written in the text box at the bottom of the window). WARNING: While the program is running, a large number of console windows will be opened, just DON'T TROUBLE THEM!

### Final result
Your mod will be fully created and placed in the **output** folder, ready to be published in the workshop or repackaged into a server package (including the Types file).\
While running the time and space optimization program, the program will use already created files (If - it is possible). For an ordinary user, this means two things:\
1. Mods weigh less\
2. In certain cases, it significantly speeds up the work of the program

### Parameters
This is a description of all the items in the parameters window:\
DayZTools Path = The path to the DayZTools folder.
Lang = Language (TIME EXCLUDED).\
Count of Stickers = The number of stickers on the tape.
Blank Texture = The original texture of the tape (The same texture of the tape, but without text or stickers). In .png format!\
Font = The path to the .tff font file used to create the cassette texture.

### Support
I'm working on this and other projects literally for free, and surviving on a salary of 10,000 when you're a mechatronics student is problematic, so I'd be glad if you'd support me: **https://boosty.to/igorir3**
If this system is not available to you, I will be glad to donate to WebMoney: https://pay.web.money/d/t4rp
