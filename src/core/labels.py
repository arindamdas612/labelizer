import pandas as pd
import io

from reportlab.graphics.barcode import qr
from reportlab.graphics.shapes import Drawing 
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.graphics import renderPDF


def get_labels(data):
    buffer = io.BytesIO()
    data = data.fillna({'QTY': 0})
    c = canvas.Canvas(buffer, bottomup=0, pagesize=(75*mm,50*mm))

    for index, row in data.iterrows():
        mrp = '{:0,.2f}'.format(row.MRP)
        for i in range(0, int(row.QTY)):
            textobject = c.beginText()
            textobject.setTextOrigin(3*mm, 5*mm)
            textobject.setFont('Courier', 10)
            textobject.textLine(text='Big Fox - ' + row.Product_Name)
            c.drawText(textobject)
            textobject.setFont('Courier', 14)
            textobject.textLine(text=' ')
            c.drawText(textobject)
            textobject.textLine(text='SKU      : ' + row.SKU)
            c.drawText(textobject)
            textobject.textLine(text='Color    : ' + row.Color)
            c.drawText(textobject)
            textobject.textLine(text='Size     : ' + str(row.Size))
            c.drawText(textobject)
            textobject.textLine(text='Price    : ' + mrp)
            c.drawText(textobject)
            textobject.textLine(text=' ')
            c.drawText(textobject)
            textobject.setFont('Courier', 8)
            textobject.textLine(text='MARKED BY - SIDDHARTH SALES')
            c.drawText(textobject)
            textobject.textLine(text='E-MAIL: siddharthsales5@gmail.com')
            c.drawText(textobject)
            # qr_code
            qr_code = qr.QrCodeWidget(f'Big_FOX<{row.SKU}_{row.Product_Name}_{row.Color}_{row.Size}_{mrp}>')
            bounds = qr_code.getBounds()
            width = bounds[2] - bounds[0]
            height = bounds[3] - bounds[1]
            d = Drawing(20*mm, 20*mm, transform=[20./width,0,0,20./height,0,0])
            d.add(qr_code)
            renderPDF.draw(d, c,65*mm, 40*mm)
            c.showPage()
    c.save()
    buffer.seek(0)
    return buffer
