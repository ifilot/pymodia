settings = dict()
occu = dict()
line = dict()

occu['value'] = 0.2
occu['color'] = "blue"

line['value'] = 0.5
line['color'] = "red"

settings["occupancy"] = occu
settings["occupancy"]["draw"] = True
settings["lines"] = line

if settings["occupancy"]["draw"]:
    print(settings["occupancy"])

# print(settings)
