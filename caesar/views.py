from django.shortcuts import render
from collections import Counter

# Integer letter weights (scaled x10 for no decimals)
LETTER_WEIGHTS = {
    'a': 82, 'b': 15, 'c': 28, 'd': 43, 'e': 127,
    'f': 22, 'g': 20, 'h': 61, 'i': 70, 'j': 2,
    'k': 8, 'l': 40, 'm': 24, 'n': 67, 'o': 75,
    'p': 19, 'q': 1, 'r': 60, 's': 63, 't': 91,
    'u': 28, 'v': 10, 'w': 24, 'x': 2, 'y': 20,
    'z': 1
}

def decrypt(ciphertext, key):
    """Simple Caesar decryption"""
    return ''.join([
        chr((ord(c) - ord('a') - key) % 26 + ord('a')) if c.isalpha() else c
        for c in ciphertext.lower()
    ])

def calculate_score(text):
    """Pure letter frequency score (higher = better)"""
    clean = [c for c in text.lower() if c in LETTER_WEIGHTS]
    if not clean:
        return 0
    
    counts = Counter(clean)
    # Simple score: sum(letter_count * letter_weight)
    return sum(counts[char] * LETTER_WEIGHTS[char] for char in counts)

def frequency_attack(ciphertext, top_n=10):
    candidates = []
    for key in range(26):
        plaintext = decrypt(ciphertext, key)
        score = calculate_score(plaintext)
        candidates.append((score, key, plaintext))
    
    # Sort by score descending, then key ascending
    candidates.sort(key=lambda x: (-x[0], x[1]))
    return candidates[:top_n]

def home(request):
    context = {}
    if request.method == 'POST':
        ciphertext = request.POST.get('ciphertext', '')
        top_n = int(request.POST.get('top_n', 10))
        results = frequency_attack(ciphertext, top_n)
        context.update({
            'results': results,
            'ciphertext': ciphertext,
            'top_n': top_n
        })
    return render(request, 'caesar/home.html', context)