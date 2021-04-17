import os
import tkinter.messagebox
from tkinter import *
from tkinter import ttk
import sumoGame

from PIL import ImageTk, Image
from cryptography.fernet import Fernet, InvalidToken


def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


resource_path('venv/UI/Sumocrypt.png')
resource_path('venv/UI/tizzycrypt.ico')


class Crypt:

    def make_key(self):  # Makes the encryption key and writes it to a file
        self.key_make = Fernet.generate_key()
        key_file = open('key.key', 'wb')
        key_file.write(self.key_make)
        key_file.close()
        key_file = open('key.key', 'rb')
        self.key = key_file.read()
        key_file.close()
        tkinter.messagebox.showinfo('Done', "Key generated. Your key is: {} ".format(self.key) + "You will find the "
                                                                                                 "file located in "
                                                                                                 "the project "
                                                                                                 "directory "
                                                                                                 "as 'key.key' ")

    def get_key(self):  # Reads the .key file and stores the key as a variable
        key_file = open('key.key', 'rb')
        self.key = key_file.read()
        key_file.close()



class Tkinter_GUI:

    def __init__(self, master):  # Defines beginning frames of the program
        self.master = master
        self.f1 = Frame(master, width=500, height=600)
        self.f1.pack()
        self.f2 = Frame(master, width=500, height=600)
        self.f2.pack()

        # Defines image to be used as background
        path = "venv/UI/Sumocrypt.png"
        img = ImageTk.PhotoImage(Image.open(path))
        panel = Label(self.f1, image=img)
        panel.photo = img
        panel.grid(column=0, row=1, )

        welcome = Label(self.f1, font=("Calibri", 16, "bold"), borderwidth=25,
                        text='Welcome to SumoCrypt, an all in one base64 encrypter and decrypter.')
        welcome.grid(column=0, row=0)

        state = Label(self.f1, text='Please Select an Option.', font=('Calibri', 14, 'bold'), borderwidth=25)
        state.grid(column=0, row=2)

        gt_gen_key_btn = Button(self.f2, font=('Calibri', 16, 'bold'), text='Generate Key',
                                command=self.gt_gen_key)
        gt_gen_key_btn.grid(column=0, row=1, sticky=W)

        gt_encrypt_btn = Button(self.f2, text='Encrypt Files', font=('Calibri', 16, 'bold'), command=self.gt_crypt)
        gt_encrypt_btn.grid(column=1, row=1)

        gt_decrypt_btn = Button(self.f2, text='Decrypt Files', font=('Calibri', 16, 'bold'), command=self.gt_decrypt)
        gt_decrypt_btn.grid(column=2, row=1)

        gt_chat_btn = Button(self.f2, text='Chat', font=('Calibri', 16, 'bold'), command=self.runGame)
        gt_chat_btn.grid(column=3, row=1)

    def gt_gen_key(self):
        self.var = 0
        self.f1.pack_forget()
        self.f2.pack_forget()
        self.f_key = Frame(self.master, width=500, height=600)
        self.f_key.pack()
        crypt = Crypt()  # Calls the previous class "Crypt" and allows the functions to be used.

        key_head = Label(self.f_key, text='Press the "Generate Key" to create a random key.',
                         font=('Calibri', 16, 'bold'), borderwidth=100)
        key_head.grid(row=0, column=0, columnspan=2)

        key_btn = Button(self.f_key, text='Generate Key', font=('Calibri', 14, 'bold'), command=crypt.make_key)
        key_btn.grid(row=1, column=1)

        k_menu_btn = Button(self.f_key, text='Return to Menu', font=('Calibri', 14, 'bold'), command=self.rtr_menu)
        k_menu_btn.grid(row=1, column=0)

    def gt_crypt(self):
        self.var = 1
        self.tizzy = 0
        self.f1.pack_forget()
        self.f2.pack_forget()
        self.f_crypt = Frame(self.master, width=500, height=600)
        self.f_crypt.pack()

        crypt_head = Label(self.f_crypt, text='Please enter in the text you wish to encrypt and chose your key.',
                           font=('Calibri', 16, 'bold'), borderwidth=25)
        crypt_head.grid(row=0, column=0, columnspan=4)

        lbl_ent_msg = Label(self.f_crypt, text='Text to be encrypted:', font=('Calibri', 14))
        lbl_ent_msg.grid(column=1, row=1)

        self.ent_msg = Entry(self.f_crypt, width=20)
        self.ent_msg.grid(column=2, row=1, pady=50)

        lbl_ent_key = Label(self.f_crypt, text='Enter custom key:', font=('Calibri', 14))
        lbl_ent_key.grid(column=1, row=2)

        self.ent_key = Entry(self.f_crypt, width=20)
        self.ent_key.grid(column=2, row=2, pady=50)

        crypt_btn_lc = Button(self.f_crypt, text='Encrypt with local key', font=('Calibri', 14, 'bold'),
                              command=self.crypt_msg_func_lc)
        crypt_btn_lc.grid(row=3, column=2)

        self.crypt_btn_cs = Button(self.f_crypt, text='Encrypt with custom key', font=('Calibri', 14, 'bold'),
                                   command=self.crypt_msg_func_cs)
        self.crypt_btn_cs.grid(row=3, column=4)

        cry_menu_btn = Button(self.f_crypt, text='Return to Menu', font=('Calibri', 14, 'bold'), command=self.rtr_menu)
        cry_menu_btn.grid(row=3, column=0)

        self.chk_cs = ttk.Checkbutton(self.f_crypt, command=self.key_chk_btn_func)
        self.chk_cs.grid(row=2, column=0)
        self.chk_cs.state(['!alternate'])

        self.crypt_btn_cs.configure(state='disabled')
        self.ent_key.configure(state='disabled')

    def gt_decrypt(self):
        self.tizzy = 1
        self.var = 2
        self.f1.pack_forget()
        self.f2.pack_forget()
        self.f_decrypt = Frame(self.master, width=500, height=600)
        self.f_decrypt.pack()

        de_head_1 = Label(self.f_decrypt, text='Please choose what file you wish to decrypt.', font=('Calibri',
                                                                                                     16, 'bold'),
                          borderwidth=50)
        de_head_1.grid(row=0, column=0, columnspan=4)

        de_lbl_ent_key = Label(self.f_decrypt, text='Enter encrypted text:', font=('Calibri', 14))
        de_lbl_ent_key.grid(column=1, row=1)

        de_lbl_ent_crypt = Label(self.f_decrypt, text='Enter in key:', font=('Calibri', 14))
        de_lbl_ent_crypt.grid(column=1, row=2)

        self.de_ent_key = Entry(self.f_decrypt, width=20)
        self.de_ent_key.grid(column=2, row=2, pady=50)

        self.ent_crypt = Entry(self.f_decrypt, width=20)
        self.ent_crypt.grid(column=2, row=1, pady=50)

        decrypt_btn_lc = Button(self.f_decrypt, text='Decrypt saved file with local key', font=('Calibri', 14, 'bold'),
                                command=self.decrypt_msg_func_lc)
        decrypt_btn_lc.grid(row=3, column=2)

        self.decrypt_btn_cs = Button(self.f_decrypt, text='Decrypt inputted text with custom key',
                                     font=('Calibri', 14, 'bold'),
                                     command=self.decrypt_msg_func_cs)
        self.decrypt_btn_cs.grid(row=3, column=4)

        de_menu_btn = Button(self.f_decrypt, text='Return to Menu', font=('Calibri', 14, 'bold'), command=self.rtr_menu)
        de_menu_btn.grid(row=3, column=0)

        self.chk_cs = ttk.Checkbutton(self.f_decrypt, command=self.key_chk_btn_func)
        self.chk_cs.grid(row=1, column=0)
        self.chk_cs.state(['!alternate'])

        self.decrypt_btn_cs.configure(state='disabled')
        self.de_ent_key.configure(state='disabled')
        self.ent_crypt.configure(state='disabled')

    def crypt_msg_func_lc(self):
        crypt = Crypt()  # Calls the previous class "Crypt" and allows the functions to be used.

        crypt.get_key()
        message = str(self.ent_msg.get())
        crypt.encode_msg = message.encode()
        crypt.f = Fernet(crypt.key)
        crypt.encrypted = crypt.f.encrypt(crypt.encode_msg)

        msg_file = open('crypt.msg', 'wb')
        msg_file.write(crypt.encrypted)
        msg_file.close()
        self.ent_msg.configure(state='disabled')

        tkinter.messagebox.showinfo('Done', 'Your file is encrypted and is protected by the sheer mass of the Sumo '
                                            'Man.  Please note, if you overwrite your key by generating a new one, '
                                            'your encrypted files will be lost forever.')

    def crypt_msg_func_cs(self):
        try:

            crypt = Crypt()  # Calls the previous class "Crypt" and allows the functions to be used.

            key = str(self.ent_key.get())
            message = str(self.ent_msg.get())
            crypt.encode_msg = message.encode()
            crypt.f = Fernet(key)
            crypt.encrypted = crypt.f.encrypt(crypt.encode_msg)

            self.ent_msg.configure(state='disabled')

            tkinter.messagebox.showinfo('Done', 'Your file is encrypted and is protected by the sheer mass of the Sumo '
                                                'Man.  Please note, if you overwrite your key by generating a new one, '
                                                'your encrypted files will be lost forever.')
        except ValueError:
            tkinter.messagebox.showwarning('Hey!', 'Please use the right format, encryption key must be 32 url-safe '
                                                   'base64-encoded bytes.')

    def rtr_menu(self):

        if self.var == 0:
            self.f_key.pack_forget()
        elif self.var == 1:
            self.f_crypt.pack_forget()
        elif self.var == 2:
            self.f_decrypt.pack_forget()

        self.f1.pack()
        self.f2.pack()

    def decrypt_msg_func_lc(self):  # Opens the encrypted message and stores it in a variable and decrypts it
        try:
            file = open('key.key', 'rb')
            key = file.read()
            file.close()

            with open('crypt.msg', 'rb') as f:
                data = f.read()

            fernet = Fernet(key)
            encrypted = fernet.decrypt(data)
            final = encrypted.decode()
            tkinter.messagebox.showinfo('Done', 'Here is your decrypted message: {}'.format(str(final)))

        except InvalidToken:
            tkinter.messagebox.showerror('Error', 'Error: File is impossible to decrypt, the key does not match. Was '
                                                  'the previous key overwritten?')

    def decrypt_msg_func_cs(self):  # Opens the encrypted message and stores it in a variable and decrypts it
        try:
            key = str(self.de_ent_key.get())
            message = str(self.ent_crypt.get())

            fernet = Fernet(key)
            encrypted = fernet.decrypt(message)
            final = encrypted.decode()
            tkinter.messagebox.showinfo('Done', 'Here is your decrypted message: {}'.format(str(final)))

        except InvalidToken:
            tkinter.messagebox.showerror('Error', 'Error: File is impossible to decrypt, the key does not match. Was '
                                                  'the previous key overwritten?')
        except ValueError:
            tkinter.messagebox.showwarning('Hey!', 'Please use the right format, encryption key must be 32 url-safe '
                                                   'base64-encoded bytes.')
        except TypeError:
            try:
                key = str(self.de_ent_key.get()).encode()
                message = str(self.ent_crypt.get()).encode()
                fernet = Fernet(key)
                encrypted = fernet.decrypt(message)
                final = encrypted.decode()
                tkinter.messagebox.showinfo('Done', 'Here is your decrypted message: {}'.format(str(final)))
            except TypeError:
                try:
                    key = str(self.de_ent_key.get()).encode()
                    message = str(self.ent_crypt.get())
                    fernet = Fernet(key)
                    encrypted = fernet.decrypt(message)
                    final = encrypted.decode()
                    tkinter.messagebox.showinfo('Done', 'Here is your decrypted message: {}'.format(str(final)))

                except TypeError:
                    try:
                        key = str(self.de_ent_key.get())
                        message = str(self.ent_crypt.get()).encode()
                        fernet = Fernet(key)
                        encrypted = fernet.decrypt(message)
                        final = encrypted.decode()
                        tkinter.messagebox.showinfo('Done', 'Here is your decrypted message: {}'.format(str(final)))

                    except TypeError:
                        tkinter.messagebox.showwarning('Hey!', 'Please use the right format, encryption key and '
                                                               'message must be in bytes format. Make sure you keep '
                                                               'the " b " before the key and message. In all '
                                                               "actuality, you shouldn't be seeing this message. If"
                                                               'you are, then you screwed up something terribly. '
                                                               'Congrats.')

    def key_chk_btn_func(self):
        if self.tizzy == 0:
            if self.chk_cs.instate(['selected']):
                self.crypt_btn_cs.configure(state='normal')
                self.ent_key.configure(state='normal')
            else:
                self.crypt_btn_cs.configure(state='disabled')
                self.ent_key.configure(state='disabled')

        if self.tizzy == 1:
            if self.chk_cs.instate(['selected']):
                self.decrypt_btn_cs.configure(state='normal')
                self.de_ent_key.configure(state='normal')
                self.ent_crypt.configure(state='normal')
            else:
                self.decrypt_btn_cs.configure(state='disabled')
                self.de_ent_key.configure(state='disabled')
                self.ent_crypt.configure(state='disabled')

    def runGame(self):
        self.master.destroy()
        sumoGame.main()



def main():  # Packs the GUI class into a main function and sets program basics
    program = Tk()
    program.title('SUMOCORE  © 2020 SUMO')
    program.geometry('1350x850')
    program.iconbitmap('venv/UI/tizzycrypt.ico')
    app = Tkinter_GUI(program)
    program.mainloop()


if __name__ == '__main__':  # Makes sure the module is being ran directly instead of being imported
    main()
