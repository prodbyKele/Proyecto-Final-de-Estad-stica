import tkinter as tk

root = tk.Tk()

root.title("Primera Interfaz")
root.geometry("500x500")

label = tk.Label(root, text="Hello World!", font=('Impact', 25))
label.pack(padx = 20, pady= 20)

textbox = tk.Text(root, height=3, font=('Impact', 20))
textbox.pack(padx = 10)

button = tk.Button(root, text='Click me', font=('Impact', 18))
button.pack(padx=10, pady=10 )

button_frame = tk.Frame(root)
button_frame.columnconfigure(0, weight=1)
button_frame.columnconfigure(1, weight=1)
button_frame.columnconfigure(2, weight=1)

btn1 = tk.Button(button_frame, text='1', font=('Impact', 18))
btn1.grid(row=0, column=0, sticky=tk.W+tk.E)

btn2 = tk.Button(button_frame, text='2', font=('Impact', 18))
btn2.grid(row=0, column=1, sticky=tk.W+tk.E)

btn3 = tk.Button(button_frame, text='3', font=('Impact', 18))
btn3.grid(row=0, column=2, sticky=tk.W+tk.E)

btn4 = tk.Button(button_frame, text='4', font=('Impact', 18))
btn4.grid(row=1, column=0, sticky=tk.W+tk.E)

btn5 = tk.Button(button_frame, text='5', font=('Impact', 18))
btn5.grid(row=1, column=1, sticky=tk.W+tk.E)

btn6 = tk.Button(button_frame, text='6', font=('Impact', 18))
btn6.grid(row=1, column=2, sticky=tk.W+tk.E)

button_frame.pack(fill = tk.X)

# Poner widgets manualmente
# antoher_button = tk.Button(root, text="TEST") 
# antoher_button.place(x=200, y=500, height=100, width=100)

root.mainloop()