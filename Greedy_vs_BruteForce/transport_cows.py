from ps1_partition import get_partitions
import time

#================================
# Part A: Transporting Space Cows
#================================

def load_cows(filename):
    """
    Read the contents of the given file.  Assumes the file contents contain
    data in the form of comma-separated cow name, weight pairs, and return a
    dictionary containing cow names as keys and corresponding weights as values.

    Parameters:
    filename - the name of the data file as a string

    Returns:
    a dictionary of cow name (string), weight (int) pairs
    """

    cow_dict = dict()

    f = open(filename, 'r')
    
    for line in f:
        line_data = line.split(',')
        cow_dict[line_data[0]] = int(line_data[1])
    return cow_dict

# Problem 1
def greedy_cow_transport(cows,limit=10):
    
    def arma_viaje(animales, limit):
        viaje = []
        peso = 0
    
        
        for vaca in animales:
            if (peso + vaca[1]) <= limit:
                viaje.append(vaca[0])
                peso += vaca[1]
        
        return viaje

    resultado = []
    
    lista = [(k, v) for k, v in cows.items()]
    
    animales = sorted(lista, key=lambda x:  x[1], reverse=True)
    
    while len(animales) > 0:
        viaje = arma_viaje(animales,limit)
        resultado.append(viaje)
        for animal in animales.copy():
            if (animal[0] in viaje):
                animales.remove(animal)
            
    return resultado


# Problem 2
def brute_force_cow_transport(cows,limit=10):

    resultado = []
    
    partitions = [v for v in get_partitions(cows)]
    sp = sorted(partitions, key=len)
    
    for item in sp:
        v = []
        for trip in item:
            peso = 0
            for cow in trip:
                peso += cows.get(cow)
            v.append(peso)
            
        if all([val <= limit for val in v]):
            resultado = item
            break
        
    return resultado    


#================================
# Compare both strategies
#================================

cows = load_cows("./ps1_cow_data.txt")
print(cows)
start = time.time()
print(greedy_cow_transport(cows,limit=10))
end = time.time()
print(end - start)
start = time.time()
print(brute_force_cow_transport(cows,limit=10))
end = time.time()
print(end - start)
