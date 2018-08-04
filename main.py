import cv2

symbols = ['.','o','-','x']

def extract_valid_colors(img):
    color_map = {}
    color_ratio = {}
    color_ratio_list = []
    valid_colors = []

    for px_list in img:
        for px in px_list:
                try:
                    color_map[str(px.tolist())]=color_map[str(px.tolist())]+1
                except:
                    color_map[str(px.tolist())]=1

    total_colors = len(color_map.keys())

    for color in color_map.keys():
        color_ratio[color] = (color_map[color]+0.000)/total_colors

    color_ratio_list = [[color_ratio[t], t] for t in color_ratio.keys()]
    color_ratio_list.sort()
    color_ratio_list.reverse()
    valid_colors.append(color_ratio_list[0][1])
    ratio = color_ratio_list[0][0]
    index = 1
    while(index < len(color_ratio_list) and int(color_ratio_list[index][0]*10/ratio)>=1):
        valid_colors.append(color_ratio_list[index][1])
        index = index+1

    return valid_colors[0:4]


timg = cv2.imread('batman.png')
width_limit = 200
height_limit = int(width_limit * len(timg)/len(timg[0]))
wstep = int(len(timg[0])/width_limit)
hstep = int(len(timg)/height_limit)
symbol_color_map = {}

img = []
for t in timg[0::hstep+1]:
    r = []
    for x in t[0::wstep+1]:
        r.append(x)
    img.append(r)

valid_colors = extract_valid_colors(img)
for t in range(0,len(valid_colors)):
    symbol_color_map[valid_colors[t]] = symbols[t]

r = ''
for px_list in img:
    t = ''
    for px in px_list:
        try:
            t = t+symbol_color_map[str(px.tolist())]
        except:
            t = t+'e'
    r = r + '\n' + t

print(r)
