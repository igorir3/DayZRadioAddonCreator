# [RUS]

Это программа - редактор, для создания модов-аддонов на мод Fox's Radio для DayZ! По мимо создания проектов, она также может напрямую экспортировать данные в .pbo и создавать полноценные моды, для экспорта в Steam Workshop. По мимо создание конфигов и конвертации, программа, также сможет создать текстуры для каждого объекта отдельно!

### Словарь
TG - Texture Generator, изменение текстур для каждого объекта за счёт алгоритма (Используется при экспорте)

Медиа файл - файл `.mp3` или `.ogg`

Объект - объект, который после будет экспортирован как предмет

Медиа объект - объект, что может быть использован в других объектах, за счёт него работает TG, а также создаются SoundSet-ы и SoundShader-ы

Объект Текстур - объект для TG, а также привязывается к каждому из объектов


### Установка:

1. Установите архив репозитория
2. Переместите файлы RadioAddonCreatorPro.exe, ffmpeg.exe, ffplay.exe, ffprobe.exe и папку data в пустую директорию
3. Готово! Можете запускать RadioAddonCreatorPro.exe

Учтите! Что при первом запуске программы в настройках нужно установить директорию где расположен DayZTools (Ну, и установить его, если его нет :) Выглядеть это будет примерно так: 

`C:\Program Files (x86)\Steam\steamapps\common\DayZ Tools`

### Использование
Учтите, что это будет не описание **как сделать мод**, а **какие есть функции и как их использовать**.

### Запуск
Сразу после запуска вы увидите консоль и уведомление о запросе прав администратора. Не пугайтесь, консоль через время свернётся, и появится полноценное окно с интерфейсом.

```Учтите, что хоть права администратора не обязательны, программа может нестабильней работать из-за блокировки Windows некоторых директорий```

### **Далее будет описания по окнам и кнопкам:**

### Главное окно
Имеет две кнопки: 

> Add - открывает окно добавления объекта
> Remove - удаление выбранного объекта

Сверху есть 3 селектора при наведеннии на которых откроется выбор:
1. `File`

    1.1 `New project` - удаляет ВООБЩЕ всё из программы, рекомендуется вначале сохранить проект, а после использовать эту кнопку
   
    1.2 `Load project` - загружает проект из файла
   
    1.3 `Save project` - сохраняет проект в файл
   
    1.4 `Check project` - проверяет открытый проект на наличие ошибок, а также недочётов. Список всех возможных сообщений:

    Ошибки - то, что помешает экспорту в DayZ мод:
   
        `Invalid type` - Не поддерживаемый программой тип объекта или тип медиа
   
        `Invalid name` - Не поддерживаемое название объекта
   
        `File doesn't exist!` - Файл указанный в объекте не существует
   
        `Media isn't a playlist but have a list of paths!` - В объекте Media указано, что оно является одиночной песней, хотя имеет список песен.
   
        `Media object doesn't exist!` - В объекте указан объект медиа, который не найден в проекте
   
        `Texture object doesn't exist!` - В объекте указан объект текстуры, который не найден в проекте
   
    Предупреждения - то, что не помешает экспорту, но может его 'подпортить':
   
        `The media is not used!` - Объект медиа, не используется не в одном из объектов
   
        `The texture is not used!` - Объект текстур, не используется не в одном из объектов
   
        `A recurring media file!` - Файл использующиеся в объекте медиа, используется в нескольких объектах
   
        `A recurring texture file!` - Файл использующиеся в объекте текстур, используется в нескольких объектах
   
    1.5 `Export as DayZ mod` - Экспорт в мод готовый для выкладывания в Steam или для добавления на сервер. При выборе этого параметра требуется выбрать папку, которая после будет преобразована в мод. ВНИМАНИЕ! УЧТИТЕ, ЧТО ВЫБИРАТЬ НУЖНО ПУСТУЮ ПАПКУ, И ИМЕННА **ПАПКА** СТАНЕТ МОДОМ. ЕСЛИ ПАПКА НЕ ПУСТА ФАЙЛЫ БУДУТ УДАЛЕНЫ! (Конечно, если пользователь этого захочет :) )
   
    1.6 `Export without PBO` - Требуется для проверки мода, экспортирует по аналогии с пунктом с `Export as DayZ mod`, но не упаковывает в PBO (Учтите, что данный режим работы более **багованный** и часто выдаёт ошибки и недочёты, так, что рекомендуется, только для продвинутых пользователей)
   
    1.7 `Import Mod` - WIP
   
