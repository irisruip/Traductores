
# Importación de bibliotecas necesarias
# flet (ft) es una biblioteca para crear interfaces gráficas modernas en Python
import flet as ft
# re es la biblioteca para trabajar con expresiones regulares en Python
import re

# Función para validar si el código ingresado es Java
def validar_java(input_text):
    """
    Valida si el código ingresado es Java.
    
    Args:
    input_text (str): El código a validar.
    
    Raises:
    ValueError: Si el código no parece ser Java.
    """
    # Conjunto de palabras clave reservadas de Java
    palabras_clave = set(["abstract", "assert", "boolean", "break", "byte", "case", "catch", "char", "class", "const", "continue", "default", "do", "double", "else", "enum", "extends", "final", "finally", "float", "for", "goto", "if", "implements", "import", "instanceof", "int", "interface", "long", "native", "new", "package", "private", "protected", "public", "return", "short", "static", "strictfp", "super", "switch", "synchronized", "this", "throw", "throws", "transient", "try", "void", "volatile", "while"])
    
    # Verifica si al menos una palabra clave de Java está presente en el texto
    if not any(re.search(rf'\b{palabra}\b', input_text) for palabra in palabras_clave):
        raise ValueError("El código ingresado no parece ser Java.")

# Función principal del analizador léxico para Java
def lexer_java(input_text):
    """
    Realiza el análisis léxico del código Java.
    
    Args:
    input_text (str): El código a analizar.
    
    Returns:
    list: La lista de tokens encontrados.
    """
    # Primero validamos que el código sea Java
    validar_java(input_text)
    
    # Definición de patrones para cada tipo de token usando expresiones regulares
    tokens = [
        # Palabras clave de Java
        ('Palabra_clave', r'\b(abstract|assert|boolean|break|byte|case|catch|char|class|const|continue|default|do|double|else|enum|extends|final|finally|float|for|goto|if|implements|import|instanceof|int|interface|long|native|new|package|private|protected|public|return|short|static|strictfp|super|switch|synchronized|this|throw|throws|transient|try|void|volatile|while)\b'),
        # Identificadores (nombres de variables, funciones, etc.)
        ('Identificador', r'\b[a-zA-Z_][a-zA-Z0-9_]*\b'),
        # Números (enteros y decimales)
        ('Numero', r'\b\d+(\.\d+)?\b'),
        # Operadores matemáticos y lógicos
        ('Operador', r'[+\-*/=<>!&|%^~]+'),
        # Símbolos de puntuación y delimitadores
        ('Simbolo', r'[{}()\[\];.,]'),
        # Cadenas de texto entre comillas
        ('Cadena', r'".*?"'),
        # Comentarios de una línea (//) y múltiples líneas (/* */)
        ('Comentario', r'//.*|/\*.*?\*/'),
        # Espacios en blanco, tabulaciones y saltos de línea
        ('WHITESPACE', r'\s+'),
        # Cualquier otro carácter no reconocido
        ('Desconocido', r'.'),
    ]
    
    # Lista para almacenar los tokens encontrados
    token_list = []
    position = 0
    
    # Analizar el texto mientras haya caracteres por procesar
    while position < len(input_text):
        match = None
        # Intentar hacer coincidir cada patrón de token
        for token_name, token_regex in tokens:
            regex = re.compile(token_regex, re.DOTALL)
            match = regex.match(input_text, position)
            if match:
                value = match.group(0)
                # No agregamos espacios en blanco a la lista de tokens
                if token_name != 'WHITESPACE':
                    token_list.append((token_name, value))
                position = match.end()
                break
        # Si no se encontró ninguna coincidencia, hay un error en el código
        if not match:
            return [("Error", f"Entrada no válida en '{input_text[position]}'")]
    return token_list

