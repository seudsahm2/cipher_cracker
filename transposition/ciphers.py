import math
from itertools import permutations

# Rail-fence Cipher
def railfence_encrypt(text, rails):
    fence = [''] * rails
    direction = 1
    row = 0
    for char in text:
        fence[row] += char
        row += direction
        if row == rails - 1 or row == 0:
            direction *= -1
    return ''.join(fence)

def railfence_decrypt(ciphertext, rails):
    length = len(ciphertext)
    fence = [[] for _ in range(rails)]
    positions = list(range(length))
    row, step = 0, 1
    for _ in range(length):
        fence[row].append(positions.pop(0))
        row += step
        if row == rails - 1 or row == 0:
            step *= -1
    indices = [idx for sub in fence for idx in sub]
    plaintext = [''] * length
    for i, char in zip(indices, ciphertext):
        plaintext[i] = char
    return ''.join(plaintext)

# Columnar Transposition
def columnar_encrypt(text, key):
    key_order = sorted(range(len(key)), key=lambda k: key[k])
    cols = len(key)
    rows = math.ceil(len(text) / cols)
    padded = text.ljust(rows * cols, 'X')
    grid = [padded[i*cols:(i+1)*cols] for i in range(rows)]
    return ''.join([grid[row][col] for col in key_order for row in range(rows)])

def columnar_decrypt(ciphertext, key):
    key_order = sorted(range(len(key)), key=lambda k: key[k])
    inv_order = [key_order.index(i) for i in range(len(key))]
    cols = len(key)
    rows = math.ceil(len(ciphertext) / cols)
    grid = [ciphertext[i*rows:(i+1)*rows] for i in range(cols)]
    return ''.join([grid[inv_order[col]][row] for row in range(rows) for col in range(cols)]).replace('X', '')

# Route Cipher (Spiral)
def route_encrypt(text, rows, cols):
    text = text.replace(' ', 'X').upper()
    grid = [list(text[i*cols:(i+1)*cols].ljust(cols, 'X')) for i in range(rows)]
    result = []
    top, bottom, left, right = 0, rows-1, 0, cols-1
    
    while top <= bottom and left <= right:
        for i in range(left, right+1):
            result.append(grid[top][i])
        top += 1
        for i in range(top, bottom+1):
            result.append(grid[i][right])
        right -= 1
        if top <= bottom:
            for i in range(right, left-1, -1):
                result.append(grid[bottom][i])
            bottom -= 1
        if left <= right:
            for i in range(bottom, top-1, -1):
                result.append(grid[i][left])
            left += 1
    return ''.join(result)

def route_decrypt(ciphertext, rows, cols):
    grid = [[None]*cols for _ in range(rows)]
    text = list(ciphertext.ljust(rows*cols, 'X'))
    top, bottom, left, right = 0, rows-1, 0, cols-1
    idx = 0
    
    while top <= bottom and left <= right:
        for i in range(left, right+1):
            grid[top][i] = text[idx]
            idx += 1
        top += 1
        for i in range(top, bottom+1):
            grid[i][right] = text[idx]
            idx += 1
        right -= 1
        if top <= bottom:
            for i in range(right, left-1, -1):
                grid[bottom][i] = text[idx]
                idx += 1
            bottom -= 1
        if left <= right:
            for i in range(bottom, top-1, -1):
                grid[i][left] = text[idx]
                idx += 1
            left += 1
    return ''.join([''.join(row) for row in grid]).replace('X', '')

# Double Transposition
def double_transposition_encrypt(text, key1, key2):
    first = columnar_encrypt(text, key1)
    return columnar_encrypt(first, key2)

def double_transposition_decrypt(ciphertext, key1, key2):
    first = columnar_decrypt(ciphertext, key2)
    return columnar_decrypt(first, key1)

# Myszkowski Transposition
def myszkowski_encrypt(text, key):
    key = key.upper()
    sorted_indices = sorted(range(len(key)), key=lambda k: key[k])
    cols = len(key)
    rows = math.ceil(len(text) / cols)
    text = text.ljust(rows*cols, 'X')
    
    groups = {}
    for i, char in enumerate(key):
        if char not in groups:
            groups[char] = []
        groups[char].append(i)
    
    ciphertext = []
    for group in groups.values():
        for col in group:
            ciphertext.extend(text[col::cols])
    return ''.join(ciphertext).replace('X', '')

def myszkowski_decrypt(ciphertext, key):
    key = key.upper()
    sorted_indices = sorted(range(len(key)), key=lambda k: key[k])
    cols = len(key)
    text_len = len(ciphertext)
    rows = math.ceil(text_len / cols)
    
    groups = {}
    for i, char in enumerate(key):
        if char not in groups:
            groups[char] = []
        groups[char].append(i)
    
    col_counts = {}
    for group in groups.values():
        count = len(group)
        for col in group:
            col_counts[col] = rows if len(ciphertext) > col*rows else text_len - col*rows
    
    grid = [['']*cols for _ in range(rows)]
    idx = 0
    for group in groups.values():
        for col in group:
            for row in range(col_counts[col]):
                if idx < text_len:
                    grid[row][col] = ciphertext[idx]
                    idx += 1
    return ''.join([''.join(row) for row in grid]).replace('X', '')