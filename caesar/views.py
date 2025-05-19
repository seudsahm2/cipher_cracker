from django.shortcuts import render
from collections import Counter

ENGLISH_FREQ_ORDER = 'etaoinshrdlcumwfgypbvkjxqz'

def decrypt_caesar(ciphertext, key):
    decrypted = ''
    for char in ciphertext:
        if char.isalpha():
            shifted = (ord(char.lower()) - ord('a') - key) % 26
            decrypted += chr(shifted + ord('a'))
        else:
            decrypted += char
    return decrypted

def score_text(text):
    text = ''.join(filter(str.isalpha, text.lower()))
    letter_counts = Counter(text)
    common_letters = [item[0] for item in letter_counts.most_common()]
    score = sum(1 for i in common_letters[:6] if i in ENGLISH_FREQ_ORDER[:6])
    return score

def frequency_attack(ciphertext, top_n):
    results = []
    for key in range(26):
        plaintext = decrypt_caesar(ciphertext, key)
        score = score_text(plaintext)
        results.append((score, key, plaintext))
    results.sort(reverse=True, key=lambda x: x[0])
    return results[:top_n]

def home(request):
    context = {}
    if request.method == 'POST':
        ciphertext = request.POST.get('ciphertext')
        top_n = int(request.POST.get('top_n', 10))
        results = frequency_attack(ciphertext, top_n)
        context['results'] = results
        context['ciphertext'] = ciphertext
        context['top_n'] = top_n
    return render(request, 'caesar/home.html', context)
