import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import pandas as pd
import numpy as np
import math
from scipy import stats
from scipy.stats import skew, kurtosis, bernoulli, binom, poisson

df_global = None


##### ÁREA DE DISTRIBUCIONES #####

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


##### ÁREA DE PROBABILIDADES #####

### PROBABILIDADES ELEMENTALES ###
def probabilidades_elementales():
    if df_global is None:
        messagebox.showwarning("Aviso", "Primero debes cargar un archivo CSV.")
        return
    
    ventana_prob = tk.Toplevel(root)
    ventana_prob.title("Probabilidades Elementales")
    ventana_prob.geometry("550x500")
    
    tk.Label(ventana_prob, text="Ingrese P(A):").pack(pady=5)
    entry_pa = tk.Entry(ventana_prob)
    entry_pa.pack(pady=5)
    
    tk.Label(ventana_prob, text="Ingrese P(B):").pack(pady=5)
    entry_pb = tk.Entry(ventana_prob)
    entry_pb.pack(pady=5)
    
    tk.Label(ventana_prob, text="Ingrese P(B|A) (solo para sucesos dependientes):").pack(pady=5)
    entry_pba = tk.Entry(ventana_prob)
    entry_pba.pack(pady=5)
    
    tk.Label(ventana_prob, text="Ingrese el espacio muestral Ω (opcional):").pack(pady=5)
    entry_omega = tk.Entry(ventana_prob)
    entry_omega.pack(pady=5)
    
    tk.Label(ventana_prob, text="Ingrese el tamaño del espacio muestral n (opcional):").pack(pady=5)
    entry_n = tk.Entry(ventana_prob)
    entry_n.pack(pady=5)
    
    tk.Label(ventana_prob, text="Seleccione el tipo de suceso:").pack(pady=5)
    tipos_sucesos = [
        "Sucesos simples",
        "Sucesos mutuamente excluyentes",
        "Sucesos no excluyentes",
        "Sucesos independientes",
        "Sucesos dependientes"
    ]
    combo_tipo = ttk.Combobox(ventana_prob, values=tipos_sucesos, state="readonly")
    combo_tipo.pack(pady=5)
    combo_tipo.current(0)
    
    resultado_text = tk.Text(ventana_prob, height=12, width=65)
    resultado_text.pack(pady=10)
    
    def calcular_probabilidades():
        try:
            pa = float(entry_pa.get())
            pb = float(entry_pb.get())
            pba_text = entry_pba.get().strip()
            pba = float(pba_text) if pba_text else None
            
            omega = entry_omega.get().strip()
            n = entry_n.get().strip()
            
            tipo = combo_tipo.get()
            
            # Validaciones básicas
            if not (0 <= pa <= 1 and 0 <= pb <= 1):
                messagebox.showerror("Error", "P(A) y P(B) deben estar entre 0 y 1.")
                return
            if tipo == "Sucesos dependientes" and (pba is None or not (0 <= pba <= 1)):
                messagebox.showerror("Error", "Para sucesos dependientes, ingresa P(B|A) entre 0 y 1.")
                return
            
            # Validar n si se ingresa
            n_val = None
            if n:
                try:
                    n_val = int(n)
                    if n_val <= 0:
                        messagebox.showerror("Error", "El tamaño del espacio muestral n debe ser un entero positivo.")
                        return
                except:
                    messagebox.showerror("Error", "El tamaño del espacio muestral n debe ser un entero válido.")
                    return
            
            resultado_text.delete("1.0", tk.END)
            resultado_text.insert(tk.END, f"Tipo de suceso: {tipo}\n")
            resultado_text.insert(tk.END, f"P(A) = {pa}\n")
            resultado_text.insert(tk.END, f"P(B) = {pb}\n")
            if pba is not None:
                resultado_text.insert(tk.END, f"P(B|A) = {pba}\n")
            if omega:
                resultado_text.insert(tk.END, f"Espacio muestral Ω = {omega}\n")
            if n_val is not None:
                resultado_text.insert(tk.END, f"Tamaño del espacio muestral n = {n_val}\n")
            resultado_text.insert(tk.END, "\n")
            
            if omega and n_val is not None:
                resultado_text.insert(tk.END, f"Nota: El espacio muestral '{omega}' tiene tamaño {n_val}.\n\n")
            
            if tipo == "Sucesos simples":
                resultado_text.insert(tk.END, "Sucesos simples: Probabilidades individuales.\n")
                if n_val is not None:
                    fa = pa * n_val
                    fb = pb * n_val
            
            elif tipo == "Sucesos mutuamente excluyentes":
                p_union = pa + pb
                if p_union > 1:
                    resultado_text.insert(tk.END, "Advertencia: P(A) + P(B) > 1, no es posible para sucesos excluyentes.\n")
                resultado_text.insert(tk.END, f"P(A ∩ B) = 0 (por definición)\n")
                resultado_text.insert(tk.END, f"P(A ∪ B) = P(A) + P(B) = {p_union}\n")
                if n_val is not None:
                    fa = pa * n_val
                    fb = pb * n_val
            
            elif tipo == "Sucesos no excluyentes":
                def pedir_interseccion():
                    def calcular_interseccion():
                        try:
                            p_inter = float(entry_inter.get())
                            if not (0 <= p_inter <= 1):
                                messagebox.showerror("Error", "P(A ∩ B) debe estar entre 0 y 1.")
                                return
                            p_union = pa + pb - p_inter
                            if p_union > 1 or p_union < 0:
                                resultado_text.insert(tk.END, "Advertencia: P(A ∪ B) fuera de rango [0,1].\n")
                            resultado_text.insert(tk.END, f"P(A ∩ B) = {p_inter}\n")
                            resultado_text.insert(tk.END, f"P(A ∪ B) = P(A) + P(B) - P(A ∩ B) = {p_union}\n")
                            if n_val is not None:
                                fa = pa * n_val
                                fb = pb * n_val
                                f_inter = p_inter * n_val
                            top_inter.destroy()
                        except:
                            messagebox.showerror("Error", "Ingresa un valor numérico válido.")
                    
                    top_inter = tk.Toplevel(ventana_prob)
                    top_inter.title("Ingresar P(A ∩ B)")
                    tk.Label(top_inter, text="Ingrese P(A ∩ B):").pack(pady=5)
                    entry_inter = tk.Entry(top_inter)
                    entry_inter.pack(pady=5)
                    btn_calc_inter = tk.Button(top_inter, text="Calcular", command=calcular_interseccion)
                    btn_calc_inter.pack(pady=5)
                
                pedir_interseccion()
            
            elif tipo == "Sucesos independientes":
                p_inter = pa * pb
                p_union = pa + pb - p_inter
                resultado_text.insert(tk.END, f"P(A ∩ B) = P(A) * P(B) = {p_inter}\n")
                resultado_text.insert(tk.END, f"P(A ∪ B) = P(A) + P(B) - P(A) * P(B) = {p_union}\n")
                if n_val is not None:
                    fa = pa * n_val
                    fb = pb * n_val
                    f_inter = p_inter * n_val
            
            elif tipo == "Sucesos dependientes":
                p_inter = pa * pba
                p_union = pa + pb - p_inter
                resultado_text.insert(tk.END, f"P(A ∩ B) = P(A) * P(B|A) = {p_inter}\n")
                resultado_text.insert(tk.END, f"P(A ∪ B) = P(A) + P(B) - P(A ∩ B) = {p_union}\n")
                if n_val is not None:
                    fa = pa * n_val
                    fb = pb * n_val
                    f_inter = p_inter * n_val
            
            else:
                resultado_text.insert(tk.END, "Tipo de suceso no reconocido.\n")
        
        except ValueError:
            messagebox.showerror("Error", "Por favor ingresa valores numéricos válidos para las probabilidades.")
    
    btn_calcular = tk.Button(ventana_prob, text="Calcular Probabilidades", command=calcular_probabilidades)
    btn_calcular.pack(pady=10)

