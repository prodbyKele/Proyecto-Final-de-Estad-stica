import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import pandas as pd
import numpy as np
import math
from scipy import stats
from scipy.stats import skew, kurtosis

df_global = None

### FUNCION PARA CARGAR EL ARCHIVO .CSV ###
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

### FUNCION PARA MOSTRAR LOS DATOS ###    
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

### TABLA DE FRECUENCIAS SIMPLES ###   
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
  
  frame_inputs = tk.Frame(ventana_frequencias)
  frame_inputs.pack(padx=10, fill=tk.X)
    
  tk.Label(frame_inputs, text="Ingrese los cuartiles que desee calcular:").grid(row=0, column=0, padx=5)
  entry_cuartiles = tk.Entry(frame_inputs, width=10)
  entry_cuartiles.insert(0, "1, 2, 3, 4")
  entry_cuartiles.grid(row=0, column=1, padx=5)
    
  tk.Label(frame_inputs, text="Ingrese los deciles que desee calcular:").grid(row=0, column=2, padx=5)
  entry_deciles = tk.Entry(frame_inputs, width=10)
  entry_deciles.insert(0, "1, 2, 3, 4, 5, 6, 7, 8, 9, 10")
  entry_deciles.grid(row=0, column=3, padx=5)
    
  tk.Label(frame_inputs, text="Ingrese los percentiles que desee calcular:").grid(row=0, column=4, padx=5)
  entry_percentiles = tk.Entry(frame_inputs, width=10)
  entry_percentiles.insert(0, "10, 25, 50, 75, 100")
  entry_percentiles.grid(row=0, column=5, padx=5)
  
  resultado_text = tk.Text(ventana_frequencias, height=10, width=200)
  resultado_text.pack(pady=10, fill=tk.BOTH, expand=True)
  
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
    
  def tendencias_centrales():
    col = combo_columnas.get()
    if not col:
      messagebox.showwarning("Aviso", "Selecciona una columna.")
      return
    
    data = df_global[col].dropna()
    if len(data) == 0:
      messagebox.showwarning("Información", "La columna no tiene datos.")
    
    media = data.mean()
    mediana = data.median()
    modas = data.mode()
    moda_str = ', '.join(map(str, modas.values))
    
    if (data <= 0).any():
      media_geom = "No definida (datos <= 0)"
    else:
      media_geom = stats.gmean(data)
      
    if (data <= 0).any():
      media_arm = "No definida (datos <= 0)"
    else:
      media_arm = stats.hmean(data)
    
    
    resultado_text.delete("1.0", tk.END)
    resultado_text.insert(tk.END, f"Estadísticas para la columna: {col}\n\n")
    resultado_text.insert(tk.END, f"Media aritmética: {media:.4f}\n")
    resultado_text.insert(tk.END, f"Mediana: {mediana:.4f}\n")
    resultado_text.insert(tk.END, f"Moda: {moda_str}\n")
    resultado_text.insert(tk.END, f"Media geométrica: {media_geom}\n")
    resultado_text.insert(tk.END, f"Media armónica: {media_arm}\n")
  
  def medidas_de_posicion():
    col = combo_columnas.get()
    if not col:
      messagebox.showwarning("Aviso", "Selecciona una columna.")
      return

    data = df_global[col].dropna()
    if len(data) == 0:
      messagebox.showinfo("Información", "La columna seleccionada no tiene datos.")
      return
    
    def parse_posiciones(text, max_val):
      try:
        posiciones = [int(x.strip()) for x in text.split(',') if x.strip() != '']
        for p in posiciones:
          if p < 1 or p > max_val:
            raise ValueError(f'Posición {p} fuera de rango (1-{max_val})')
        return posiciones
      except Exception as e:
        messagebox.showerror("Error", f'Error en posicion: {e}')
        return None
    
    max_cuartiles = 4
    max_deciles = 10
    max_percentiles = 100
    
    pos_cuartiles = parse_posiciones(entry_cuartiles.get(), max_cuartiles)
    if pos_cuartiles is None:
      return
    
    pos_deciles = parse_posiciones(entry_deciles.get(), max_deciles)
    if pos_deciles is None:
      return
    
    pos_percentiles = parse_posiciones(entry_percentiles.get(), max_percentiles)
    if pos_percentiles is None:
      return
    
    resultado_text.delete("1.0", tk.END)
    resultado_text.insert(tk.END, f"Medidas de Posición para la columna: {col}\n\n")
        
    if pos_cuartiles:
      q_probs = [p / max_cuartiles for p in pos_cuartiles]
      cuartiles = data.quantile(q_probs)
      resultado_text.insert(tk.END, "Cuartiles:\n")
      for p, val in zip(pos_cuartiles, cuartiles):
        resultado_text.insert(tk.END, f" Q{p} ({(p/max_cuartiles)*100:.2f}%): {val:.4f}\n")
      resultado_text.insert(tk.END, "\n")
        
    if pos_deciles:
      d_probs = [p / max_deciles for p in pos_deciles]
      deciles = data.quantile(d_probs)
      resultado_text.insert(tk.END, "Deciles:\n")
      for p, val in zip(pos_deciles, deciles):
        resultado_text.insert(tk.END, f" D{p} ({(p/max_deciles)*100:.2f}%): {val:.4f}\n")
      resultado_text.insert(tk.END, "\n")
        
    if pos_percentiles:
      p_probs = [p / max_percentiles for p in pos_percentiles]
      percentiles = data.quantile(p_probs)
      resultado_text.insert(tk.END, "Percentiles:\n")
      for p, val in zip(pos_percentiles, percentiles):
        resultado_text.insert(tk.END, f" P{p} ({(p/max_percentiles)*100:.2f}%): {val:.4f}\n")
      resultado_text.insert(tk.END, "\n")

  def medidas_de_variabilidad():
    col = combo_columnas.get()
    if not col:
      messagebox.showwarning("Aviso", "Selecciona una columna.")
      return

    data = df_global[col].dropna()
    if len(data) == 0:
      messagebox.showinfo("Información", "La columna seleccionada no tiene datos.")
      return
    
    rango = data.max() - data.min()
    media = data.mean()
    desviacion_media = (data - media).abs().mean()
    desviacion_estandar = data.var(ddof=1)
    varianza = data.var(ddof=1)
    
    if media != 0:
      coeficiente_var = (desviacion_estandar/media) * 100
      coeficiente_var_str = f"{coeficiente_var:.2} %"
    else:
      coeficiente_var_str = "Indefinido (media = 0)"
      
    resultado_text.delete("1.0", tk.END)
    resultado_text.insert(tk.END, f"Medidas de Variabilidad o Dispersion para la columna: {col}\n\n")
    resultado_text.insert(tk.END, f"Rango: {rango:.4f}\n")
    resultado_text.insert(tk.END, f"Desviación media: {desviacion_media:.4}\n")
    resultado_text.insert(tk.END, f"Desviacion estándar: {desviacion_estandar:.4} \n")
    resultado_text.insert(tk.END, f"Varianza: {varianza:.4f}\n")
    resultado_text.insert(tk.END, f"Coeficiente de variación: {coeficiente_var_str}\n")
  
  def medidas_de_forma():
    col = combo_columnas.get()
    if not col:
      messagebox.showwarning("Aviso", "Selecciona una columna.")
      return

    data = df_global[col].dropna()
    if len(data) == 0:
      messagebox.showinfo("Información", "La columna seleccionada no tiene datos.")
      return
    
    asimetria = skew(data, bias=True)
    curtosis = kurtosis(data, fisher=False, bias=False)
    
    resultado_text.delete("1.0", tk.END)
    resultado_text.insert(tk.END, f"Medidas de Forma para la columna: {col} \n\n")
    resultado_text.insert(tk.END, f"Asimetría de Fisher: {asimetria:.4f}\n")
    resultado_text.insert(tk.END, f"Curtosis de Fisher: {curtosis:.4f}\n")
  
  
  #boton para calcular la tabla de frecuencias simples
  btn_calcular = tk.Button(ventana_frequencias, text="Calcular frecuencias", command=calcular)
  btn_calcular.pack(side="left", padx=20, pady= 20)
  
  #boton para mostrar las medidas de tendencia central  
  btn_mostrar_tendencias = tk.Button(ventana_frequencias, text="Mostrar medidas de tendencia central", command=tendencias_centrales)
  btn_mostrar_tendencias.pack(side="left", padx=20, pady=20)
  
  #boton para calcular medidas de posicion
  btn_posicion = tk.Button(ventana_frequencias, text="Calcular Medidas de Posición", command=medidas_de_posicion)
  btn_posicion.pack(side="left", padx=20, pady=20)
  
  #boton para mosrar las medidas de variabilidad
  btn_variabilidad = tk.Button(ventana_frequencias, text="Calcular Medidas de Varibilidad", command=medidas_de_variabilidad)
  btn_variabilidad.pack(side="left", padx=20, pady=20)
  
  #boton para mostrar las medidas de forma
  btn_formas = tk.Button(ventana_frequencias, text="Calcular las Medidas de Forma", command=medidas_de_forma)
  btn_formas.pack(side="left", padx=20, pady=20)

