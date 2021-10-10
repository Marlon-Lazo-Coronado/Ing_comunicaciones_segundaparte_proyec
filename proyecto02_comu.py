"""
Universidad de Costa Rica
IE0527 - Ingeniería de Comunicaciones
Proyecto 2: Codificación de canal
"""
import numpy as np

#Con esto se lee el archivo
fichero = open("mensaje.txt", "r")
#Se lee caracter por caracter
caracter = fichero.read(1)
bits_a_enviar = "" #arreglode bits a enviar
while caracter != "":
    
    #Transformamor a binario
    convertido_a_binario = ' '.join(format(ord(c), 'b') for c in caracter)
    #Completamos los 7 bits que a los que faltan
    #Con esto y todos los caracteres tienen la misma cantidad de bits
    while len(convertido_a_binario) <= 6:
        convertido_a_binario = "0" + convertido_a_binario
    #Concatenamos todos los caracteres
    bits_a_enviar = bits_a_enviar + convertido_a_binario
    caracter = fichero.read(1)
print("The Binary Representation is:", bits_a_enviar)

bits_a_enviar = bits_a_enviar.replace('1', ' 1 ')
bits_a_enviar = bits_a_enviar.replace('0', ' 0 ')
bits_a_enviar = bits_a_enviar.split()
for i in range(len(bits_a_enviar)):
    bits_a_enviar[i] = int(bits_a_enviar[i])


#======================LISTO EL ARREGLO DE BITS============================
#======================CODIFICACIÓN Y CANAL================================
def make_G(n,m_n): #Se crea la matriz G,  de 6x6
    I = np.identity(n)
    P = np.random.choice([0, 1], size=(n,m_n),p=[1./2, 1./2])
    G = np.hstack((I, P))
    print("La matriz G es:\n", G)
    return G, P
n = 6
G, P = make_G(n, 6)
def vectores_m(M, G, n): #Se crean los vectores u
    u = []
    m_i = []
    M_temp = []
    cont = 1
    for i in range(len(M)):
        m_i.append(M[i])
        if cont == (n):
            M_temp.append(m_i)
            m_i = []
            cont = 0
        cont = cont + 1
    
    for i in range(len(M_temp)):
        T = np.dot(M_temp[i],G)
        for i in range(len(T)):
            if (T[i] % 2) == 0:
                T[i] = 0
            else:
                T[i] = 1
        u.append(T.tolist())
    #print("Los vectores u son:\n", u)
    return u , M_temp
#y = [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1]
    
u, m = vectores_m(bits_a_enviar, G, n)
#Se crea la matriz H
def make_H(n,m_n, P):
    I = np.identity(n)
    H = np.vstack((P, I))
    print("La matriz H es:\n", H)
    return H
#Se crea los errores del canal, se tiene que se trabaja con una baja probabilidad de error.
def error(u):
    error = 0
    verdadero = 0
    for vec_i in range(len(u)):
        for bit_u in range(len(u[vec_i])):
            sorteo = np.random.randint(0,100)
            bit = u[vec_i][bit_u]
            #print("SORTEO:", sorteo)
            if sorteo == 7:
                if bit == 1:
                    bit = 0
                else:
                    bit = 1
                error = error + 1
            else:
                bit = bit
                verdadero = verdadero + 1
            u[vec_i][bit_u] = bit
    return u
            
u_error = error(u)
comp = np.array_equal(u_error, u)
H = make_H(6, 6, P)

def make_U(u, H):
    U = []
    for i in range(len(u)):
        T = np.dot(u[i],H)
        for i in range(len(T)):
            if (T[i] % 2) == 0:
                T[i] = 0
            else:
                T[i] = 1
        U.append(T)
    return U
#Aqui se hace una comparación con los vectores V
def comparison(u, m, n):
    comp = []
    for i in range(len(u)):
        temp = u[i]
        comp = np.array_equal(temp[:n], m[i])
        #print(comp)
    return comp

make_U(u, H)
comparison(u , m , n)


#Aqui los vectores u obtenidos pasan a ser string para entrar en la
#parte de decodificación.
def u_string(u):
    u_string = ''
    for vec in range(len(u)):
        for bit in range(len(u[vec])):
            u_string = u_string + str(int(u[vec][bit]))
    #print("EL STRING ES:", u_string)
    return u_string

bits_a_enviar1 = u_string(u)
#Aquí agarramos sólo los primeros 6 bits del vector u que tenemos,
#ya que el tamaño está de 12 bits.
def extrac_bits(bits_a_enviar1):
    cont = 0
    m_get = ''
    for bit in bits_a_enviar1:
        if cont < 6:
            m_get = m_get + bit
            cont = cont + 1
        else:
            if cont < 11:
                m_get = m_get 
                cont = cont + 1
            else:
                cont = 0
    return m_get
    
bits_a_enviar1 = extrac_bits(bits_a_enviar1) 

#==============================================================================

cont = 0

bits_recibidos = ""
print("¡Ya se escribió el mensaje!")
#se abre el archivo en modo escritura
file = open("PROYECTO_2.txt", "w")
#reconstruimos el caracter
for i in bits_a_enviar1:
    bits_recibidos = bits_recibidos + i
    cont = cont + 1
    if cont == 7:
        #print(bits_recibidos,"\n")
        numero_decimal = int(bits_recibidos, 2)
        letra = chr(numero_decimal)
        #print(letra)
        cont = 0
        bits_recibidos = ""
#=====================Aqui ya tenemos la letras (decodificacion)==============
#
#
#El sumidero
        file.write(letra)
file.close()
