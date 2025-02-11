from tkinter import Tk, Canvas
from tkinter.filedialog import asksaveasfilename
from PIL import Image, ImageTk

class RecortarImagen:
    def __init__(self, ruta_imagen):
        self.ruta_imagen = ruta_imagen
        self.imagen = Image.open(ruta_imagen)
        self.coordenadas = []
        self.recorte_hecho = False

        # Configuración de la ventana de Tkinter
        self.ventana = Tk()
        self.ventana.title("Selecciona el área para recortar")
        self.canvas = Canvas(self.ventana, width=self.imagen.width, height=self.imagen.height)
        self.canvas.pack()

        # Convertir la imagen para Tkinter
        self.tk_imagen = ImageTk.PhotoImage(self.imagen)
        self.canvas.create_image(0, 0, anchor="nw", image=self.tk_imagen)

        # Eventos para dibujar el área de recorte
        self.canvas.bind("<Button-1>", self.marcar_inicio)
        self.canvas.bind("<ButtonRelease-1>", self.marcar_fin)

    def marcar_inicio(self, evento):
        """
        Marca el punto inicial (esquina superior izquierda) del área de recorte.
        """
        self.coordenadas = [(evento.x, evento.y)]

    def marcar_fin(self, evento):
        """
        Marca el punto final (esquina inferior derecha) y realiza el recorte.
        """
        self.coordenadas.append((evento.x, evento.y))
        self.recortar()

    def recortar(self):
        """
        Recorta la imagen según las coordenadas seleccionadas.
        """
        if len(self.coordenadas) == 2:
            x1, y1 = self.coordenadas[0]
            x2, y2 = self.coordenadas[1]

            # Recortar la imagen
            area_recorte = (x1, y1, x2, y2)
            imagen_recortada = self.imagen.crop(area_recorte)

            # Guardar la imagen recortada
            ruta_salida = asksaveasfilename(
                defaultextension=".jpg",
                filetypes=[("Archivo JPEG", "*.jpg"), ("Archivo PNG", "*.png")],
                title="Guardar imagen recortada"
            )
            if ruta_salida:
                imagen_recortada.save(ruta_salida)
                print(f"Imagen recortada guardada en: {ruta_salida}")
                self.recorte_hecho = True

            # Cerrar la ventana
            self.ventana.destroy()

    def ejecutar(self):
        """
        Ejecuta la ventana de Tkinter.
        """
        self.ventana.mainloop()

# Ejecutar el programa
if __name__ == "__main__":
    ruta_imagen = "imagen_original.jpg"  # Cambia esta ruta por la imagen que quieras usar
    recortador = RecortarImagen(ruta_imagen)
    recortador.ejecutar()from tkinter import Tk, Canvas
from tkinter.filedialog import asksaveasfilename
from PIL import Image, ImageTk

class RecortarImagen:
    def __init__(self, ruta_imagen):
        self.ruta_imagen = ruta_imagen
        self.imagen = Image.open(ruta_imagen)
        self.coordenadas = []
        self.recorte_hecho = False

        # Configuración de la ventana de Tkinter
        self.ventana = Tk()
        self.ventana.title("Selecciona el área para recortar")
        self.canvas = Canvas(self.ventana, width=self.imagen.width, height=self.imagen.height)
        self.canvas.pack()

        # Convertir la imagen para Tkinter
        self.tk_imagen = ImageTk.PhotoImage(self.imagen)
        self.canvas.create_image(0, 0, anchor="nw", image=self.tk_imagen)

        # Eventos para dibujar el área de recorte
        self.canvas.bind("<Button-1>", self.marcar_inicio)
        self.canvas.bind("<ButtonRelease-1>", self.marcar_fin)

    def marcar_inicio(self, evento):
        """
        Marca el punto inicial (esquina superior izquierda) del área de recorte.
        """
        self.coordenadas = [(evento.x, evento.y)]

    def marcar_fin(self, evento):
        """
        Marca el punto final (esquina inferior derecha) y realiza el recorte.
        """
        self.coordenadas.append((evento.x, evento.y))
        self.recortar()

    def recortar(self):
        """
        Recorta la imagen según las coordenadas seleccionadas.
        """
        if len(self.coordenadas) == 2:
            x1, y1 = self.coordenadas[0]
            x2, y2 = self.coordenadas[1]

            # Recortar la imagen
            area_recorte = (x1, y1, x2, y2)
            imagen_recortada = self.imagen.crop(area_recorte)

            # Guardar la imagen recortada
            ruta_salida = asksaveasfilename(
                defaultextension=".jpg",
                filetypes=[("Archivo JPEG", "*.jpg"), ("Archivo PNG", "*.png")],
                title="Guardar imagen recortada"
            )
            if ruta_salida:
                imagen_recortada.save(ruta_salida)
                print(f"Imagen recortada guardada en: {ruta_salida}")
                self.recorte_hecho = True

            # Cerrar la ventana
            self.ventana.destroy()

    def ejecutar(self):
        """
        Ejecuta la ventana de Tkinter.
        """
        self.ventana.mainloop()

# Ejecutar el programa
if __name__ == "__main__":
    ruta_imagen = "imagen_original.jpg"  # Cambia esta ruta por la imagen que quieras usar
    recortador = RecortarImagen(ruta_imagen)
    recortador.ejecutar()
