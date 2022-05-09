from cgitb import text
from distutils import text_file
from os import system
import sys
from tabulate import tabulate

archivo = open("prueba.txt")
# archivo = open("naive_bayes.txt")
línea = archivo.readline()
texto = ""
while línea != '':
    texto = texto + línea
    línea = archivo.readline()

texto = texto.split('\n')
texto = [x.split(' - ') for x in texto]

categorias = [x[0] for x in texto]
categorias = ' '.join(categorias)
categorias = categorias.split(' ')
categorias = set(categorias)
categorias = list(categorias)
categorias = sorted(categorias)
trabajos = [x[0] for x in texto]

trabajo_categoria = dict(texto)
categoria_trabajos = {}
for x in texto:
    if(x[1] in categoria_trabajos):
        if(x[0] not in categoria_trabajos[x[1]]):
            categoria_trabajos[x[1]].append(x[0])
    else:
        categoria_trabajos[x[1]] = [x[0]]

mod_probabilistico = []
mod_probabilistico_debug = []
mod_probabilistico_categoria = {}

laplace_smoothing = 1
n1 = 2

def actualizar_probabilidades():
    mod_probabilistico.clear()
    mod_probabilistico_categoria.clear()

    for trabajo in trabajos:
        probabilidades = []
        for categoria in categorias:
            probabilidad = 0
            if(categoria in trabajo.split(' ')):
                probabilidad = 1
            probabilidades.append(probabilidad)
        if(trabajo_categoria[trabajo] in mod_probabilistico_categoria):
            if(trabajo not in mod_probabilistico_categoria[trabajo_categoria[trabajo]]):
                mod_probabilistico_categoria[trabajo_categoria[trabajo]
                                             ][trabajo] = probabilidades
        else:
            mod_probabilistico_categoria[trabajo_categoria[trabajo]] = {
                trabajo: probabilidades}

        mod_probabilistico.append(probabilidades)
        probabilidades_debug = probabilidades.copy()
        probabilidades_debug.append(trabajo)
        mod_probabilistico_debug.append(probabilidades_debug)


actualizar_probabilidades()
categorias_debug = categorias.copy()
categorias_debug.append('nombre')

# print("Probabilidades de cada categoria:")
# print(mod_probabilistico_debug)
# print(tabulate(mod_probabilistico_debug, headers=categorias_debug))

def agregar_trabajo(trabajo):
    if('sin clasificar' in categoria_trabajos):
        categoria_trabajos['sin clasificar'].append(trabajo)
    else:
        categoria_trabajos['sin clasificar'] = [trabajo]
    trabajo_categoria[trabajo] = 'sin clasificar'
    trabajos.append(trabajo)


def pCk(Ck):
    totalCategorias = 0
    for categoria in categoria_trabajos:
        if(categoria != 'sin clasificar'):
            totalCategorias = totalCategorias + \
                len(categoria_trabajos[categoria])
    return len(categoria_trabajos[Ck]) / totalCategorias


def pxiCk(xi, Ck):
    probabilidades = []
    for prob in mod_probabilistico_categoria[Ck]:
        probabilidades.append(mod_probabilistico_categoria[Ck][prob])

    # if(Ck == 'finance' and xi == 'junior data analyst'):
    #     print(tabulate(probabilidades, headers=categorias))

    ocurrencias = {}
    for i, categoria in enumerate(categorias):
        if(categoria not in ocurrencias):
            ocurrencias[categoria] = 0

    xDiv = xi.split(' ')
    for prob in probabilidades:
        for i, probabilidad in enumerate(prob):
            if(probabilidad == 1):
                ocurrencias[categorias[i]] = ocurrencias[categorias[i]] + 1

    for categoria in categorias:
        if(categoria in xDiv):
            ocurrencias[categoria] = (ocurrencias[categoria] + laplace_smoothing) / (
                len(categoria_trabajos[Ck]) + (laplace_smoothing*n1))
        else:
            ocurrencias[categoria] = ((len(categoria_trabajos[Ck]) - ocurrencias[categoria]) +
                                      laplace_smoothing) / (len(categoria_trabajos[Ck]) + (laplace_smoothing*n1))

    # if(Ck == 'finance' and xi == 'junior data analyst'):
    #     print(ocurrencias)

    final = 1
    for ocurrencia in ocurrencias:
        final = final * ocurrencias[ocurrencia]
        # if(Ck == 'finance' and xi == 'junior data analyst'):
        #     print("Final : ",final)

    return final


