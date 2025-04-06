import flet as ft
import requests
from datetime import datetime

def main(page: ft.Page):
    # Configuración inicial de la página
    page.title = "Sistema Experto Médico"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 30
    page.scroll = ft.ScrollMode.AUTO
    page.window_width = 1000
    page.window_height = 700

    # Componentes de la interfaz
    titulo = ft.Text(
        "🧠 DIAGNÓSTICO MÉDICO EXPERTO", 
        size=28, 
        weight="bold", 
        color=ft.colors.BLUE_800
    )

    campo_sintomas = ft.TextField(
        label="Describe tus síntomas en detalle...",
        multiline=True,
        min_lines=3,
        max_lines=5,
        width=700,
        border_color=ft.colors.BLUE_400,
        filled=True
    )

    diagnostico_actual = ft.Text("", size=18, weight="bold")
    explicacion_actual = ft.Text("", size=14)
    grupo_radios = ft.RadioGroup(content=ft.Column([]))
    historial_diagnosticos = ft.Column([], scroll=ft.ScrollMode.AUTO)

    # Funciones de apoyo
    def mostrar_mensaje(texto, color):
        historial_diagnosticos.controls.append(
            ft.Text(texto, color=color, size=14)
        )
        page.update()

    def limpiar_interfaz():
        diagnostico_actual.value = ""
        explicacion_actual.value = ""
        grupo_radios.content.controls = []
        page.update()

    def agregar_al_historial(datos):
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

    # Función principal
    def consultar_diagnostico(e):
        sintomas = campo_sintomas.value.strip()
        if not sintomas:
            mostrar_mensaje("⚠️ Por favor describe tus síntomas", ft.colors.RED)
            return

        limpiar_interfaz()
        mostrar_mensaje("🔍 Analizando síntomas...", ft.colors.BLUE)

        try:
            response = requests.post(
                "http://127.0.0.1:1880/pregunta",
                json={"pregunta": sintomas},
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

        diagnostico_actual.value = datos.get("diagnostico", "Diagnóstico no disponible")
        explicacion_actual.value = datos.get("explicacion", "")

        grupo_radios.content.controls = [
            ft.Radio(
                value=opcion.get("valor"),
                label=ft.Text(opcion.get("texto", "Opción"), size=14),
                data=opcion.get("explicacion", "")
            ) for opcion in datos.get("opciones", [])
        ]

        agregar_al_historial(datos)
        mostrar_mensaje("✅ Diagnóstico generado", ft.colors.GREEN)

    def mostrar_detalle_opcion(e):
        if grupo_radios.value:
            for opcion in grupo_radios.content.controls:
                if opcion.value == grupo_radios.value:
                    explicacion_actual.value = opcion.data
                    break
        page.update()

    # Configuración de eventos
    grupo_radios.on_change = mostrar_detalle_opcion

    boton_consultar = ft.ElevatedButton(
        "Consultar Diagnóstico",
        icon=ft.icons.SEARCH,
        on_click=consultar_diagnostico,
        style=ft.ButtonStyle(
            padding=20,
            bgcolor=ft.colors.BLUE_600,
            color=ft.colors.WHITE
        )
    )

    # Diseño de paneles
    panel_izquierdo = ft.Column([
        ft.Text("📋 Síntomas:", weight="bold"),
        campo_sintomas,
        boton_consultar,
        ft.Divider(),
        ft.Text("📊 Historial:", weight="bold"),
        ft.Container(
            historial_diagnosticos,
            height=300,
            border=ft.border.all(1, ft.colors.GREY_300),
            padding=10,
            border_radius=10
        )
    ], spacing=15, expand=True)

    panel_derecho = ft.Column([
        ft.Text("🩺 Diagnóstico:", weight="bold"),
        ft.Container(
            diagnostico_actual,
            padding=10,
            bgcolor=ft.colors.BLUE_50,
            border_radius=10
        ),
        ft.Text("📝 Explicación:", weight="bold"),
        ft.Container(
            explicacion_actual,
            padding=10,
            bgcolor=ft.colors.GREY_50,
            border_radius=10
        ),
        ft.Divider(),
        ft.Text("🔍 Opciones:", weight="bold"),
        ft.Container(
            grupo_radios,
            padding=20,
            border=ft.border.all(1, ft.colors.GREY_300),
            border_radius=10
        )
    ], spacing=15, expand=True)

    # Layout final
    page.add(
        ft.Column([
            titulo,
            ft.Row([
                panel_izquierdo,
                ft.VerticalDivider(),
                panel_derecho
            ], expand=True)
        ], spacing=20)
    )

if __name__ == "__main__":
    ft.app(target=main)