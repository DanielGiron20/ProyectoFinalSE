import flet as ft
import requests
from datetime import datetime
import speech_recognition as sr
import os

def main(page: ft.Page):
    # Configuración inicial
    page.title = "Sistema Experto Médico - Hipertensión"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 30
    page.window_width = 1300
    page.window_height = 850

    # ============ FUNCIÓN LIMPIAR INTERFAZ ============
    def limpiar_interfaz():
        """Resetea los componentes de diagnóstico"""
        diagnostico_actual.value = ""
        explicacion_actual.value = ""
        grupo_radios.content.controls = []
        img_preview.visible = False
        img_preview.src = None
        page.update()

    # ============ COMPONENTES DE VOZ ============
    reconocedor = sr.Recognizer()
    grabando = False

    def toggle_grabacion(e):
        nonlocal grabando
        if not grabando:
            iniciar_grabacion()
            boton_voz.text = "🛑 Detener Voz"
            boton_voz.bgcolor = ft.colors.RED_400
        else:
            detener_grabacion()
            boton_voz.text = "🎤 Comandos por Voz"
            boton_voz.bgcolor = ft.colors.BLUE_400
        grabando = not grabando
        page.update()

    def iniciar_grabacion():
        def grabacion_thread():
            with sr.Microphone() as source:
                reconocedor.adjust_for_ambient_noise(source)
                audio = reconocedor.listen(source)
                try:
                    texto = reconocedor.recognize_google(audio, language="es-ES")
                    campo_sintomas.value = texto
                    page.update()
                except Exception as e:
                    mostrar_mensaje(f"❌ Error de voz: {str(e)}", ft.colors.RED)
        import threading
        threading.Thread(target=grabacion_thread, daemon=True).start()

    def detener_grabacion():
        pass

    # ============ COMPONENTES DE IMÁGENES ============
    def subir_imagen(e: ft.FilePickerResultEvent):
        if e.files:
            img_path = e.files[0].path
            img_preview.src = img_path
            img_preview.visible = True
            try:
                with open(img_path, "rb") as f:
                    files = {'imagen': f}
                    response = requests.post(
                        "http://127.0.0.1:1880/analizar-imagen",
                        files=files,
                        timeout=20
                    )
                    if response.status_code == 200:
                        resultado = response.json()
                        mostrar_mensaje(f"🔍 Análisis: {resultado.get('diagnostico', '')}", ft.colors.GREEN)
                        diagnostico_actual.value = resultado.get("diagnostico_imagen", "")
                        explicacion_actual.value = resultado.get("explicacion_imagen", "")
            except Exception as ex:
                mostrar_mensaje(f"❌ Error analizando imagen: {str(ex)}", ft.colors.RED)
            page.update()

    file_picker = ft.FilePicker(on_result=subir_imagen)
    page.overlay.append(file_picker)
    img_preview = ft.Image(width=200, visible=False)

    # ============ COMPONENTES UI ============
    titulo = ft.Text("🧠 DIAGNÓSTICO DE HIPERTENSIÓN", size=28, weight="bold", color=ft.colors.BLUE_800)

    campo_sintomas = ft.TextField(
        label="Describe síntomas o usa voz/cámara...",
        multiline=True,
        min_lines=3,
        width=700,
        border_color=ft.colors.BLUE_400,
        filled=True
    )

    def crear_arbol_hipertension():
        return ft.Column([
            ft.ExpansionTile(
                title=ft.Text("1. Síntomas Primarios", weight="bold", color=ft.colors.RED),
                controls=[
                    ft.ListTile(title=ft.Text("Cefalea, mareos, visión borrosa, epistaxis")),
                    ft.ExpansionTile(
                        title=ft.Text("2. Clasificación TA", weight="bold"),
                        controls=[
                            ft.ListTile(title=ft.Text("Normal: <120/<80, Elevada: 120-129/<80")),
                            ft.ListTile(title=ft.Text("Hipertensión Etapa 1: 130-139/80-89")),
                            ft.ListTile(title=ft.Text("Hipertensión Etapa 2: ≥140/90")),
                            ft.ExpansionTile(
                                title=ft.Text("3. Factores de Riesgo", weight="bold"),
                                controls=[
                                    ft.ListTile(title=ft.Text("Edad >65, obesidad, sedentarismo")),
                                    ft.ListTile(title=ft.Text("Antecedentes familiares, dieta alta en sodio")),
                                    ft.ExpansionTile(
                                        title=ft.Text("4. Comorbilidades", weight="bold"),
                                        controls=[
                                            ft.ListTile(title=ft.Text("Diabetes, enfermedad renal crónica")),
                                            ft.ListTile(title=ft.Text("Dislipidemia, apnea del sueño")),
                                            ft.ExpansionTile(
                                                title=ft.Text("5. Evaluación Inicial", weight="bold"),
                                                controls=[
                                                    ft.ListTile(title=ft.Text("Historia clínica completa")),
                                                    ft.ListTile(title=ft.Text("Examen físico: peso, talla, IMC")),
                                                    ft.ExpansionTile(
                                                        title=ft.Text("6. Exámenes Laboratorio", weight="bold"),
                                                        controls=[
                                                            ft.ListTile(title=ft.Text("Hemograma, glucosa ayunas")),
                                                            ft.ListTile(title=ft.Text("Perfil lipídico, creatinina")),
                                                            ft.ExpansionTile(
                                                                title=ft.Text("7. Estudios Complementarios", weight="bold"),
                                                                controls=[
                                                                    ft.ListTile(title=ft.Text("Electrocardiograma")),
                                                                    ft.ListTile(title=ft.Text("Ecocardiograma si indicado")),
                                                                    ft.ExpansionTile(
                                                                        title=ft.Text("8. Clasificación Etiología", weight="bold"),
                                                                        controls=[
                                                                            ft.ListTile(title=ft.Text("Primaria (90-95% casos)")),
                                                                            ft.ListTile(title=ft.Text("Secundaria (5-10% casos)")),
                                                                            ft.ExpansionTile(
                                                                                title=ft.Text("9. Daño Órgano Blanco", weight="bold"),
                                                                                controls=[
                                                                                    ft.ListTile(title=ft.Text("Retinopatía hipertensiva")),
                                                                                    ft.ListTile(title=ft.Text("Hipertrofia ventricular izq.")),
                                                                                    ft.ExpansionTile(
                                                                                        title=ft.Text("10. Estratificación Riesgo", weight="bold"),
                                                                                        controls=[
                                                                                            ft.ListTile(title=ft.Text("Bajo, moderado, alto, muy alto")),
                                                                                            ft.ExpansionTile(
                                                                                                title=ft.Text("11. Objetivos Terapéuticos", weight="bold"),
                                                                                                controls=[
                                                                                                    ft.ListTile(title=ft.Text("<130/80 para mayoría")),
                                                                                                    ft.ListTile(title=ft.Text("<140/90 para ancianos")),
                                                                                                    ft.ExpansionTile(
                                                                                                        title=ft.Text("12. Medidas No Farmacológicas", weight="bold"),
                                                                                                        controls=[
                                                                                                            ft.ListTile(title=ft.Text("Dieta DASH, reducción sodio")),
                                                                                                            ft.ListTile(title=ft.Text("Ejercicio aeróbico regular")),
                                                                                                            ft.ExpansionTile(
                                                                                                                title=ft.Text("13. Fármacos Primera Línea", weight="bold"),
                                                                                                                controls=[
                                                                                                                    ft.ListTile(title=ft.Text("IECAs, ARA II, CCB, diuréticos")),
                                                                                                                    ft.ExpansionTile(
                                                                                                                        title=ft.Text("14. Seguimiento", weight="bold"),
                                                                                                                        controls=[
                                                                                                                            ft.ListTile(title=ft.Text("Control mensual inicial")),
                                                                                                                            ft.ListTile(title=ft.Text("Monitoreo ambulatorio TA")),
                                                                                                                            ft.ExpansionTile(
                                                                                                                                title=ft.Text("15. Complicaciones", weight="bold"),
                                                                                                                                controls=[
                                                                                                                                    ft.ListTile(title=ft.Text("ACV, infarto, insuficiencia renal")),
                                                                                                                                    ft.ListTile(title=ft.Text("Encefalopatía hipertensiva"))
                                                                                                                                ]
                                                                                                                            )
                                                                                                                        ]
                                                                                                                    )
                                                                                                                ]
                                                                                                            )
                                                                                                        ]
                                                                                                    )
                                                                                                ]
                                                                                            )
                                                                                        ]
                                                                                    )
                                                                                ]
                                                                            )
                                                                        ]
                                                                    )
                                                                ]
                                                            )
                                                        ]
                                                    )
                                                ]
                                            )
                                        ]
                                    )
                                ]
                            )
                        ]
                    )
                ]
            )
        ])

    arbol_hipertension = crear_arbol_hipertension()

    # ============ COMPONENTES DIAGNÓSTICO ============
    diagnostico_actual = ft.Text("", size=18, weight="bold")
    explicacion_actual = ft.Text("", size=14)
    grupo_radios = ft.RadioGroup(content=ft.Column([]))
    historial_diagnosticos = ft.Column([], scroll=ft.ScrollMode.AUTO)

    # ============ FUNCIONALIDAD ============
    def mostrar_mensaje(texto, color):
        historial_diagnosticos.controls.append(ft.Text(texto, color=color, size=14))
        page.update()

    def consultar_diagnostico(e):
        sintomas = campo_sintomas.value.strip()
        if not sintomas:
            mostrar_mensaje("⚠️ Describe síntomas o sube una imagen", ft.colors.RED)
            return

        limpiar_interfaz()
        mostrar_mensaje("🔍 Analizando...", ft.colors.BLUE)

        try:
            response = requests.post(
                "http://127.0.0.1:1880/pregunta",
                json={
                    "pregunta": sintomas,
                    "tipo": "hipertension"
                },
                timeout=15
            )

            if response.status_code == 200:
                procesar_respuesta(response.json())
            else:
                mostrar_mensaje(f"❌ Error del servidor: {response.status_code}", ft.colors.RED)

        except Exception as e:
            mostrar_mensaje(f"❌ Error de conexión: {str(e)}", ft.colors.RED)

    def procesar_respuesta(datos):
        if "error" in datos:
            mostrar_mensaje(f"❌ {datos['error']}", ft.colors.RED)
            return

        diagnostico_actual.value = datos.get("diagnostico", "Hipertensión no clasificada")
        explicacion_actual.value = datos.get("explicacion", "")

        grupo_radios.content.controls = [
            ft.Radio(
                value=opcion.get("valor"),
                label=ft.Text(opcion.get("texto", "Opción"), size=14),
                data=opcion.get("explicacion", "")
            ) for opcion in datos.get("opciones", [])
        ]

        historial_diagnosticos.controls.append(
            ft.Card(
                ft.Container(
                    ft.Column([
                        ft.Text(f"📅 {datetime.now().strftime('%H:%M')}", size=12),
                        ft.Text(datos.get("diagnostico", ""), weight="bold"),
                        ft.Text(datos.get("explicacion", ""), size=12)
                    ]),
                    padding=10
                )
            )
        )
        mostrar_mensaje("✅ Diagnóstico generado", ft.colors.GREEN)
        page.update()

    def mostrar_detalle_opcion(e):
        if grupo_radios.value:
            for opcion in grupo_radios.content.controls:
                if opcion.value == grupo_radios.value:
                    explicacion_actual.value = opcion.data
                    break
        page.update()

    # ============ DISEÑO FINAL ============
    panel_izquierdo = ft.Column([
        ft.Text("📋 Entrada de Datos", weight="bold"),
        campo_sintomas,
        ft.Row([
            ft.ElevatedButton(
                text="🎤 Comandos por Voz",
    on_click=toggle_grabacion,
    bgcolor=ft.colors.BLUE_400,
    color=ft.colors.WHITE
            ),
            ft.ElevatedButton(
                "📸 Subir Imagen",
                on_click=lambda _: file_picker.pick_files(
                    allowed_extensions=["jpg", "jpeg", "png"],
                    dialog_title="Seleccionar imagen médica"
                ),
                icon=ft.icons.CAMERA_ALT
            )
        ], spacing=10),
        img_preview,
        ft.ElevatedButton(
            "🔍 Consultar Diagnóstico",
            on_click=consultar_diagnostico,
            icon=ft.icons.SEARCH,
            style=ft.ButtonStyle(padding=20, bgcolor=ft.colors.BLUE_600)
        ),
        ft.Divider(),
        ft.Text("📊 Historial Clínico", weight="bold"),
        ft.Container(
            ft.Column([historial_diagnosticos], scroll=ft.ScrollMode.AUTO),
            height=300,
            border=ft.border.all(1, ft.colors.GREY_300),
            padding=10,
            border_radius=10
        )
    ], spacing=15, expand=True)

    panel_central = ft.Column([
        ft.Text("🌳 Árbol de Decisión (Hipertensión)", weight="bold"),
        ft.Container(
            ft.Column([arbol_hipertension], scroll=ft.ScrollMode.AUTO),
            height=500,
            padding=10,
            border=ft.border.all(1, ft.colors.BLUE_100),
            border_radius=10
        )
    ], spacing=15, width=400)

    panel_derecho = ft.Container( content= ft.Column([
        ft.Text("🩺 Diagnóstico", weight="bold"),
        ft.Container(
            diagnostico_actual,
            padding=10,
            bgcolor=ft.colors.RED_50,
            border_radius=10
        ),
        ft.Text("📝 Explicación", weight="bold"),
        ft.Container(
            explicacion_actual,
            padding=10,
            bgcolor=ft.colors.GREY_50,
            border_radius=10
        ),
        ft.Divider(),
        ft.Text("🔍 Opciones", weight="bold"),
        ft.Container(
            ft.Column([grupo_radios], scroll=ft.ScrollMode.AUTO),
            height=200,
            padding=20,
            border=ft.border.all(1, ft.colors.GREY_300),
            border_radius=10
        )
       
    ], spacing=15, width=300)
    )

    # Configuración final
    boton_voz = panel_izquierdo.controls[2].controls[0]
    grupo_radios.on_change = mostrar_detalle_opcion

    page.add(
        ft.Column([
            titulo,
            ft.Row([
                panel_izquierdo,
                ft.VerticalDivider(),
                panel_central,
                ft.VerticalDivider(),
                panel_derecho
            ], expand=True, spacing=20)
        ], spacing=20)
    )

if __name__ == "__main__":
    ft.app(target=main)