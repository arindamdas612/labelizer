import pandas as pd
import io
import labels
from reportlab.graphics import shapes
from django.http import FileResponse

def draw_label(label, width, height, obj):
    
    label.add(shapes.String(5, 60, 'BIG FOX', fontName="Courier", fontSize=8))
    label.add(shapes.String(50, 60, obj.Product_Name, fontName="Courier", fontSize=6))
    label.add(shapes.String(5, 50, 'SKU    :', fontName="Courier", fontSize=8))
    label.add(shapes.String(50, 50, str(obj.SKU), fontName="Courier", fontSize=8))
    label.add(shapes.String(5, 40, 'COLOR  :', fontName="Courier", fontSize=8))
    label.add(shapes.String(50, 40, obj.Color, fontName="Courier", fontSize=8))
    label.add(shapes.String(5, 30, 'SIZE   :', fontName="Courier", fontSize=8))
    label.add(shapes.String(50, 30, str(obj.Size), fontName="Courier", fontSize=8))
    label.add(shapes.String(5, 20, 'MRP    :', fontName="Courier", fontSize=8))
    label.add(shapes.String(50, 20, str(obj.MRP), fontName="Courier", fontSize=8))
    label.add(shapes.String(5, 10, 'MARKED BY - SIDDHARTH SALES', fontName="Courier", fontSize=8))
    label.add(shapes.String(5, 3, 'E-MAIL: siddharthsales5@gmail.com', fontName="Courier", fontSize=6))

def get_labels(data):
    buffer = io.BytesIO()
    specs = labels.Specification(210, 297, 3, 8, 50, 25, corner_radius=1)

    sheet = labels.Sheet(specs, draw_label, border=True)

    for idx, product in data.iterrows():
        for i in range(0, product.QTY):
            sheet.add_label(product)
    
    sheet.save(buffer)
    buffer.seek(0)
    return buffer

    
