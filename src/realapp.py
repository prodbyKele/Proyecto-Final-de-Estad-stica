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
      
    except Exception as error:
      messagebox.showinfo("Error", f"No se pudo cargar el archivo:\n{error}")
  else:
    messagebox.showwarning("Aviso", "No se seleccionó ningún archivos.")
 
def mostrar_datos():
  #Limpieza de la tabla
  for item in tree.get_children():
    tree.delete(item)
    
  if df_global is not None:
    #configuracion de columnas del treeview
    tree["columns"] = list(df_global.columns)
    tree["show"] = "headings"
    
    #Crear encabezados
    for col in df_global.columns:
      tree.heading(col, text=col)
      tree.column(col, width=150, anchor='center')
    
    #Crear filas
    for _, row in df_global.iterrows():
      tree.insert("", "end", values=list(row))
      
  else:
    messagebox.showwarning("Aviso", "No hay datos para mostrar")
    
def calcular_frecuencias_simples():
  if df_global is None:
    messagebox.showwarning("Aviso", "Primero debes cargar un archivo CSV.")
      
  ventana_frequencias = tk.Toplevel(root)
  ventana_frequencias.title("Frecuencias Simples")
  ventana_frequencias.geometry("1600x500")
    
  tk.Label(ventana_frequencias, text="Selecciona una columna:").pack(pady=5)
  columnas = list(df_global.columns)
  combo_columnas = ttk.Combobox(ventana_frequencias, values=columnas, state="readonly")
  combo_columnas.pack(pady=5)
  
  resultado_text = tk.Text(ventana_frequencias, height=20, width=200)
  resultado_text.pack(pady=10)
  
  def calcular():
    col = combo_columnas.get()
    if not col:
      messagebox.showwarning("Aviso", "Selecciona una columna.")
      return
    
    data = df_global[col].dropna()
    
    #Frecuencia Absoluta
    f = data.value_counts().sort_index()
    n = f.sum()
    
    #Frecuencia Absoluta Porcentual
    f_porcentual = f / n * 100
    
    #Frecuancia Acumulada
    Fa = f.cumsum()
    
    #Frecuencia Acumulada Porcentual
    Fa_porcentual = f_porcentual.cumsum()
    
    #Frecuencia Descendente
    Fd = f.iloc[::-1].cumsum().iloc[::-1]
    
    #Frecuencia Descendente Porcentual
    Fd_porcentual = Fd / n * 100 
    
    df_distribucion_simple = pd.DataFrame({
      "Valor": f.index,
      "Frecuencia Absoluta (f)": f.values,
      "Frecuencia Relativa (fr%)": f_porcentual.values,
      "Frecuencia Acumulada (Fa)": Fa.values,
      "Frecuencia Acumulada Porcentual (Fa%)": Fa_porcentual.values,
      "Frecuencia Descendente (Fd)": Fd.values,
      "Frecuencia Descendente Porcentual (Fd%)": Fd_porcentual.values
    })
    
    resultado_text.delete("1.0", tk.END)
    resultado_text.insert(tk.END, "Frecuencias: \n")
    resultado_text.insert(tk.END, df_distribucion_simple.to_string(index=False))
    
    #boton para calcular la tabla de frecuencias simples
  btn_calcular = tk.Button(ventana_frequencias, text="Calcular", command=calcular)
  btn_calcular.pack(pady=5)

 
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
tree.pack(expand=True, fill="both")

#scroll
# scrollbar = tk.Scrollbar(tree)
# scrollbar.pack(side="right", fill="y")

#boton para frecuencias simples
btn_frecuencias_simples = tk.Button(root, text="Calcular Frecuencias Simples", command=calcular_frecuencias_simples)
btn_frecuencias_simples.pack(pady=10)

#boton para mostrar datos
btn_mostrar_datos = tk.Button(root, text="Mostrar datos cargados", command=mostrar_datos)
btn_mostrar_datos.pack(padx=0, pady=10)


root.mainloop()