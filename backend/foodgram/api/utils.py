import datetime as dt
import io

from reportlab.lib.pagesizes import A4
from reportlab.pdfbase.pdfmetrics import registerFont
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas


def pdf_file_create(list, text):
    """Кастомный метод для создания файла PDF"""

    buffer = io.BytesIO()
    NOW = dt.datetime.now()
    START_A, START_B = 40, 720

    cart = canvas.Canvas(buffer, pagesize=A4)
    registerFont(TTFont('BuyanThin', '../foodgram/api/fonts/BuyanThin.ttf'))
    registerFont(TTFont('BuyanReg', '../foodgram/api/fonts/BuyanRegular.ttf'))
    cart.setFont('BuyanReg', 25)
    cart.setTitle(f'{text}')
    cart.drawString(START_A,
                    START_B + 25,
                    f'{text} на {NOW.strftime("%d-%m-%Y")}')
    START_B -= 30
    cart.setFont('BuyanThin', 17)
    for num, obj in enumerate(list, start=1):
        if START_B < 100:
            START_B = 750
            cart.showPage()
            cart.setFont('BuyanThin', 17)
        cart.drawString(
            START_A,
            START_B,
            f'{num}. {obj["ingredient__name"]} - '
            f'{obj["ingredient_total"]} '
            f'{obj["ingredient__measurement_unit"]}.'
        )
        START_B -= 30
    cart.showPage()
    cart.save()
    buffer.seek(0)
    return buffer
