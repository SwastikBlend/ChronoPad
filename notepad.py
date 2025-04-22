import tkinter as tk
from tkinter import filedialog , messagebox, font
import os

class SimpleNotePad:
    def __init__(self,root):
        self.root =root
        self.root.title("Simple NotePad")
        self.root.geometry("800x600")
        self.root.iconbitmap("Notepadicon.ico")
        self.current_file=None
        self.create_text_area()
        self.create_menu()
        self.create_status_bar()
        self.setup_shortcuts()
        
        
    def create_text_area(self):
        self.text_frame = tk.Frame(self.root)
        self.text_frame.pack(fill= tk.BOTH, expand=True)

        self.scrollbar_y = tk.Scrollbar(self.text_frame)
        self.scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)

        self.scrollbar_x = tk.Scrollbar(self.text_frame , orient=tk.HORIZONTAL)
        self.scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)

        self.text_area = tk.Text(
            self.text_frame,
            yscrollcommand=self.scrollbar_y.set,
            xscrollcommand=self.scrollbar_x.set,
            wrap=tk.NONE,
            undo=True

        )
        modern_font = font.Font(family="Cascadia Code", size=15)
        self.text_area.configure(
            font=modern_font,
            bg="#1e1e1e",
            fg="#ffffff",
            insertbackground="#ffffff",
            selectbackground="#44475a",
            selectforeground="#ffffff"
            )

        self.text_area.pack(fill=tk.BOTH,expand=True)

        self.scrollbar_y.config(command=self.text_area.yview)
        self.scrollbar_x.config(command=self.text_area.xview)

        self.text_area.focus_set()

    def create_menu(self):
        self.menu_bar = tk.Menu(self.root)
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.file_menu.add_command(label="New", command=self.new_file, accelerator="Ctrl+N")
        self.file_menu.add_command(label="Open", command=self.open_file, accelerator="Ctrl+O")
        self.file_menu.add_command(label="Save", command=self.save_file, accelerator="Ctrl+S")
        self.file_menu.add_command(label="Save As", command=self.save_as_file)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=self.exit_app)
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)


        self.edit_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.edit_menu.add_command(label="Undo", command=self.text_area.edit_undo, accelerator="Ctrl+X")
        self.edit_menu.add_command(label="Redo", command=self.text_area.edit_redo, accelerator="Ctrl+Y")
        self.edit_menu.add_separator()
        self.edit_menu.add_command(label="Cut", command=self.cut_text, accelerator="Ctrl+X")
        self.edit_menu.add_command(label="Copy", command=self.copy_text, accelerator="Ctrl+C")
        self.edit_menu.add_command(label="Paste", command=self.paste_text, accelerator="Ctrl+V")
        self.edit_menu.add_separator()
        self.edit_menu.add_command(label="Select All", command=self.select_all, accelerator="Ctrl+A")
        self.menu_bar.add_cascade(label="Edit", menu=self.edit_menu)

        self.format_menu = tk.Menu(self.menu_bar,tearoff=0)
        self.format_menu.add_command(label="World Wrap", command=self.toggle_word_wrap)
        self.menu_bar.add_cascade(label="Format", menu=self.format_menu)

        self.root.config(menu=self.menu_bar)

    def create_status_bar(self):
        self.status_bar = tk.Label(self.root, text="Ready", anchor=tk.W , bg="#2c2c2c",fg= "#ffffff")
        self.status_bar.pack(side=tk.BOTTOM , fill=tk.X)

    def setup_shortcuts(self):
        self.root.bind("<Control-n>", lambda event : self.new_file())
        self.root.bind("<Control-o>", lambda event : self.open_file())
        self.root.bind("<Control-s>", lambda event : self.save_file())
        self.root.bind("<Control-a>", lambda event : self.select_all())

    def new_file(self):
        if self.text_area.edit_modified():
            response = messagebox.askyesnocancel("Unsaved changes", "Do you still want to create a new file?")

            if response is None:
                return
            elif response:
                if not self.save_file():
                    return
                
        self.text_area.delete(1.0, tk.END)
        self.current_file = None
        self.root.title("Notepad Simple")
        self.text_area.edit_modified(False)
        self.status_bar.config(text="New File")

    def open_file(self):
        if self.text_area.edit_modified():
            response = messagebox.askyesnocancel("Unsaved Changes","Do you still want to save changes before opening another file?")
            
            if response:
                if not self.save_file():
                    return
                
            elif response:
                return
                
        file_path = filedialog.askopenfilename(
            defaultextension= ".txt",
            filetypes=[("Text Files","*.txt"),("All files","*.*")]
        )

            
        if file_path:
            self.load_file(file_path)

    def load_file(self , file_path):
        try:
            with open(file_path, 'r' ,encoding='utf-8') as file:
                file_content= file.read()

            self.text_area.delete(1.0, tk.END)
            self.text_area.insert(1.0, file_content)
            self.current_file = file_path 
            self.root.title(f"{os.path.basename(file_path)} - Notepad Simple")
            self.text_area.edit_modified(False)
            self.status_bar.config(text=f"Opened: {file_path}")
        except Exception as e:
            messagebox.showerror("Error" , f"Could not open file: {e}" )
            

    def save_file(self):
        if self.current_file:
            return self._save_to_file(self.current_file)
        else :
            return self.save_as_file()
        
    def save_as_file(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension= ".txt",
            filetypes=[("Text Files", "*.txt"),("All Files", "*.*")]
        )
        if file_path:
            success = self._save_to_file(file_path)
            if success:
                self.current_file=file_path
                self.root.title(f"{os.path.basename(file_path)} - Notepad Simple")
            return success
        return False


    def _save_to_file(self, file_path):
        try:
            content = self.text_area.get(1.0 , tk.END)
            with open(file_path ,'w', encoding= 'utf-8') as file:
                file.write(content)
            self.text_area.edit_modified(False)
            self.status_bar.config(text=f"File saved : {file_path}")
            return True
        except Exception as e:
            messagebox.showerror("Error",f"Could not save file : {e}")
            return False
        
    def exit_app(self):
        if self.text_area.edit_modified():
            response = messagebox.showerror("Unsaved Changes", "Do you want to save changes befor exiting?")

            if response is None:
                return
            elif response: 
                if not self.save_file():
                    return
        self.root.destroy()

    def cut_text(self):
        if self.text_area.tag_ranges(tk.SEL):
            self.copy_text()
            self.text_area.delete(tk.SEL_FIRST , tk.SEL_LAST)

    def copy_text(self):
        if self.text_area.tag_ranges(tk.SEL):
            selected_text = self.text_area.get(tk.SEL_FIRST, tk.SEL_LAST)
            self.root.clipboard_clear()
            self.root.clipboard_append(selected_text)

    def paste_text(self):
        try:
            text = self.root.clipboard_get()
            self.text_area.insert(tk.INSERT , text)
        except tk.TclError:
            pass

    def select_all(self):
        self.text_area.tag_add(tk.SEL, "1.0" , tk.END)
        self.text_area.mark_set(tk.INSERT, "1.0")
        self.text_area.see(tk.INSERT)
        return 'break'
    
    def toggle_word_wrap(self):
        if self.text_area.cget("wrap") == tk.NONE:
            self.text_area.configure(wrap=tk.WORD)
            self.status_bar.config(text="Word Warp: On")
        else:
            self.text_area.configure(wrap=tk.WORD)
            self.status_bar.config(text="Word Warp: Off")

if __name__ == "__main__":
    root = tk.Tk()
    app = SimpleNotePad(root)
    root.mainloop()




                                   

        



        