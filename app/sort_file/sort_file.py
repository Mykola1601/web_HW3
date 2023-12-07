
from threading import Thread
from sys import argv
from pathlib import Path
import shutil
import os

class SortFile:
    def __init__(self, default_path):
        self.DEFAULT_PATH = Path(default_path)
        self.OTHER_FOLDER = "other"

        self.FOLDERS_DATA = {
            "archives": ('ZIP', 'GZ', 'TAR'),
            "video": ('AVI', 'MP4', 'MOV', 'MKV'),
            "audio": ('MP3', 'OGG', 'WAV', 'AMR'),
            "documents": ('DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX', 'CSV', 'XLS'),
            "images": ('JPEG', 'PNG', 'JPG', 'SVG'),
            self.OTHER_FOLDER: ()
        }

        self.CYRILLIC_SYMBOLS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ"
        self.TRANSLATION = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s",
                            "t", "u", "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "ya", "je", "i", "ji", "g")

        self.TRANS = {}
        for c, l in zip(list(self.CYRILLIC_SYMBOLS), self.TRANSLATION):
            self.TRANS[ord(c)] = l
            self.TRANS[ord(c.upper())] = l.upper()

    def makelist(self,path):
        ...

    def normalize(self, text):
        trans_str = ''

        for ch in text:
            tr_ch = '_'
            if ch.isalnum():
                tr_ch = ch.translate(self.TRANS)
            trans_str += tr_ch
    
        return trans_str

    def create_directories(self, path):
        for name in self.FOLDERS_DATA:
            folder_path = f"{path.parent}/{path.name}/{name}"
            if not Path(folder_path).exists():
                os.mkdir(folder_path)

    def create_file_name(self, path, ext, counter = 0):
        file_name = f"{path}{ext}" if not counter else f"{path}_{counter}{ext}"
        return self.create_file_name(path, ext, counter + 1) if os.path.exists(file_name) else file_name           

    def handle_file(self, path): 
        parent_folder_name = self.OTHER_FOLDER
        file = path.name.split('.')
        file_ext = file.pop()
        file_name = '.'.join(file)
        for name, file_list in self.FOLDERS_DATA.items():
            if file_ext.upper() in file_list:
                parent_folder_name = name
                break

        if parent_folder_name:
            file_name = self.create_file_name(f"{self.DEFAULT_PATH}/{parent_folder_name}/{self.normalize(file_name)}", path.suffix)
            os.rename(path, file_name)
            # print(path, '-->', file_name)


    def arrange(self, path):
        if not path.exists():
            print(f"Folder '{path.name}' in '{path.parent}' doesn't exist!")
        elif path.is_file():
            print(f"'{path.name}' is not a folder!")
        else:
            for i in path.iterdir():
                if i.is_dir() and i.name not in self.FOLDERS_DATA:
                    thread1 = Thread(target = self.arrange, args=(i,))
                    thread1.start()
                    threads.append(thread1)
                    # self.arrange(i)
                    # try:
                    #     os.rmdir(i)
                    # except OSError as error:
                    #     print(error)
                    #     print(f"Path {i} can't be removed")
                elif i.is_file():
                    thread2 = Thread(target = self.handle_file, args=(i,))
                    thread2.start()
                    threads.append(thread2)
                    # self.handle_file(i)



    # tread for unpack
    def unpac_tread(self, i, string):
        shutil.unpack_archive(i, string)

    def archives(self, path):
        p = Path(f'{path}\\archives\\')   # p Вказує на папку
        for i in p.iterdir():
            if i.is_file():
                thread = Thread(target=self.unpac_tread, args=(i,  str(i)[: str(i).rindex('.')]))
                thread.start()
                # shutil.unpack_archive(i,  str(i)[: str(i).rindex('.')])


    def empty_dirs_delet(self, path):
        p = Path(path)    # p Вказує на папку
        for i in p.iterdir():
             if i.is_dir() and i.name not in self.FOLDERS_DATA:
                contents = os.listdir(i)
                if len(contents) == 0:
                    # print("deleting empty dir =", i)
                    shutil.rmtree(i)
                    self.empty_dirs_delet(path="")
                else:
                    self.empty_dirs_delet(path=i)





if __name__ == "__main__":
    if len(argv) < 2:
        print('to short folder name!')
        exit()
    # argv.append("D:\\goit\\hlam")
    organizer = SortFile(argv[1])
    lst = organizer.makelist(argv[1])
    print(lst)
    threads = []
    organizer.create_directories(organizer.DEFAULT_PATH)
    organizer.arrange(organizer.DEFAULT_PATH)
    [el.join() for el in threads]
    organizer.empty_dirs_delet(organizer.DEFAULT_PATH)
    organizer.archives(organizer.DEFAULT_PATH)

