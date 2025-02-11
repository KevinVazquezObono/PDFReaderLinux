import os
import PyPDF2
import argparse
from pdf2image import convert_from_path
import pytesseract
from PIL import Image, ImageEnhance

class PDFToImageTextReader:
    def __init__(self, pdf_path):
        """
        Inicializa la clase.
        :param pdf_path: Ruta al archivo PDF.
        """
        self.pdf_path = pdf_path
        self.output_folder = os.path.join(os.getcwd(), "tmp_img")
        self.images = []

        # Crear carpeta de salida si no existe
        if not os.path.exists(self.output_folder):
            os.makedirs(self.output_folder)

    def convert_pdf_to_images(self, dpi=300, image_format="JPEG"):
        """
        Convierte cada página del PDF en una imagen.
        :param dpi: Resolución de las imágenes generadas.
        :param image_format: Formato de las imágenes generadas (ejemplo: "JPEG").
        """
        try:
            self.images = convert_from_path(self.pdf_path, dpi=dpi, fmt=image_format)
            for idx, image in enumerate(self.images):
                image_path = os.path.join(self.output_folder, f"page_{idx + 1}.{image_format.lower()}")
                image.save(image_path, image_format)
        except Exception as e:
            raise Exception(f"Error al convertir el PDF a imágenes: {e}")

    def enhance_contrast(self, image_path):
        """
        Aumenta el contraste de una imagen.
        :param image_path: Ruta de la imagen a procesar.
        :return: Imagen con contraste mejorado.
        """
        try:
            image = Image.open(image_path)
            enhancer = ImageEnhance.Contrast(image)
            enhanced_image = enhancer.enhance(2.0)  # El valor 2.0 dobla el contraste, ajusta según necesidad.
            return enhanced_image
        except Exception as e:
            raise Exception(f"Error al mejorar el contraste de la imagen {image_path}: {e}")

    def read_text_from_images(self, lang="esp"):
        """
        Lee texto de las imágenes generadas usando Tesseract.
        """
        if not os.listdir(self.output_folder):
            raise ValueError("Primero debes convertir el PDF a imágenes usando 'convert_pdf_to_images()'.")

        all_text = ""
        try:
            for idx, image_file in enumerate(sorted(os.listdir(self.output_folder))):
                image_path = os.path.join(self.output_folder, image_file)

                # Aumentar el contraste de la imagen antes de procesarla
                enhanced_image = self.enhance_contrast(image_path)

                # Extraer texto usando Tesseract
                text = pytesseract.image_to_string(enhanced_image, lang=lang)
                all_text += f"Texto de la página {idx + 1}:\n{text}\n"
        except Exception as e:
            raise Exception(f"Error al extraer texto de las imágenes: {e}")
        return all_text

    def cleanup(self):
        """
        Elimina las imágenes temporales generadas.
        """
        for file in os.listdir(self.output_folder):
            file_path = os.path.join(self.output_folder, file)
            if os.path.isfile(file_path):
                os.unlink(file_path)
        os.rmdir(self.output_folder)


class PDFReader:
    def __init__(self, filepath):
        """
        Inicializa el lector de PDF.
        :param filepath: Ruta del archivo PDF.
        """
        self.filepath = filepath
        self.pdf_file = None
        self.reader = None

    def open_pdf(self):
        """
        Abre el archivo PDF y prepara el lector.
        """
        try:
            self.pdf_file = open(self.filepath, 'rb')
            self.reader = PyPDF2.PdfReader(self.pdf_file)
        except FileNotFoundError:
            raise FileNotFoundError(f"El archivo '{self.filepath}' no existe.")
        except Exception as e:
            raise Exception(f"Ocurrió un error al abrir el archivo PDF: {e}")

    def get_page_text(self, page_number):
        """
        Obtiene el texto de una página específica del PDF.
        :param page_number: Número de la página (empezando desde 0).
        :return: Texto de la página.
        """
        if not self.reader:
            raise ValueError("El archivo PDF no está abierto. Llama a 'open_pdf()' primero.")
        try:
            return self.reader.pages[page_number].extract_text()
        except IndexError:
            raise IndexError(f"El número de página {page_number} está fuera del rango.")
        except Exception as e:
            raise Exception(f"Ocurrió un error al leer la página: {e}")

    def get_all_text(self):
        """
        Obtiene el texto de todas las páginas del PDF.
        :return: Texto completo del PDF.
        """
        if not self.reader:
            raise ValueError("El archivo PDF no está abierto. Llama a 'open_pdf()' primero.")
        try:
            return "\n".join([page.extract_text() for page in self.reader.pages])
        except Exception as e:
            raise Exception(f"Ocurrió un error al leer el contenido del PDF: {e}")

    def get_metadata(self):
        """
        Obtiene los metadatos del PDF.
        :return: Diccionario con los metadatos del PDF.
        """
        if not self.reader:
            raise ValueError("El archivo PDF no está abierto. Llama a 'open_pdf()' primero.")
        try:
            metadata = self.reader.metadata
            return {key: metadata[key] for key in metadata.keys()}
        except Exception as e:
            raise Exception(f"Ocurrió un error al obtener los metadatos: {e}")

    def close_pdf(self):
        """
        Cierra el archivo PDF si está abierto.
        """
        if self.pdf_file:
            self.pdf_file.close()
            self.pdf_file = None
            self.reader = None


# Configuración de argparse para recibir argumentos de línea de comandos
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Lector de PDFs con metadatos y texto.")
    parser.add_argument("filepath", type=str, help="Ruta al archivo PDF.")
    parser.add_argument("--page", type=int, help="Número de la página que deseas leer (empezando desde 0).")
    parser.add_argument("--lang", type=str, default="spa", help="Idioma para Tesseract OCR (por defecto 'spa').")

    args = parser.parse_args()

    try:
        # Instancia para leer el texto del PDF directamente
        pdf_reader = PDFReader(args.filepath)
        pdf_reader.open_pdf()

        print("\nMetadatos del PDF:")
        metadata = pdf_reader.get_metadata()
        for key, value in metadata.items():
            print(f"{key}: {value}")

        if args.page is not None:
            print(f"\nTexto de la página {args.page + 1}:")
            print(pdf_reader.get_page_text(args.page))
        else:
            print("\nTexto completo del PDF:")
            print(pdf_reader.get_all_text())

        # Usar OCR para leer texto de las imágenes del PDF
        reader = PDFToImageTextReader(args.filepath)
        print("\nConvirtiendo PDF a imágenes...")
        reader.convert_pdf_to_images()
        print("\nExtrayendo texto de las imágenes...")
        text = reader.read_text_from_images(lang=args.lang)
        print("\nTexto extraído con OCR:")
        print(text)
    except Exception as e:
        print(f"Error: {e}")
    finally:
        pdf_reader.close_pdf()
        reader.cleanup()
