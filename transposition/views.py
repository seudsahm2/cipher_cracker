from django.shortcuts import render
from .forms import TranspositionForm
from .ciphers import *

def transposition_view(request):
    result = None
    form = TranspositionForm(request.POST or None)
    
    if request.method == 'POST' and form.is_valid():
        data = form.cleaned_data
        cipher_type = data['cipher_type']
        operation = data['operation']
        text = data['text']
        
        try:
            if cipher_type == 'railfence':
                result = handle_railfence(data, operation)
            elif cipher_type == 'columnar':
                result = handle_columnar(data, operation)
            elif cipher_type == 'route':
                result = handle_route(data, operation)
            elif cipher_type == 'double':
                result = handle_double(data, operation)
            elif cipher_type == 'myszkowski':
                result = handle_myszkowski(data, operation)
                
        except Exception as e:
            result = f"Error: {str(e)}"
    
    return render(request, 'transposition/cipher.html', {
        'form': form,
        'result': result
    })

def handle_railfence(data, operation):
    rails = data['rails']
    if not rails:
        raise ValueError("Number of rails is required")
    return railfence_encrypt(data['text'], rails) if operation == 'encrypt' else railfence_decrypt(data['text'], rails)

def handle_columnar(data, operation):
    key = data['key']
    if not key:
        raise ValueError("Key is required")
    return columnar_encrypt(data['text'], key) if operation == 'encrypt' else columnar_decrypt(data['text'], key)

def handle_route(data, operation):
    rows = data['rows']
    cols = data['cols']
    if not rows or not cols:
        raise ValueError("Rows and columns are required")
    return route_encrypt(data['text'], rows, cols) if operation == 'encrypt' else route_decrypt(data['text'], rows, cols)

def handle_double(data, operation):
    key1 = data['key1']
    key2 = data['key2']
    if not key1 or not key2:
        raise ValueError("Both keys are required")
    return double_transposition_encrypt(data['text'], key1, key2) if operation == 'encrypt' else double_transposition_decrypt(data['text'], key1, key2)

def handle_myszkowski(data, operation):
    key = data['key']
    if not key:
        raise ValueError("Key is required")
    return myszkowski_encrypt(data['text'], key) if operation == 'encrypt' else myszkowski_decrypt(data['text'], key)