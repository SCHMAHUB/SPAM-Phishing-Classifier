"""
main.py — Clasificador de Spam y Phishing (versión PRODUCCIÓN)
==============================================================
Se conecta a Gmail via IMAP, descarga los emails de la bandeja de entrada
y muestra automáticamente la clasificación y confianza de cada uno.

Antes de ejecutar:
    Edita config.py con tu email y contraseña de aplicación de Gmail.

Uso:
    python main.py

Requiere Python 3.8+. Sin dependencias externas (solo librería estándar).
"""

import sys #O(1)
from classifier import EmailClassifier #O(1)
from email_connector import GmailConnector #O(1)
from config import EMAIL_CONFIG #O(1)

# Colores ANSI para formateo de salida en consola | Creación dict: O(c) donde c son los colores
COLOR = {
    'LEGITIMO':   '\033[92m', #O(1)
    'SOSPECHOSO': '\033[93m', #O(1)
    'SPAM':       '\033[91m', #O(1)
    'PHISHING':   '\033[95m', #O(1)
    'RESET':      '\033[0m',  #O(1)
    'BOLD':       '\033[1m',  #O(1)
    'DIM':        '\033[2m',  #O(1)
    'RED':        '\033[91m', #O(1)
}

# Constantes de control
MAX_SPAM     = 200 #O(1)
MAX_PHISHING = 150 #O(1)

def confianza(spam_score: int, phishing_score: int, clasificacion: str) -> int:
    """Calcula porcentaje de confianza (0-100) en la clasificación."""
    if clasificacion == 'PHISHING': #O(1)
        return min(100, int(phishing_score / MAX_PHISHING * 100)) #O(1) operaciones aritméticas y cast
    if clasificacion == 'SPAM': #O(1)
        return min(100, int(spam_score / MAX_SPAM * 100)) #O(1)
    if clasificacion == 'SOSPECHOSO': #O(1)
        score = max(spam_score, phishing_score) #O(1)
        return min(99, int(score / 15 * 60)) #O(1)
    
    # En caso de LEGITIMO
    score = max(spam_score, phishing_score) #O(1)
    return max(0, 100 - score * 10) #O(1)


# Genera un string de barra de progreso visual
def barra(pct: int, width: int = 20) -> str:
    filled = int(pct / 100 * width) #O(1)
    return '[' + '#' * filled + '-' * (width - filled) + ']' #O(width) complejidad proporcional a la longitud de la cadena 'width'


# Validación inicial de parámetros en config
def check_config() -> bool:
    if EMAIL_CONFIG['email'] == 'tu_correo@gmail.com': #O(1) búsqueda en dict
        print() #O(1)
        print(COLOR['RED'] + '[!] Configura tus credenciales en config.py antes de ejecutar.' + COLOR['RESET']) #O(1)
        print('    → Cambia "email" con tu direccion de Gmail.') #O(1)
        print('    → Cambia "password" con tu contrasena de aplicacion (16 caracteres).') #O(1)
        print('    → Instrucciones detalladas dentro de config.py') #O(1)
        print() #O(1)
        return False #O(1)
    return True #O(1)


