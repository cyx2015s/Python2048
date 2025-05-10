BACKGROUND = "#bbada0"
color_map = {None: ("#f9f6f2", "#ccc0b3"), 2: ("#776e65", "#eee4da"), 4: ("#776e65", "#ede0c8"),
             8: ("#f9f6f2", "#f2b179"), 16: ("#f9f6f2", "#f2b179"), 32: ("#f9f6f2", "#f67c5f"),
             64: ("#f9f6f2", "#f65e3b"), 128: ("#f9f6f2", "#edcf72"), 256: ("#f9f6f2", "#edcc61"),
             512: ("#f9f6f2", "#edc850"), 1024: ("#f9f6f2", "#edc53f"), 2048: ("#f9f6f2", "#edc22e")}


def get_color(name):
    if name in color_map.keys():
        return color_map[name]
    return '#f9f6f2', '#3c3a32'

if __name__ == "__main__":
    print("Godot Script as followes: \n")
    print("const TEXTCOLORS = [",",\n\t".join(map(lambda x:"Color(\"{}\")".format(x[0]),
                                               color_map.values())),"\n]",sep="")
    print("const TILECOLORS = [", ",\n\t".join(map(lambda x: "Color(\"{}\")".format(x[1]),
                                                   color_map.values())), "\n]", sep="")