# Función principal del analizador sintáctico para Java
def parser_java(tokens):
    """
    Realiza el análisis sintáctico del código Java y formatea los errores como una tabla.

    Args:
    tokens (list): La lista de tokens a analizar.

    Returns:
    str: El resultado del análisis sintáctico formateado como una tabla.
    """
    index = 0
    errors = []

    def match(expected_type, expected_value=None):
        nonlocal index
        if index < len(tokens):
            token_type, token_value = tokens[index]
            if token_type == expected_type and (expected_value is None or token_value == expected_value):
                index += 1
                return True
        return False

    def peek(offset=0):
        nonlocal index
        if index + offset < len(tokens):
            return tokens[index + offset]
        return None, None

    def parse_class():
        nonlocal index
        start_index = index

        # Modificador de acceso opcional
        match("Palabra_clave", "public") or match("Palabra_clave", "private") or match("Palabra_clave", "protected")

        if match("Palabra_clave", "class"):
            if not match("Identificador"):
                errors.append({"Posición": index, "Token": peek(), "Descripción": "Nombre de clase inválido"})
                index = start_index
                return False

            if not match("Simbolo", "{"):
                errors.append({"Posición": index, "Token": peek(), "Descripción": "'{' esperado después del nombre de la clase"})
                index = start_index
                return False

            # Procesar miembros de clase
            while index < len(tokens) and not match("Simbolo", "}"):
                if not parse_method() and not parse_variable_declaration():
                    errors.append({"Posición": index, "Token": peek(), "Descripción": "Elemento inválido dentro de la clase"})
                    index += 1  # Recuperación de error: saltar token problemático

            if not match("Simbolo", "}"):
                errors.append({"Posición": index, "Token": peek(), "Descripción": "'}' esperado al final de la clase"})
                index = start_index
                return False

            return True
        else:
            errors.append({"Posición": index, "Token": peek(), "Descripción": "Declaración de clase no encontrada"})
            return False

    def parse_method():
        # (El resto de las funciones de análisis permanecen igual, pero almacenan los errores en la lista 'errors' como diccionarios)
        pass

    def parse_variable_declaration():
        # (El resto de las funciones de análisis permanecen igual, pero almacenan los errores en la lista 'errors' como diccionarios)
        pass

    def parse_expression():
        # (El resto de las funciones de análisis permanecen igual, pero almacenan los errores en la lista 'errors' como diccionarios)
        pass

    # Análisis comienza aquí
    if not parse_class():
        if not errors:
            errors.append({"Posición": 0, "Token": tokens[0] if tokens else None, "Descripción": "Declaración de clase no encontrada al inicio del archivo"})

    if errors:
        return format_errors_as_table(errors)
    else:
        return "Análisis sintáctico completado sin errores."

def format_errors_as_table(errors):
    """
    Formatea la lista de errores como una tabla con columnas alineadas y numeración de filas.

    Args:
    errors (list): La lista de errores.

    Returns:
    str: La tabla formateada como una cadena.
    """
    if not errors:
        return "No se encontraron errores."

    # Calcular el ancho máximo de cada columna
    max_row_width = len(str(len(errors)))
    max_position_width = max(len(str(error['Posición'])) for error in errors)
    max_token_width = max(len(str(error['Token'])) for error in errors)
    max_description_width = max(len(error['Descripción']) for error in errors)

    # Crear el encabezado de la tabla
    header = f"{'#':<{max_row_width}} | {'Posición':<{max_position_width}} | {'Token':<{max_token_width}} | {'Descripción':<{max_description_width}}"
    separator = "-" * len(header)

    # Crear las filas de la tabla
    rows = []
    for i, error in enumerate(errors):
        row = f"{i + 1:<{max_row_width}} | {error['Posición']:<{max_position_width}} | {str(error['Token']):<{max_token_width}} | {error['Descripción']:<{max_description_width}}"
        rows.append(row)

    # Combinar el encabezado, el separador y las filas
    table = "\n".join([header, separator] + rows)
    return table



