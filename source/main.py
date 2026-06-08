"""
main.py — Clasificador de Spam y Phishing 

Analiza automáticamente todos los archivos .txt de la carpeta emails/
y muestra una tabla de resultados con la clasificación y confianza.
"""

import os
from classifier import EmailClassifier
from email_parser import load_emails_from_folder

EMAILS_FOLDER = os.path.join(os.path.dirname(__file__), 'emails')

# Colores ANSI - Generado IA
COLOR = {
    'LEGITIMO':   '\033[92m',
    'SOSPECHOSO': '\033[93m',
    'SPAM':       '\033[91m',
    'PHISHING':   '\033[95m',
    'RESET':      '\033[0m',
    'BOLD':       '\033[1m',
    'DIM':        '\033[2m',
}

# Umbrales máximos para calcular % de confianza
MAX_SPAM     = 200
MAX_PHISHING = 150


def confianza(spam_score: int, phishing_score: int, clasificacion: str) -> int:
    """
    Devuelve un porcentaje de confianza (0-100) en la decisión tomada.
    """
    if clasificacion == 'PHISHING':
        return min(100, int(phishing_score / MAX_PHISHING * 100))
    if clasificacion == 'SPAM':
        return min(100, int(spam_score / MAX_SPAM * 100))
    if clasificacion == 'SOSPECHOSO':
        score = max(spam_score, phishing_score)
        return min(99, int(score / 15 * 60))
    # LEGITIMO: confianza inversa — cuanto más bajo el score, más seguro
    score = max(spam_score, phishing_score)
    return max(0, 100 - score * 10)


def barra(pct: int, width: int = 20) -> str:
    filled = int(pct / 100 * width)
    return '[' + '#' * filled + '-' * (width - filled) + ']'


def main():
    print()
    print(COLOR['BOLD'] + '  CLASIFICADOR DE SPAM Y PHISHING  -  version LOCAL' + COLOR['RESET'])
    print(COLOR['DIM']  + '  Algoritmos: BST + Diccionarios + Exploracion Recursiva' + COLOR['RESET'])
    print()

    #construir BSTs
    clf = EmailClassifier()

    #cargar emails
    emails = load_emails_from_folder(EMAILS_FOLDER)
    if not emails:
        print('[!] No se encontraron archivos .txt en:', EMAILS_FOLDER)
        return

    print(f'  Emails encontrados: {len(emails)}')
    print()

    #cabecera tabla
    col1, col2, col3, col4 = 30, 13, 7, 28
    sep = '-' * (col1 + col2 + col3 + col4 + 6)
    print(COLOR['BOLD']
          + f'  {"ARCHIVO":<{col1}} {"CLASIFICACION":<{col2}} {"CONF.":<{col3}} {"CONFIANZA":<{col4}}'
          + COLOR['RESET'])
    print('  ' + sep)

    results = []
    for email in emails:
        result = clf.analyze(email)
        label  = result['classification']
        pct    = confianza(result['spam_score'], result['phishing_score'], label)
        c      = COLOR.get(label, '')
        rst    = COLOR['RESET']

        nombre = email['filename']
        bar    = barra(pct)

        print(f'  {nombre:<{col1}} '
              f'{c}{label:<{col2}}{rst} '
              f'{pct:>5}%  '
              f'{c}{bar}{rst}')

        results.append({**result, 'filename': nombre, 'confianza': pct})

    print('  ' + sep)
    print()

    #resumen por clasificacion
    conteos = {'LEGITIMO': 0, 'SOSPECHOSO': 0, 'SPAM': 0, 'PHISHING': 0}
    for r in results:
        conteos[r['classification']] += 1

    print(COLOR['BOLD'] + '  RESUMEN' + COLOR['RESET'])
    for label, cnt in conteos.items():
        if cnt > 0:
            c   = COLOR.get(label, '')
            rst = COLOR['RESET']
            print(f'    {c}{label:<12}{rst} {cnt} email(s)')
    print()

    #detalle de detecciones
    print(COLOR['BOLD'] + '  DETALLE DE PALABRAS DETECTADAS' + COLOR['RESET'])
    for r in results:
        c   = COLOR.get(r['classification'], '')
        rst = COLOR['RESET']
        print(f"\n  {r['filename']}  ->  {c}{r['classification']}{rst}")
        if r['spam_keywords_found']:
            print(f"    SPAM:     {r['spam_keywords_found']}")
        if r['phishing_keywords_found']:
            print(f"    PHISHING: {r['phishing_keywords_found']}")
        if r['suspicious_domains']:
            print(f"    DOMINIOS: {r['suspicious_domains']}")
        if not r['spam_keywords_found'] and not r['phishing_keywords_found']:
            print(f"    (sin palabras de alerta detectadas)")
    print()


if __name__ == '__main__':
    main()
