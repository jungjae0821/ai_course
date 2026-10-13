# main.py
import flet as ft
from logic import convert

def main(page: ft.Page):
    page.title = "단위 변환기"
    page.window.width = 400
    page.window.height = 300
    page.window.resizable = False
    page.theme_mode = ft.ThemeMode.LIGHT
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    # UI 요소 생성
    result_text = ft.Text(value="", size=30, weight=ft.FontWeight.BOLD)
    error_text = ft.Text(value="", color=ft.Colors.RED)

    def update_result(e=None):
        val_str = value_input.value.strip()
        
        # 입력값이 비어있으면 결과와 에러를 비움
        if not val_str:
            result_text.value = ""
            error_text.value = ""
        else:
            res, err = convert(val_str, from_unit.value, to_unit.value)
            if err:
                result_text.value = ""
                error_text.value = err
            else:
                result_text.value = res
                error_text.value = ""
            
        page.update()

    value_input = ft.TextField(
        label="값", 
        width=120, 
        on_change=update_result
    )
    
    from_unit = ft.Dropdown(
        label="원본 단위", 
        value="mm", 
        width=100,
        options=[
            ft.dropdown.Option("mm"),
            ft.dropdown.Option("cm"),
            ft.dropdown.Option("m"),
            ft.dropdown.Option("km"),
            ft.dropdown.Option("°C"),
            ft.dropdown.Option("°F"),
        ],
        on_select=update_result
    )
    
    to_unit = ft.Dropdown(
        label="대상 단위", 
        value="°C", 
        width=100,
        options=[
            ft.dropdown.Option("mm"),
            ft.dropdown.Option("cm"),
            ft.dropdown.Option("m"),
            ft.dropdown.Option("km"),
            ft.dropdown.Option("°C"),
            ft.dropdown.Option("°F"),
        ],
        on_select=update_result
    )

    # 화면 구성
    page.add(
        ft.Column(
            controls=[
                ft.Row(
                    [value_input, from_unit, to_unit], 
                    alignment=ft.MainAxisAlignment.CENTER
                ),
                ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
                result_text,
                error_text,
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
    )

if __name__ == "__main__":
    ft.run(main)
