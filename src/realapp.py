import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import pandas as pd

df_global = None


#ÁREA DE FUNCIONES DE LAS ACCIONES A REALIZAR EN EL PROGRAMA
def cargar_archivo():
  global df_global
  ruta_archivo = filedialog.askopenfilename(
    title="Seleccione un archivo en formato CSV",
    filetypes=[("Archivos CSV", "*.csv")]
  )
  
  if ruta_archivo:
    try:
      df_global = pd.read_csv(ruta_archivo)
      messagebox.showinfo("Éxitoso", f"Archivo cargado correctamente. \nColumnas: {list(df_global.columns)}")
      return df_global
    except Exception as error:
      messagebox.showinfo("Error", f"No se pudo cargar el archivo:\n{error}")
  else:
    messagebox.showwarning("Aviso", "No se seleccionó ningún archivos.")
 
def mostrar_datos():
  for item in tree.get_children():
    tree.delete(item)
    
    if df_global is not None:
      #configuracion de columnas del treeview
      tree["columns"] = list(df_global)
      tree["show"] = "headings"
    
 
#ÁREA DE VENTANAS CON TKINTER 
#Ventana principal
root = tk.Tk()
root.title("Proyecto Estadística")
root.geometry("1080x720")

#boton para cargar archivo
btn_cargar = tk.Button(root, text="Cargar archivo CSV", command=cargar_archivo)
btn_cargar.pack(padx=0, pady=10)

#treeview
tree = ttk.Treeview(root)


root.mainloop()