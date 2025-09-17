import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import pandas as pd
import numpy as np
import math

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
    
    #Frecuencia Relativa Porcentual
    fr_porcentual = f / n * 100
    
    #Frecuancia Acumulada
    Fa = f.cumsum()
    
    #Frecuencia Acumulada Porcentual
    Fa_porcentual = fr_porcentual.cumsum()
    
    #Frecuencia Descendente
    Fd = f.iloc[::-1].cumsum().iloc[::-1]
    
    #Frecuencia Descendente Porcentual
    Fd_porcentual = Fd / n * 100 
    
    df_distribucion_simple = pd.DataFrame({
      "Valor": f.index,
      "Frecuencia Absoluta (f)": f.values,
      "Frecuencia Relativa (fr%)": fr_porcentual.values,
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

# def calcular_frecuencias_intervalos():
#   if df_global is None:
#     messagebox.showwarning("Aviso", "Primero carga un archivo csv.")
#     return
  
#   ventana_frecuencias_intervalos = tk.Toplevel(root)
#   ventana_frecuencias_intervalos.title("Distribución de Frecuencias por Intervalos.")
#   ventana_frecuencias_intervalos.geometry("1600x500")
  
#   tk.Label(ventana_frecuencias_intervalos, text="Selecciona una columna: ").pack(pady=5)
#   columnas_num = [col for col in df_global.columns if np.issubdtype(df_global[col].dtype, np.number)]
#   combo_col = ttk.Combobox(ventana_frecuencias_intervalos, values=columnas_num, state="readonly")
#   combo_col.pack(pady=5)
  
#   resultado_text = tk.Text(ventana_frecuencias_intervalos, height=20, width=200)
#   resultado_text.pack(pady=10)
  
#   def calcular():
#     col = combo_col.get()
#     if not col:
#       messagebox.showwarning("Aviso", "Selecciona una columna.")
#       return
    
#     data = df_global[col].dropna()
#     n = len(data)
    
#     #regla de sturges
#     k = int(np.ceil(1+ 3.322 * np.log10(n)))
    
#     #Crear limites
#     bins = np.linspace(data.min(), data.max(), num=k+1)
    
#     epsilon = 1e-6
#     limites_inf = bins[:-1]
#     limites_sup = bins[1:] - epsilon
#     limites_sup[-1] = bins[-1]
    
#     #creación de intervalos
#     categorias = pd.cut(data, bins=bins, right=False, include_lowest=True)
    
#     #Intervalos
#     intervalos = categorias.cat.categories
    
#     #LI
#     lim_inf = math.floor(int(categorias.left))
    
#     #LS
#     lim_sup = math.ceil(int(categorias.right))
    
#     #Centro
#     Xi = ((lim_inf + lim_sup) / 2)
    
#     #Frecuencia Absoluta por Intervalos
#     f = categorias.value_counts().sort_index()
    
#     #Frecuencia Relativa Porcentual
#     Fr = f / n * 100
    
#     #Frecuencia Acumulada Ascendente
#     Fa = f.cumsum()
    
#     #Frecuencia Acumulada Porcentual
#     Fa_porcentual = Fr.cumsum()
    
#     #Frecuencia Descendente
#     Fd = f.iloc[::-1].cumsum().iloc[::-1]
    
#     #Frecuencia Descendente Porcentual
#     Fd_porcentual = Fd / n *100
    
#     #dataframe 
#     df_distribucion_intervalos = pd.DataFrame({
#       "LI": lim_inf.values,
#       "LS": lim_sup.values,
#       "Xi": Xi.values,
#       "Frecuencia Absoluta": f.values,
#       "Frecuencia Relativa (%)": Fr.values,
#       "Frecuencia Acumulada": Fa.values,
#       "Frecuencia Acumulada (%)": Fa_porcentual.values,
#       "Frecuencia Descendente": Fd.values,
#       "Frecuencia Descendente (%)": Fd_porcentual.values
#     })
    
#     resultado_text.delete("1.0", tk.END)
#     resultado_text.insert(tk.END, f"Numero de Intervalos: {k} \n\n")
#     resultado_text.insert(tk.END, df_distribucion_intervalos.to_string(index=False))
  
#   btn_calcular = tk.Button(ventana_frecuencias_intervalos, text="Calcular", command=calcular)
#   btn_calcular.pack(pady=5)


#####
def frecuencias_intervalos():
  if df_global is None:
    messagebox.showwarning("Aviso", "Primero carga un archivo csv.")
    return
  
  ventana_frecuencias_intervalos = tk.Toplevel(root)
  ventana_frecuencias_intervalos.title("Distribución de Frecuencias por Intervalos.")
  ventana_frecuencias_intervalos.geometry("1600x500")
  
  tk.Label(ventana_frecuencias_intervalos, text="Selecciona una columna: ").pack(pady=5)
  columnas_num = [col for col in df_global.columns if np.issubdtype(df_global[col].dtype, np.number)]
  combo_col = ttk.Combobox(ventana_frecuencias_intervalos, values=columnas_num, state="readonly")
  combo_col.pack(pady=5)
  
  resultado_text = tk.Text(ventana_frecuencias_intervalos, height=20, width=200)
  resultado_text.pack(pady=10)
    
  def calcular():
    col = combo_col.get()
    if not col:
      messagebox.showwarning("Aviso", "Selecciona una columna.")
      return
    
    data = df_global[col].dropna()
    
    n = len(data)
    k = int(np.ceil(1 + 3.322 * np.log10(n)))
    
    min_val = int(np.floor(data.min()))
    max_val = int(np.ceil(data.max()))
    
    ancho = max(1, int(np.ceil((max_val - min_val + 1) / k)))
    
    li = []
    ls = []
    start = min_val
    for i in range(k):
      li_val = start
      ls_val = li_val + ancho - 1
      if ls_val > max_val:
        ls_val = max_val
      if li_val > ls_val:
        break
      li.append(li_val)
      ls.append(ls_val)
      start = ls_val + 1
      
    intervalos = pd.IntervalIndex.from_arrays(li, ls, closed="both")
    
    categorias = pd.cut(data, bins=intervalos)
    
    f = categorias.value_counts().sort_index()
    Fr_porcentual = f / n * 100
    Fa = f.cumsum()
    Fa_porcentual = Fr_porcentual.cumsum()
    Fd = f.iloc[::-1].cumsum().iloc[::-1]
    Fd_porcentual = Fd / n * 100
    
    xi = [(li_val + ls_val) / 2 for li_val, ls_val in zip(li, ls)]
    
    intervalos_str = [f"[{li_val}, {ls_val}]" for li_val, ls_val in zip(li, ls)]
    
    df_distribucion_intervalos = pd.DataFrame({
      "Intervalos": intervalos_str,
      "LI": li,
      "LS": ls,
      "Xi": xi,
      "Frecuencia Absoluta": f.values,
      "Frecuencia Relativa (%)": Fr_porcentual.values,
      "Frecuencia Acumulada": Fa.values,
      "Frecuencia Acumulada (%)": Fa_porcentual.values,
      "Frecuencia Descendente": Fd.values,
      "Frecuencia Descendente (%)": Fd_porcentual.values
    })
    
    resultado_text.delete("1.0", tk.END)
    resultado_text.insert(tk.END, f"Numero de Intervalos: {k} \n\n")
    resultado_text.insert(tk.END, df_distribucion_intervalos.to_string(index=False))
  
  btn_calcular = tk.Button(ventana_frecuencias_intervalos, text="Calcular", command=calcular)
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

#boton para mostrar datos
btn_mostrar_datos = tk.Button(root, text="Mostrar datos cargados", command=mostrar_datos)
btn_mostrar_datos.pack(padx=0, pady=10)

#boton para frecuencias simples
btn_frecuencias_simples = tk.Button(root, text="Calcular Frecuencias Simples", command=calcular_frecuencias_simples)
btn_frecuencias_simples.pack(pady=10)

btn_frecuencias_intervalos = tk.Button(root, text="Calcular Frecuencias por Intervalos", command=frecuencias_intervalos)
btn_frecuencias_intervalos.pack(pady=10)

root.mainloop()
