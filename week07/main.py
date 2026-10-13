import flet as ft
from logic import convert


def main(page: ft.Page):
    page.title = "단위 변환기"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    result_text = ft.Text(value="", size=30, weight=ft.FontWeight.BOLD)
    error_text = ft.Text(value="", color="red", visible=False)

    def update_result(e=None):
        value_str = value_input.value.strip()

        if value_str == "":
            result_text.value = ""
            error_text.value = ""
            error_text.visible = False
            page.update()
            return

        result, error = convert(value_str, from_unit.value, to_unit.value)

        if error:
            result_text.value = ""
            error_text.value = error
            error_text.visible = True
        else:
            result_text.value = result
            error_text.value = ""
            error_text.visible = False

        page.update()

    value_input = ft.TextField(label="값", width=150, value="")

    from_unit = ft.Dropdown(
        label="원본 단위",
        value="mm",
        width=120,
        options=[
            ft.DropdownOption("mm"),
            ft.DropdownOption("cm"),
            ft.DropdownOption("m"),
            ft.DropdownOption("km"),
            ft.DropdownOption("°C"),
            ft.DropdownOption("°F"),
        ],
    )

    to_unit = ft.Dropdown(
        label="대상 단위",
        value="°C",
        width=120,
        options=[
            ft.DropdownOption("mm"),
            ft.DropdownOption("cm"),
            ft.DropdownOption("m"),
            ft.DropdownOption("km"),
            ft.DropdownOption("°C"),
            ft.DropdownOption("°F"),
        ],
    )

    convert_button = ft.Button("변환", on_click=update_result)

    page.add(
        ft.Column(
            controls=[
                ft.Row(
                    [value_input, from_unit, to_unit],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                ft.Row([convert_button], alignment=ft.MainAxisAlignment.CENTER),
                result_text,
                error_text,
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
    )


if __name__ == "__main__":
    ft.run(main)
