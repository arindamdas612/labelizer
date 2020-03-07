import io
import pandas as pd
from xlsxwriter.workbook import Workbook
from django.contrib import messages

class ProductFile():
    sheet_name = 'products'
    header_columns = [
        'SKU',
        'Product_Name',
        'Color',
        'Size',
        'MRP',
        'QTY'
    ]
    header_width = [10, 25, 10, 3, 10, 10]

    def get_template(self):
        output = io.BytesIO()
        workbook = Workbook(output, {'in_memory': True})
        product_sheet = workbook.add_worksheet(self.sheet_name)
        cur_row = 0
        header_format = workbook.add_format({
            'bg_color': '#F7F7F7',
            'color': 'black',
            'align': 'center',
            'valign': 'top',
            'border': 1
        })
        for header in self.header_columns:
            col_num = self.header_columns.index(header)
            product_sheet.write(cur_row, self.header_columns.index(header) ,header , header_format)
            product_sheet.set_column(col_num, 1, self.header_width[col_num])
        workbook.close()
        output.seek(0)
        return output
    
    def get_sheet(self, file, request):
        data = {}
        xl_data = pd.ExcelFile(file)
        try:
            prod_data = xl_data.parse(self.sheet_name, header=0)
            return [prod_data, True]
        except:
            messages.add_message(
                request, messages.WARNING, 
                f'{self.sheet_name} Sheet does not exist in the file. Make Sure the File is as per Template.'
            )
            return [None, False]


    def validate_data(self, data, request):
        missing_headers = []
        valid = True
        for t_header in self.header_columns:
            if t_header not in (list(data.columns)):
                missing_headers.append(t_header)
        
        if missing_headers != []:
            valid = False
            err_string = f"Expected: {str(self.header_columns)}, Recieved: {str(list(data.columns))} and Missing: {str(missing_headers)}. Upload proper File. Download the template from this page."
            messages.add_message(
                request, messages.WARNING, 
                err_string
            )
        return valid
        
