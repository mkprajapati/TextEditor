import os
from tkinter import *
import tkinter.filedialog
import tkinter.messagebox
Title="My Text Editor"
root=Tk()
root.geometry('800x600')
root.title(Title)

#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
def show_popup_menu(event):
    popup_menu.tk_popup(event.x_root, event.y_root)
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
def show_cursor_info_bar():
    show_cursor_info_checked = show_cursor_info.get()
    if show_cursor_info_checked:
        cursor_info_bar.pack(expand='no', fill=None, side='right', anchor='se')
    else:
        cursor_info_bar.pack_forget()
def update_cursor_info_bar(event=None):
    row, col = contenttext.index(INSERT).split('.')
    line_num, col_num = str(int(row)), str(int(col) + 1)  # col starts at 0
    infotext = "Line: {0} | Column: {1}".format(line_num, col_num)
    cursor_info_bar.config(text=infotext)
# change themes
def change_theme(event=None):
    selected_theme = theme_choice.get()
    fg_bg_colors = color_schemes.get(selected_theme)
    foreground_color, background_color = fg_bg_colors.split('.')
    contenttext.config(
        background=background_color, fg=foreground_color)
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
def update_line_numbers(event=None):
    line_numbers = get_line_numbers()
    line_number_bar.config(state='normal')
    line_number_bar.delete('1.0', 'end')
    line_number_bar.insert('1.0', line_numbers)
    line_number_bar.config(state='disabled')
def highlight_line(interval=100):
    contenttext.tag_remove("active_line", 1.0, "end")
    contenttext.tag_add(
        "active_line", "insert linestart", "insert lineend+1c")
    contenttext.after(interval, toggle_highlight)
def undo_highlight():
    contenttext.tag_remove("active_line", 1.0, "end")
def toggle_highlight(event=None):
    if to_highlight_line.get():
        highlight_line()
    else:
        undo_highlight()
def on_content_changed(event=None):
    update_line_numbers()
    update_cursor_info_bar()
def get_line_numbers():
    output = ''
    if show_line_number.get():
        row, col = contenttext.index("end").split('.')
        for i in range(1, int(row)):
            output += str(i) + '\n'


    return output
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
def display_about_messagebox(event=None):
    tkinter.messagebox.showinfo(
        "About", Title + "\n Hey, this is\n simple editor")
def display_help_messagebox(event=None):
    tkinter.messagebox.showinfo(
        "Help", "Help Book: \nDeveloped by\n Mukesh Chakravarti",
        icon='question')
def exit_editor(event=None):
    if tkinter.messagebox.askokcancel("Quit?", "Really quit?"):
        root.destroy()
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
def new_file(event=None):
    root.title("Untitled")
    global file_name
    file_name = None
    contenttext.delete(1.0, END)
def open_file(event=None):
    input_file_name = tkinter.filedialog.askopenfilename(defaultextension=".txt",
                                                         filetypes=[("All Files", "*.*"), ("Text Documents", "*.txt")])
    if input_file_name:
        global file_name
        file_name = input_file_name
        root.title('{} - {}'.format(os.path.basename(file_name), Title))
        contenttext.delete(1.0, END)
        with open(file_name) as _file:
            contenttext.insert(1.0, _file.read())
def write_to_file(file_name):
    try:
        content = contenttext.get(1.0, 'end')
        with open(file_name, 'w') as the_file:
            the_file.write(content)
    except IOError:
        pass  # in actual we will show a error message box.
        # we discuss message boxes in the next section so ignored here.
def save_as(event=None):
    input_file_name = tkinter.filedialog.asksaveasfilename(defaultextension=".txt",
                                                           filetypes=[("All Files", "*.*"), ("Text Documents", "*.txt")])
    if input_file_name:
        global file_name
        file_name = input_file_name
        write_to_file(file_name)
        root.title('{} - {}'.format(os.path.basename(file_name), Title))
    return "break"
def save(event=None):
    global file_name
    if not file_name:
        save_as()
    else:
        write_to_file(file_name)
    return "break"
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
def select_all(event=None):
    contenttext.tag_add('sel', '1.0', 'end')
    return "break"