2. `Edit`
   
    2.1 `Import Media` - Открывает окно для добавления объекта медиа
   
    2.2 `Import Texture` - Открывает окно для добавления объекта текстур
   
    2.3 `Edit Media` - Открывает окно для редактирования объектов медиа
   
    2.4 `Edit Texture` - Открывает окно для редактирования объекта текстур
   
3. `Settings` - Открывает настройки

### Окно добавления объекта 
Чек боксы сверху - выбор типа объекта, если выбрать больше одного, будет созданы копии объекта с разными типами. Например: Cassette Object - создаст кассету, а выбор CD и Cassette object создаст два объекта, один CD, и другой Cassette.

Селектор медиа, нужен для выбора привязанного объекта медиа, если выбрать `Add New` открывает окно добавления объекта медиа

Кнопка Okay закроет окно и создаст объекты, кнопка Cancel, закроет окно, но без создания объектов


### Окно редактирования объекта
Для открытия объекта для редактирования, дважды нажмите на нужный объект.
1. Выбор типа объекта
2. `Name` - Имя объекта
3. `Desc` - Описание объекта
4. `File` - Объект медия привязанного к данному объекту
5. `Texture` - Выбор объекта текстуры привязанного к объекту 
6. `Save` - Сохранение изменений

### Окно добавления объекта медиа
В поле для текста можно написать путь к файлу, либо же нажав на кнопку в виде папки, открыть окно для выбора файлов медиа.

Если вы хотите создать плейлист, поставьте галочку в `Playlist`, учтите, что для создания плей листов, нужно выбрать несколько файлов! Если же вы выделете множество файлов, но не нажмёте на `Playlist`, то будет создано множество media файлов для каждого из файлов

### Окно добавления текстур
Схож с окном для добавления медиа, однако не имеет чек бокса `Playlist`, и импортирует не медиа файлы, а png изображения

### Окно редактирования медиа
Первое, что нас встретит, окно для выбора объекта для редактирования, просто дважды кликните, на нужный объект.
Далее откроется окно для редактирования:
1. `Name` - Имя медиа объекта
2. `Path` - Путь к файлу, схож с аналогичным полем для объекта медиа
3. `Album` - Альбом привязанный к медиа
4. `Artist` - Исполнитель привязанный к медиа
5. `Media images` - Изображения привязанные к данному медиа, можно добавлять по аналогии с окном для добавления текстур, использует, также png картинки
6. `Description` - Описание, для медиа, довольно-таки бесполезно, но почему бы и нет :)
7. `Is playlist?` - Выбор является ли медиа плейлистом (галочка стоит — значит да, если её нет, то нет)
8. `Save` - Сохраняет изменения

### Окно редактирования текстур
Начинаестя с окна для выбора объекта для редактирования, также как и в окне для редактирования медиа. Но далее... ХАХАХА! 
1. `Name` - Название текстуры
2. `Path` - Путь к файлу текстуры
3. Поле для работы с текстурой
4. Кнопка для добавления поля на текстуры
5. `Save` - сохранения изменений

Поле — это объект размещаемой на текстуре по средством выделения двух крайних точек. 
1. Параметр — Это пустое поле для текста, сюда нужно вписать, то, что должно быть в поле. C `/` начинается команда для вставки, а параметры между двумя `%` обозначает placeholder

    1.1 `/sticker` - Устанавливает изображение, обрезанное по кругу привязанное к медиа, установленное для объекта, для которого создаётся текстура
   
    1.2 `%name%` - Имя media
   
    1.3 `%album%` - Aльбом media
   
    1.4 `%artist%` - Исполнитель media
   
    1.5 `%author%` - Такой же как %artist%
   
    1.6 `%objectname%` - Имя объекта
   
2. Две кнопки для установки крайних точек. Нажимаете на кнопку, а после жмёте на нужное вам место на текстуре. И как бы это не было контр-интуитивно, но точку 2 рекомендуется ставить снизу справа, а точку 1 слева сверху
3. `Rotation` — Это выбор под каким углом, будет расположен вставляемый объект (Применяется для в основном для текста)
4. `-` - Удаление поля

### Настройки
Окно для настройки программы.
1. `DayZTools` - Путь к DayZ Tools
2. `Local` - Выбор языка (WIP)
3. `Number of subprocesses` - Кол-во паралельных процессов (Используется при экспорте в DayZ мод)
4. `Save` - Сохранение изменения