def main():
    print() #O(1)
    print(COLOR['BOLD'] + '  CLASIFICADOR DE SPAM Y PHISHING  -  version PRODUCCION' + COLOR['RESET']) #O(1)
    print(COLOR['DIM']  + '  Algoritmos: BST + Diccionarios + Exploracion Recursiva  |  Gmail IMAP SSL' + COLOR['RESET']) #O(1)
    print() #O(1)

    if not check_config(): #O(1)
        sys.exit(1) #O(1)

    # Construir BSTs
    clf = EmailClassifier() #O(N * log N) asumiendo que inserta internamente los elementos de los diccionarios en los árboles

    # Conectar a Gmail
    print('[*] Conectando a Gmail...') #O(1)
    connector = GmailConnector(EMAIL_CONFIG) #O(1)

    # La conexión tiene latencia de red, pero algorítmicamente la tratamos como constante
    if not connector.connect(): #O(1)
        print('[!] No se pudo conectar. Revisa config.py y la seccion de ayuda en README.md') #O(1)
        sys.exit(1) #O(1)

    try:
        # Descargar emails
        emails = connector.fetch_emails() #O(E) donde E es el total de emails descargados
        if not emails: #O(1)
            print('[!] No se encontraron emails en el buzon.') #O(1)
            return #O(1)

        print(f'\n  Emails descargados: {len(emails)}') #O(1)
        print() #O(1)

        # Cabecera de tabla
        col1, col2, col3, col4 = 40, 13, 7, 28 #O(1)
        sep = '-' * (col1 + col2 + col3 + col4 + 6) #O(C) donde C es la longitud total de la línea de separación
        print(COLOR['BOLD']
              + f'  {"ASUNTO":<{col1}} {"CLASIFICACION":<{col2}} {"CONF.":<{col3}} {"CONFIANZA":<{col4}}'
              + COLOR['RESET']) #O(C) formateo
        print('  ' + sep) #O(C)

        results = [] #O(1)
        
        # Iteración sobre los correos obtenidos
        for email in emails: #O(E)
            # El tiempo de análisis depende de la cantidad de palabras del email (W) y los nodos del BST (K)
            result = clf.analyze(email) #O(W * log K) 
            label  = result['classification'] #O(1) acceso a dict
            pct    = confianza(result['spam_score'], result['phishing_score'], label) #O(1)
            c      = COLOR.get(label, '') #O(1)
            rst    = COLOR['RESET'] #O(1)

            # Acorte de strings (Slices) proporcionales a la longitud
            asunto = email['subject'][:38] + '..' if len(email['subject']) > 38 else email['subject'] #O(S) donde S es la long del string copiado
            bar    = barra(pct) #O(width)

            print(f'  {asunto:<{col1}} '
                  f'{c}{label:<{col2}}{rst} '
                  f'{pct:>5}%  '
                  f'{c}{bar}{rst}') #O(S + width) impresión formateada

            # Empaquetado en la lista de resultados
            results.append({**result, 'subject': email['subject'],
                             'sender': email['sender'], 'confianza': pct}) #O(K_result) tiempo amortizado de copia de dict (pequeño)

        print('  ' + sep) #O(C)
        print() #O(1)

        # Resumen
        conteos = {'LEGITIMO': 0, 'SOSPECHOSO': 0, 'SPAM': 0, 'PHISHING': 0} #O(1)
        for r in results: #O(E) se recorre nuevamente la lista completa
            conteos[r['classification']] += 1 #O(1)

        print(COLOR['BOLD'] + '  RESUMEN' + COLOR['RESET']) #O(1)
        for label, cnt in conteos.items(): #O(1) Bucle fijo a 4 iteraciones de las categorías
            if cnt > 0: #O(1)
                c   = COLOR.get(label, '') #O(1)
                rst = COLOR['RESET'] #O(1)
                print(f'    {c}{label:<12}{rst} {cnt} email(s)') #O(1)
        print() #O(1)

        # List Comprehension para filtrar, recorre toda la lista original
        alertas = [r for r in results if r['classification'] != 'LEGITIMO'] #O(E)
        
        # Detalle de alertas encontradas (solo emails no legítimos)
        if alertas: #O(1)
            print(COLOR['BOLD'] + '  ALERTAS DETECTADAS' + COLOR['RESET']) #O(1)
            for r in alertas: #O(A) donde A es el numero de alertas filtradas (peor caso O(E))
                c   = COLOR.get(r['classification'], '') #O(1)
                rst = COLOR['RESET'] #O(1)
                print(f"\n  Asunto: {r['subject'][:60]}") #O(S) slice
                print(f"  De:     {r['sender'][:60]}") #O(S)
                print(f"  Tipo:   {c}{r['classification']}{rst}") #O(1)
                if r['spam_keywords_found']: #O(1) evaluacion booleana de lista
                    print(f"  SPAM:     {r['spam_keywords_found'][:5]}") #O(K_spam) sublista
                if r['phishing_keywords_found']: #O(1)
                    print(f"  PHISHING: {r['phishing_keywords_found'][:5]}") #O(K_phish) sublista
                if r['suspicious_domains']: #O(1)
                    print(f"  DOMINIOS: {r['suspicious_domains']}") #O(1) imprime list str
            print() #O(1)

    finally:
        # Cierre seguro, asegurando desconexión sin importar excepciones previas
        connector.disconnect() #O(1)


if __name__ == '__main__': #O(1)
    main()