# modulos de ordenamiento
def bubble_sort(lista):
    if len(lista) <= 1:
        return lista
    for i in range(len(lista)):
            for j in range(0, len(lista)-1-i):
                left = lista[j]
                right = lista [j+1]
                if left > right:
                    lista[j] = right
                    lista[j+1] = left
    return lista

def quick_sort (lista):
    if len(lista) <= 1:
        return lista
    pivote = lista[len(lista) // 2]
    left = [i for i in lista if i < pivote]
    middle = [j for j in lista if j == pivote]
    right = [k for k in lista if k > pivote]
    
    return quick_sort(left) + middle + quick_sort(right)


def merge_sort(lista):
    if len(lista) <= 1:
        return lista
    mid = lista[len(lista) // 2]
    left = [i for i in lista if i < mid]
    right = [k for k in lista if k > mid]
    
    return merge_sort(left) + merge_sort(right)
    
    
def  insertion_sort(lista):
    if len(lista) <= 1:
        return lista
    for i in range(1, len(lista)):
        pivote = lista[i]
        j = i - 1
        while j >= 0 and pivote < lista[j]:
            lista[j + 1] = lista[j]
            j -= 1
        lista[j + 1] = pivote
    return lista