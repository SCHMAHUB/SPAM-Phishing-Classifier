# Clasificador de Spam y Phishing

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python&logoColor=white)
![Sin dependencias](https://img.shields.io/badge/dependencias-ninguna-brightgreen)
![Licencia](https://img.shields.io/badge/licencia-MIT-lightgrey)

Proyecto de la asignatura de **Algoritmos y Estructuras de Datos**.  
Clasificador de correos electrónicos que combina un **Árbol Binario de Búsqueda (BST)** con diccionarios Python para detectar spam y phishing — todo en local, sin librerías externas y sin conexión a internet.

---

## ¿Qué hace?

Lee archivos `.txt` que simulan correos electrónicos, analiza su contenido y los clasifica en cuatro categorías:

| Clasificación | Descripción |
|:---:|---|
| `LEGITIMO` | Correo normal, sin señales de alarma |
| `SOSPECHOSO` | Tiene algunas palabras sospechosas, pero no supera el umbral |
| `SPAM` | Publicidad agresiva o mensajes engañosos |
| `PHISHING` | Intento de suplantación de identidad o robo de datos |

El resultado se muestra en una tabla con el porcentaje de confianza de cada decisión.

---

## Cómo ejecutarlo

**Requisitos:** Python 3.8 o superior. Sin librerías externas.

```bash
cd project
python main.py
```

Y listo. El programa detecta automáticamente todos los `.txt` dentro de `emails/` y los analiza.

---

## Salida esperada

```
CLASIFICADOR DE SPAM Y PHISHING  -  version LOCAL
Algoritmos: BST + Diccionarios + Exploracion Recursiva

Emails encontrados: 3

  ARCHIVO                        CLASIFICACION  CONF.   CONFIANZA
  -----------------------------------------------------------------------
  email_legitimo.txt             LEGITIMO        100%   [####################]
  email_phishing.txt             PHISHING         83%   [################----]
  email_spam.txt                 SPAM             78%   [###############-----]
  -----------------------------------------------------------------------

  RESUMEN
    LEGITIMO      1 email(s)
    SPAM          1 email(s)
    PHISHING      1 email(s)

  DETALLE DE PALABRAS DETECTADAS
  email_spam.txt  ->  SPAM
    SPAM:     ['gratis', 'ganador', 'loteria', 'millonario', 'casino', ...]

  email_phishing.txt  ->  PHISHING
    PHISHING: ['su cuenta sera cerrada', 'actividad inusual', 'tarjeta de credito']
    DOMINIOS: ['paypa1.com']
```

---

## Estructuras de datos

### Árbol Binario de Búsqueda (BST)

Es la pieza central del proyecto. Se construyen **dos árboles independientes**: uno para spam y otro para phishing. Cada nodo guarda una palabra clave, su categoría y un peso de severidad del 1 al 10.

```
               "loteria" (9)
              /             \
        "gratis" (7)      "urgente" (8)
        /                 /         \
  "casino" (8)     "tiempo..." (8)  "viagra" (10)
```

El invariante del BST (`izquierda < raíz < derecha`) asegura búsquedas en **O(log n)** en lugar de recorrer todo.

Operaciones implementadas:

| Operación | Complejidad |
|---|:---:|
| Inserción recursiva | O(log n) |
| Búsqueda | O(log n) |
| Recorrido inorder | O(n) |
| Exploración por categoría | O(n) |

### Diccionarios Python

Los diccionarios se usan por dos razones: son la fuente de verdad de las palabras clave, y permiten buscar **frases compuestas** (subcadenas) que el BST no puede tokenizar directamente.

```python
SPAM_KEYWORDS = {
    "gratis":          7,
    "click aqui":      8,   # frase multi-palabra
    "tiempo limitado": 8,   # no se puede buscar como token individual
    ...
}
```

Búsqueda por clave exacta: **O(1)** (tabla hash interna de Python).

### ¿Por qué los dos juntos?

No se trata de elegir uno u otro — cada uno cubre lo que el otro no puede:

- El **diccionario** detecta frases como `"verify your account"` o `"su cuenta sera cerrada"` que el BST no puede manejar porque se tokenizarían en palabras sueltas que pierden el significado.
- El **BST** permite recorridos ordenados, exploración recursiva por categoría y demuestra las propiedades de la estructura de árbol.

---

## Algoritmos implementados

### Inserción recursiva

Compara la nueva palabra con el nodo actual y baja hacia la izquierda o la derecha hasta encontrar una posición libre. Si la palabra ya existe, actualiza el peso al máximo de los dos.

```python
def _insert_recursive(self, current, keyword, category, weight):
    if keyword < current.keyword:
        if current.left is None:
            current.left = BSTNode(keyword, category, weight)
            return True
        return self._insert_recursive(current.left, keyword, category, weight)
    elif keyword > current.keyword:
        if current.right is None:
            current.right = BSTNode(keyword, category, weight)
            return True
        return self._insert_recursive(current.right, keyword, category, weight)
    else:
        current.weight = max(current.weight, weight)  # duplicado
        return False
```

### Recorrido inorder

Visita los nodos en orden `izquierda → raíz → derecha`, lo que garantiza que las palabras aparezcan en **orden alfabético ascendente** — propiedad fundamental del BST.

```python
def _inorder_recursive(self, current, result):
    if current is not None:
        self._inorder_recursive(current.left, result)
        result.append(current)
        self._inorder_recursive(current.right, result)
```

### Exploración por categoría

A diferencia de `search()`, esta función **recorre el árbol completo** porque la categoría de un nodo no determina su posición (eso lo hace la palabra clave).

```python
def _explore_by_category(self, current, category, result):
    if current is None:
        return
    self._explore_by_category(current.left, category, result)
    if current.category == category:
        result.append(current)
    self._explore_by_category(current.right, category, result)
```

---

## Emails de prueba

En la carpeta `emails/` hay varios correos de ejemplo que cubren todas las categorías posibles: legítimos, sospechosos, spam y phishing. Se pueden usar directamente para probar el clasificador o como referencia para entender qué patrones activan cada categoría.

---

## Añadir tus propios emails

Crea un `.txt` en la carpeta `emails/` con este formato:

```
From: remitente@dominio.com
Subject: Asunto del correo

El cuerpo empieza después de la línea en blanco.
Puede tener varias líneas, URLs, lo que sea.
```

En la siguiente ejecución de `python main.py` aparecerá automáticamente en la tabla.

---

*Proyecto realizado con Python 3.8+ — sin dependencias externas.*
