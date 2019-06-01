from collections import deque
import random, copy


# Функция алгоритма
def method(t1, t2_mtx, order=None, processors=None):

    new_vert_order = order
    pairs = create_pairs(new_vert_order, processors)
    kr = 0

    for e_ind in list(t1.edges.keys())[1:]:
        v1 = t1.edges[e_ind].vertex_1.id
        v2 = t1.edges[e_ind].vertex_2.id
        f = 0
        path_t = []
        for v in pairs:
            if f == 0:
                if v[0] == v1:
                    f = 1
                    path_t.append(v[1])
                    continue
                if v[0] == v2:
                    f = -1
                    path_t.append(v[1])
                    continue
            if f == 1:
                path_t.append(v[1])
                if v[0] == v2:
                    break
            if f == -1:
                path_t.append(v[1])
                if v[0] == v1:
                    break
        k_sum = 0
        for ind in range(len(path_t) - 1):
            k_sum += t2_mtx[path_t[ind]][path_t[ind + 1]]
        kr += t1.mtx_ed[v1][v2] * k_sum
    return kr


# поиск вершины с минимальной степенью
def min_power_vertex(tree, zero_sign=0, start_ind=0):
    min_vertex_index = None
    min_vertex_power = float('inf')

    for ind, vertex_connections in enumerate(tree, start_ind):
        vertex_neighbours = 0
        for connection in vertex_connections:
            if connection != zero_sign:
                vertex_neighbours += 1
        if vertex_neighbours < min_vertex_power:
            min_vertex_power = vertex_neighbours
            min_vertex_index = ind

    return min_vertex_index, min_vertex_power


# строительство структуры уровней смежности графа
def levels(tree, start=None, with_dict=False):
    levels = [float('inf')] * len(tree)
    levels_dict = dict()
    visited = set()
    level = 0
    levels_dict[level] = list()
    vert = random.randint(0, len(tree) - 1) if start is None else start
    levels_dict[level].append(vert)
    visited.add(vert)
    while float('inf') in levels:
        levels_dict[level+1] = list()
        for vert in levels_dict[level]:
            for neighbour, connection in enumerate(tree[vert]):
                if connection != 0 and neighbour not in visited:
                    levels_dict[level+1].append(neighbour)
                    visited.add(neighbour)
        for el in levels_dict[level]:
            levels[el] = level
        level += 1
    if not levels_dict[list(levels_dict.keys())[-1]]:
        del levels_dict[list(levels_dict.keys())[-1]]
    return (levels, levels_dict) if with_dict else levels


# номера вершин последнего уровня
def find_the_deepest_vertexes(levels_list):
    levels_with_indexes = [(ind, level) for ind, level in enumerate(levels_list)]
    levels_with_indexes.sort(key=lambda pair: pair[1], reverse=True)
    max_level = levels_with_indexes[0][1]
    last_level_indexes = []
    for (ind, level) in levels_with_indexes:
        if level != max_level:
            break
        last_level_indexes.append(ind)
    return max_level, last_level_indexes


def power_of_vertex(tree, vertex, null_symbol=0):
    power = 0
    for i in range(len(tree)):
        if (tree[vertex][i]) != null_symbol:
            power += 1
    return power