def teorema_de_bayes():
    if df_global is None:
        messagebox.showwarning("Aviso", "Primero debes cargar un archivo CSV.")
        return
    
    ventana_bayes = tk.Toplevel(root)
    ventana_bayes.title("Teorema de Bayes")
    ventana_bayes.geometry("500x400")
    
    tk.Label(ventana_bayes, text="Ingrese P(A):").pack(pady=5)
    entry_pa = tk.Entry(ventana_bayes)
    entry_pa.pack(pady=5)
    
    tk.Label(ventana_bayes, text="Ingrese P(B|A):").pack(pady=5)
    entry_pba = tk.Entry(ventana_bayes)
    entry_pba.pack(pady=5)
    
    tk.Label(ventana_bayes, text="Ingrese P(B|¬A):").pack(pady=5)
    entry_pbna = tk.Entry(ventana_bayes)
    entry_pbna.pack(pady=5)
    
    resultado_text = tk.Text(ventana_bayes, height=10, width=60)
    resultado_text.pack(pady=10)
    
    def calcular_bayes():
        try:
            pa = float(entry_pa.get())
            pba = float(entry_pba.get())
            pbna = float(entry_pbna.get())
            
            if not (0 <= pa <= 1 and 0 <= pba <= 1 and 0 <= pbna <= 1):
                messagebox.showerror("Error", "Todas las probabilidades deben estar entre 0 y 1.")
                return
            
            pna = 1 - pa
            denominador = pba * pa + pbna * pna
            if denominador == 0:
                messagebox.showerror("Error", "Denominador es cero, revise las probabilidades ingresadas.")
                return
            
            pab = (pba * pa) / denominador
            
            resultado_text.delete("1.0", tk.END)
            resultado_text.insert(tk.END, f"P(A) = {pa}\n")
            resultado_text.insert(tk.END, f"P(B|A) = {pba}\n")
            resultado_text.insert(tk.END, f"P(B|¬A) = {pbna}\n")
            resultado_text.insert(tk.END, f"\nP(¬A) = {pna}\n")
            resultado_text.insert(tk.END, f"\nP(A|B) = {pab:.6f}\n")
        
        except ValueError:
            messagebox.showerror("Error", "Por favor ingresa valores numéricos válidos para las probabilidades.")
    
    btn_calcular = tk.Button(ventana_bayes, text="Calcular P(A|B)", command=calcular_bayes)
    btn_calcular.pack(pady=10)