def pX(xi):
    final = 0
    for categoria in categoria_trabajos:
        if(categoria != 'sin clasificar'):
            final = final + pCk(categoria) * pxiCk(xi, categoria)

    return final


def bayes(ck, xi):
    return ((pxiCk(xi, ck) * pCk(ck)) / (pX(xi)))


def clasificar(trabajo):
    actualizar_probabilidades()

    probalidadMayor = 0
    categoriaFinal = ''
    for categoria in categoria_trabajos:
        if(categoria != 'sin clasificar'):
            bayesFinal = bayes(categoria, trabajo)
            print("| Probabilidad de que " + trabajo +
                  " sea categorizado como " + categoria + ": ", bayesFinal , '\t|')

            if(probalidadMayor < bayesFinal):
                categoriaFinal = categoria
                probalidadMayor = bayesFinal

    print('=========================================================================================================')
    print("|\t\t\tLa probabilidad mayor es: ", categoriaFinal, " con ", probalidadMayor,'\t\t\t|')
    print('=========================================================================================================')
    print("\nClasificando...")
    trabajo_categoria[trabajo] = categoriaFinal

    if(categoriaFinal in categoria_trabajos):
        categoria_trabajos[categoriaFinal].append(trabajo)
    else:
        categoria_trabajos[categoriaFinal] = [trabajo]

    if('sin clasificar' in categoria_trabajos):
        categoria_trabajos['sin clasificar'].remove(trabajo)
    
    if('sin clasificar' in categoria_trabajos):
        if(len(categoria_trabajos['sin clasificar']) == 0):
            del categoria_trabajos['sin clasificar']


def full_actions(trabajo):
    agregar_trabajo(trabajo)
    print('Categoria ' + trabajo + ': ',
          trabajo_categoria[trabajo])
    print()
    clasificar(trabajo)
    print()
    print('Categoria ' + trabajo + ': ', trabajo_categoria[trabajo])


def main():
    # full_actions('data analyst manager')
    # full_actions('junior data analyst')

    print('=================================================')
    print('|                 Categorizacion                |')
    print('=================================================')
    
    sort_orders = sorted(trabajo_categoria.items(), key=lambda x: x[1])
    print(tabulate(sort_orders,
          headers=['Trabajo', 'Categoria']), '\n')
    opt = -1;

    input('Presione enter para continuar...')
    
    while opt != 0:
        system('cls')
        print('=================================================')
        print('|            Clasificador de empleos            |')
        print('=================================================')
        print('|                    MENU                       |')
        print('=================================================')
        print('|    0. Salir del categorizador                 |')
        print('|    1. Categorizar un empleo                   |')
        print('|    2. Mostrar trabajos con categorias         |')
        print('=================================================')
        opt = int(input("Ingrese una opcion: "))        
        if opt == 1:
                system('cls')
                empleo = input("Ingrese el empleo que desea clasificar: ")
                system('cls')
                print('=================================================')
                print('|               PROBABILIDADES                  |')
                print('=================================================')
                full_actions(empleo)
                print('\n')
                input('Presione enter para continuar...')
        if opt == 2:
            system('cls')
            print('=================================================')
            print('|              Categorias actuales              |')
            print('=================================================')
            sort_orders = sorted(trabajo_categoria.items(), key=lambda x: x[1])
            print(tabulate(sort_orders,
                headers=['Trabajo', 'Categoria']), '\n')
            input('Presione enter para continuar...')




    system('cls')
    print('=================================================')
    print('|              Categorias finales               |')
    print('=================================================')
    sort_orders = sorted(trabajo_categoria.items(), key=lambda x: x[1])
    print(tabulate(sort_orders,
          headers=['Trabajo', 'Categoria']))
    print('\n')


main()