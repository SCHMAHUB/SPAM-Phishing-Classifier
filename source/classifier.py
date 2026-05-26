"""
classifier.py — Motor de clasificación Spam/Phishing

Combina dos estructuras de datos complementarias:

  1. Diccionario Python  >> búsqueda O(1) para frases/subcadenas exactas
  2. BST                 >> búsqueda O(log n) por token, recorrido ordenado,
                           exploración recursiva por categoría

Flujo de análisis de un email:
  texto >> normalización >> [Dict search + BST search + chequeo dominios]
       >> cálculo de puntuación >> clasificación final
"""

import re
from bst import BST
from dictionary import (
    SPAM_KEYWORDS, PHISHING_KEYWORDS, PHISHING_DOMAINS, THRESHOLDS
)


# clasificador principal que combina busqueda en diccionario O(1) y BST O(log n) [spam_bst <> phishing_bst]
class EmailClassifier:

    def __init__(self):
        self.spam_bst     = BST()  #O(1)
        self.phishing_bst = BST()  #O(1)
        self._build_trees()  #O(n) n = total palabras clave

    # carga cada entrada del diccionario en los BSTs | separa fuentes de verdad de la estructura de busqueda
    def _build_trees(self):
        print("[*] Construyendo BST de SPAM      ...")  #O(1)
        for keyword, weight in SPAM_KEYWORDS.items():  #O(n_spam)
            self.spam_bst.insert(keyword, "spam", weight)  #O(log n)
        print(f"    OK {self.spam_bst.size} palabras cargadas en BST SPAM")  #O(1)

        print("[*] Construyendo BST de PHISHING  ...")  #O(1)
        for keyword, weight in PHISHING_KEYWORDS.items():  #O(n_phish)
            self.phishing_bst.insert(keyword, "phishing", weight)  #O(log n)
        print(f"    OK {self.phishing_bst.size} palabras cargadas en BST PHISHING\n")  #O(1)

    # La funcion '_normalize()' fue generada con IA, adaptandose a este codigo. Es solamente para detectar ofuscaciones homoglifas en el texto | La complejidad NO
    def _normalize(self, text: str) -> str:
        """Normaliza texto: minúsculas + reemplazo de homoglifos (0→o, 1→i, 3→e, 4→a, 5→s)."""
        text = text.lower()  #O(m) m = longitud del texto
        for char, rep in {'0': 'o', '1': 'i', '3': 'e', '4': 'a', '5': 's'}.items():  #O(1) — dict fijo de 5 entradas
            text = text.replace(char, rep)  #O(m)
        return text  #O(1)

    # La funcion '_extract_urls()' fue generada con IA, adaptandose a este codigo. Es solamente para extraer URLs del texto con expresion regular | La complejidad NO
    def _extract_urls(self, text: str) -> list:
        """Extrae URLs con expresión regular."""
        return re.findall(r'https?://[^\s]+', text)  #O(m) m = longitud del texto

    # busqueda en diccionario Python O(1) por entrada | detecta frases y subcadenas, devuelve lista de (keyword, weight)
    def _dict_search(self, text: str, keyword_dict: dict) -> list:
        found = []  #O(1)
        for keyword, weight in keyword_dict.items():  #O(n) n = tamaño del diccionario
            if keyword in text:  #O(m) m = longitud del texto
                found.append((keyword, weight))  #O(1)
        return found  #O(1)

    # busqueda en BST O(log n) por token | detecta palabras individuales, devuelve lista de BSTNode encontrados
    def _bst_search_tokens(self, tokens: list, bst: BST) -> list:
        seen  = set()  #O(1)
        found = []  #O(1)
        for token in tokens:  #O(t) t = numero de tokens
            if token not in seen:  #O(1)
                node = bst.search(token)  #O(log n)
                if node:  #O(1)
                    found.append(node)  #O(1)
                seen.add(token)  #O(1)
        return found  #O(1)

    # analisis completo de un email | dict search + BST search + dominios >> puntuacion >> clasificacion final
    def analyze(self, email: dict) -> dict:
        subject = email.get('subject', '')  #O(1)
        sender  = email.get('sender', '')  #O(1)
        body    = email.get('body', '')  #O(1)

        full_text  = f"{subject} {body}"  #O(m)
        normalized = self._normalize(full_text)  #O(m)
        tokens     = re.findall(r'\b\w+\b', normalized)  #O(m)

        # busqueda en diccionario >> frases y subcadenas exactas
        spam_dict_hits     = self._dict_search(normalized, SPAM_KEYWORDS)  #O(n_spam * m)
        phishing_dict_hits = self._dict_search(normalized, PHISHING_KEYWORDS)  #O(n_phish * m)

        # busqueda en BST >> tokens individuales O(log n)
        spam_bst_hits     = self._bst_search_tokens(tokens, self.spam_bst)  #O(t * log n_spam)
        phishing_bst_hits = self._bst_search_tokens(tokens, self.phishing_bst)  #O(t * log n_phish)

        # verificacion de dominios sospechosos
        urls         = self._extract_urls(full_text)  #O(m)
        domain_hits  = []  #O(1)
        for url in urls:  #O(u) u = numero de URLs
            domain_hits.extend(self._dict_search(url.lower(), PHISHING_DOMAINS))  #O(n_dom)

        # puntuacion >> dict hits + BST hits sin doble conteo
        dict_spam_kws = {k for k, _ in spam_dict_hits}  #O(n_spam)
        spam_score    = sum(w for _, w in spam_dict_hits)  #O(n_spam)
        for node in spam_bst_hits:  #O(hits_spam)
            if node.keyword not in dict_spam_kws:  #O(1)
                spam_score += node.weight  #O(1)

        dict_phishing_kws = {k for k, _ in phishing_dict_hits}  #O(n_phish)
        phishing_score    = sum(w for _, w in phishing_dict_hits)  #O(n_phish)
        for node in phishing_bst_hits:  #O(hits_phish)
            if node.keyword not in dict_phishing_kws:  #O(1)
                phishing_score += node.weight  #O(1)
        phishing_score += sum(w for _, w in domain_hits)  #O(u)

        # clasificacion final
        classification = self._classify(spam_score, phishing_score)  #O(1)

        return {  #O(1)
            'classification':          classification,
            'spam_score':              spam_score,
            'phishing_score':          phishing_score,
            'spam_keywords_found':     [k for k, _ in spam_dict_hits],
            'phishing_keywords_found': [k for k, _ in phishing_dict_hits],
            'bst_spam_hits':           [n.keyword for n in spam_bst_hits],
            'bst_phishing_hits':       [n.keyword for n in phishing_bst_hits],
            'suspicious_domains':      [k for k, _ in domain_hits],
            'urls_found':              urls,
        }

    # reglas de clasificacion usando umbrales del diccionario | phishing >> spam >> sospechoso >> legitimo
    def _classify(self, spam_score: int, phishing_score: int) -> str:
        if phishing_score >= THRESHOLDS['phishing_score']:  #O(1)
            return 'PHISHING'  #O(1)
        if spam_score >= THRESHOLDS['spam_score']:  #O(1)
            return 'SPAM'  #O(1)
        if spam_score >= THRESHOLDS['suspicious_score'] or \
           phishing_score >= THRESHOLDS['suspicious_score']:  #O(1)
            return 'SOSPECHOSO'  #O(1)
        return 'LEGITIMO'  #O(1)

    # La funcion 'show_bst_traversal()' fue generada con IA, adaptandose a este codigo. Es solamente para realizar un display ordenado de los keywords de ambos BSTs | La complejidad NO
    def show_bst_traversal(self):
        """Recorrido inorder completo de ambos BSTs (muestra keywords ordenadas)."""
        print("\n" + "─" * 62)  #O(1)
        print(" Recorrido BST SPAM — inorder (todas las palabras en orden)")  #O(1)
        print("─" * 62)  #O(1)
        for node in self.spam_bst.inorder_traversal():  #O(n_spam)
            print(f"  {node.keyword:<40s}  peso={node.weight}")  #O(k) k = longitud keyword

        print("\n" + "─" * 62)  #O(1)
        print(" Recorrido BST PHISHING — inorder")  #O(1)
        print("─" * 62)  #O(1)
        for node in self.phishing_bst.inorder_traversal():  #O(n_phish)
            print(f"  {node.keyword:<40s}  peso={node.weight}")  #O(k)

    # La funcion 'show_bst_structure()' fue generada con IA, adaptandose a este codigo. Es solamente para realizar un display de la estructura grafica de los BSTs | La complejidad NO
    def show_bst_structure(self):
        """Muestra la estructura gráfica de los BSTs."""
        print("\n" + "─" * 62)  #O(1)
        print(" Estructura BST SPAM")  #O(1)
        print("─" * 62)  #O(1)
        self.spam_bst.display_tree()  #O(n_spam)
        print("\n" + "─" * 62)  #O(1)
        print(" Estructura BST PHISHING")  #O(1)
        print("─" * 62)  #O(1)
        self.phishing_bst.display_tree()  #O(n_phish)

    # exploracion recursiva completa del arbol filtrando por categoria | recorre todos los nodos sin poda
    def explore_by_category(self, category: str):
        bst   = self.spam_bst if category == 'spam' else self.phishing_bst  #O(1)
        nodes = bst.get_nodes_by_category(category)  #O(n) n = total nodos del arbol
        print(f"\n Nodos '{category}' (exploración recursiva) — {len(nodes)} nodo(s)")  #O(1)
        print("─" * 62)  #O(1)
        for node in nodes:  #O(n)
            print(f"  {node.keyword:<40s}  peso={node.weight}")  #O(k)