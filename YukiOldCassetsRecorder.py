from genericpath import isfile
import os
import shutil
import transliterate
import eyed3
import time
import random
import sys
import rich
import multiprocessing
import configparser
from tqdm import tqdm
from pydub import AudioSegment



DEBUG = False
LOGGING = False
DAYZTOOLSDIRARGV = False
ARGVADDON = False
ARGVMODE = False
WORKDIR = os.path.abspath(__file__).replace(os.path.basename(__file__), '')
ARTISTFOLDERS = False
PAUSEBEFOREPBO = False


def debug(text, status = 0):
    global DEBUG
    global LOGGING
    if LOGGING == True:
        global logfile
        match status:
            case 0: state = 'fine '
            case 1: state = 'warn '
            case 2: state = 'error'
        logfile.write(f"[{time.strftime('%H:%M:%S', time.localtime(time.time()))} {state}] {text} \n")
    if DEBUG == True:
        match status:
            case 0: rich.print(f"[{time.strftime('%H:%M:%S', time.localtime(time.time()))}] {text}")
            case 1: rich.print(f"[{time.strftime('%H:%M:%S', time.localtime(time.time()))}][bold][yellow] {text}[/bold][/yellow]")
            case 2: rich.print(f"[{time.strftime('%H:%M:%S', time.localtime(time.time()))}][bold][yellow] {text}[/bold][/yellow]")
                
def symboltest(symbol):
    noncesordsymbol = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    if symbol in noncesordsymbol:
        return True
    else:
        return False
        
def syntaxofsymbols(text, lite = False):
    if lite == False:
        text = transliterate.translit(text, language_code='ru', reversed=True)
        getVals = list([val for val in text
                                if symboltest(val) == True])
        text = "".join(getVals)
        text = text.replace(' ', "_")
        debug(f"syntaxofsymbols() returned {text}")
        return text
    else:
        censoredsymbols = ['"', "'", "{", "}", ";"]
        debug(f"syntaxofsymbols({text}) called in lite mode")
        for aa in range(len(censoredsymbols)):
            text = text.replace(censoredsymbols[aa], "")
        return text

def mp3toogg(file, dist):
    if os.path.isfile(file):
        AudioSegment.from_mp3(f"{file}").export(f"{dist}", format='ogg')
        os.remove(f"{file}")
    else:
        debug(f"File {file}", 2)
        debug(f"Dist {dist}", 2)

