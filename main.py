import flet as ft
import requests

def main(page: ft.Page):
    page.title = "Sistema Experto - Diagnóstico de Diabetes"
    page.scroll = True

    # Etiqueta título
    titulo = ft.Text("🧠 Diagnóstico Médico de Diabetes", size=30, weight="bold")

    # Entrada del usuario
    entrada = ft.TextField(label="Escribe tus síntomas o pregunta...", width=500)

    # Simulación de respuesta (más adelante se conecta con IA)
    respuesta = ft.Text("Respuesta del sistema experto aparecerá aquí.", size=18)

    # Función para enviar la pregunta a Node-RED
    def consultar_click(e):
        pregunta = entrada.value
        if pregunta.strip() == "":
            respuesta.value = "Por favor escribe una pregunta válida."
            page.update()
            return
        
        try:
            # Hacer una solicitud POST a Node-RED
            response = requests.post("http://127.0.0.1:1880/pregunta", json={"pregunta": pregunta})
            
            # Revisar la respuesta de Node-RED
            if response.status_code == 200:
                respuesta_json = response.json()
                respuesta.value = respuesta_json.get("respuesta", "No se pudo obtener una respuesta.")
            else:
                respuesta.value = f"Error en la comunicación con Node-RED. Status: {response.status_code}"
        except Exception as e:
            respuesta.value = f"Error al conectar con Node-RED: {str(e)}"
        
        page.update()

    boton_consultar = ft.ElevatedButton("Consultar Diagnóstico", on_click=consultar_click)

    # Árbol jerárquico de categorías/preguntas
    arbol = ft.Column([
        ft.Text("📌 1. ¿Qué es la diabetes?", weight="bold"),
        ft.Text("Es una enfermedad metabólica crónica que se caracteriza por niveles elevados de glucosa en sangre debido a una disfunción en la producción o acción de la insulina."),
        
        ft.ExpansionTile(
            title=ft.Text("📌 2. Tipos de Diabetes"),
            controls=[
                ft.ListTile(title=ft.Text("Diabetes tipo 1")),
                ft.ListTile(title=ft.Text("Diabetes tipo 2")),
                ft.ListTile(title=ft.Text("Diabetes gestacional")),
            ]
        ),
        
        ft.ExpansionTile(
            title=ft.Text("📌 3. Factores de Riesgo"),
            controls=[
                ft.ListTile(title=ft.Text("Edad, obesidad, antecedentes familiares")),
                ft.ListTile(title=ft.Text("Inactividad física, dieta poco saludable")),
            ]
        ),
        
        ft.ExpansionTile(
            title=ft.Text("📌 4. Síntomas de la Diabetes"),
            controls=[
                ft.ListTile(title=ft.Text("Sed excesiva, fatiga, visión borrosa")),
                ft.ListTile(title=ft.Text("Pérdida de peso inexplicada")),
            ]
        ),
        
        ft.ExpansionTile(
            title=ft.Text("📌 5. Pruebas de Diagnóstico"),
            controls=[
                ft.ListTile(title=ft.Text("Glucosa en ayunas")),
                ft.ListTile(title=ft.Text("HbA1c ≥ 6.5%")),
            ]
        ),
        
        ft.ExpansionTile(
            title=ft.Text("📌 6. Importancia del Diagnóstico Temprano"),
            controls=[
                ft.ListTile(title=ft.Text("Previene complicaciones graves")),
            ]
        ),
        
        ft.ExpansionTile(
            title=ft.Text("📌 7. Prevención y Control"),
            controls=[
                ft.ListTile(title=ft.Text("Dieta equilibrada, ejercicio")),
                ft.ListTile(title=ft.Text("Control del peso, monitoreo")),
            ]
        ),
        
        ft.ExpansionTile(
            title=ft.Text("📌 8. Tratamientos Comunes"),
            controls=[
                ft.ListTile(title=ft.Text("Medicamentos orales")),
                ft.ListTile(title=ft.Text("Insulina y cambios en el estilo de vida")),
            ]
        ),
    ])

    # Opciones seleccionables (simulación, luego se ajusta)
    opciones = ft.Column([
        ft.Checkbox(label="Sed excesiva"),
        ft.Checkbox(label="Orina frecuente"),
        ft.Checkbox(label="Fatiga"),
        ft.Checkbox(label="Visión borrosa"),
        ft.Checkbox(label="Pérdida de peso inexplicada"),
    ])

    # Construcción de la interfaz
    page.add(
        titulo,
        entrada,
        boton_consultar,
        respuesta,
        ft.Divider(),
        ft.Text("🗂️ Árbol Jerárquico del Conocimiento", size=22, weight="bold"),
        arbol,
        ft.Divider(),
        ft.Text("🩺 Síntomas Seleccionados", size=22, weight="bold"),
        opciones
    )

ft.app(target=main)