def find_text(event=None):
    searchtoplevel = Toplevel(root)
    searchtoplevel.title('Find Text')
    searchtoplevel.transient(root)
    searchtoplevel.resizable(False, False)
    Label(searchtoplevel, text="Find All:").grid(row=0, column=0, sticky='e')
    searchentrywidget = Entry(
        searchtoplevel, width=25)
    searchentrywidget.grid(row=0, column=1, padx=2, pady=2, sticky='we')
    searchentrywidget.focus_set()
    ignorecasevalue = IntVar()
    Checkbutton(searchtoplevel, text='Ignore Case', variable=ignorecasevalue).grid(
        row=1, column=1, sticky='e', padx=2, pady=2)
    Button(searchtoplevel, text="Find All", underline=0,
           command=lambda: search_output(
               searchentrywidget.get(), ignorecasevalue.get(),
               contenttext, searchtoplevel, searchentrywidget)
           ).grid(row=0, column=2, sticky='e' + 'w', padx=2, pady=2)

    def close_search_window():
        contenttext.tag_remove('match', '1.0', END)
        searchtoplevel.destroy()
    searchtoplevel.protocol('WM_DELETE_WINDOW', close_search_window)
    return "break"
def search_output(needle, if_ignore_case, contenttext,
                  searchtoplevel, search_box):
    contenttext.tag_remove('match', '1.0', END)
    matchesfound = 0
    if needle:
        startpos = '1.0'
        while True:
            startpos = contenttext.search(needle, startpos,
                                                   nocase=if_ignore_case, stopindex=END)
            if not startpos:
                break
            end_pos = '{}+{}c'.format(startpos, len(needle))
            contenttext.tag_add('match', startpos, end_pos)
            matchesfound += 1
            startpos = end_pos
        contenttext.tag_config(
            'match', foreground='red', background='yellow')
    search_box.focus_set()
    searchtoplevel.title('{} matches found'.format(matchesfound))
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
def cut():
    contenttext.event_generate("<<Cut>>")
    return "break"
def copy():
    contenttext.event_generate("<<Copy>>")
    return "break"
def paste():
    contenttext.event_generate("<<Paste>>")
    return "break"
def undo():
    contenttext.event_generate("<<Undo>>")
    return "break"
def redo(event=None):
    contenttext.event_generate("<<Redo>>")
    return 'break'
newfileicon = PhotoImage(file='icons/new_file.gif')
openfileicon = PhotoImage(file='icons/open_file.gif')
savefileicon = PhotoImage(file='icons/save.gif')
cuticon = PhotoImage(file='icons/cut.gif')
copyicon = PhotoImage(file='icons/copy.gif')
pasteicon = PhotoImage(file='icons/paste.gif')
undoicon = PhotoImage(file='icons/undo.gif')
redoicon = PhotoImage(file='icons/redo.gif')
menubar = Menu(root) 
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label='New', accelerator='Ctrl+N',
                      compound='left', image=newfileicon, underline=0 ,command=new_file)
filemenu.add_command(label='Open', accelerator='Ctrl+O',
                      compound='left', image=openfileicon, underline=0 ,command=open_file)
filemenu.add_command(label='Save', accelerator='Ctrl+S',
                      compound='left', image=savefileicon, underline=0,command=save)
filemenu.add_command(label='Save as', accelerator='Shift+Ctrl+S',command=save_as)
filemenu.add_separator()
filemenu.add_command(label='Exit', accelerator='Alt+F4')
menubar.add_cascade(label='File', menu=filemenu)
#---------
editmenu = Menu(menubar, tearoff=0)
editmenu.add_command(label='Undo', accelerator='Ctrl+Z',
                      compound='left', image=undoicon,command=undo)
editmenu.add_command(label='Redo', accelerator='Ctrl+Y',
                      compound='left', image=redoicon,command=redo)
editmenu.add_separator()
editmenu.add_command(label='Cut', accelerator='Ctrl+X',
                      compound='left', image=cuticon,command=cut)
editmenu.add_command(label='Copy', accelerator='Ctrl+C',
                      compound='left', image=copyicon,command=copy)
editmenu.add_command(label='Paste', accelerator='Ctrl+V',
                      compound='left', image=pasteicon,command=paste)
editmenu.add_separator()
editmenu.add_command(label='Find', underline=0, accelerator='Ctrl+F',command=find_text)
editmenu.add_separator()
editmenu.add_command(label='Select All', underline=7, accelerator='Ctrl+A',command=select_all)
menubar.add_cascade(label='Edit', menu=editmenu)
#---------------------------------------
viewmenu = Menu(menubar, tearoff=0)
show_line_number = IntVar()
show_line_number.set(1)
viewmenu.add_checkbutton(label='Show Line Number', variable=show_line_number,command=update_line_numbers)
show_cursor_info = IntVar()
show_cursor_info.set(1)
viewmenu.add_checkbutton(
    label='Show Cursor Location at Bottom', variable=show_cursor_info,command=show_cursor_info_bar)
