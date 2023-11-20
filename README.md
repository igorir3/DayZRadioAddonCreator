# DayZRadioAddonCreator

## [RUS]

Это программа для авто создания аддонов на модификации от Yuki и FoX добавляющие радио.
Версия для мода Yuki не будет обнавлена, до выхода бета версии (На данный момент, только Альфа)
Главное отличие программы для Yuki и FoX - это то, что в новой есть функция создания текстур, а также система для локализации на другие языки

Для использования программы требуется DayZTools, а также ffmpeg, но инструкция по его установке уже написана.

### Процесс установки
Шаг 1: Зайдите на сайт https://github.com/igorir3/DayZRadioAddonCreator и скачайте Zip-файл.\
Шаг 2: Распакуйте папку DayZRadioAddonCreator-main и удалите **YukiOldCassetsRecorder.py** и **YukiInit.bat**, чтобы остались только FoXy файлы.\
Шаг 3: Зайдите на сайт https://github.com/BtbN/FFmpeg-Builds/releases и скачайте **ffmpeg-n4.4-latest-win64-gpl-4.4.zip**.\
Шаг 4: **Извлеките папку ffmpeg-n4.4-latest-win64-gpl-4.4\bin** в папку **DayZRadioAddonCreator-main**\
Шаг 5: Скачайте и установите **Python 3.11** из **Microsoft Store**.\
Шаг 6: Щелкните правой кнопкой мыши на папке **DayZRadioAddonCreator-main** и откройте ее в терминале.\
Шаг 7: Используйте следующую команду для установки некоторых пакетов python (это может занять некоторое время)\
```pip install transliterate==1.10.2 rich==13.6.0 tqdm==4.66.1 pydub==0.25.1 Pillow==10.0.1 eyed3==0.9.7```

### Процесс создания мода
Шаг 8: Запустите файл **FoxInit.bat**\
Шаг 9: Скопируйте полный путь к папке DayZ Tools и вставьте в новое окно **консоли с запущенной программой** и нажмите Enter/Return.\
Шаг 10: **СКОПИРУЙТЕ** MP3 (должен содержать метаданные) или OGG в новую папку **input**, эти файлы будут преобразованы и перемещены в конечный результат.\
Шаг 11: В окне **консоли с запущенной программой** вставьте название вашего мода (название аддона) и нажмите Enter/Return.\
Шаг 12: Выберите режим **Режим ввода** и нажмите Enter/Return.\
1 = Использует имена файлов\
2 = Ручной ввод (конечный результат не будет конвертироваться в pbo)\
3 = Использует метаданные Mp3\
4 = Сломанный\
Шаг 13: Выберите **Режим генератора текстур** и нажмите Enter/Return\
1 = Пустые текстуры\
2 = Пользовательские текстуры\
Шаг 14: После завершения нажмите Enter/Return.\

### Конечный результат
Ваш мод будет полностью создан и помещен в папку **output**, готов к публикации в мастерской или перепаковке в серверный пакет (включая файл Types).\

### Изменение файлов
Если вы хотите добавить свой язык, либо же отредактировать существующий перейдите в datapack/lang, и добавьте или же измените файл .txt с кодом вашего языка.\
Для изменения изначальной текстуры кассеты, просто замените datapack/blanck.png на свой файл с тем же именем.\
Если же вы хотите поменять шрифт, замените файл datapack/font.tff на свой с тем же именем.\

### Аргументы запуска
`-debug` - Вывод дополнительной информации\
`-logging` - использовать с -debug, сохраняет весь вывод консоли\
`-addonname [ИмяАддона]` - ввод имени аддона до запуска\
`-mode [РежимВвода]` - ввод режима ввода\
`-dtdir [Path]` - ввод пути к DayZTools, учтите, что в пути не должно быть пробелов\
`-pausebeforepbo` - позволяет приостановить выполнение программы перед запаковкой в .pbo, можно использовать для изменения или же проверки файлов перед их запоковки\
`-texturemode [РежимГенератораТекстур]` - ввод режима работы текстурного генератора\
`-countofstickers [Кол-воСтикеров]` - ввод кол-ва стикеров на одну кассету (стикеры создаются на основе изображений из meta данных mp3 файлов, если нет изображений, то и стикеров не будет)\


## [ENG]
This is a program for auto creation of addons for mods from Yuki and FoX that add radio.
The version for Yuki mod will not be updated until the beta version is released (At the moment, only Alpha)
The main difference between the program for Yuki and FoX - is that the new one has a function for creating textures, as well as a system for localization to other languages

To use the program requires DayZTools, as well as ffmpeg, but the instructions for installing it is already written.

### Install Process
Step 1: Visit https://github.com/igorir3/DayZRadioAddonCreator and download the Zip File\
Step 2: Extract DayZRadioAddonCreator-main folder and delete **YukiOldCassetsRecorder.py** & **YukiInit.bat** so you are only left with FoXy Files.\
Step 3: Visit https://github.com/BtbN/FFmpeg-Builds/releases and download **ffmpeg-n4.4-latest-win64-gpl-4.4.zip**\
Step 4: **Extract ffmpeg-n4.4-latest-win64-gpl-4.4\bin** folder to **DayZRadioAddonCreator-main**\
Step 5: Download & Install **Python 3.11** from the **Microsoft Store**\
Step 6: Right Click **DayZRadioAddonCreator-main** folder and Open in Terminal\
Step 7: Use the following command to install some python packages (This may take some time)\
```pip install transliterate==1.10.2 rich==13.6.0 tqdm==4.66.1 pydub==0.25.1 Pillow==10.0.1 eyed3==0.9.7```

### Mod Creation Process
Step 8: Run **FoxInit.bat**\
Step 9: Copy the Full Path of your DayZ Tools folder and paste into the new **Addon Creator Console Window** and press Enter/Return\
Step 10: **COPY** your MP3 (Must include MetaData) or OGG into the new **input** folder, these files will be converted and moved into your End Result\
Step 11: In the **Addon Creator Console Window** insert your Mod Name (Addon Name) and press Enter/Return\
Step 12: Choose your **Input Mode** and press Enter/Return\
1 = Uses Filenames\
2 = Manual Input (End Result will not convert to pbo)\
3 = Uses Mp3 Meta Data\
4 = Broken\
Step 13: Choose your **Texture Generator Mode** and press Enter/Return\
1 = Blank Textures\
2 = Custom Textures\
Step 14: When Complete press Enter/Return\


### End Result
Your Mod will be fully created and placed in the **output** folder ready to be published to the workshop or repacked into a server pack (Including the Types File)\

### Change files
If you want to add your own language, or edit an existing one, go to **datapack/lang**, and add or edit a .txt file with the code for your language.\
To change the original texture of the tape, just replace **datapack/blanck.png** with your file with the same name.\
If you want to change the font, replace the **datapack/font.tff** file with your own file with the same name.\

### Startup Arguments
`-debug` - Output additional information\
`-logging` - use with -debug, saves all console output\
`-addonname [AddonName]` - input addon name before startup\
`-mode [InputMode]` - input input mode\
`-dtdir [Path]` - enter the path to DayZTools, note that there should be no spaces in the path\
`-pausebeforepbo` - allows you to pause program execution before packing into .pbo, can be used to modify or check files before packing them\
`-texturemode [TextureGeneratorMode]` - input texture generator mode\
`-countofstickers [NumberOfStickers]` - enter the number of stickers for one tape (stickers are created on the basis of images from mp3 files meta data, if there are no images, there will be no stickers).\