if __name__ == "__main__": #иначе пизда multiprocessing

    for aa in range(len(sys.argv)):                     #Обработка аргументов
            if sys.argv[aa].lower() == "-debug":
                DEBUG = True
            if sys.argv[aa].lower() == "-logging":
                LOGGING = True
            if sys.argv[aa].lower() == "-addonname":
                ARGVADDON = True
                NameOfAddon = sys.argv[aa + 1]
                aa = aa + 1
            if sys.argv[aa].lower() == "-mode":
                ARGVMODE = True
                Mode = sys.argv[aa + 1]
                aa = aa + 1
            if sys.argv[aa].lower() == "-dtdir":
                DAYZTOOLSDIRARGV = True
                dayztooldir = sys.argv[aa + 1]
                aa = aa + 1
            if sys.argv[aa].lower() == "-artistfolders":
                ARTISTFOLDERS = True
            if sys.argv[aa].lower() == "-pausebeforepbo":
                PAUSEBEFOREPBO = True

    if LOGGING == True:
        if os.path.isdir("logs"):
            pass
        else:
            print("Папка logs не найдена! Создание...")
            os.mkdir("logs")
        logfile = open(f"logs\\{time.strftime('%H-%M-%S', time.localtime(time.time()))}.log", "w", encoding='utf8')
        logfile.write(f'''Это файл для логирования debug вывода который был создан {time.strftime('%d.%m.%Y г. %H:%M:%S', time.localtime(time.time()))} \n''')
        
    if ARTISTFOLDERS == True:
        Mode = str(input("Режим ввода >>> "))
        if not(os.path.exists("specinput")):
            os.mkdir("specinput")
        fdjf = input("!НАЖМИТЕ ENTER ПОСЛЕ ПЕРЕНОСА ФАЙЛОВ!")
        artistfoldersfiles = os.listdir("specinput\\")
    else:
        artistfoldersfiles = ['None']
    for artis in range(len(artistfoldersfiles)):
        if ARTISTFOLDERS == True:
            artisinspec = os.listdir(f"specinput\\{artistfoldersfiles[artis]}\\")
            for inartis in range(len(artisinspec)):
                shutil.move(f"specinput\\{artistfoldersfiles[artis]}\\{artisinspec[inartis]}", "input\\")
        #Уникальный id для файлов (на всякий)
        UnikID = ""
        for x in range(5):UnikID = UnikID + str(int(time.time()))[random.randint(0, len(str(int(time.time()))) - 1)]
        UnikID = str(hex(int(UnikID)))[2:]
        debug(f"UnikID = {UnikID}")

        # Основной код 
        if os.path.isdir("input"):
            pass
        else:
            print("Папка input не найдена! Создание...")
            os.mkdir("input")
            debug("Создание папки input", 1)
        if os.path.isdir("output"):
            pass
        else:
            print("Папка output не найдена! Создание...")
            os.mkdir("output")
            debug("Создание папки Output", 1)

        if os.path.exists("config.ini"):
            configfile = configparser.ConfigParser()
            configfile.read('config.ini')
            debug(configfile)
            if DAYZTOOLSDIRARGV == False:
                dayztooldir = configfile["MAIN"]["dayztoolsdir"]
                debug(dayztooldir)
            if  not(os.path.exists(f"{dayztooldir}\\Bin\\AddonBuilder\\AddonBuilder.exe") and os.path.exists(f"{dayztooldir}\\Bin\\DsUtils\\DSCreateKey.exe") and os.path.exists(f"{dayztooldir}\\Bin\\DsUtils\\DSSignFile.exe") and os.path.exists(f"{dayztooldir}\\Bin\\ImageToPAA\\ImageToPAA.exe")):
                print(f"файлы dayztools не найдены или повреждены, пожалуйста введите новой путь к файлам DayZTools")
                debug(f"{dayztooldir}\\Bin\\AddonBuilder\\AddonBuilder.exe - " + str(os.path.exists(f'{dayztooldir}\\Bin\\AddonBuilder\\AddonBuilder.exe')))
                debug(f"{dayztooldir}\\Bin\\DsUtils\\DSCreateKey.exe - " + str(os.path.exists(f'{dayztooldir}\\Bin\\DsUtils\\DSCreateKey.exe')))
                debug(f"{dayztooldir}\\Bin\\DsUtils\\DSSignFile.exe - " + str(os.path.exists(f'{dayztooldir}\\Bin\\DsUtils\\DSSignFile.exe')))
                debug(f"{dayztooldir}\\Bin\\DsUtils\\DSSignFile.exe - " + str(os.path.exists(f'{dayztooldir}\\Bin\\DsUtils\\DSSignFile.exe')))
                debug(f"{dayztooldir}\\Bin\\ImageToPAA\\ImageToPAA.exe - " + str(os.path.exists(f'{dayztooldir}\\Bin\\ImageToPAA\\ImageToPAA.exe')))
                config = configparser.ConfigParser()
                while True:
                    dayztooldir = str(input("Путь к папке Dayz Tools >>>"))
                    debug(f"{dayztooldir}\\Bin\\AddonBuilder\\AddonBuilder.exe - " + os.path.exists(f'{dayztooldir}\\Bin\\AddonBuilder\\AddonBuilder.exe'))
                    debug(f"{dayztooldir}\\Bin\\DsUtils\\DSCreateKey.exe - " + os.path.exists(f'{dayztooldir}\\Bin\\DsUtils\\DSCreateKey.exe'))
                    debug(f"{dayztooldir}\\Bin\\DsUtils\\DSSignFile.exe - " + os.path.exists(f'{dayztooldir}\\Bin\\DsUtils\\DSSignFile.exe'))
                    debug(f"{dayztooldir}\\Bin\\DsUtils\\DSSignFile.exe - " + os.path.exists(f'{dayztooldir}\\Bin\\DsUtils\\DSSignFile.exe'))
                    debug(f"{dayztooldir}\\Bin\\ImageToPAA\\ImageToPAA.exe - " + os.path.exists(f'{dayztooldir}\\Bin\\ImageToPAA\\ImageToPAA.exe'))
                    if  os.path.exists(f"{dayztooldir}\\Bin\\AddonBuilder\\AddonBuilder.exe") and os.path.exists(f"{dayztooldir}\\Bin\\DsUtils\\DSCreateKey.exe") and os.path.exists(f"{dayztooldir}\\Bin\\DsUtils\\DSSignFile.exe") and os.path.exists(f"{dayztooldir}\\Bin\\ImageToPAA\\ImageToPAA.exe"):
                        config['MAIN'] = {'dayztoolsdir': dayztooldir}
                        with open('config.ini', 'w') as configfile:
                            config.write(configfile)
                            break
                    else:
                        print(f"файлы dayztools не найдены или повреждены, пожалуйста повторите попытку")
        else:
            config = configparser.ConfigParser()
            while True:
                dayztooldir = str(input("Путь к папке Dayz Tools >>>"))
                if  os.path.exists(f"{dayztooldir}\\Bin\\AddonBuilder\\AddonBuilder.exe") and os.path.exists(f"{dayztooldir}\\Bin\\DsUtils\\DSCreateKey.exe") and os.path.exists(f"{dayztooldir}\\Bin\\DsUtils\\DSSignFile.exe") and os.path.exists(f"{dayztooldir}\\Bin\\ImageToPAA\\ImageToPAA.exe"):
                    config['MAIN'] = {'dayztoolsdir': dayztooldir}
                    with open('config.ini', 'w') as configfile:
                        config.write(configfile)
                        break
                else:
                    print(f"файлы dayztools не найдены или повреждены, пожалуйста повторите попытку")

        if ARGVADDON == False and ARTISTFOLDERS == False:
            NameOfAddon = input("Название аддона >>> ")
        elif ARTISTFOLDERS == True:
            NameOfAddon = syntaxofsymbols(artistfoldersfiles[artis])
        while True:
            if os.path.isdir(f"output\\{NameOfAddon}"):
                print(f"{NameOfAddon} уже создан, ")
                print("выберите другое название или нажмите ENTER, что бы пересоздать аддон с тем же именем")
                print(" ")
                INPUT_AAA = input("Название аддона >>> ")
                if INPUT_AAA == "":
                    shutil.rmtree(f"output\\{NameOfAddon}")
                    break
                else:
                    NameOfAddon = INPUT_AAA
            else:
                break

        files = os.listdir("input\\")
        for t in range(len(files)):
            if os.path.isdir(f"input\\{files[t]}"):
                files_two = os.listdir(f"input\\{files[t]}")
                debug(files_two)
                files_three = []
                for td in range(len(files_two)):
                    if files_two[td].endswith('.mp3'):
                        files_three.append(files_two[td])
                    elif files_two[td].endswith('.ogg'):
                        files_three.append(files_two[td])
                if len(files_three) == 1:
                    debug(f"Папка с одним файлом - {files_three}", 1)
                    if not(os.path.exists(f"input\\{files_three[0]}")):
                        shutil.move(f"input\\{files[t]}\\{files_three[0]}", "input\\")
                    shutil.rmtree(f"input\\{files[t]}\\")
                elif len(files_three) == 0:
                    debug(f"Папка без файлов - {files_three}", 1)
                    shutil.rmtree(f"input\\{files[t]}\\")

        if ARGVMODE == False and ARTISTFOLDERS == False:
            print("Режим ввода информации")
            print('1. Автоматическое')
            print("2. Ручное")
            print("3. Данные из mp3")
            print("4. С помощью конфига")
            print(" ")
            Mode = str(input("Режим ввода >>> ")) 
        if Mode != "1" and Mode != "2" and Mode != "3" and Mode != "4":
            print("Режим ввода некорректен! Автоматический режим установлен")
            Mode = "1"
        os.system("cls")

        debug(f"NameOfAddon - {NameOfAddon}, Mode - {Mode}",0)
        os.mkdir(f"output\\{NameOfAddon}")
        debug(f"output\\{NameOfAddon}",0)
        os.mkdir(f"output\\{NameOfAddon}\\Cassettes")
        debug(f"output\\{NameOfAddon}\\Cassettes",0)
        os.mkdir(f"output\\{NameOfAddon}\\Cassettes\\sounds")
        debug(f"output\\{NameOfAddon}\\Cassettes\\sounds",0)
        scriptfile = open(f"output\\{NameOfAddon}\\config.cpp", "w", encoding='utf8')
        debug(f"scriptfile = output\\{NameOfAddon}\\config.cpp, 'w', encoding='utf8'", 0)
        files = os.listdir("input\\")
        debug(f"Files: \n{files}",1)

        print("Создание импортов")
        scriptfile.write("class CfgPatches { \n")
        scriptfile.write(f"	class {NameOfAddon}_Cassettes\n")
        scriptfile.write('	{\n')
        scriptfile.write('		units[]={};\n')
        scriptfile.write('		weapons[]={};\n')
        scriptfile.write('		requiredVersion=0.1;\n')
        scriptfile.write('		requiredAddon[]=\n')
        scriptfile.write('		{\n')
        scriptfile.write('			"DZ_Data",\n')
        scriptfile.write('			"YK_Radio"\n')
        scriptfile.write('		};\n')
        scriptfile.write('	};\n')
        scriptfile.write('};\n')
        oggfiles = []
        totreadinglistoffiles = []
        metadata = []
        playlists = []
        process = []
        print("Создание файловой системы")
        for i in tqdm(range(len(files))):
            error = False
            filename = None
            if files[i].endswith('.mp3'):
                debug(f"for i = {i}", 0)
                filename = files[i].removesuffix('.mp3')
                debug(f"filename = {filename}", 0)
                oldfilename = filename
                debug(f"filename = {filename}", 0)
                filename = filename.replace("–", "")
                debug(f"filename = {filename}", 0)
                oggfiles.append(filename)
                debug(f"oggfiles = {oggfiles}", 0)
                if Mode == "3":
                    audiofile = eyed3.load(f"input\\{oldfilename}.mp3")
                    title = audiofile.tag.title
                    album = audiofile.tag.album
                    artist = audiofile.tag.artist
                    debug(f'''title = {title}
                        album = {album}
                        artist = {artist}
                        ''', 0)
                    title = title.replace("/", ", ")
                    album = album.replace("/", ", ")
                    artist = artist.replace("/", ", ")
                    debug(f'''title = {title}
                        album = {album}
                        artist = {artist}
                        ''', 0)
                    debug(f'''title = {title}
                        album = {album}
                        artist = {artist}
                        ''', 0)
                    metadata.append([title, artist, album])
                    debug(f"metadata - {metadata}")
                if not(os.path.exists(f"input\\{syntaxofsymbols(filename)}.mp3")):
                    os.rename(f"input\\{oldfilename}.mp3", f"input\\{syntaxofsymbols(filename)}.mp3")
                else:
                    debug(f"Найден повторяющийся файл {syntaxofsymbols(filename)}.mp3", 1)
                    os.remove(f"input\\{oldfilename}.mp3")
                if os.path.isfile(f"output\\{NameOfAddon}\\Cassettes\\sounds\\{syntaxofsymbols(filename)}.ogg") == False:
                    p = multiprocessing.Process(target=mp3toogg, args = (f"input\\{syntaxofsymbols(filename)}.mp3", f"output\\{NameOfAddon}\\Cassettes\\sounds\\{syntaxofsymbols(filename)}.ogg"))
                    process.append(p)
                    p.start()
                else:
                    debug(f'os.path.isfile(f"output\\{NameOfAddon}\\Cassettes\\sounds\\{syntaxofsymbols(filename)}.ogg") == True', 2)
                    error = True
            elif files[i].endswith('.ogg'):
                if Mode == "3":
                    debug(f"Найден не mp3 файл!", 2)
                    print("Найден не mp3 файл! Вы можете завершить программу или же будет установлен автоматический режим ввода!")
                    aaa = input("Завершить программу [Y/n] >>> ")
                    if aaa.lower() == "y":
                        raise SystemExit
                    else:
                        Mode = "1"
                filename = files[i].removesuffix('.ogg')
                debug(f"filename = {filename}", 0)
                oldfilename = filename
                debug(f"filename = {filename}", 0)
                oggfiles.append(filename)
                debug(f"oggfiles = {oggfiles}", 0)
                if not(os.path.exists(f"input\\{syntaxofsymbols(filename)}.ogg")):
                    os.rename(f"input\\{oldfilename}.ogg", f"input\\{syntaxofsymbols(filename)}.ogg")
                else:
                    debug(f"Найден повторяющийся файл {syntaxofsymbols(filename)}.ogg", 1)
                    os.remove(f"input\\{oldfilename}.ogg")
                if os.path.isfile(f"output\\{NameOfAddon}\\Cassettes\\sounds\\{syntaxofsymbols(filename)}.ogg") == False:   
                    shutil.move(f"input\\{syntaxofsymbols(filename)}.ogg", f"output\\{NameOfAddon}\\Cassettes\\sounds\\")
                else:
                    debug(f'os.path.isfile(f"output\\{NameOfAddon}\\Cassettes\\sounds\\{syntaxofsymbols(filename)}.ogg") == True', 2)
                    os.remove(f"input\\{syntaxofsymbols(filename)}.ogg")
                    error = True
            elif os.path.isdir(f"input\\{files[i]}"):
                filesinplaylist = os.listdir(f"input\\{files[i]}")
                debug(f"filesinplaylist = {filesinplaylist}")
                print(f"Создание Playlist {files[i]}")
                toplaylist = []
                for t in tqdm(range(len(filesinplaylist))):
                        if filesinplaylist[t].endswith('.mp3'):
                            filename = filesinplaylist[t].removesuffix('.mp3')
                            debug(f"filename - {filename}")
                            oldfilename = filename
                            debug(f"filename - {filename}")
                            if not(os.path.isfile(f"input\\{files[i]}\\{syntaxofsymbols(filename)}.mp3")):
                                os.rename(f"input\\{files[i]}\\{oldfilename}.mp3", f"input\\{files[i]}\\{syntaxofsymbols(filename)}.mp3")
                            else:
                                os.remove(f"input\\{files[i]}\\{oldfilename}.mp3")
                            if os.path.isfile(f"output\\{NameOfAddon}\\Cassettes\\sounds\\{syntaxofsymbols(filename)}_playlist{syntaxofsymbols(files[i])}.ogg") == False:   
                                p = multiprocessing.Process(target= mp3toogg, args = (f"input\\{files[i]}\\{syntaxofsymbols(filename)}.mp3", f"output\\{NameOfAddon}\\Cassettes\\sounds\\{syntaxofsymbols(filename)}_playlist{syntaxofsymbols(files[i])}.ogg"))
                                process.append(p)
                                p.start()
                                toplaylist.append(f"{syntaxofsymbols(filename)}_playlist{syntaxofsymbols(files[i])}")
                                debug(f"toplaylist - {toplaylist}")
                            else:
                                debug(f'os.path.isfile(f"output\\{NameOfAddon}\\Cassettes\\sounds\\{syntaxofsymbols(filename)}_playlist{syntaxofsymbols(files[i])}.ogg") == True', 2)
                                error = True
                        elif filesinplaylist[t].endswith('.ogg'):
                            filename = filesinplaylist[t].removesuffix('.ogg')
                            debug(f"filename - {filename}")
                            oldfilename = filename
                            debug(f"filename - {filename}")
                            if not(os.path.isfile(f"input\\{files[i]}\\{syntaxofsymbols(filename)}_playlist{syntaxofsymbols(files[i])}.ogg")):
                                os.rename(f"input\\{files[i]}\\{oldfilename}.ogg", f"input\\{files[i]}\\{syntaxofsymbols(filename)}_playlist{syntaxofsymbols(files[i])}.ogg")
                            else:
                                os.remove(f"input\\{files[i]}\\{oldfilename}.ogg")
                            if os.path.isfile(f"output\\{NameOfAddon}\\Cassettes\\sounds\\{syntaxofsymbols(filename)}_playlist{syntaxofsymbols(files[i])}.ogg") == False:   
                                shutil.move(f"input\\{files[i]}\\{syntaxofsymbols(filename)}_playlist{syntaxofsymbols(files[i])}.ogg", f"output\\{NameOfAddon}\\Cassettes\\sounds\\")
                                toplaylist.append(f"{syntaxofsymbols(filename)}_playlist{syntaxofsymbols(files[i])}")
                                debug(f"toplaylist - {toplaylist}")
                            else:
                                os.remove(f"input\\{files[i]}\\{syntaxofsymbols(filename)}_playlist{syntaxofsymbols(files[i])}.ogg")
                                debug(f'os.path.isfile(f"output\\{NameOfAddon}\\Cassettes\\sounds\\{syntaxofsymbols(filename)}_playlist{syntaxofsymbols(files[i])}.ogg") == True', 2)
                                error = True
                playlists.append(dict(Name=f"{files[i]}", Playlist=toplaylist))
                debug(f"playlists - {playlists}")
        print("Ожидание завершения конвертации...")
        for dp in process:
            dp.join()
        print("ГОТОВО!")
        print("Создание class CfgVechiles")
        scriptfile.write('class CfgVehicles {\n' )
        scriptfile.write('    class YK_Cassette_Base;\n' )
        if Mode == "1":
            for j in tqdm(range(len(oggfiles))):
                scriptfile.write(f'    class {NameOfAddon}_{syntaxofsymbols(oggfiles[j])}: YK_Cassette_Base\n' )
                scriptfile.write('        {\n' )
                scriptfile.write('        scope=2;\n')
                scriptfile.write(f'        displayName="Кассета {syntaxofsymbols(oggfiles[j], True)}";\n' )
                scriptfile.write('        descriptionShort="Автоматический ввод";\n' )
                scriptfile.write("        hiddenSelectionsTextures[]=\n" )
                scriptfile.write("        {\n" )
                scriptfile.write('            "YK_Radio\Cassettes\Clear\data\cassette_co.paa"\n' )
                scriptfile.write("        };\n" )
                scriptfile.write("        class CfgCassette\n" )
                scriptfile.write("        {\n" )
                scriptfile.write(f'            soundSet="{NameOfAddon}_SoundSet_{syntaxofsymbols(oggfiles[j])}";\n' )
                scriptfile.write("        };\n" )
                scriptfile.write("    };\n" )
        if Mode == "2":
            for j in tqdm(range(len(oggfiles))):
                scriptfile.write(f'    class {NameOfAddon}_{syntaxofsymbols(oggfiles[j])}: YK_Cassette_Base\n' )
                scriptfile.write('        {\n' )
                scriptfile.write('        scope=2;\n')
                scriptfile.write(f'        displayName="{input(f"Имя {oggfiles[j]} >>> ")}";\n' )
                scriptfile.write(f'        descriptionShort="{input(f"Описание {oggfiles[j]} >>> ")}";\n' )
                scriptfile.write("        hiddenSelectionsTextures[]=\n" )
                scriptfile.write("        {\n" )
                scriptfile.write('            "YK_Radio\Cassettes\Clear\data\cassette_co.paa"\n' )
                scriptfile.write("        };\n" )
                scriptfile.write("        class CfgCassette\n" )
                scriptfile.write("        {\n" )
                scriptfile.write(f'            soundSet="{NameOfAddon}_SoundSet_{syntaxofsymbols(oggfiles[j])}";\n' )
                scriptfile.write("        };\n" )
                scriptfile.write("    };\n" )
        if Mode == "3":
            for j in tqdm(range(len(oggfiles))):
                scriptfile.write(f'    class {NameOfAddon}_{syntaxofsymbols(oggfiles[j])}: YK_Cassette_Base\n' )
                scriptfile.write('        {\n' )
                scriptfile.write('        scope=2;\n')
                scriptfile.write(f'        displayName="Кассета {syntaxofsymbols(metadata[j][0], True)}";\n' )
                scriptfile.write(f'        descriptionShort="Песня альбома {syntaxofsymbols(metadata[j][2], True)}, под авторством {syntaxofsymbols(metadata[j][1], True)}";\n' )
                scriptfile.write("        hiddenSelectionsTextures[]=\n" )
                scriptfile.write("        {\n" )
                scriptfile.write('            "YK_Radio\Cassettes\Clear\data\cassette_co.paa"\n' )
                scriptfile.write("        };\n" )
                scriptfile.write("        class CfgCassette\n" )
                scriptfile.write("        {\n" )
                scriptfile.write(f'            soundSet="{NameOfAddon}_SoundSet_{syntaxofsymbols(oggfiles[j])}";\n' )
                scriptfile.write("        };\n" )
                scriptfile.write("    };\n" )
        if Mode == "4":
            pass
        if len(playlists) > 0:
            for p in range(len(playlists)):
                scriptfile.write(f'    class {NameOfAddon}_{syntaxofsymbols(playlists[p].get("Name"))}_Collection: YK_Cassette_Base\n' )
                scriptfile.write('        {\n' )
                scriptfile.write('        scope=2;\n')
                scriptfile.write(f'        displayName="Альбом {syntaxofsymbols(playlists[p].get("Name"), True)}";\n' )
                scriptfile.write(f'        descriptionShort=" ";\n' )
                scriptfile.write("        hiddenSelectionsTextures[]=\n" )
                scriptfile.write("        {\n" )
                scriptfile.write('            "YK_Radio\Cassettes\Clear\data\cassette_co.paa"\n' )
                scriptfile.write("        };\n" )
                scriptfile.write("        class CfgCassette\n" )
                scriptfile.write("        {\n" )
                scriptfile.write("             isPlaylist=1;\n" )
                scriptfile.write('             soundSets[]=\n' )
                scriptfile.write("             {\n" )
                for k in range(len(playlists[p].get("Playlist"))):
                    if k == len(playlists[p].get("Playlist")) - 1:
                        scriptfile.write(f'            "{NameOfAddon}_SoundSet_{syntaxofsymbols(playlists[p].get("Name"))}_{playlists[p].get("Playlist")[k]}"\n' )
                    else:
                        scriptfile.write(f'            "{NameOfAddon}_SoundSet_{syntaxofsymbols(playlists[p].get("Name"))}_{playlists[p].get("Playlist")[k]}",\n' )
                scriptfile.write("             };\n" )
                scriptfile.write("        };\n" )
                scriptfile.write("    };\n" )
        scriptfile.write("};\n" )

        print("ГОТОВО!")
        print("Создание class CfgSoundSets")
        scriptfile.write('class CfgSoundSets {\n' )
        scriptfile.write('	class Mods_SoundSet_Base;\n' )
        for u in tqdm(range(len(oggfiles))):
            scriptfile.write(f'	class {NameOfAddon}_SoundSet_{syntaxofsymbols(oggfiles[u])}\n' )
            scriptfile.write('  {\n' )
            scriptfile.write('		soundShaders[]=\n' )
            scriptfile.write('		{\n' )
            scriptfile.write(f'			"{NameOfAddon}_{syntaxofsymbols(oggfiles[u])}_Shader"\n' )
            scriptfile.write('		};\n' )
            scriptfile.write('	};\n' )
        if len(playlists) > 0:
            for b in tqdm(range(len(playlists))):
                for h in tqdm(range(len(playlists[b].get("Playlist")))):
                    scriptfile.write(f'	class {NameOfAddon}_SoundSet_{syntaxofsymbols(playlists[b].get("Name"))}_{playlists[b].get("Playlist")[h]}\n' )
                    scriptfile.write('  {\n' )
                    scriptfile.write('		soundShaders[]=\n' )
                    scriptfile.write('		{\n' )
                    scriptfile.write(f'			"{NameOfAddon}_{syntaxofsymbols(playlists[b].get("Name"))}_{playlists[b].get("Playlist")[h]}_Shader"\n' )
                    scriptfile.write('		};\n' )
                    scriptfile.write('	};\n' )
        scriptfile.write('};\n' )

        print("ГОТОВО!")
        print("Создание class CfgSoundShaders")
        scriptfile.write('class CfgSoundShaders {\n' )
        scriptfile.write('	class YK_Cassette_SoundShader_Base;\n' )
        for t in tqdm(range(len(oggfiles))):
            scriptfile.write(f'	class {NameOfAddon}_{syntaxofsymbols(oggfiles[t])}_Shader: YK_Cassette_SoundShader_Base\n' )
            scriptfile.write('  {\n' )
            scriptfile.write('		samples[]=\n' )
            scriptfile.write('		{\n' )
            scriptfile.write('			{\n' )
            scriptfile.write(f'				"{NameOfAddon}\Cassettes\sounds\{syntaxofsymbols(oggfiles[t])}.ogg",\n' )
            scriptfile.write('				1\n' )
            scriptfile.write('			}\n' )
            scriptfile.write('		};\n' )
            scriptfile.write('	};\n' )
        if len(playlists) > 0:
            for s in tqdm(range(len(playlists))):
                for a in tqdm(range(len(playlists[s].get("Playlist")))):
                    scriptfile.write(f'	class {NameOfAddon}_{syntaxofsymbols(playlists[s].get("Name"))}_{playlists[s].get("Playlist")[a]}_Shader: YK_Cassette_SoundShader_Base\n' )
                    scriptfile.write('  {\n' )
                    scriptfile.write('		samples[]=\n' )
                    scriptfile.write('		{\n' )
                    scriptfile.write('			{\n' )
                    scriptfile.write(f'				"{NameOfAddon}\Cassettes\sounds\{playlists[s].get("Playlist")[a]}.ogg",\n' )
                    scriptfile.write('				1\n' )
                    scriptfile.write('			}\n' )
                    scriptfile.write('		};\n' )
                    scriptfile.write('	};\n' )
        scriptfile.write('};\n' )
        print("ГОТОВО!")
        print("Создание types.xml")

        f = open(f"output\\{NameOfAddon}_{UnikID}_types.xml", "w", encoding='utf8')
        for t in tqdm(range(len(oggfiles))):
            xmlstrpart = f'''   <type name="{NameOfAddon}_{syntaxofsymbols(oggfiles[t])}">
                <nominal>2</nominal>
                <lifetime>21600</lifetime>
                <restock>7200</restock>
                <min>1</min>
                <quantmin>-1</quantmin>
                <quantmax>-1</quantmax>
                <cost>100</cost>
                <flags count_in_cargo="0" count_in_hoarder="0" count_in_map="1" count_in_player="0" crafted="0" deloot="0"/>
                <category name="tools"/>
                <tag name="shelves"/>
                <usage name="Town"/>
                <usage name="Village"/>
                <usage name="School"/>
            </type>'''
            f.write(xmlstrpart)
        for e in tqdm(range(len(playlists))):
                xmlstrpart = f'''   <type name="{NameOfAddon}_{syntaxofsymbols(playlists[e].get("Name"))}_Collection">
                <nominal>2</nominal>
                <lifetime>21600</lifetime>
                <restock>7200</restock>
                <min>1</min>
                <quantmin>-1</quantmin>
                <quantmax>-1</quantmax>
                <cost>100</cost>
                <flags count_in_cargo="0" count_in_hoarder="0" count_in_map="1" count_in_player="0" crafted="0" deloot="0"/>
                <category name="tools"/>
                <tag name="shelves"/>
                <usage name="Town"/>
                <usage name="Village"/>
                <usage name="School"/>
                </type>'''
                f.write(xmlstrpart)
        f.close()
        scriptfile.close()

        #PACK IN PBO - #### YOU DAYZ TOOLS
        if PAUSEBEFOREPBO == True:
            x = input("PAUSE")
            if x.lower() == "exit":
                raise SystemExit
        print(f"Запоковка {NameOfAddon} в PBO")
        debug(f"Запоковка {NameOfAddon} в PBO")
        debug(f"dayztooldir - {dayztooldir}")
        includefile = open(f"output\\{NameOfAddon}_{UnikID}_include.txt", "w", encoding='utf8')
        includefile.write("*.emat;*.edds;*.ptc;*.c;*.imageset;*.layout;*.ogg;*.paa;*.rvmat;")
        includefile.close()
        debug(f'chdir "{dayztooldir}\\Bin\\AddonBuilder\\"')
        os.chdir(f"{dayztooldir}\\Bin\\AddonBuilder")
        debug(f'AddonBuilder.exe "{WORKDIR}output\\{NameOfAddon}" "{WORKDIR}output\\{NameOfAddon}" -clear -packonly -include="{WORKDIR}output\\{NameOfAddon}_{UnikID}_include.txt"')
        os.system(f'AddonBuilder.exe "{WORKDIR}output\\{NameOfAddon}" "{WORKDIR}output\\{NameOfAddon}" -clear -packonly -include="{WORKDIR}output\\{NameOfAddon}_{UnikID}_include.txt"')
        os.chdir(WORKDIR)

        debug("Создание директорий") 
        os.remove(f"output\\{NameOfAddon}_{UnikID}_include.txt")
        os.mkdir(f"output\\@{NameOfAddon}")
        os.mkdir(f"output\\@{NameOfAddon}\\Keys")
        os.mkdir(f"output\\@{NameOfAddon}\\Addons")

        debug("Перемещение файлов")
        shutil.move(f"output\\{NameOfAddon}_{UnikID}_types.xml", f"output\\@{NameOfAddon}")
        shutil.move(f"output\\{NameOfAddon}\\{NameOfAddon}.pbo", f"output\\@{NameOfAddon}\\Addons")
        shutil.rmtree(f"output\\{NameOfAddon}")

        debug("Создание ключа")
        os.chdir(f"{dayztooldir}\\Bin\\DsUtils")
        os.system(f'DSCreateKey.exe {UnikID}')
        shutil.copy(f"{dayztooldir}\\Bin\\DsUtils\\{UnikID}.bikey", f"{WORKDIR}output\\@{NameOfAddon}\\Keys")

        debug("Присвоение ключа")
        os.system(f'DSSignFile.exe {UnikID}.biprivatekey "{WORKDIR}output\\@{NameOfAddon}\\Addons\\{NameOfAddon}.pbo"')
        if os.path.exists(f"{dayztooldir}\\Bin\\DsUtils\\{UnikID}.bikey"):
            debug(f"os.remove(f'{dayztooldir}\\Bin\\DsUtils\\{UnikID}.bikey')")
            os.remove(f"{dayztooldir}\\Bin\\DsUtils\\{UnikID}.bikey")
        if os.path.exists(f"{dayztooldir}\\Bin\\DsUtils\\{UnikID}.biprivatekey"):
            debug(f"os.remove(f'{dayztooldir}\\Bin\\DsUtils\\{UnikID}.biprivatekey')")
            os.remove(f"{dayztooldir}\\Bin\\DsUtils\\{UnikID}.biprivatekey")
        
        os.chdir(WORKDIR)
        inputlistdir = os.listdir("input")
        for uuu in range(len(inputlistdir)):
            if os.path.isdir(f"input\\{inputlistdir[uuu]}"):
                shutil.rmtree(f"input\\{inputlistdir[uuu]}")
            if os.path.isfile(f"input\\{inputlistdir[uuu]}"):
                os.remove(f"input\\{inputlistdir[uuu]}")
    debug("Done!")
    input("Нажмите ENTER для выхода! ")
    os.system("cls")