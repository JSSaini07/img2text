
import cv2
import sys
import os
import numpy as np
from colr import color as cl

def dist(s1,s2):
    s1 = s1.split(',')
    s2 = s2.split(',')
    return (int(s1[0])-int(s2[0]))**2+(int(s1[1])-int(s2[1]))**2+(int(s1[2])-int(s2[2]))**2

def extract_valid_colors(img, num_colors, similarity):

    symbols = ['.','o','*','<','c','~','>','z','n','w']
    symbol_color_map = {}

    # convert image to linear array of color strings
    img = img.reshape(len(img)*len(img[0]), 3).tolist()
    img_string = np.array([','.join([str(x) for x in t]) for t in img])
    color_frequency = np.unique(img_string, return_counts = True)
    temp_color_frequency = []
    for t in np.argsort(color_frequency,1)[1]:
        temp_color_frequency.append(color_frequency[0][t])

    color_frequency = [t for t in temp_color_frequency]
    color_frequency.reverse()

    symbol_color_map[color_frequency[0]] = symbols[0]

    last_used_color = color_frequency[0]
    current_symbol = 1
    updated = True

    while(updated and current_symbol<num_colors):
        marked = None
        updated = False
        for color in color_frequency:
            if symbol_color_map.get(color,'') == '':
                if(dist(last_used_color,color)<similarity):
                    symbol_color_map[color] = symbol_color_map[last_used_color]
                elif not marked:
                    symbol_color_map[color] = symbols[current_symbol]
                    current_symbol = current_symbol+1
                    marked = color
                    updated = True
        last_used_color = marked

    return symbol_color_map

def get_transformation_steps(img, width_limit = None, height_limit = None):
    if width_limit:
        height_limit = int(width_limit * len(img)/(len(img[0])+1000))
    elif height_limit:
        width_limit = int(height_limit * len(img[0])/len(img))
    else:
        return [0,0]
    wstep = int(len(img[0])/width_limit)
    hstep = int(len(img)/height_limit)
    return [wstep,hstep]


def draw_image(img, symbol_color_map, color_disable):
    result = ''
    for px_list in img:
        temp_result = ''
        for px in px_list:
            color = ','.join([str(t) for t in px])
            try:
                pixels = px.tolist()
                pixels.reverse()

                if not color_disable:
                    pxvalue = cl(symbol_color_map[color],fore = pixels)
                else:
                    pxvalue = symbol_color_map[color]

                temp_result = temp_result+pxvalue
            except:
                temp_result = temp_result+' '
        result = result + '\n' + temp_result

    return result


def convert(img_path, num_colors, similarity, width_limit = None, height_limit = None, color_disable=False):
    img = cv2.imread(img_path)
    wstep, hstep = get_transformation_steps(img, width_limit, height_limit)
    # step over the entire image matrix wstep along the width and hstep along the
    # height. Transpose is used to easily convert rows to columns and remove the
    # rows and transform back, saves from writing a loop and stepping

    img = img[0::hstep+1].transpose(1,0,2)[0::wstep+1].transpose(1,0,2)

    symbol_color_map = extract_valid_colors(img, num_colors, similarity)

    result = draw_image(img, symbol_color_map, color_disable=color_disable)

    return result


if __name__ == "__main__":

    save_file = [t for t in sys.argv[1:] if t.startswith('--output=')]
    color_disable = [t for t in sys.argv[1:] if t.startswith('--color_disable')]

    if(len(save_file)):
        save_file = save_file[0].split('--output=')[1]

    if(len(color_disable)):
        color_disable = True
    else:
        color_disable = False

    result = convert(img_path = './images/batman.png', num_colors = 10, similarity = 10000, width_limit=100, color_disable=color_disable)

    if save_file:
        open(save_file,'w').write(result)
        print('file saved in {}'.format(save_file))
    else:
        print(result)