to_highlight_line = BooleanVar()
viewmenu.add_checkbutton(label='Highlight Current Line', onvalue=1,
                          offvalue=0, variable=to_highlight_line, command=toggle_highlight)
themesmenu = Menu(menubar, tearoff=0)
viewmenu.add_cascade(label='Themes', menu=themesmenu)

color_schemes = {
    'Default': '#000000.#FFFFFF',
    'Greygarious': '#83406A.#D1D4D1',
    'Aquamarine': '#5B8340.#D1E7E0',
    'Bold Beige': '#4B4620.#FFF0E1',
    'Cobalt Blue': '#ffffBB.#3333aa',
    'Olive Green': '#D1E7E0.#5B8340',
    'Night Mode': '#FFFFFF.#000000',
}
theme_choice = StringVar()
theme_choice.set('Default')
for k in sorted(color_schemes):
    themesmenu.add_radiobutton(label=k, variable=theme_choice,command=change_theme)
menubar.add_cascade(label='View', menu=viewmenu)
#------------
aboutmenu = Menu(menubar, tearoff=0)
aboutmenu.add_command(label='About',command=display_about_messagebox)
aboutmenu.add_command(label='Help',command=display_help_messagebox)
menubar.add_cascade(label='About',  menu=aboutmenu)

root.config(menu=menubar)

shortcutbar = Frame(root,  height=25, background='yellow')
shortcutbar.pack(expand='no', fill='x')

#@@@@@@@@@@@@@@@@@@@@@@@@@@@@
icons = ('new_file', 'open_file', 'save', 'cut', 'copy', 'paste',
         'undo', 'redo', 'find_text')
for i, icon in enumerate(icons):
    tool_bar_icon = PhotoImage(file='icons/{}.gif'.format(icon))
    cmd = eval(icon)
    tool_bar = Button(shortcutbar, image=tool_bar_icon, command=cmd)
    tool_bar.image = tool_bar_icon
    tool_bar.pack(side='left')
line_number_bar = Text(root, width=4, padx=3, takefocus=0,  border=0,
                      foreground='white', background='blue', state='disabled',  wrap='none')
line_number_bar.pack(side='left',  fill='y')
contenttext = Text(root, wrap='word')
contenttext.pack(expand='yes', fill='both')
scrollbar = Scrollbar(contenttext)
contenttext.configure(yscrollcommand=scrollbar.set)
scrollbar.config(command=contenttext.yview)
scrollbar.pack(side='right', fill='y')
cursor_info_bar = Label(contenttext, text='Line: 1 | Column: 1')
cursor_info_bar.pack(expand='no', fill=None, side='right', anchor='se')
contenttext.bind('<KeyPress-F1>', display_help_messagebox)
contenttext.bind('<Control-N>', new_file)
contenttext.bind('<Control-n>', new_file)
contenttext.bind('<Control-O>', open_file)
contenttext.bind('<Control-o>', open_file)
contenttext.bind('<Control-S>', save)
contenttext.bind('<Control-s>', save)
contenttext.bind('<Control-f>', find_text)
contenttext.bind('<Control-F>', find_text)
contenttext.bind('<Control-A>', select_all)
contenttext.bind('<Control-a>', select_all)
contenttext.bind('<Control-y>', redo)
contenttext.bind('<Control-Y>', redo)
contenttext.bind('<Any-KeyPress>', on_content_changed)
contenttext.tag_configure('active_line', background='ivory2')
#@@@@@@@@@@@@@@@@@@@@@@
popup_menu = Menu(contenttext)
for i in ('cut', 'copy', 'paste', 'undo', 'redo'):
    cmd = eval(i)
    popup_menu.add_command(label=i, compound='left', command=cmd)
popup_menu.add_separator()
popup_menu.add_command(label='Select All', underline=7, command=select_all)
contenttext.bind('<Button-3>', show_popup_menu)
contenttext.bind('<Button-3>', show_popup_menu)
contenttext.focus_set()
root.protocol('WM_DELETE_WINDOW', exit_editor)
root.mainloop()








