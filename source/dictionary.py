"""
dictionary.py — Diccionarios de palabras clave

proporciona los diccionarios Python (búsqueda O(1) por clave exacta)
que se usan para poblar los BSTs del clasificador.

estructura: { "palabra_clave": peso_severidad (1-10) }

Archivo completo generado por IA -> objetivo: tener variedad de parametros de clasificación
"""

# ── Palabras clave de SPAM ─────────────────────────────────────────────────────
SPAM_KEYWORDS: dict = {
    # Premios y sorteos
    "gratis":            7,
    "free":              7,
    "ganador":           9,
    "winner":            9,
    "premio":            8,
    "prize":             8,
    "loteria":           9,
    "lottery":           9,
    "sorteo":            8,

    # Ofertas y descuentos
    "oferta":            6,
    "offer":             6,
    "descuento":         5,
    "discount":          5,
    "promocion":         6,
    "promotion":         6,
    "exclusivo":         5,
    "exclusive":         5,
    "100%":              6,

    # Llamadas agresivas de urgencia
    "click aqui":        8,
    "click here":        8,
    "haga clic":         7,
    "compra ahora":      7,
    "buy now":           7,
    "actua ya":          8,
    "act now":           8,
    "tiempo limitado":   8,
    "limited time":      8,

    # Dinero y negocios dudosos
    "dinero":            6,
    "money":             6,
    "ingresos":          6,
    "income":            6,
    "millonario":        9,
    "millionaire":       9,
    "guaranteed":        8,
    "garantizado":       8,
    "risk free":         8,
    "sin riesgo":        8,
    "no cost":           7,
    "sin costo":         7,

    # Productos ilegales y spam farmacéutico
    "viagra":           10,
    "casino":            7,
    "pharma":            7,

    # Metadatos spam
    "unsubscribe":       3,
}

# ── Palabras clave de PHISHING ─────────────────────────────────────────────────
PHISHING_KEYWORDS: dict = {
    # Verificación de identidad y cuenta
    "verify your account":       10,
    "verifica tu cuenta":        10,
    "confirm your identity":     10,
    "confirma tu identidad":     10,
    "update your information":    9,
    "actualiza tu informacion":   9,
    "enter your details":         9,
    "ingresa tus datos":          9,

    # Amenazas y urgencia
    "account locked":            10,
    "cuenta bloqueada":          10,
    "suspended":                  9,
    "suspendida":                 9,
    "your account will be closed": 10,
    "su cuenta sera cerrada":    10,
    "unusual activity":           9,
    "actividad inusual":          9,
    "urgent action required":    10,
    "accion urgente requerida":  10,
    "security alert":             9,
    "alerta de seguridad":        9,

    # Datos sensibles solicitados
    "password":                   8,
    "contraseña":                 8,
    "credit card":                9,
    "tarjeta de credito":         9,
    "ssn":                       10,
    "social security":           10,

    # Suplantación de marcas
    "paypal":                     7,
    "amazon":                     5,
    "apple":                      5,
    "microsoft":                  5,
    "netflix":                    5,
    "banco":                      6,
    "bank":                       6,

    # Acceso y login
    "login":                      7,
    "iniciar sesion":             7,

    # URLs sospechosas
    "click the link":             8,
    "haga click en el enlace":    8,
    "bit.ly":                     8,
    "tinyurl":                    8,
}

# ── Dominios sospechosos conocidos ────────────────────────────────────────────
PHISHING_DOMAINS: dict = {
    "paypa1.com":               10,
    "amaz0n.com":               10,
    "g00gle.com":               10,
    "micros0ft.com":            10,
    "apple-id-verify.com":      10,
    "account-verify.net":        9,
    "secure-login.info":         9,
    "bankofamerica-verify.com": 10,
    "update-account.net":        9,
    "login-secure.com":          9,
    "paypal-verify-secure.com": 10,
    "netflix-billing.com":       9,
}

# ── Umbrales de clasificación ─────────────────────────────────────────────────
THRESHOLDS: dict = {
    "spam_score":       15,   # Puntuación mínima → SPAM
    "phishing_score":   12,   # Puntuación mínima → PHISHING
    "suspicious_score":  5,   # Puntuación mínima → SOSPECHOSO
}
