#trabajo mi interfaz con flet porque i love it so much
import flet as ft
import re


#esto es para trabajar excepciones, y tratar de que solo se analice a java y no se ingresen mas lenguajes (detecta la mayoria, pero tiene debilidades, para ser sincera)
def validar_java(input_text):
    palabras_clave = set(["abstract", "assert", "boolean", "break", "byte", "case", "catch", "char", "class", "const", "continue", "default", "do", "double", "else", "enum", "extends", "final", "finally", "float", "for", "goto", "if", "implements", "import", "instanceof", "int", "interface", "long", "native", "new", "package", "private", "protected", "public", "return", "short", "static", "strictfp", "super", "switch", "synchronized", "this", "throw", "throws", "transient", "try", "void", "volatile", "while"])
    
    if not any(re.search(rf'\b{palabra}\b', input_text) for palabra in palabras_clave):
        raise ValueError("El código ingresado no parece ser Java.")


#aqui defino las expresiones para los tokens
def lexer_java(input_text):
    validar_java(input_text)#me aseguro que sea java
    
    tokens = [
        ('PALABRA_CLAVE', r'\b(abstract|assert|boolean|break|byte|case|catch|char|class|const|continue|default|do|double|else|enum|extends|final|finally|float|for|goto|if|implements|import|instanceof|int|interface|long|native|new|package|private|protected|public|return|short|static|strictfp|super|switch|synchronized|this|throw|throws|transient|try|void|volatile|while)\b'),
        ('IDENTIFICADOR', r'\b[a-zA-Z_][a-zA-Z0-9_]*\b'),
        ('NUMERO', r'\b\d+(\.\d+)?\b'),
        ('OPERADOR', r'[+\-*/=<>!&|%^~]+'),
        ('SIMBOLO', r'[{}()\[\];.,]'),
        ('CADENA', r'".*?"'),
        ('COMENTARIO', r'//.*|/\*.*?\*/'),
        ('WHITESPACE', r'\s+'),
        ('DESCONOCIDO', r'.'),
    ]
    
    

    token_list = []
    position = 0
    while position < len(input_text):#aqui verifico que haya caracteres en input_text
        match = None
        for token_name, token_regex in tokens:
            regex = re.compile(token_regex, re.DOTALL)
            match = regex.match(input_text, position)#busco coincidencias
            if match:
                value = match.group(0)#si encuentro un token extraigo el valor
                if token_name != 'WHITESPACE':#si no es un espacio en blanco lo agrego
                    token_list.append(f"Token: {token_name}, Valor: {value}")
                position = match.end()#final del token que encontre
                break
        if not match:
            return [f"Error: Entrada no válida en '{input_text[position]}'"]
    return token_list

#puro frontend bonito
def main(page: ft.Page):
    page.title = "Analizador Léxico de Java"
    page.window_width = 600
    page.window_height = 400
    page.bgcolor = "#d9d9d9"
    
    # Manejo opcional de imagen de fondo
    background_image = None
    try:
        background_image = ft.Image(src="C:/Users/LENOVO/Downloads/Analizador (1)/Traductores/Compilador/Colorful Brushstrokes Beauty YouTube Intro (2).png", fit=ft.ImageFit.COVER, width=page.window_width, height=page.window_height)
    except Exception as e:
        print(f"No se pudo cargar la imagen de fondo: {e}")
    
    #manual 
    def show_manual(e):
        page.views.clear()
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
    
    #front del analizador
    def show_analyzer(e):
        def cargar_archivo(e):
            if e.files:
                file = e.files[0]
                # Validar extensión del archivo
                if not file.name.lower().endswith('.java'):
                    result.value = "Por favor, selecciona un archivo .java"
                    result.color = "#ff0000"
                    page.update()
                    return
                
                try:
                    with open(file.path, 'r') as f:
                        contenido = f.read()
                        texto_input.value = contenido
                        
                        # Limpiar el resultado anterior
                        result.value = ""
                        result.color = "#ffffff"
                        
                        page.update()
                except Exception as ex:
                    result.value = f"Error al leer el archivo: {str(ex)}"
                    result.color = "#ff0000"
                    page.update()
        
        def mostrar_selector_archivos(e):
            boton_cargar.pick_files()
        
        def analyze_text(e):
            try:
                # Primero intenta analizar el campo superior si tiene contenido
                if texto_input.value.strip():
                    result.value = "\n".join(lexer_java(texto_input.value))
                # Si el campo superior está vacío, analiza el campo de "Ingresar código Java"
                else:
                    result.value = "\n".join(lexer_java(input_box.value))
                result.color = "#ffffff"
            except ValueError as ex:
                result.value = str(ex)
                result.color = "#ff0000"
            page.update()
        
        texto_input = ft.TextField(label='Código Java', multiline=True, width=300, height=100, bgcolor="#0057b7", color="#ffffff")
        
        boton_cargar = ft.FilePicker(on_result=cargar_archivo)
        page.overlay.append(boton_cargar)
        
        boton_cargar_archivo = ft.ElevatedButton("Cargar archivo", on_click=mostrar_selector_archivos, bgcolor="#0057b7", color="#ffffff")
        
        input_box = ft.TextField(label="Ingresa código Java", width=400, multiline=True, min_lines=5, max_lines=10, bgcolor="#0057b7", color="#ffffff")
        result = ft.Text()
        result_container = ft.Container(content=ft.Column([result], scroll=ft.ScrollMode.AUTO), width=300, height=100, bgcolor="#0057b7")
        
        page.views.clear()
        page.views.append(
            ft.View("/analyzer", [
                ft.Container(
                    content=ft.Column([
                        texto_input,
                        boton_cargar_archivo,
                        input_box,
                        ft.ElevatedButton("Analizar", on_click=analyze_text, bgcolor="#0057b7", color="#ffffff"),
                        result_container,
                        ft.ElevatedButton("Volver", on_click=lambda e: show_main(), bgcolor="#0057b7", color="#ffffff")
                    ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER), alignment=ft.alignment.center
                )
            ], bgcolor="#d9d9d9")
        )
        page.go("/analyzer")

    def show_main():
        page.views.clear()#primero limpio para agregar
        page.views.append(
            ft.View("/", [
                ft.Container(
                    content=ft.Column([
                        background_image if background_image else ft.Text(""),
                        ft.ElevatedButton("Ir al Analizador", on_click=show_analyzer, bgcolor="#0057b7", color="#ffffff"),
                        ft.ElevatedButton("Manual de Usuario", on_click=show_manual, bgcolor="#0057b7", color="#ffffff")
                    ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER), alignment=ft.alignment.center
                )
            ], bgcolor="#d9d9d9")
        )
        page.go("/")
    
    show_main()

#listico
print("Iniciando aplicación...")
ft.app(target=main)
