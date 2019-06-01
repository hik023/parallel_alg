from constants import (
    GRAPH_5 as mtx1,
    GRAPH_5 as line)
from tree import Tree
from algorithms import *
import cProfile


mtx = matrix_exporter('matrixes/USAir97.mtx')
print('|G|={}, |H|={}'.format(len(mtx[0]), len(line[0])))

def alg_func():
    print('Algorithm:')
    results = list()
    for i in range(5):
        # print('+ : ', i, end='\t')
        t = Tree(mtx=mtx)
        t2 = Tree(mtx=line)
        new_order = find_pseudo_with_levels(mtx, repeat_flag_max=5)
        processors = find_pseudo_with_levels(line)[1]
        ext_new_order = extend_levels(new_order[1], len(line[1]))
        # print('order: ', new_order[1], end='\t')
        # print('ext_order: ', ext_new_order, end='\t')
        result = method(t, line[1], ext_new_order, processors)
        # print('K =', result)
        results.append(result)
    print('Max: {0}, Min: {1}, Avg: {2}'.format(max(results), min(results), sum(results)/len(results)))
    print(end='\n\n')


def rand_func():
    print('Rand:')
    results = list()
    for i in range(5):
        # print('- : ', i, end='\t')
        t = Tree(mtx=mtx)
        start_vertex = random.randint(0, len(mtx[0]) - 1)
        new_order = levels(mtx[1], start_vertex)
        ext_new_order = extend_levels(new_order, len(line[1]))
        processors = find_pseudo_with_levels(line)[1]
        # new_order = find_pseudo_with_levels(mtx)
        result = method(t, line[1],order=ext_new_order, processors=processors)
        # print('K =', result)
        results.append(result)
    print('Max: {0}, Min: {1}, Avg: {2}'.format(max(results), min(results),
                                                sum(results) / len(results)))

# alg_func()
# rand_func()
cProfile.run('alg_func()')
cProfile.run('rand_func()')
