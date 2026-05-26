"""
Árbol Binario de Búsqueda (BST) - Estructura central del clasificador de Spam/Phishing.
Cada nodo almacena una palabra clave con su categoría y peso de peligrosidad con una tokenizacion de las palabras clave.
Implementa:
  - insert()                >> Insercion recursiva O(log n)
  - search()                >> Busqueda en diccionario BST [O(log n)]
  - inorder_traversal()     >> Recorrido BST completo (inorder){en orden}
  - get_nodes_by_category() >> Exploración recursiva por categoría
"""

# nodo del arbol BST que representa una palabra clave [nodo <> clave]
class BSTNode:
    def __init__(self, keyword: str, category: str, weight: int):
        self.keyword  = keyword.lower() #O(k)
        self.category = category   #O(1)
        self.weight   = weight  #O(1)
        self.left     = None  #O(1) 
        self.right    = None  #O(1) 

    def __repr__(self):
        return f"BSTNode('{self.keyword}', cat='{self.category}', w={self.weight})"  # O(k) crea longitud proporcional a keyword (k)


# clase de arbol binario de busqueda para almacenamiento + search palabra clave | nodo_izq < nodo_act < nodo_derech
class BST:
    def __init__(self):
        self.root  = None  #O(1)
        self._size = 0  #O(1)

    # insert de palabra clave en el BST ignorando duplicados | actualizando peso
    def insert(self, keyword: str, category: str, weight: int):
        keyword = keyword.lower()#O(k)
        if self.root is None:#O(1)
            self.root = BSTNode(keyword, category, weight)#O(k)
            self._size += 1#O(1)
        else:
            added = self._insert_recursive(self.root, keyword, category, weight)#O(log n)
            if added:#O(1)
                self._size += 1#O(1)

    # insercion recursiva, si se crea un nodo nuevo devuelve 'TRUE'
    def _insert_recursive(self, current: BSTNode, keyword: str,
                           category: str, weight: int) -> bool:
        if keyword < current.keyword:#O(k)
            if current.left is None:#O(1)
                current.left = BSTNode(keyword, category, weight)#O(k)
                return True #O(1)
            return self._insert_recursive(current.left, keyword, category, weight)#O(log n)
        elif keyword > current.keyword:#O(k)
            if current.right is None:#O(1)
                current.right = BSTNode(keyword, category, weight)#O(k)
                return True#O(1)
            return self._insert_recursive(current.right, keyword, category, weight)#O(log n)
        else:
            # palabra clave ya existe >> conservar el mayor peso
            current.weight = max(current.weight, weight)#O(1)
            return False #O(1)


    # busqueda en BST, devuelve el BSTNode si se encuentra y 'None' en caso contrario
    def search(self, keyword: str):
        return self._search_recursive(self.root, keyword.lower())#{O(k + log n) — O(k) [por lower()] + O(log n) [por la búsqueda]}

    def _search_recursive(self, current, keyword: str):
        if current is None:#O(1)
            return None  #O(1)
        if keyword == current.keyword:#O(k)
            return current#O(1)
        elif keyword < current.keyword: #O(k)
            return self._search_recursive(current.left, keyword)#O(log n)
        else:
            return self._search_recursive(current.right, keyword)#O(log n)

    # recorrido BST completo en el orden {izq. >> root >> derecha} devuelve lista ordenada de todos los nodos generados
    def inorder_traversal(self) -> list:
        result = []#O(1)
        self._inorder_recursive(self.root, result)#O(n)
        return result  #O(1)

    # recursividad 'inorder'
    def _inorder_recursive(self, current, result: list):
        if current is not None: #O(1)
            self._inorder_recursive(current.left, result) #O(n_izq) 
            result.append(current) #O(1)
            self._inorder_recursive(current.right, result)#O(n_der)


    # recursividad completa del arbol filtrando por categoria (recorre todos los nodos)
    def get_nodes_by_category(self, category: str) -> list:
        result = []#O(1)
        self._explore_by_category(self.root, category.lower(), result)#O(n)
        return result #O(1)

    def _explore_by_category(self, current, category: str, result: list):
        if current is None:#O(1)
            return#O(1)
        self._explore_by_category(current.left, category, result) #O(n_izq)
        if current.category == category:#O(1)
            result.append(current)#O(1)
        self._explore_by_category(current.right, category, result)#O(n_der)


    @property
    def size(self) -> int:
        return self._size #O(1)

    # La funcion 'display_tree()' fue generada con IA, adaptandose a este codigo. Es solamente para realizar un display de la informacion del arbol | La complejidad NO
    def display_tree(self, node=None, level: int = 0, prefix: str = "Root: "):
        """Muestra la estructura del árbol en consola (para depuración/presentación)."""
        if node is None and level == 0: #O(1)
            node = self.root#O(1)
        if node is not None:  #O(1)
            print(" " * (level * 4) + prefix +
                  f"{node.keyword}  [{node.category}, peso={node.weight}]")#O(level + k)
            if node.left is not None or node.right is not None:#O(1)
                left_label  = "L── "  #O(1)
                right_label = "R── " #O(1)
                if node.left: #O(1)
                    self.display_tree(node.left,  level + 1, left_label)#O(n_izq)
                else:
                    print(" " * ((level + 1) * 4) + left_label + "(vacío)")#O(level)
                if node.right:#O(1)
                    self.display_tree(node.right, level + 1, right_label)#O(n_der)
                else:
                    print(" " * ((level + 1) * 4) + right_label + "(vacío)")#O(level)