# Función principal para la interfaz gráfica
def main(page: ft.Page):
    """
    Función principal para la interfaz gráfica.
    
    Args:
    page (ft.Page): La página de la aplicación.
    """
    # Configuración inicial de la ventana
    page.title = "Analizador Léxico y Sintáctico de Java"
    page.window_width = 600
    page.window_height = 400
    page.bgcolor = "#d9d9d9"
    
    # Intento de cargar una imagen de fondo
    background_image = None
    try:
        background_image = ft.Image(src="C:/Users/LENOVO/Downloads/Analizador (1)/Traductores/Compilador/Colorful Brushstrokes Beauty YouTube Intro (2).png", fit=ft.ImageFit.COVER, width=page.window_width, height=page.window_height)
    except Exception as e:
        print(f"No se pudo cargar la imagen de fondo: {e}")
    
    # Función para mostrar el manual de usuario
    def show_manual(e):
        """
        Muestra el manual de usuario.
        
        Args:
        e: El evento que activó la función.
        """
        # Limpia las vistas existentes
        page.views.clear()
        # Agrega la vista del manual
        page.views.append(
            ft.View("/manual", [
                ft.Container(
                    content=ft.Column([
                        background_image if background_image else ft.Text(""),
                        ft.Text("Manual de Usuario:\n1. Ingrese código en Java.\n2. Presione Analizar.\n3. Verifique los tokens identificados.", color="#0057b7"),
                        ft.ElevatedButton("Volver", on_click=lambda e: show_main(), bgcolor="#0057b7", color="#ffffff")
                    ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER), alignment=ft.alignment.center
                )
            ], bgcolor="#d9d9d9")
        )
        page.go("/manual")
    
    # Función para mostrar el analizador
    def show_analyzer(e):
        """
        Muestra el analizador.
        
        Args:
        e: El evento que activó la función.
        """
        # Función para cargar archivo
        def cargar_archivo(e):
            """
            Carga un archivo.
            
            Args:
            e: El evento que activó la función.
            """
            if e.files:
                file = e.files[0]
                # Validación de extensión .java
                if not file.name.lower().endswith('.java'):
                    result.value = "Por favor, selecciona un archivo .java"
                    result.color = "#ff0000"
                    page.update()
                    return
                
                try:
                    # Lectura del archivo
                    with open(file.path, 'r') as f:
                        contenido = f.read()
                        texto_input.value = contenido
                        result.value = ""
                        result.color = "#ffffff"
                        page.update()
                except Exception as ex:
                    result.value = f"Error al leer el archivo: {str(ex)}"
                    result.color = "#ff0000"
                    page.update()
        
        # Función para mostrar el selector de archivos
        def mostrar_selector_archivos(e):
            """
            Muestra el selector de archivos.
            
            Args:
            e: El evento que activó la función.
            """
            boton_cargar.pick_files()
        
        # Función para analizar el texto léxicamente
        def analyze_text_lexico(e):
            """
            Analiza el texto léxicamente.
            
            Args:
            e: El evento que activó la función.
            """
            try:
                # Analiza el texto del campo superior si tiene contenido
                if texto_input.value.strip():
                    tokens = lexer_java(texto_input.value)
                    result.value = "\n".join([f"TOKEN: {token_name} -------> VALOR: {token_value}" for token_name, token_value in tokens])
                # Si no, analiza el campo inferior
                else:
                    tokens = lexer_java(input_box.value)
                    result.value = "\n".join([f"TOKEN: {token_name} -------> VALOR: {token_value}" for token_name, token_value in tokens])
                result.color = "#ffffff"
            except ValueError as ex:
                result.value = str(ex)
                result.color = "#ff0000"
            page.update()
        
        # Función para analizar el texto sintácticamente
        def analyze_text_sintactico(e):
            """
            Analiza el texto sintácticamente.
            
            Args:
            e: El evento que activó la función.
            """
            try:
                # Analiza el texto del campo superior si tiene contenido
                if texto_input.value.strip():
                    tokens = lexer_java(texto_input.value)
                    result.value = parser_java(tokens)
                # Si no, analiza el campo inferior
                else:
                    tokens = lexer_java(input_box.value)
                    result.value = parser_java(tokens)
                result.color = "#ffffff"
            except ValueError as ex:
                result.value = str(ex)
                result.color = "#ff0000"
            page.update()
        
        def clear_text(e):
            """
            Limpia el texto.
            
            Args:
            e: El evento que activó la función.
            """
            texto_input.value = ""
            input_box.value = ""
            result.value = ""
            page.update()
        
        # Creación de elementos de la interfaz
        texto_input = ft.TextField(label='Código Java', multiline=True, width=300, height=100, bgcolor="#0057b7", color="#ffffff")
        boton_cargar = ft.FilePicker(on_result=cargar_archivo)
        page.overlay.append(boton_cargar)
        boton_cargar_archivo = ft.ElevatedButton("Cargar archivo", on_click=mostrar_selector_archivos, bgcolor="#0057b7", color="#ffffff")
        input_box = ft.TextField(label="Ingresa código Java", width=400, height=200, multiline=True, min_lines=5, max_lines=10, bgcolor="#0057b7", color="#ffffff")
        result = ft.Text()
        result_container = ft.Container(content=ft.Column([result], scroll=ft.ScrollMode.AUTO), width=600, height=300, bgcolor="#0057b7")
        
        # Configuración de la vista del analizador
        page.views.clear()
        page.views.append(
            ft.View("/analyzer", [
                ft.Container(
                    content=ft.Column([
                        texto_input,
                        boton_cargar_archivo,
                        input_box,
                        ft.Row([
                            ft.ElevatedButton("Analizar Léxicamente", on_click=analyze_text_lexico, bgcolor="#0057b7", color="#ffffff"),
                            ft.ElevatedButton("Analizar Sintácticamente", on_click=analyze_text_sintactico, bgcolor="#0057b7", color="#ffffff"),
                            ft.ElevatedButton("Limpiar", on_click=clear_text, bgcolor="#0057b7", color="#ffffff")
                        ], alignment=ft.MainAxisAlignment.CENTER),
                        result_container,
                        ft.ElevatedButton("Volver", on_click=lambda e: show_main(), bgcolor="#0057b7", color="#ffffff")
                    ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER), alignment=ft.alignment.center
                )
            ], bgcolor="#d9d9d9")
        )
        page.go("/analyzer")

    # Función para mostrar la página principal
    def show_main():
        """
        Muestra la página principal.
        """
        page.views.clear()
        page.views.append(
            ft.View("/", [
                ft.Container(
                    content=ft.Column([
                        background_image if background_image else ft.Text(""),
                        ft.ElevatedButton("Ir al analizador", on_click=show_analyzer, bgcolor="#0057b7", color="#ffffff"),
                        ft.ElevatedButton("Manual de Usuario", on_click=show_manual, bgcolor="#0057b7", color="#ffffff"),
                        ft.ElevatedButton("Irisbel Ruiz", bgcolor="#ffffff", color="#000000")
                    ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER), alignment=ft.alignment.center
                )
            ], bgcolor="#d9d9d9")
        )
        page.go("/")
    
    # Iniciar mostrando la página principal
    show_main()

# Iniciar la aplicación
print("Iniciando aplicación...")
ft.app(target=main)