def extend_levels_2(levels_1, levels_2):
    processors = max(levels_2)
    levels = len(levels_1//processors)
    curr_level = 0
    for ind, level in enumerate(levels_1):
        if ind % levels == 0:
            levels_1[ind] = (curr_level + 1)*levels
            curr_level += 1
    return levels_1


def create_pairs(levels_1, levels_2):
    levels = len(levels_1)//len(levels_2)
    curr_level = -1
    pairs = list()
    for ind, vert_1 in enumerate(levels_1):
        if ind % levels == 0 and curr_level != len(levels_2)-1:
            curr_level+=1
        pairs.append((vert_1, levels_2[curr_level]))
    return pairs


def extend_levels(levels_list, v_count_2):
    space = v_count_2 - max(levels_list) - 1
    if space > 0:
        level_vertexes = create_vert_dict(levels_list)
        new_levels_list = copy.copy(levels_list)

        while max(new_levels_list) != v_count_2 - 1:
            vertexes = max_pair(level_vertexes)
            vertexes.pop(0)
            value_to_add = 1
            for ind in vertexes:
                new_levels_list[ind] += value_to_add
                value_to_add += 1
                if max(new_levels_list) == v_count_2 - 1:
                    break
            level_vertexes = create_vert_dict(new_levels_list)
        return new_levels_list

    if space < 0:
        level_vertexes = create_vert_dict(levels_list)
        new_levels_list = copy.copy(levels_list)

        while max(new_levels_list) != v_count_2 - 1:
            vertexes = min_pair(level_vertexes)
            if len(vertexes) != 1:
                vertexes.pop(0)
            value_to_add = 1
            for ind in vertexes:
                new_levels_list[ind] -= value_to_add
                # value_to_add += 1
                if max(new_levels_list) == v_count_2 - 1:
                    break
            level_vertexes = create_vert_dict(new_levels_list)
        return new_levels_list

    return levels_list


def create_vert_dict(levels_list):
    level_vertexes = {}
    for vert, level in enumerate(levels_list):
        if level_vertexes.get(level) is None:
            level_vertexes[level] = [vert]
        else:
            level_vertexes[level].append(vert)
    return level_vertexes


def create_count_dict(levels_dict):
    vert_count_dict = dict()
    for level, vertexes in levels_dict.items():
        vert_count_dict[level] = len(vertexes)
    return vert_count_dict


def average_list(levels_list):
    c = len(levels_list) // (max(levels_list)+1)
    new_levels_list = copy.copy(levels_list)
    for ind in range(max(levels_list)+1):
        count_dict = create_count_dict()
        # if count_dict[ind]<c:


def min_pair(levels_dict):
    vert_count_dict = create_count_dict(levels_dict)
    first = {0: vert_count_dict[0]}
    del vert_count_dict[0]
    local_min = min(vert_count_dict.values())
    vert_count_dict.update(first)
    sorted_x = sorted(vert_count_dict.items(), key=lambda kv: kv[0])

    only_pairs = [pair for pair in sorted_x if pair[1] <= local_min]
    return copy.copy(levels_dict.get(only_pairs[-1][0]))


def max_pair(levels_dict):
    vert_count_dict = create_count_dict(levels_dict)
    sorted_x = sorted(vert_count_dict.items(), key=lambda kv: kv[0])
    only_pairs = [pair for pair in sorted_x if pair[1] > 1]
    return copy.copy(levels_dict.get(only_pairs[-1][0]))


def make_components(tree, vertexes):
    components = list()
    used = set()
    ind = 0
    for vert in vertexes:
        isAdded = False
        if ind != 0 and vert in components[ind-1]:
            ind -= 1
        if vert not in used:
            components.append(list())
            components[ind].append(vert)
            isAdded = True
            used.add(vert)
        for vert_2 in vertexes:
            if tree[vert][vert_2] != 0 and vert_2 not in used:
                components[ind].append(vert_2)
                isAdded = True
                used.add(vert_2)
        if isAdded:
            ind += 1
    new_components = [comp for comp in components if comp != []]
    return new_components


def vertex_power(tree, vert):
    power = 0
    for connection in tree[vert]:
        if connection != 0:
            power += 1
    return power


def get_new_levels_structure(graph, vert):
    tree_levels, levels_dict = levels(graph, start=vert, with_dict=True)
    max_level, ll_vertexes = max(tree_levels), levels_dict[max(tree_levels)]
    components = make_components(graph, ll_vertexes)

    vss = [min(vs, key=lambda v: vertex_power(graph, v)) for vs in components]
    return max_level, vss, tree_levels


def find_pseudo_with_levels(input_graph, repeat_flag_max=5):
    graph = input_graph[1]
    vertexes = deque()
    vertexes.append(min_power_vertex(graph)[0])
    best_levels, best_max_level, best_start_vert = None, 0, 0
    repeat_flag = 0
    used_start_vertexes = set()

    while len(vertexes) != 0 and repeat_flag < repeat_flag_max:
        vert = vertexes.popleft()
        max_level, vss, tree_levels = get_new_levels_structure(graph, vert)
        used_start_vertexes.add(vert)
        for vs in vss:
            if vs not in used_start_vertexes:
                vertexes.append(vs)
        if max_level > best_max_level:
            best_max_level = max_level
            best_levels = tree_levels
            best_start_vert = vert
            repeat_flag = 0
        else:
            repeat_flag += 1

    vertexes_and_levels = [(v, l) for v, l in enumerate(best_levels)]
    vertexes_and_levels.sort(key=lambda x: x[1])
    return best_start_vert, [pair[0] for pair in vertexes_and_levels]


def matrix_exporter(file):
    f = open(file,'r+')
    firstLine = True
    matrix = None
    size = 0
    for line in f.readlines():
        if line[0] != '%':
            if firstLine:
                size = int(line.split(' ')[0])
                matrix = [[0 for _ in range(size)] for _ in range(size)]
                firstLine = False
            else:
                values = line.split(' ')
                matrix[int(values[0])-1][int(values[1])-1] = float(values[2])
                matrix[int(values[1])-1][int(values[0])-1] = float(values[2])
    min_edge = abs(min([min(line) for line in matrix])) + 1
    positive_matrix = [[0 if val == 0 else val + min_edge for val in line] for line in matrix]
    result_matrix = [[1 for _ in range(size)], positive_matrix]
    return result_matrix


if __name__ == '__main__':
    from constants import *

    find_pseudo_with_levels(MATRIX)