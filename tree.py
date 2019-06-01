# Класс дерева
class Tree:
    def __init__(self, root_data=None, mtx=None):
        self.edges = {0: None}
        self.vertexes = {}
        if root_data:
            root = self._Node(root_data)
            root.id = 0
            self.vertexes[0] = root
        else:
            mtx_v = mtx[0]
            mtx_ed = self.mtx_ed = mtx[1]
            for ind, v in enumerate(mtx_v):
                vert = self._Node(v)
                vert.id = ind
                self.vertexes[ind] = vert
            for line_ind in range(len(mtx_ed)):
                for el_ind in range(line_ind, len(mtx_ed[line_ind])):
                    if mtx_ed[line_ind][el_ind] != 0:
                        v1 = self.vertexes[line_ind]
                        v2 = self.vertexes[el_ind]
                        edge = self._Edge(v1, v2, mtx_ed[line_ind][el_ind])
                        self.edges[list(self.edges.keys())[-1] + 1] = edge
                        v1.add_child(v2)
                        v2.add_child(v1)

    # Подкласс ребра
    class _Edge:
        def __init__(self, vertex_1, vertex_2, weight):
            self.vertex_1 = vertex_1
            self.vertex_2 = vertex_2
            self.weight = weight
            self.id = None

        # Функция получения основной информации о ребре
        def get_info(self):
            return 'Edge #{num}:\n' \
                   'Weight: {weight}\n' \
                   'Connect {v1} and {v2}\n'.format(
                num=self.id,
                weight=self.weight,
                v1=self.vertex_1.id,
                v2=self.vertex_2.id)

    # Подкласс вершины
    class _Node:
        def __init__(self, data):
            self.id = None
            self.data = data
            self.children = []

        # Функция добавления смежной вершины
        def add_child(self, obj):
            self.children.append(obj)

        # Функция получения основной информации о вершине
        def get_info(self):
            return 'Vertex #{num}:\n' \
                   'Data: {data}\n' \
                   'Connected: {neighbours}\n'.format(
                num=self.id,
                data=self.data,
                neighbours=str([child.id for child in self.children])
            )

    # Функция добавления ребра
    def add_edge(self, vertex_1, vertex_2, weight=0):
        try:
            v1 = self.vertexes[vertex_1]
            v2 = self.vertexes[vertex_2]
            edge = self._Edge(v1, v2, weight)
            self.edges[list(self.edges.keys())[-1] + 1] = edge
            v1.add_child(v2)
            v2.add_child(v1)
        except:
            print('Enter correct vertexes')

    # Функция добавления вершины
    def add_vertex(self, data):
        vertex = self._Node(data)
        vertex.id = list(self.vertexes.keys())[-1] + 1
        self.vertexes[list(self.vertexes.keys())[-1] + 1] = vertex

    # Функция получения веса ребра по номерам смежных вершин
    def get_egde_weight(self, v1, v2):
        for ind in list(self.edges.keys())[1:]:
            if (self.edges[ind].vertex_1.id == v1 and self.edges[ind].vertex_2.id == v2) or (
                    self.edges[ind].vertex_1.id == v2 and self.edges[ind].vertex_2.id == v1):
                return self.edges[ind].weight
        return None

    # Функция преобразования нулей в матрице в очень большое число
    @staticmethod
    def get_inf_path(mtx):
        import copy
        temp = copy.copy(mtx)
        print(len(temp))
        for line_ind in range(len(temp)):
            for el_ind in range(len(temp)):
                if temp[line_ind][el_ind] == 0:
                    temp[line_ind][el_ind] = 999999
        return temp

    # Функция возращающая матрицу кратчайших путей между всеми вершинами
    def get_min_path(self):
        import copy
        d = copy.copy(self.get_inf_path(self.mtx_ed))
        for k in range(0, len(d)):
            for i in range(0, len(d)):
                for j in range(0, len(d)):
                    if i != j:
                        d[i][j] = min(d[i][j], d[i][k] + d[k][j])
        return d

    # Функция вывода информации о всех вершинах
    def print_vertexes(self):
        print('Vertexes info:\n\n')
        for key in self.vertexes.keys():
            print(self.vertexes[key].get_info())

    # Функция вывода информации о всех ребрах
    def print_edges(self):
        print('Edges info:\n\n')
        for key in list(self.edges.keys())[1:]:
            print(self.edges[key].get_info())

    # Функция вывода информации о всех ребрах в вид матрицы
    def print_edges_matrix(self):
        print('Edges info (mtx):\n')
        edges_mtx = [['-' for key in list(self.vertexes.keys())] for _ in
                     list(self.vertexes.keys())]
        for key in list(self.edges.keys())[1:]:
            v1 = self.edges[key].vertex_1.id
            v2 = self.edges[key].vertex_2.id
            edges_mtx[v1][v2] = self.edges[key].weight
            edges_mtx[v2][v1] = self.edges[key].weight
        print(end='\t')
        for key in self.vertexes.keys():
            print(key, end='\t')
        print()
        for ind, str_mtx in enumerate(edges_mtx):
            print(ind, end='\t')
            for el in str_mtx:
                print(el, end='\t')
            print()
        print()

    # Функция вывода информации о всех вершинах в виде матрицы
    def print_vertexes_matrix(self):
        print('Vertexes info (mtx):\n')
        for key in self.vertexes.keys():
            v = self.vertexes[key]
            print(v.id, '-', v.data)
        print()

    # Функция вывода основной информации о дереве
    def print_tree(self):
        self.print_vertexes()
        self.print_edges()

    # Функция вывода основной информации о дереве в виде матриц
    def print_tree_matrix(self):
        self.print_vertexes_matrix()
        self.print_edges_matrix()

