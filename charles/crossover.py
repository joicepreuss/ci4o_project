from random import randint, sample, uniform


def single_point_co(p1, p2):
    """Implementation of single point crossover.

    Args:
        p1 (Individual): First parent for crossover.
        p2 (Individual): Second parent for crossover.

    Returns:
        Individuals: Two offspring, resulting from the crossover.
    """
    co_point = randint(1, len(p1)-2)

    offspring1 = p1[:co_point] + p2[co_point:]
    offspring2 = p2[:co_point] + p1[co_point:]

    return offspring1, offspring2

def cycle_xo(p1,p2):
    """Implementation of cycle crossover.

    Args:
        p1 (Individual): First parent for crossover.
        p2 (Individual): Second parent for crossover.

    Returns:
        Individuals: Two offspring, resulting from the crossover.
    """
    # offspring placeholder
    offspring1 = [None]*len(p1)
    offspring2 = [None]*len(p2)

    # cycle
    while None in offspring1:
        index = offspring1.index(None)
        val1 = p1[index]
        val2 = p2[index]

        while val1 != val2:
            offspring1[index] = p1[index]
            offspring2[index] = p2[index]
            val2 = p2[index]
            index = p1.index(val2)

        # after cycle is done
        for element in offspring1:
            if element == None:
                index = offspring1.index(None)
                if offspring1[index] is None:
                    offspring1[index] = p2[index]
                    offspring2[index] = p1[index]

    return offspring1, offspring2

def pmx(p1,p2):
    '''
    Args:
        p1 (Individual): First parent for crossover.
        p2 (Individual): Second parent for crossover.

    Returns:
        Individuals: Two offspring, resulting from the crossover.
    '''
    xo_points = sample(range(len(p1)),2)
    xo_points.sort()
    def pmx_off(x,y):
        o = [None]*len(p1) #placeholder for offspring

        # copy the segment from the other parent
        o[xo_points[0]:xo_points[1]] = x[xo_points[0]:xo_points[1]] #copying the segment part of the first parent to the offspring
        z = set(y[xo_points[0]:xo_points[1]]) - set(x[xo_points[0]:xo_points[1]])

        # get the pair of the numbers from the other parent
        for number in z:
            temp = number
            index = y.index(x[y.index(temp)])
            while o[index] is not None:
                temp = index
                index = y.index(x[temp])
            o[index] = number
        while None in o :
            index = o.index(None)
            o[index] = y[index]
        return o
    offspring1, offspring2 = pmx_off(p1,p2), pmx_off(p2,p1)
    return offspring1, offspring2

def arithmetic_xo(p1,p2) :
    o1 = [None]*len(p1)
    o2 = [None]*len(p1)
    alpha = uniform(0,1)
    for i in range(len(p1)):
        o1[i] = p1[i]*alpha + p2[i]*(1-alpha)
        o2[i] = p1[i]*(1-alpha) + p2[i]*alpha
    return o1,o2


if __name__ == '__main__':
    p1, p2 = [9,8,4,5,6,7,1,2,3,10], [8,7,1,2,3,10,9,5,4,6]
    o1, o2 = cycle_xo(p1, p2)