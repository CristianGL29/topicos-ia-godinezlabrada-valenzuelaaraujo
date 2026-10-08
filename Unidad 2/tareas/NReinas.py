import tkinter as tk
from tkinter import ttk, messagebox


class AlgoritmosNReinas:
  

    def __init__(self, n):
        self.n = n

    def contar_ataques(self, estado):

        ataques = 0
        for i in range(self.n):
            for j in range(i + 1, self.n):
                if estado[i] == estado[j] or abs(estado[i] - estado[j]) == abs(i - j):
                    ataques += 1
        return ataques

    def generar_vecinos(self, estado):

        hijos = []
        for col in range(self.n):
            for nueva_fila in range(self.n):
                if nueva_fila != estado[col]:
                    nuevo_estado = list(estado)
                    nuevo_estado[col] = nueva_fila
                    hijos.append(tuple(nuevo_estado))
        return hijos

    def bfs(self):

        nodo = tuple([0] * self.n)

        frontera = [nodo]
        explorados = set()

        while True:
            if not frontera:
                return False

            nodo = frontera.pop(0)
            yield nodo, False

            if nodo in explorados:
                continue

            explorados.add(nodo)

            if self.contar_ataques(nodo) == 0:
                yield nodo, True
                return nodo

            hijos = self.generar_vecinos(nodo)
            frontera.extend(hijos)

    def dfs(self):

        nodo = tuple([0] * self.n)

        frontera = [nodo]
        explorados = set()

        while True:
            if not frontera:
                return False



            nodo = frontera.pop(0)
            yield nodo, False

            if nodo in explorados:
                continue

            explorados.add(nodo)

            if self.contar_ataques(nodo) == 0:
                yield nodo, True
                return nodo

            hijos = self.generar_vecinos(nodo)
            frontera = hijos + frontera

    def iddfs(self):

        limite = 1
        while True:

            resultado = yield from self.ldfs(limite)

            if resultado is False:
                limite = limite + 1
                if limite > self.n * 4:
                    return False
            else:
                break

    def ldfs(self, limite):

        nodo = tuple([0] * self.n)


        frontera = [(nodo, 0)]
        explorados = set()

        while True:
            if not frontera:
                return False

            nodo_actual, prof_actual = frontera.pop(0)
            yield nodo_actual, False

            if nodo_actual in explorados:
                continue

            explorados.add(nodo_actual)

            if self.contar_ataques(nodo_actual) == 0:
                yield nodo_actual, True
                return nodo_actual

            if prof_actual < limite:
                hijos_base = self.generar_vecinos(nodo_actual)
                hijos = [(h, prof_actual + 1) for h in hijos_base]
                frontera = hijos + frontera

    def voraz(self):

        nodo = tuple([0] * self.n)
        explorados = set()

        while True:
            if nodo is None:
                return False

            yield nodo, False

            if nodo in explorados:
                nodo = None
                continue

            explorados.add(nodo)

            if self.contar_ataques(nodo) == 0:
                yield nodo, True
                return nodo

            hijos = self.generar_vecinos(nodo)



            hijos_ordenados = sorted(hijos, key=lambda h: self.contar_ataques(h))

            if hijos_ordenados:
                nodo = hijos_ordenados.pop(0)
            else:
                nodo = None

    def a_star(self):

        nodo_inicial = tuple([0] * self.n)



        frontera = [(self.contar_ataques(nodo_inicial), 0, nodo_inicial)]
        explorados = set()

        while True:
            if not frontera:
                return False


            f, g, nodo = frontera.pop(0)
            yield nodo, False

            if nodo in explorados:
                continue

            explorados.add(nodo)

            if self.contar_ataques(nodo) == 0:
                yield nodo, True
                return nodo

            hijos = self.generar_vecinos(nodo)


            hijos_evaluados = []
            for h in hijos:
                nuevo_g = g + 1
                nuevo_h = self.contar_ataques(h)
                nuevo_f = nuevo_g + nuevo_h  # F = G + H
                hijos_evaluados.append((nuevo_f, nuevo_g, h))

            frontera.extend(hijos_evaluados)


            frontera.sort(key=lambda x: x[0])


