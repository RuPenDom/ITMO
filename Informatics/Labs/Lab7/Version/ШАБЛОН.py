import sys, random, copy
from PIL import Image #Подключим необходимые библиотеки. 

IMAGE_PATH = "" #Путь до картинки, с которой будем работать, пустой если находится в той же директоррии, что и программа.
IMAGE_NAME = "pic" #Имя картинки.
IMAGE_TYPE = "jpg" #Тип картинки, крайне рекомендуется jpg.

original_image = Image.open(IMAGE_PATH + IMAGE_NAME + "." + IMAGE_TYPE) #Открываем изображение. 
#draw = ImageDraw.Draw(image) #Создаем инструмент для рисования. 

#ЛИНЕЙНЫЕ ФИЛЬТРЫ

#Константное преобразование
def constant(pixel):
    r, g, b = pixel
    return r, g, b

#Выделение красной компоненты.
def only_red(pixel):
    r, g, b = pixel
    return r, 0, 0

#Список преобразований
linear_transformations = [constant, only_red]

#Последовательное применение всех преобразований с сохранением результата.
for transformation in linear_transformations:
    image = original_image.copy() #Создаем новое изображение, чтобы не испортить оригинальное.
    width = image.size[0] #Определяем ширину. 
    height = image.size[1] #Определяем высоту.  
    pixels = image.load() #Выгружаем значения пикселей.
    
    #Перебираем каждый пиксель
    for i in range(width):
        for j in range(height):
            pixels[i, j] = transformation(pixels[i, j]) #Применяем текущее преобразование.
    
    image.save(IMAGE_PATH + IMAGE_NAME + "_" + transformation.__name__ + "." + IMAGE_TYPE); #Сохранение картинки.

#МАТРИЧНЫЕ ФИЛЬТРЫ

#Константная матрица 3x3.
def const(): 
    return [[0, 0, 0], [0, 1, 0], [0, 0, 0]]

matrix_filters = [const]

def matrix_transformation(old_pixels, width, height, x, y, get_matrix):
    matrix = get_matrix()
    n = len(matrix) #Узнаем размерность матрицы.
    new_color = [0, 0, 0]
    matrix_sum = 0 #Посчитаем сумму в матрице преобразования для того, чтобы потом поделить на это значение.
                   #Таким образом интенсивность изображения не измениться.
    #Перебираем соседей
    for i in range(n):
        for j in range(n):
            new_x = x - n // 2 + i  #Вычисляем координату соседа, с учетом того, что "мы" в центре матрицы.
            new_y = y - n // 2 + j
           
            #Проверяем соседа на существование.
            if new_x >= 0 and new_x < width and new_y >= 0 and new_y < height:
                matrix_sum += matrix[i][j]
                #Перебираем цветовую компоненту.
                for c in range(3):
                    new_color[c] += old_pixels[new_x, new_y][c] * matrix[i][j] #Добавляем цвет соседа умноженный на коэффициент из матрицы.
    
    for c in range(3):
        if matrix_sum != 0:
            new_color[c] /= matrix_sum #Нормируем цвет.
        else:
            new_color[c] = 0
    return int(new_color[0]), int(new_color[1]), int(new_color[2])

for matrix in matrix_filters:
    image = original_image.copy() #Создаем новое изображение, чтобы не испортить оригинальное.
    width = image.size[0] #Определяем ширину.
    height = image.size[1] #Определяем высоту.
    pixels = image.load() #Выгружаем значения пикселей.
    old_pixels = original_image.load() #Выгружаем значения пикселей оригинального изображения.
    
    #Перебираем каждый пиксель
    for i in range(width):
        for j in range(height):
            pixels[i, j] = matrix_transformation(old_pixels, width, height, i, j, matrix) #Применяем текущее преобразование.

    image.save(IMAGE_PATH + IMAGE_NAME + "_matrix_" + matrix.__name__ + "." + IMAGE_TYPE); #Сохранение картинки.


