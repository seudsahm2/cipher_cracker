# views.py
from django.shortcuts import render
from .helpers import encrypt, decrypt

def home(request):
    context = {}
    
    if request.method == 'POST':
        text = request.POST.get('text', '')
        operation = request.POST.get('operation', 'encrypt')
        key = int(request.POST.get('key', 0))
        top_n = int(request.POST.get('top_n', 10))
        
        if operation == 'encrypt':
            result = encrypt(text, key)
            context['result'] = result
        elif operation == 'decrypt':
            result = decrypt(text, key)
            context['result'] = result
        elif operation == 'frequency_attack':
            possible_plaintexts = []
            for i in range(26):
                possible_plaintext = decrypt(text, i)
                possible_plaintexts.append((i, possible_plaintext))
            context['possible_plaintexts'] = possible_plaintexts[:top_n]
        
        context.update({
            'text': text,
            'operation': operation,
            'key': key,
            'top_n': top_n
        })
    
    return render(request, 'caesar/home.html', context)