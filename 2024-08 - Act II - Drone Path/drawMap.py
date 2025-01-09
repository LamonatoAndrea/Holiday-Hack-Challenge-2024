import folium

coords = []
with open("ELF-HAWK-dump.csv", "r") as file:
    for line in file.read().split("\n")[1:-1]:
        line_array = line.split(",")
        y = float(line_array[4])
        x = float(line_array[5])
        coords.append((x,y))

m = folium.Map()
folium.PolyLine(coords).add_to(m)
m.save("map.html")