### TABLA DE FRECUENCIAS EN INTERVALOS ###
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
  
  frame_inputs = tk.Frame(ventana_frecuencias_intervalos)
  frame_inputs.pack(padx=10, fill=tk.X)
    
  tk.Label(frame_inputs, text="Ingrese los cuartiles que desee calcular:").grid(row=0, column=0, padx=5)
  entry_cuartiles = tk.Entry(frame_inputs, width=10)
  entry_cuartiles.insert(0, "1, 2, 3, 4")
  entry_cuartiles.grid(row=0, column=1, padx=5)
    
  tk.Label(frame_inputs, text="Ingrese los deciles que desee calcular:").grid(row=0, column=2, padx=5)
  entry_deciles = tk.Entry(frame_inputs, width=10)
  entry_deciles.insert(0, "1, 2, 3, 4, 5, 6, 7, 8, 9, 10")
  entry_deciles.grid(row=0, column=3, padx=5)
    
  tk.Label(frame_inputs, text="Ingrese los percentiles que desee calcular:").grid(row=0, column=4, padx=5)
  entry_percentiles = tk.Entry(frame_inputs, width=10)
  entry_percentiles.insert(0, "10, 25, 50, 75, 100")
  entry_percentiles.grid(row=0, column=5, padx=5)
  
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
  
  def tendencias_centrales():
    col = combo_col.get()
    if not col:
      messagebox.showwarning("Aviso", "Selecciona una columna.")
      return
    
    data = df_global[col].dropna()
    if len(data) == 0:
      messagebox.showwarning("Información", "La columna no tiene datos.")
    
    media = data.mean()
    mediana = data.median()
    modas = data.mode()
    moda_str = ', '.join(map(str, modas.values))
    
    if (data <= 0).any():
      media_geom = "No definida (datos <= 0)"
    else:
      media_geom = stats.gmean(data)
      
    if (data <= 0).any():
      media_arm = "No definida (datos <= 0)"
    else:
      media_arm = stats.hmean(data)
    
    
    resultado_text.delete("1.0", tk.END)
    resultado_text.insert(tk.END, f"Estadísticas para la columna: {col}\n\n")
    resultado_text.insert(tk.END, f"Media aritmética: {media:.4f}\n")
    resultado_text.insert(tk.END, f"Mediana: {mediana:.4f}\n")
    resultado_text.insert(tk.END, f"Moda: {moda_str}\n")
    resultado_text.insert(tk.END, f"Media geométrica: {media_geom}\n")
    resultado_text.insert(tk.END, f"Media armónica: {media_arm}\n")
  
  def medidas_de_posicion():
    col = combo_col.get()
    if not col:
      messagebox.showwarning("Aviso", "Selecciona una columna.")
      return

    data = df_global[col].dropna()
    if len(data) == 0:
      messagebox.showinfo("Información", "La columna seleccionada no tiene datos.")
      return
    
    def parse_posiciones(text, max_val):
      try:
        posiciones = [int(x.strip()) for x in text.split(',') if x.strip() != '']
        for p in posiciones:
          if p < 1 or p > max_val:
            raise ValueError(f'Posición {p} fuera de rango (1-{max_val})')
        return posiciones
      except Exception as e:
        messagebox.showerror("Error", f'Error en posicion: {e}')
        return None
    
    max_cuartiles = 4
    max_deciles = 10
    max_percentiles = 100
    
    pos_cuartiles = parse_posiciones(entry_cuartiles.get(), max_cuartiles)
    if pos_cuartiles is None:
      return
    
    pos_deciles = parse_posiciones(entry_deciles.get(), max_deciles)
    if pos_deciles is None:
      return
    
    pos_percentiles = parse_posiciones(entry_percentiles.get(), max_percentiles)
    if pos_percentiles is None:
      return
    
    resultado_text.delete("1.0", tk.END)
    resultado_text.insert(tk.END, f"Medidas de Posición para la columna: {col}\n\n")
        
    if pos_cuartiles:
      q_probs = [p / max_cuartiles for p in pos_cuartiles]
      cuartiles = data.quantile(q_probs)
      resultado_text.insert(tk.END, "Cuartiles:\n")
      for p, val in zip(pos_cuartiles, cuartiles):
        resultado_text.insert(tk.END, f" Q{p} ({(p/max_cuartiles)*100:.2f}%): {val:.4f}\n")
      resultado_text.insert(tk.END, "\n")
        
    if pos_deciles:
      d_probs = [p / max_deciles for p in pos_deciles]
      deciles = data.quantile(d_probs)
      resultado_text.insert(tk.END, "Deciles:\n")
      for p, val in zip(pos_deciles, deciles):
        resultado_text.insert(tk.END, f" D{p} ({(p/max_deciles)*100:.2f}%): {val:.4f}\n")
      resultado_text.insert(tk.END, "\n")
        
    if pos_percentiles:
      p_probs = [p / max_percentiles for p in pos_percentiles]
      percentiles = data.quantile(p_probs)
      resultado_text.insert(tk.END, "Percentiles:\n")
      for p, val in zip(pos_percentiles, percentiles):
        resultado_text.insert(tk.END, f" P{p} ({(p/max_percentiles)*100:.2f}%): {val:.4f}\n")
      resultado_text.insert(tk.END, "\n")
  
  def medidas_de_variabilidad():
    col = combo_col.get()
    if not col:
      messagebox.showwarning("Aviso", "Selecciona una columna.")
      return

    data = df_global[col].dropna()
    if len(data) == 0:
      messagebox.showinfo("Información", "La columna seleccionada no tiene datos.")
      return
    
    rango = data.max() - data.min()
    media = data.mean()
    desviacion_media = (data - media).abs().mean()
    desviacion_estandar = data.var(ddof=1)
    varianza = data.var(ddof=1)
    
    if media != 0:
      coeficiente_var = (desviacion_estandar/media) * 100
      coeficiente_var_str = f"{coeficiente_var:.2} %"
    else:
      coeficiente_var_str = "Indefinido (media = 0)"
      
    resultado_text.delete("1.0", tk.END)
    resultado_text.insert(tk.END, f"Medidas de Variabilidad o Dispersion para la columna: {col}\n\n")
    resultado_text.insert(tk.END, f"Rango: {rango:.4f}\n")
    resultado_text.insert(tk.END, f"Desviación media: {desviacion_media:.4}\n")
    resultado_text.insert(tk.END, f"Desviacion estándar: {desviacion_estandar:.4} \n")
    resultado_text.insert(tk.END, f"Varianza: {varianza:.4f}\n")
    resultado_text.insert(tk.END, f"Coeficiente de variación: {coeficiente_var_str}\n")
  
  def medidas_de_forma():
    col = combo_col.get()
    if not col:
      messagebox.showwarning("Aviso", "Selecciona una columna.")
      return

    data = df_global[col].dropna()
    if len(data) == 0:
      messagebox.showinfo("Información", "La columna seleccionada no tiene datos.")
      return
    
    asimetria = skew(data, bias=True)
    curtosis = kurtosis(data, fisher=False, bias=False)
    
    resultado_text.delete("1.0", tk.END)
    resultado_text.insert(tk.END, f"Medidas de Forma para la columna: {col} \n\n")
    resultado_text.insert(tk.END, f"Asimetría de Fisher: {asimetria:.4f}\n")
    resultado_text.insert(tk.END, f"Curtosis de Fisher: {curtosis:.4f}\n")
  
  #boton para calcular la tabla de frecuencias por intervalos
  btn_calcular = tk.Button(ventana_frecuencias_intervalos, text="Calcular", command=calcular)
  btn_calcular.pack(side="left", padx=20, pady= 20)    
  
  #boton para mostrar las medidas de tendencia central  
  btn_mostrar_tendencias = tk.Button(ventana_frecuencias_intervalos, text="Mostrar medidas de tendencia central", command=tendencias_centrales)
  btn_mostrar_tendencias.pack(side="left", padx=20, pady=20)
  
  #boton para calcular medidas de posicion
  btn_posicion = tk.Button(ventana_frecuencias_intervalos, text="Calcular Medidas de Posición", command=medidas_de_posicion)
  btn_posicion.pack(side="left", padx=20, pady=20)
  
  #boton para mostrar las medidas de variabilidad
  btn_variabilidad = tk.Button(ventana_frecuencias_intervalos, text="Calcular Medidas de Varibilidad", command=medidas_de_variabilidad)
  btn_variabilidad.pack(side="left", padx=20, pady=20)
  
  #boton para mostrar las medidas de forma
  btn_formas = tk.Button(ventana_frecuencias_intervalos, text="Calcular las Medidas de Forma", command=medidas_de_forma)
  btn_formas.pack(side="left", padx=20, pady=20)


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
btn_mostrar_datos.pack(side="left", padx=10, pady=10)

#boton para frecuencias simples
btn_frecuencias_simples = tk.Button(root, text="Calcular Frecuencias Simples", command=calcular_frecuencias_simples)
btn_frecuencias_simples.pack(side="left", padx=10, pady=10)

#boton para frecuencias en intervalos
btn_frecuencias_intervalos = tk.Button(root, text="Calcular Frecuencias por Intervalos", command=frecuencias_intervalos)
btn_frecuencias_intervalos.pack(side="left", padx=10, pady=10)

root.mainloop()