def distribuciones_probabilidad():
    ventana_dist = tk.Toplevel(root)
    ventana_dist.title("Distribuciones de Probabilidad")
    ventana_dist.geometry("600x500")
    
    tk.Label(ventana_dist, text="Seleccione la distribución:").pack(pady=5)
    distribuciones = ["Bernoulli", "Binomial", "Poisson"]
    combo_dist = ttk.Combobox(ventana_dist, values=distribuciones, state="readonly")
    combo_dist.pack(pady=5)
    combo_dist.current(0)
    
    frame_params = tk.Frame(ventana_dist)
    frame_params.pack(pady=10)
    
    # Parámetros dinámicos según distribución
    label_param1 = tk.Label(frame_params, text="p (probabilidad de éxito):")
    entry_param1 = tk.Entry(frame_params)
    label_param1.grid(row=0, column=0, padx=5, pady=5)
    entry_param1.grid(row=0, column=1, padx=5, pady=5)
    
    label_param2 = tk.Label(frame_params, text="n (número de ensayos):")
    entry_param2 = tk.Entry(frame_params)
    # Por defecto oculto, solo para binomial
    label_param2.grid(row=1, column=0, padx=5, pady=5)
    entry_param2.grid(row=1, column=1, padx=5, pady=5)
    
    label_param3 = tk.Label(frame_params, text="λ (tasa promedio):")
    entry_param3 = tk.Entry(frame_params)
    # Por defecto oculto, solo para poisson
    label_param3.grid(row=2, column=0, padx=5, pady=5)
    entry_param3.grid(row=2, column=1, padx=5, pady=5)
    
    # Ocultar parámetros no usados inicialmente
    label_param2.grid_remove()
    entry_param2.grid_remove()
    label_param3.grid_remove()
    entry_param3.grid_remove()
    
    resultado_text = tk.Text(ventana_dist, height=15, width=70)
    resultado_text.pack(pady=10)
    
    def actualizar_campos(event):
        dist = combo_dist.get()
        if dist == "Bernoulli":
            label_param1.config(text="p (probabilidad de éxito):")
            label_param1.grid()
            entry_param1.grid()
            label_param2.grid_remove()
            entry_param2.grid_remove()
            label_param3.grid_remove()
            entry_param3.grid_remove()
        elif dist == "Binomial":
            label_param1.config(text="p (probabilidad de éxito):")
            label_param1.grid()
            entry_param1.grid()
            label_param2.grid()
            entry_param2.grid()
            label_param3.grid_remove()
            entry_param3.grid_remove()
        elif dist == "Poisson":
            label_param1.grid_remove()
            entry_param1.grid_remove()
            label_param2.grid_remove()
            entry_param2.grid_remove()
            label_param3.config(text="λ (tasa promedio):")
            label_param3.grid()
            entry_param3.grid()
    
    combo_dist.bind("<<ComboboxSelected>>", actualizar_campos)
    
    def calcular_distribucion():
        dist = combo_dist.get()
        resultado_text.delete("1.0", tk.END)
        
        try:
            if dist == "Bernoulli":
                p = float(entry_param1.get())
                if not (0 <= p <= 1):
                    messagebox.showerror("Error", "p debe estar entre 0 y 1.")
                    return
                resultado_text.insert(tk.END, f"Distribución Bernoulli con p = {p}\n\n")
                # Valores posibles: 0 y 1
                for x in [0,1]:
                    prob = bernoulli.pmf(x, p)
                    resultado_text.insert(tk.END, f"P(X={x}) = {prob:.6f}\n")
            
            elif dist == "Binomial":
                n = int(entry_param2.get())
                p = float(entry_param1.get())
                if n <= 0:
                    messagebox.showerror("Error", "n debe ser un entero positivo.")
                    return
                if not (0 <= p <= 1):
                    messagebox.showerror("Error", "p debe estar entre 0 y 1.")
                    return
                resultado_text.insert(tk.END, f"Distribución Binomial con n = {n}, p = {p}\n\n")
                # Mostrar pmf para x=0..n
                for x in range(n+1):
                    prob = binom.pmf(x, n, p)
                    resultado_text.insert(tk.END, f"P(X={x}) = {prob:.6f}\n")
            
            elif dist == "Poisson":
                lam = float(entry_param3.get())
                if lam <= 0:
                    messagebox.showerror("Error", "λ debe ser un número positivo.")
                    return
                resultado_text.insert(tk.END, f"Distribución Poisson con λ = {lam}\n\n")
                # Mostrar pmf para x=0..(lam+4*sqrt(lam)) aprox
                max_x = int(lam + 4 * (lam**0.5)) + 1
                for x in range(max_x):
                    prob = poisson.pmf(x, lam)
                    resultado_text.insert(tk.END, f"P(X={x}) = {prob:.6f}\n")
            
            else:
                resultado_text.insert(tk.END, "Distribución no reconocida.\n")
        
        except ValueError:
            messagebox.showerror("Error", "Por favor ingresa valores numéricos válidos para los parámetros.")
    
    btn_calcular = tk.Button(ventana_dist, text="Calcular Distribución", command=calcular_distribucion)
    btn_calcular.pack(pady=10)


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

#boton para calcular probabilidades elementales
btn_prob_elementales = tk.Button(root, text="Probabilidades Elementales", command=probabilidades_elementales)
btn_prob_elementales.pack(side="left", padx=10, pady=10)

#boton para probabilidades con teorema de bayes
btn_teorema_bayes = tk.Button(root, text="Teorema de Bayes", command=teorema_de_bayes)
btn_teorema_bayes.pack(side="left", padx=10, pady=10)

#boton para bernoulli
btn_distribuciones = tk.Button(root, text="Distribuciones de Probabilidad", command=distribuciones_probabilidad)
btn_distribuciones.pack(side="left", padx=10, pady=10)


root.mainloop()