class InterfazGraficaNReinas:


    def __init__(self, root):
        self.root = root
        self.root.title("Problema N Reinas - Algoritmos Puros")
        self.root.geometry("700x550")

        self.n_var = tk.IntVar(value=4)
        self.algo_var = tk.StringVar(value="Voraz")
        self.velocidad_var = tk.IntVar(value=100)

        self.generador_algoritmo = None
        self.corriendo = False

        self.crear_widgets()
        self.dibujar_tablero_vacio()

    def crear_widgets(self):
        panel_control = tk.Frame(self.root, width=200, bg="#f0f0f0", padx=10, pady=10)
        panel_control.pack(side=tk.LEFT, fill=tk.Y)

        tk.Label(panel_control, text="Tamaño (N):", bg="#f0f0f0").pack(anchor="w", pady=(0, 5))
        tk.Spinbox(panel_control, from_=4, to=8, textvariable=self.n_var, width=10).pack(anchor="w", pady=(0, 15))

        tk.Label(panel_control, text="Algoritmo:", bg="#f0f0f0").pack(anchor="w", pady=(0, 5))
        algoritmos = ["BFS", "DFS", "LDFS/ILDFS", "Voraz", "A Star"]
        combo_algo = ttk.Combobox(panel_control, textvariable=self.algo_var, values=algoritmos, state="readonly",
                                  width=15)
        combo_algo.pack(anchor="w", pady=(0, 15))

        tk.Label(panel_control, text="Velocidad (ms):", bg="#f0f0f0").pack(anchor="w", pady=(0, 5))
        tk.Scale(panel_control, from_=10, to=1000, orient=tk.HORIZONTAL, variable=self.velocidad_var,
                 bg="#f0f0f0").pack(anchor="w", pady=(0, 20))

        self.btn_iniciar = tk.Button(panel_control, text="Iniciar Simulación", command=self.iniciar_simulacion,
                                     bg="#4CAF50", fg="white", font=("Arial", 10, "bold"))
        self.btn_iniciar.pack(fill=tk.X, pady=5)

        self.btn_detener = tk.Button(panel_control, text="Detener", command=self.detener_simulacion, bg="#f44336",
                                     fg="white", font=("Arial", 10, "bold"))
        self.btn_detener.pack(fill=tk.X, pady=5)
        self.btn_detener.config(state=tk.DISABLED)

        self.lbl_estado = tk.Label(panel_control, text="Esperando...", bg="#f0f0f0", fg="blue")
        self.lbl_estado.pack(pady=20)

        self.canvas_size = 500
        self.canvas = tk.Canvas(self.root, width=self.canvas_size, height=self.canvas_size, bg="white")
        self.canvas.pack(side=tk.RIGHT, padx=10, pady=10)

    def dibujar_tablero_vacio(self):
        self.canvas.delete("all")
        n = self.n_var.get()
        tam_celda = self.canvas_size / n

        for fila in range(n):
            for col in range(n):
                x1 = col * tam_celda
                y1 = fila * tam_celda
                x2 = x1 + tam_celda
                y2 = y1 + tam_celda
                color = "#FFCE9E" if (fila + col) % 2 == 0 else "#D18B47"
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="black")

    def dibujar_estado(self, estado):
        self.dibujar_tablero_vacio()
        n = self.n_var.get()
        tam_celda = self.canvas_size / n

        for col, fila in enumerate(estado):
            x = (col * tam_celda) + (tam_celda / 2)
            y = (fila * tam_celda) + (tam_celda / 2)
            font_size = int(tam_celda * 0.6)
            self.canvas.create_text(x, y, text="♛", font=("Arial", font_size), fill="black")

    def iniciar_simulacion(self):
        self.detener_simulacion()
        self.corriendo = True
        self.btn_iniciar.config(state=tk.DISABLED)
        self.btn_detener.config(state=tk.NORMAL)

        n = self.n_var.get()
        algoritmo = self.algo_var.get()
        motor = AlgoritmosNReinas(n)

        if algoritmo == "BFS":
            self.generador_algoritmo = motor.bfs()
        elif algoritmo == "DFS":
            self.generador_algoritmo = motor.dfs()
        elif algoritmo == "LDFS/ILDFS":
            self.generador_algoritmo = motor.iddfs()
        elif algoritmo == "Voraz":
            self.generador_algoritmo = motor.voraz()
        elif algoritmo == "A Star":
            self.generador_algoritmo = motor.a_star()

        self.lbl_estado.config(text=f"Buscando con {algoritmo}...")
        self.ejecutar_paso()

    def ejecutar_paso(self):
        if not self.corriendo:
            return
        try:
            estado, es_solucion = next(self.generador_algoritmo)
            self.dibujar_estado(estado)

            if es_solucion:
                self.lbl_estado.config(text="¡Solución Encontrada!", fg="green")
                self.finalizar()
                messagebox.showinfo("Éxito", "¡Se ha encontrado una solución!")
            else:
                self.root.after(self.velocidad_var.get(), self.ejecutar_paso)

        except StopIteration:
            self.lbl_estado.config(text="Sin solución", fg="red")
            self.finalizar()
            messagebox.showwarning("Fin",
                                   "Se exploró el árbol y no se encontró solución o se atascó en un bucle local.")

    def detener_simulacion(self):
        self.corriendo = False
        self.finalizar()
        self.lbl_estado.config(text="Detenido", fg="black")

    def finalizar(self):
        self.btn_iniciar.config(state=tk.NORMAL)
        self.btn_detener.config(state=tk.DISABLED)


if __name__ == "__main__":
    ventana_principal = tk.Tk()
    app = InterfazGraficaNReinas(ventana_principal)
    ventana_principal.mainloop()