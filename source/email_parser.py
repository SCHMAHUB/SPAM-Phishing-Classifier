"""
email_parser.py — Parser de emails locales

Lee archivos .txt que simulan emails con el formato:

    From: remitente@dominio.com
    Subject: Asunto del email
    (línea en blanco)
    Cuerpo del mensaje...
"""

import os


def parse_email_file(filepath: str) -> dict:
    """
    parsea un archivo 'txt' con formato de email.

    Retorna:
        {
          'filename': str,
          'sender':   str,
          'subject':  str,
          'body':     str,
        }
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    sender  = ""
    subject = ""
    body    = ""

    lines      = content.split('\n')
    body_start = len(lines)  # por si no hay línea en blanco

    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped.lower().startswith('from:'):
            sender = stripped[5:].strip()
        elif stripped.lower().startswith('subject:'):
            subject = stripped[8:].strip()
        elif stripped == '' and i > 0:
            body_start = i + 1
            break

    body = '\n'.join(lines[body_start:]).strip()

    return {
        'filename': os.path.basename(filepath),
        'sender':   sender,
        'subject':  subject,
        'body':     body,
    }


def load_emails_from_folder(folder: str) -> list:
    """
    carga todos los archivos '.txt' de la carpeta especificada.
    los ordena alfabéticamente por nombre de archivo.

    retorna lista de dicts
    """
    if not os.path.isdir(folder):
        print(f"[!] Carpeta NO encontrada: '{folder}'")
        return []

    emails = []
    files  = sorted(f for f in os.listdir(folder) if f.endswith('.txt'))

    if not files:
        print(f"[!] NO se encontraron archivos .txt en '{folder}'")
        return []

    for filename in files:
        filepath = os.path.join(folder, filename)
        email    = parse_email_file(filepath)
        emails.append(email)

    return emails
