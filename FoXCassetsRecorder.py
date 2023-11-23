import os
import shutil
import transliterate #1.10.2
import time
import sys
import rich #13.6.0
import multiprocessing
import configparser
from tqdm import tqdm #4.66.1
from pydub import AudioSegment #0.25.1
from PIL import Image #Pillow - 10.0.1
from PIL import ImageFont
from PIL import ImageDraw
from PIL import ImageFilter, ImageEnhance
import eyed3 #0.9.7
import random
from io import BytesIO
import ctypes
import locale

DEBUG = False
LOGGING = False
DAYZTOOLSDIRARGV = False
ARGVADDON = False
ARGVMODE = False
WORKDIR = os.path.abspath(__file__).replace(os.path.basename(__file__), '')
ARTISTFOLDERS = False
PAUSEBEFOREPBO = False
TEXTUREMODE = False
COUNTOFSTICKERS = 1

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
            case 2: rich.print(f"[{time.strftime('%H:%M:%S', time.localtime(time.time()))}][bold][red] {text}[/bold][/red]")

def symboltest(symbol, include_ = False):
    noncesordsymbol = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    if include_:
        noncesordsymbol = noncesordsymbol + "_"
    if symbol in noncesordsymbol:
        return True
    else:
        return False

def wordtest(word):
    error = False
    for x in range(len(word)):
        if symboltest(word[x], True):
            pass
        else:
            error = True
    if error == False:
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
    for aa in range(len(sys.argv)):
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
            if sys.argv[aa].lower() == "-texturemode":
                TEXTUREMODE = True
                TextureMode = sys.argv[aa + 1]
                aa = aa + 1
            if sys.argv[aa].lower() == "-countofstickers":
                COUNTOFSTICKERS = int(sys.argv[aa + 1])
                aa = aa + 1

    if LOGGING == True:
        if os.path.isdir("logs"):
            pass
        else:
            print("The logs folder was not found! Creation...")
            os.mkdir("logs")
        logfile = open(f"logs\\{time.strftime('%H-%M-%S', time.localtime(time.time()))}.log", "w", encoding='utf8')
        logfile.write(f'''This is the file for logging debug output that was created {time.strftime('%d.%m.%Y г. %H:%M:%S', time.localtime(time.time()))} \n''')

    if ARTISTFOLDERS == True:
        Mode = str(input("Input mode >>> "))
        if not(os.path.exists("specinput")):
            os.mkdir("specinput")
        fdjf = input("!PRESS ENTER AFTER TRANSFERRING FILES!")
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
            print("The input folder was not found! Creation...")
            os.mkdir("input")
            debug("Creating an input folder", 1)
        if os.path.isdir("output"):
            pass
        else:
            print("Output folder not found! Creation...")
            os.mkdir("output")
            debug("Creating the Output folder", 1)

        if os.path.isdir("datapack"):
            pass
        else:
            print("datapack folder not found!")
            debug("Critical files were not found, shutdown...", 2)
            raise SystemExit

        if os.path.exists("datapack\\blank.png"):
            pass
        else:
            print("blank.png not found!")
            debug("Critical file was not found, shutdown...", 2)
            raise SystemExit

        if os.path.exists("datapack\\font.ttf"):
            pass
        else:
            print("font.ttf not found!")
            debug("Critical file was not found, shutdown...", 2)
            raise SystemExit

        if os.path.isdir("datapack\\lang"):
            pass
        else:
            print("lang folder not found!")
            debug("Critical files were not found, shutdown...", 2)
            raise SystemExit

        if os.path.exists("config.ini"):
            configfile = configparser.ConfigParser()
            configfile.read('config.ini')
            debug(configfile)
            if DAYZTOOLSDIRARGV == False:
                dayztooldir = configfile["MAIN"]["dayztoolsdir"]
                debug(dayztooldir)
            if  not(os.path.exists(f"{dayztooldir}\\Bin\\AddonBuilder\\AddonBuilder.exe") and os.path.exists(f"{dayztooldir}\\Bin\\DsUtils\\DSCreateKey.exe") and os.path.exists(f"{dayztooldir}\\Bin\\DsUtils\\DSSignFile.exe") and os.path.exists(f"{dayztooldir}\\Bin\\ImageToPAA\\ImageToPAA.exe")):
                print(f"the dayztools files were not found or damaged, please enter the new path to the DayZTools files")
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
                        print(f"dayztools files not found or corrupted, please try again")
        else:
            config = configparser.ConfigParser()
            windll = ctypes.windll.kernel32
            locallang = locale.windows_locale[ windll.GetUserDefaultUILanguage()]
            if not(locallang + '.txt' in os.listdir(f'datapack\\lang\\')):
                locallang == 'en_US'
            while True:
                dayztooldir = str(input("The path to the DayzTools folder >>>"))
                if os.path.exists(f"{dayztooldir}\\Bin\\AddonBuilder\\AddonBuilder.exe") and os.path.exists(f"{dayztooldir}\\Bin\\DsUtils\\DSCreateKey.exe") and os.path.exists(f"{dayztooldir}\\Bin\\DsUtils\\DSSignFile.exe") and os.path.exists(f"{dayztooldir}\\Bin\\ImageToPAA\\ImageToPAA.exe"):
                    config['MAIN'] = {'dayztoolsdir': dayztooldir, 'lang' : locallang}
                    with open('config.ini', 'w') as configfile:
                        config.write(configfile)
                        break
                else:
                    print(f"dayztools files not found or corrupted, please try again")

        configfile = configparser.ConfigParser()
        configfile.read('config.ini')

        if os.path.exists("datapack\\lang\\" + configfile["MAIN"]["lang"] + ".txt"):
            langfile = open("datapack\\lang\\" + configfile["MAIN"]["lang"] + ".txt", encoding='utf-8')
        else:
            langfile = open("datapack\\lang\\en_US.txt", encoding='utf-8')
        rawlangpacket = langfile.readlines()
        langpacket = [b.rstrip() for b in rawlangpacket]

        if ARGVADDON == False and ARTISTFOLDERS == False:
            NameOfAddon = input(f"{langpacket[0]} >>> ").replace(" ", "_")
            if wordtest(NameOfAddon) == False:
                while True:
                    print(langpacket[1])
                    NameOfAddon = input(f"{langpacket[0]} >>> ").replace(" ", "_")
                    if wordtest(NameOfAddon) == True:
                        break
        elif ARTISTFOLDERS == True:
            NameOfAddon = syntaxofsymbols(artistfoldersfiles[artis])
        while True:
            if os.path.isdir(f"output\\{NameOfAddon}"):
                print(f"{NameOfAddon} {langpacket[2]} ")
                print(langpacket[3])
                print(" ")
                INPUT_AAA = input(f"{langpacket[0]} >>> ")
                if INPUT_AAA == "":
                    shutil.rmtree(f"output\\{NameOfAddon}")
                    break
                else:
                    NameOfAddon = INPUT_AAA
            else:
                break

        files = os.listdir("input\\")

        if len(files) == 0:
            print(langpacket[4])
            while True:
                input()
                files = os.listdir("input\\")
                if len(files) > 0:
                    break
                else:
                    print(langpacket[5])

        fordellist = []
        for t in range(len(files)):
            if os.path.isdir(f"input\\{files[t]}"):
                print(f"File {files[t]} is a folder, it will be ignored")
                fordellist.append(t)
        for ta in range(len(fordellist)):
            files.pop(fordellist[ta])

        if ARGVMODE == False and ARTISTFOLDERS == False:
            print(langpacket[6])
            print(langpacket[7])
            print(langpacket[8])
            print(langpacket[9])
            print(langpacket[10])
            print(" ")
            Mode = str(input(f"{langpacket[11]} >>> "))
        if Mode != "1" and Mode != "2" and Mode != "3" and Mode != "4":
            print(langpacket[12])
            Mode = "1"
        if TEXTUREMODE == False and ARTISTFOLDERS == False:
            print(langpacket[13])
            print(langpacket[14])
            print(langpacket[15])
            print(" ")
            TextureMode = str(input(f"{langpacket[13]} >>> "))
        if TextureMode != "1" and TextureMode != "2":
            print(langpacket[16])
            TextureMode = "1"
        if TextureMode == "2" and Mode == "2":
            print(langpacket[17])
            TextureMode = "1"

        debug(f"NameOfAddon - {NameOfAddon}, Mode - {Mode}",0)
        os.mkdir(f"output\\{NameOfAddon}")
        debug(f"output\\{NameOfAddon}",0)
        os.mkdir(f"output\\{NameOfAddon}\\Cassettes")
        debug(f"output\\{NameOfAddon}\\Cassettes",0)
        os.mkdir(f"output\\{NameOfAddon}\\Cassettes\\sounds")
        debug(f"output\\{NameOfAddon}\\Cassettes\\sounds",0)
        if TextureMode == "2":
            os.mkdir(f"output\\{NameOfAddon}\\Cassettes\\textures")
            debug(f"output\\{NameOfAddon}\\Cassettes\\textures", 0)
        scriptfile = open(f"output\\{NameOfAddon}\\config.cpp", "w", encoding='utf8')
        debug(f"scriptfile = output\\{NameOfAddon}\\config.cpp, 'w', encoding='utf8'", 0)
        debug(f"Files: \n{files}",1)

        print(langpacket[18])
        scriptfile.write("class CfgPatches { \n")
        scriptfile.write(f"	class {NameOfAddon}_Cassettes\n")
        scriptfile.write('	{\n')
        scriptfile.write('		units[]={};\n')
        scriptfile.write('		weapons[]={};\n')
        scriptfile.write('		requiredVersion=0.1;\n')
        scriptfile.write('		requiredAddon[]=\n')
        scriptfile.write('		{\n')
        scriptfile.write('			"DZ_Data",\n')
        scriptfile.write('			"FoXyRadio"\n')
        scriptfile.write('		};\n')
        scriptfile.write('	};\n')
        scriptfile.write('};\n')
        scriptfile.write("class CfgMods { \n")
        scriptfile.write(f"	class {NameOfAddon}_Cassettes\n")
        scriptfile.write('	{\n')
        scriptfile.write(f'      dir="{NameOfAddon}";\n')
        scriptfile.write(f'      name="{NameOfAddon}";\n')
        scriptfile.write('		author="Igorir3-s bot";\n')
        scriptfile.write('		type="mod";\n')
        scriptfile.write('		dependencies[]={};\n')
        scriptfile.write('  };\n')
        scriptfile.write('};\n')
        oggfiles = []
        totreadinglistoffiles = []
        metadata = []
        playlists = []
        process = []
        fordeleatefile = []
        ListOfTextures = []
        print(langpacket[19])
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
                    if audiofile.tag == None:
                        debug(f"mp3 are corrupted", 2)
                        print(f"{langpacket[20]} {oldfilename}{langpacket[21]}")
                        aaa = input(f"{langpacket[22]} >>> ")
                        if aaa.lower() == "y":
                            raise SystemExit
                        else:
                            fordeleatefile.append(f"{oldfilename}.mp3")
                            oggfiles = oggfiles[:-1]
                            continue
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
                    debug(f"metadata - {[title, artist, album]}")

                    #texture module/
                    if TextureMode == "2":
                        stickerimage = audiofile.tag.images
                        debug(f"len(stickerimage) == {len(stickerimage)}")
                        if len(stickerimage) > 0:
                            listofstickers = []
                            for x in stickerimage:
                                img = Image.open(BytesIO(x.image_data))
                                enhancer = ImageEnhance.Brightness(img)
                                img = enhancer.enhance(1.5)
                                img = img.filter(ImageFilter.MedianFilter(size=1))
                                img = img.filter(ImageFilter.SMOOTH)

                                listofstickers.append(img)
                            while True:
                                if len(listofstickers) > COUNTOFSTICKERS:
                                    listofstickers.pop()
                                elif len(listofstickers) < COUNTOFSTICKERS:
                                    listofstickers.append(listofstickers[len(listofstickers) - 1])
                                else:
                                    break
    
                        img = Image.open("datapack\\blank.png")
                        draw = ImageDraw.Draw(img)
                        # font = ImageFont.truetype(<font-file>, <font-size>)
                        text = audiofile.tag.title
                        fontsize = 1

                        while True:
                            font = ImageFont.truetype('datapack\\font.ttf', fontsize)
                            if font.getbbox(text)[2] < 540 - 80 and font.getbbox(text)[3] < 90 - 54:
                                fontsize = fontsize + 1
                            else:
                                break
                        # draw.text((x, y),"Sample Text",(r,g,b))
                        text_image = Image.new('RGBA', (476,36), (0,0,0,0))
                        dr = ImageDraw.Draw(text_image)
                        dr.text((0, 0), text, (0, 0, 0), font=font, fontsize=fontsize)
                        text_image = text_image.transpose(Image.FLIP_LEFT_RIGHT)
                        img.paste(text_image, (80, 54), text_image)

                        if len(stickerimage) > 0:
                            for a in listofstickers:
                                a = a.resize((100, 100))
                                a = a.transpose(Image.FLIP_LEFT_RIGHT)
                                mask_im = Image.new("L", a.size, 0)
                                draw = ImageDraw.Draw(mask_im)
                                draw.ellipse((0, 0, 100, 100), fill=255)
                                img.paste(a.rotate(random.randint(0, 120) - 60),(random.randint(0, 400), random.randint(100, 290 - 90)), mask_im)
                        img.save(f'{syntaxofsymbols(filename)}.png')

                        os.chdir(f"{dayztooldir}\\Bin\\ImageToPAA")
                        os.system(f"ImageToPAA.exe {WORKDIR}\\{syntaxofsymbols(filename)}.png {WORKDIR}\\output\\{NameOfAddon}\\Cassettes\\textures\\{syntaxofsymbols(filename)}.paa")
                        os.chdir(WORKDIR)
                        if os.path.exists(f'{syntaxofsymbols(filename)}.png'):
                            os.remove(f'{syntaxofsymbols(filename)}.png')

                        ListOfTextures.append(f"{NameOfAddon}\\Cassettes\\textures\\{syntaxofsymbols(filename)}.paa")

                    #\texture module

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
                    debug(f"No mp3 file found!", 2)
                    print(langpacket[23])
                    aaa = input(f"{langpacket[22]} [Y/n] >>> ")
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
                if syntaxofsymbols(filename) != oldfilename:
                    if not(os.path.exists(f"input\\{syntaxofsymbols(filename)}.ogg")):
                        os.rename(f"input\\{oldfilename}.ogg", f"input\\{syntaxofsymbols(filename)}.ogg")
                    else:
                        debug(f"Duplicate file found {syntaxofsymbols(filename)}.ogg", 1)
                        os.remove(f"input\\{oldfilename}.ogg")
                if os.path.isfile(f"output\\{NameOfAddon}\\Cassettes\\sounds\\{syntaxofsymbols(filename)}.ogg") == False:
                    shutil.move(f"input\\{syntaxofsymbols(filename)}.ogg", f"output\\{NameOfAddon}\\Cassettes\\sounds\\")
                else:
                    debug(f'os.path.isfile(f"output\\{NameOfAddon}\\Cassettes\\sounds\\{syntaxofsymbols(filename)}.ogg") == True', 2)
                    os.remove(f"input\\{syntaxofsymbols(filename)}.ogg")
                    error = True
                if TextureMode == "2":
                    img = Image.open("datapack\\blank.png")
                    draw = ImageDraw.Draw(img)
                    # font = ImageFont.truetype(<font-file>, <font-size>)
                    text = filename
                    fontsize = 1
                    while True:
                        font = ImageFont.truetype('datapack\\font.ttf', fontsize)
                        if font.getbbox(text)[2] < 540 - 80 and font.getbbox(text)[3] < 90 - 54:
                            fontsize = fontsize + 1
                        else:
                            if fontsize != 1:
                                fontsize = fontsize - 1
                            break
                    # draw.text((x, y),"Sample Text",(r,g,b))
                    text_image = Image.new('RGBA', (476, 36), (0, 0, 0, 0))
                    dr = ImageDraw.Draw(text_image)
                    dr.text((0, 0), text, (0, 0, 0), font=font, fontsize=fontsize)
                    text_image = text_image.transpose(Image.FLIP_LEFT_RIGHT)
                    img.paste(text_image, (80, 54), text_image)
                    img.save(f'{syntaxofsymbols(filename)}.png')

                    os.chdir(f"{dayztooldir}\\Bin\\ImageToPAA")
                    os.system(
                        f"ImageToPAA.exe {WORKDIR}\\{syntaxofsymbols(filename)}.png {WORKDIR}\\output\\{NameOfAddon}\\Cassettes\\textures\\{syntaxofsymbols(filename)}.paa")
                    os.chdir(WORKDIR)
                    if os.path.exists(f'{syntaxofsymbols(filename)}.png'):
                        os.remove(f'{syntaxofsymbols(filename)}.png')

                    ListOfTextures.append(f"{NameOfAddon}\\Cassettes\\textures\\{syntaxofsymbols(filename)}.paa")

            if len(fordeleatefile) > 0:
                for x in fordeleatefile:
                    os.remove(x)

        print(langpacket[24])
        for dp in process:
            dp.join()
        print(langpacket[25])
        print(langpacket[26])
        if TextureMode == "2":
            if len(oggfiles) != len(ListOfTextures):
                debug("CRITICAL ERROR! len(oggfiles) != len(ListOfTextures)")
                raise SystemExit
        scriptfile.write('class CfgVehicles {\n' )
        scriptfile.write('    class Cassette;\n' )
        if Mode == "1":
            for j in tqdm(range(len(oggfiles))):
                if TextureMode == "2":
                    TextureLink = ListOfTextures[j]
                else:
                    TextureLink = "FoXyRadio\\data\\textures\\cassettes\\blank.paa"
                debug(TextureLink)
                scriptfile.write(f'    class {NameOfAddon}_{syntaxofsymbols(oggfiles[j])}: Cassette\n' )
                scriptfile.write('        {\n' )
                scriptfile.write(f'       displayName="{langpacket[35]} {syntaxofsymbols(oggfiles[j], True)}";\n' )
                scriptfile.write(f'        descriptionShort="{langpacket[37]}";\n' )
                scriptfile.write('        hiddenSelections[] =' )
                scriptfile.write('        {' )
                scriptfile.write('            "zbytek"' )
                scriptfile.write('        };' )
                scriptfile.write("        hiddenSelectionsTextures[]=\n" )
                scriptfile.write("        {\n" )
                scriptfile.write(f'            "{TextureLink}"\n')
                scriptfile.write("        };\n" )
                scriptfile.write("    };\n" )
        if Mode == "2":
            for j in tqdm(range(len(oggfiles))):
                print(oggfiles[j])
                scriptfile.write(f'    class {NameOfAddon}_{syntaxofsymbols(oggfiles[j])}: Cassette\n')
                scriptfile.write('        {\n')
                scriptfile.write(f'       displayName="{input(f"{langpacket[33]} {oggfiles[j]} >>> ")}";\n')
                scriptfile.write(f'        descriptionShort="{input(f"{langpacket[34]} {oggfiles[j]} >>> ")}";\n')
                scriptfile.write('        hiddenSelections[] =')
                scriptfile.write('        {')
                scriptfile.write('            "zbytek"')
                scriptfile.write('        };')
                scriptfile.write("        hiddenSelectionsTextures[]=\n")
                scriptfile.write("        {\n")
                scriptfile.write('            "FoXyRadio\\data\\textures\\cassettes\\blank.paa"\n')
                scriptfile.write("        };\n")
                scriptfile.write("    };\n")
        if Mode == "3":
            for j in tqdm(range(len(oggfiles))):
                if TextureMode == "2":
                    TextureLink = ListOfTextures[j]
                else:
                    TextureLink = "FoXyRadio\\data\\textures\\cassettes\\blank.paa"
                debug(TextureLink)
                scriptfile.write(f'    class {NameOfAddon}_{syntaxofsymbols(oggfiles[j])}: Cassette\n')
                scriptfile.write('        {\n')
                scriptfile.write(f'       displayName="{langpacket[35]} {syntaxofsymbols(metadata[j][0], True)}";\n')
                scriptfile.write(f'        descriptionShort="{langpacket[36]} {syntaxofsymbols(metadata[j][2], True)}{langpacket[38]} {syntaxofsymbols(metadata[j][1], True)}";\n')
                scriptfile.write('        hiddenSelections[] =')
                scriptfile.write('        {')
                scriptfile.write('            "zbytek"')
                scriptfile.write('        };')
                scriptfile.write("        hiddenSelectionsTextures[]=\n")
                scriptfile.write("        {\n")
                scriptfile.write(f'            "{TextureLink}"\n')
                scriptfile.write("        };\n")
                scriptfile.write("    };\n")
        if Mode == "4":
            pass
        scriptfile.write("};\n" )

        print(langpacket[25])
        print(langpacket[27])

        scriptfile.write('class CfgSoundSets {\n')
        scriptfile.write('class FoXyRadio_SoundSet_Base;\n')
        scriptfile.write('class FoXyRadioLoop_SoundSet_Base;\n')
        for u in tqdm(range(len(oggfiles))):
            scriptfile.write(f'	class {NameOfAddon}_{syntaxofsymbols(oggfiles[u])}_SoundSet: FoXyRadio_SoundSet_Base\n')
            scriptfile.write('  {\n' )
            scriptfile.write('		soundShaders[]=\n' )
            scriptfile.write('		{\n' )
            scriptfile.write(f'			"{NameOfAddon}_{syntaxofsymbols(oggfiles[u])}_SoundShader"\n')
            scriptfile.write('		};\n' )
            scriptfile.write('	};\n' )
        scriptfile.write('};\n' )

        print(langpacket[25])
        print(langpacket[28])
        scriptfile.write('class CfgSoundShaders {\n' )
        scriptfile.write('	class FoXyRadio_SoundShader_Base;\n' )
        for t in tqdm(range(len(oggfiles))):
            scriptfile.write(f'	class {NameOfAddon}_{syntaxofsymbols(oggfiles[t])}_SoundShader: FoXyRadio_SoundShader_Base\n' )
            scriptfile.write('  {\n' )
            scriptfile.write('		samples[]=\n' )
            scriptfile.write('		{\n' )
            scriptfile.write('			{\n' )
            scriptfile.write(f'				"{NameOfAddon}\Cassettes\sounds\{syntaxofsymbols(oggfiles[t])}.ogg",\n' )
            scriptfile.write('				1\n' )
            scriptfile.write('			}\n' )
            scriptfile.write('		};\n' )
            scriptfile.write('	};\n' )
        scriptfile.write('};\n' )
        print(langpacket[25])
        print(langpacket[29])

        f = open(f"output\\{NameOfAddon}_{UnikID}_types.xml", "w", encoding='utf8')
        for t in tqdm(range(len(oggfiles))):
            xmlstrpart = f'''           <type name="{NameOfAddon}_{syntaxofsymbols(oggfiles[t])}">
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
            </type>\n'''
            f.write(xmlstrpart)
        f.close()
        scriptfile.close()

        #PACK IN PBO - #### YOU DAYZ TOOLS
        if PAUSEBEFOREPBO == True:
            x = input("PAUSE")
            if x.lower() == "exit":
                raise SystemExit
        print(f"{langpacket[30]} {NameOfAddon} {langpacket[31]}")
        debug(f"Packing {NameOfAddon} in PBO")
        debug(f"dayztooldir - {dayztooldir}")
        includefile = open(f"output\\{NameOfAddon}_{UnikID}_include.txt", "w", encoding='utf8')
        includefile.write("*.emat;*.edds;*.ptc;*.c;*.imageset;*.layout;*.ogg;*.paa;*.rvmat;")
        includefile.close()
        debug(f'chdir "{dayztooldir}\\Bin\\AddonBuilder\\"')
        os.chdir(f"{dayztooldir}\\Bin\\AddonBuilder")
        debug(f'AddonBuilder.exe "{WORKDIR}output\\{NameOfAddon}" "{WORKDIR}output\\{NameOfAddon}" -clear -packonly -include="{WORKDIR}output\\{NameOfAddon}_{UnikID}_include.txt"')
        os.system(f'AddonBuilder.exe "{WORKDIR}output\\{NameOfAddon}" "{WORKDIR}output\\{NameOfAddon}" -clear -packonly -include="{WORKDIR}output\\{NameOfAddon}_{UnikID}_include.txt"')
        os.chdir(WORKDIR)

        debug("Creating directories")
        os.remove(f"output\\{NameOfAddon}_{UnikID}_include.txt")
        os.mkdir(f"output\\@{NameOfAddon}")
        os.mkdir(f"output\\@{NameOfAddon}\\Keys")
        os.mkdir(f"output\\@{NameOfAddon}\\Addons")

        debug("Moving files")
        shutil.move(f"output\\{NameOfAddon}_{UnikID}_types.xml", f"output\\@{NameOfAddon}")
        shutil.move(f"output\\{NameOfAddon}\\{NameOfAddon}.pbo", f"output\\@{NameOfAddon}\\Addons")
        shutil.rmtree(f"output\\{NameOfAddon}")

        debug("Creating a key")
        os.chdir(f"{dayztooldir}\\Bin\\DsUtils")
        os.system(f'DSCreateKey.exe {UnikID}')
        shutil.copy(f"{dayztooldir}\\Bin\\DsUtils\\{UnikID}.bikey", f"{WORKDIR}output\\@{NameOfAddon}\\Keys")

        debug("Assigning a key")
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
    input(langpacket[32])
    os.system("cls")