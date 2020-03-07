from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .forms import ProductListForm
from .utils import ProductFile
from .labels import get_labels
# Create your views here.

@login_required
def home(request):
    template_name = 'home.html'
    form =ProductListForm(request.POST or None)
    if request.method == 'POST':
        uploaded_file = request.FILES['docfile']
        if uploaded_file.name.endswith('.xlsx'):
            prod_file = ProductFile()
            data, valid_sheet = prod_file.get_sheet(file=uploaded_file, request=request)
            if valid_sheet:
               valid_data = prod_file.validate_data(data=data, request=request)
               if valid_data:
                    label = get_labels(data)
                    response = HttpResponse(label, content_type="application/pdf")
                    response['Content-Disposition'] = "attachment; filename=" + "Labelizer_labels.pdf"
                    form = ProductListForm()
                    return response
        else:
            messages.add_message(
                request, messages.WARNING, 
                f'Only "xlsx" is allowed. Recieved file type is "{uploaded_file.name.split(".")[-1]}".'
            )
    
    
    context = {}
    context['title'] = 'Home'
    context['form'] = form
    context['avatar_path'] = "img/avatars/" + request.user.userprofile.avatar_name + ".jpg"
    return render(request, template_name, context=context)

@login_required
def download_template(request):
    product_file = ProductFile()
    xlsx_data = product_file.get_template()
    response = HttpResponse(xlsx_data.read(), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response['Content-Disposition'] = "attachment; filename=" + "template.xlsx"
    return response