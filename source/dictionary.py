"""
dictionary.py — Diccionarios de palabras clave (versión producción)
====================================================================
Mismo contenido que la versión local.
Contiene las estructuras de datos estáticas (Hash Tables) para la inicialización.
"""

# Diccionario de palabras clave de Spam | Creación del diccionario completo: O(N_spam)
SPAM_KEYWORDS: dict = {
    "gratis": 7, "free": 7, "ganador": 9, "winner": 9,        # Inserción individual en hash table: O(1)
    "premio": 8, "prize": 8, "loteria": 9, "lottery": 9, "sorteo": 8, #O(1)
    "oferta": 6, "offer": 6, "descuento": 5, "discount": 5,           #O(1)
    "promocion": 6, "promotion": 6, "exclusivo": 5, "exclusive": 5,   #O(1)
    "100%": 6,                                                        #O(1)
    "click aqui": 8, "click here": 8, "haga clic": 7,                 #O(1)
    "compra ahora": 7, "buy now": 7, "actua ya": 8, "act now": 8,     #O(1)
    "tiempo limitado": 8, "limited time": 8,                          #O(1)
    "dinero": 6, "money": 6, "ingresos": 6, "income": 6,              #O(1)
    "millonario": 9, "millionaire": 9,                                #O(1)
    "guaranteed": 8, "garantizado": 8,                                #O(1)
    "risk free": 8, "sin riesgo": 8, "no cost": 7, "sin costo": 7,    #O(1)
    "viagra": 10, "casino": 7, "pharma": 7,                           #O(1)
    "unsubscribe": 3,                                                 #O(1)
}

# Diccionario de palabras clave de Phishing | Creación completa: O(N_phishing)
PHISHING_KEYWORDS: dict = {
    "verify your account": 10, "verifica tu cuenta": 10,              #O(1)
    "confirm your identity": 10, "confirma tu identidad": 10,         #O(1)
    "update your information": 9, "actualiza tu informacion": 9,      #O(1)
    "enter your details": 9, "ingresa tus datos": 9,                  #O(1)
    "account locked": 10, "cuenta bloqueada": 10,                     #O(1)
    "suspended": 9, "suspendida": 9,                                  #O(1)
    "your account will be closed": 10, "su cuenta sera cerrada": 10,  #O(1)
    "unusual activity": 9, "actividad inusual": 9,                    #O(1)
    "urgent action required": 10, "accion urgente requerida": 10,     #O(1)
    "security alert": 9, "alerta de seguridad": 9,                    #O(1)
    "password": 8, "contraseña": 8,                                   #O(1)
    "credit card": 9, "tarjeta de credito": 9,                        #O(1)
    "ssn": 10, "social security": 10,                                 #O(1)
    "paypal": 7, "amazon": 5, "apple": 5, "microsoft": 5,             #O(1)
    "netflix": 5, "banco": 6, "bank": 6,                              #O(1)
    "login": 7, "iniciar sesion": 7,                                  #O(1)
    "click the link": 8, "haga click en el enlace": 8,                #O(1)
    "bit.ly": 8, "tinyurl": 8,                                        #O(1)
}

# Diccionario de dominios maliciosos conocidos | Creación completa: O(N_domains)
PHISHING_DOMAINS: dict = {
    "paypa1.com": 10, "amaz0n.com": 10, "g00gle.com": 10,             #O(1)
    "micros0ft.com": 10, "apple-id-verify.com": 10,                   #O(1)
    "account-verify.net": 9, "secure-login.info": 9,                  #O(1)
    "bankofamerica-verify.com": 10, "update-account.net": 9,          #O(1)
    "login-secure.com": 9, "paypal-verify-secure.com": 10,            #O(1)
    "netflix-billing.com": 9,                                         #O(1)
}

# Diccionario con umbrales límite de puntuación | Creación: O(1) al ser tamaño constante y diminuto
THRESHOLDS: dict = {
    "spam_score":       15, #O(1)
    "phishing_score":   12, #O(1)
    "suspicious_score":  5, #O(1)
}