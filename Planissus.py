import numpy as np
import matplotlib.pyplot as plt
import random

# define duration of the simulation
years = 100
months = 0
days = 3
total_days = years * 100 + months * 10 + days

# define the percentage of initial variables
water_percentage = 15

# vegetob variables
initial_vegetob_intensity = 5  # negative number to reduce vegetob presence
max_vegetob_intensity = 100
growing = 1  # grow rate per day

# define dimension of the terrain
width = 32
height = 32
grid_total_ground = int(width * height * (100 - water_percentage) / 100)

# define starting number of animals
num_erbast = -10, 30
num_carniz = -15, 20

# define max heard
max_erbast_heard = meh = 30
max_carniz_heard = mch = 20

# colors
g_cmap = plt.cm.colors.ListedColormap([(0.5, 1, 1), (0.6, 0.4, 0.1, 0.2)])
vegetob_cmap = plt.cm.get_cmap("Greens")
erbast_cmap = plt.cm.get_cmap("Reds")
carniz_cmap = plt.cm.get_cmap("Purples")
# show the graph
fig, ax = plt.subplots()

# define the data types for the dictionary keys
# data for terrain
dt_t = np.dtype([
    ("t_type", int)
])
# data for vegetob
dt_v = np.dtype([
    ("v_number", int)
])
# data for erbast
dt_e = np.dtype([
    ("e_number", int),
    ("e_energy", int), ("e_age", int), ("e_lifespan", int), ("e_social", int), ("e_daily_energy", int)
])

# data for carniz
dt_c = np.dtype([
    ("c_number", int),
    ("c_energy", int), ("c_age", int), ("c_lifespan", int), ("c_social", int), ("c_daily_energy", int)
])

# generate arrays with map dimension
t_data = np.empty((width, height), dtype=dt_t)
v_data = np.empty((width, height), dtype=dt_v)
e_data = np.empty((width, height), dtype=dt_e)
c_data = np.empty((width, height), dtype=dt_c)

# set water and terrain squares [1, 2]
for x in range(width):
    for y in range(height):
        if random.randint(0, 100) <= water_percentage:
            t_data[x][y]["t_type"] = 1
        else:
            t_data[x][y]["t_type"] = 2

# define spawn of vegetob for day 0
for x in range(width):
    for y in range(height):
        if t_data[x][y]["t_type"] == 1:
            v_data[x][y]["v_number"] = 0

        elif t_data[x][y]["t_type"] == 2:
            v_data[x][y]["v_number"] = np.random.randint(initial_vegetob_intensity, max_vegetob_intensity)

# define spawn of erbast for day 0
for x in range(width):
    for y in range(height):
        if t_data[x][y]["t_type"] == 1:
            e_data[x][y]["e_number"] = 0
        if t_data[x][y]["t_type"] == 2 and random.randint(0, 100) < 25:
            e_data[x][y]["e_number"] = random.randint(1, 5)

        if e_data[x][y]["e_number"] <= 0:
            e_data[x][y]["e_number"] = 0
            e_data[x][y]["e_energy"] = 0
            e_data[x][y]["e_lifespan"] = 0
            e_data[x][y]["e_age"] = 0
            e_data[x][y]["e_social"] = 0
            e_data[x][y]["e_daily_energy"] = 0

        elif e_data[x][y]["e_number"] >= 1:
            e_data[x][y]["e_energy"] = np.random.randint(low=10, high=25)
            e_data[x][y]["e_lifespan"] = np.random.randint(low=10, high=25)
            e_data[x][y]["e_age"] = np.random.randint(low=1, high=25)
            e_data[x][y]["e_social"] = np.random.randint(low=1, high=2)
            e_data[x][y]["e_daily_energy"] = 1

# print(e_data)
# define spawn of carniz for day 0
for x in range(width):
    for y in range(height):
        if t_data[x][y]["t_type"] == 1:
            c_data[x][y]["c_number"] = 0
        elif t_data[x][y]["t_type"] == 2 and random.randint(0, 100) < 20:
            c_data[x][y]["c_number"] = random.randint(1, 5)

        if c_data[x][y]["c_number"] <= 0:
            c_data[x][y]["c_number"] = 0
            c_data[x][y]["c_energy"] = 0
            c_data[x][y]["c_lifespan"] = 0
            c_data[x][y]["c_age"] = 0
            c_data[x][y]["c_social"] = 0
            c_data[x][y]["c_daily_energy"] = 0

        elif c_data[x][y]["c_number"] >= 1:
            c_data[x][y]["c_energy"] = np.random.randint(low=10, high=25)
            c_data[x][y]["c_lifespan"] = np.random.randint(low=10, high=25)
            c_data[x][y]["c_age"] = np.random.randint(low=1, high=25)
            c_data[x][y]["c_social"] = np.random.randint(low=1, high=2)
            c_data[x][y]["c_daily_energy"] = 1


# print(g_data)

# Finds the lowest value of datatype in ground tile around input tile(top, bottom, right, left), outputs coordinates
def get_low_tile(grid_data, o, p, data_type):
    values = []
    if o > 0 and t_data[o - 1][p]["t_type"] == 2 and grid_data[o - 1][p][data_type]:
        values.append((o - 1, p))
    if o < len(grid_data) - 1 and t_data[o + 1][p]["t_type"] == 2 and grid_data[o + 1][p][data_type]:
        values.append((o + 1, p))
    if p > 0 and t_data[o][p - 1]["t_type"] == 2 and grid_data[o][p - 1][data_type]:
        values.append((o, p - 1))
    if p < len(grid_data[0]) - 1 and t_data[o][p + 1]["t_type"] == 2 and grid_data[o][p + 1][data_type]:
        values.append((o, p + 1))
    if not values:
        return None
    return min(values, key=lambda t: grid_data[t[0]][t[1]][data_type])


# Finds the highest value of datatype in ground tile around input tile(top, bottom, right, left) outputs coordinates
def get_max_tile(grid_data, o, p, data_type):
    values = []
    if o > 0 and grid_data[o - 1][p]["terrain"]["t_type"] == 2 and grid_data[o - 1][p][data_type]:
        values.append((o - 1, p))
    if o < len(grid_data) - 1 and grid_data[o + 1][p]["terrain"]["t_type"] == 2 and grid_data[o + 1][p][data_type]:
        values.append((o + 1, p))
    if p > 0 and grid_data[o][p - 1]["terrain"]["t_type"] == 2 and grid_data[o][p - 1][data_type]:
        values.append((o, p - 1))
    if p < len(grid_data[0]) - 1 and grid_data[o][p + 1]["terrain"]["t_type"] == 2 and grid_data[o][p + 1][data_type]:
        values.append((o, p + 1))
    if not values:
        return None
    return max(values, key=lambda t: grid_data[t[0]][t[1]][data_type])


# Finds the highest value of datatype in ground tile around input tile(top, bottom, right, left) outputs value
def get_max_value(grid_data, o, p, data_type):
    mx_tile = get_max_tile(grid_data, o, p, data_type)
    if mx_tile is None:
        return None
    return grid_data[mx_tile[0]][mx_tile[1]][data_type]


# Checks the presence of input animal around input tile
def check_for_animals(datatype, animal, tile):
    o, p = tile
    # check top tile
    if o > 0 and datatype[o - 1][p]["terrain"]["t_type"] == 2 and datatype[o - 1][p][animal].size > 0:
        return True
    # check bottom tile
    if o < width - 1 and datatype[o + 1][p]["terrain"]["t_type"] == 2 and datatype[o + 1][p][animal].size > 0:
        return True
    # check right tile
    if p < height - 1 and datatype[o][p + 1]["terrain"]["t_type"] == 2 and datatype[o][p + 1][animal].size > 0:
        return True
    # check left tile
    if p > 0 and datatype[o][p - 1]["terrain"]["t_type"] == 2 and datatype[o][p - 1][animal].size > 0:
        return True
    # if no adjacent tile has animal or terrain is 1, return False
    return False


# define what happens every day
for d in range(total_days):
    # define Vegetob growth
    for x in range(width):
        for y in range(height):
            if t_data[x][y]["t_type"] == 1:  # if terrain is water
                pass
            if t_data[x][y]["t_type"] == 2:  # if terrain is ground
                # if vegetob is lower than 100, grow by growing
                if v_data[x][y]["v_number"] < 100 and random.randint(1, 100) < 50:
                    # print("before:", v_data[x][y]["v_number"])
                    v_data[x][y]["v_number"] = v_data[x][y]["v_number"] + growing
                    # print("after:", v_data[x][y]["v_number"])

                # if vegetob == 100, grow the next lowest tile by 1
                elif v_data[x][y]["v_number"] == 100:
                    # lowest value near tile
                    lowest = get_low_tile(v_data, x, y, "v_number")
                    if lowest is None:
                        pass
                    else:
                        lw0 = lowest[0]
                        lw1 = lowest[1]
                        v_data[lw0][lw1]["v_number"] += 1

                elif v_data[x][y]["v_number"] > max_vegetob_intensity or \
                        v_data[x][y]["v_number"] == max_vegetob_intensity:
                    # sets eventual vegetob over max_vegetob_intensity to max_vegetob_intensity
                    v_data[x][y]["v_number"] = max_vegetob_intensity

            # define Erbast behavior
            if t_data[x][y]["t_type"] == 1:  # if terrain is water, skip
                pass
            if t_data[x][y]["t_type"] == 2:  # if terrain is ground
                if isinstance(e_data[x][y], int):  # check if erbast present
                    for e in range(e_data[x][y]["e_number"]):  # make every individual in a tile choose what to do
                        # define natural death
                        if (v_data[x][y]["v_number"] + v_data[x + 1][y]["v_number"] +
                            v_data[x][y + 1]["v_number"] + v_data[x - 1][y]["v_number"] +
                                v_data[x][y - 1]["v_number"]) >= 390 or e_data[x][y][e]["e_energy"] == 0:
                            e_data[x][y]["e_number"] -= 1
                            e_data[x][y][e]["e_energy"] = 0
                            e_data[x][y][e]["e_lifespan"] = 0
                            e_data[x][y][e]["e_age"] = 0
                            e_data[x][y][e]["e_social"] = 0
                            e_data[x][y][e]["e_daily_energy"] = 0

                        # define moving
                        # moving for stronger, non-social individuals, (they move half of the time)
                        if e_data[x][y][e]["e_social"] == 2 and random.randint(0, 100) <= 50\
                                and e_data[x][y][e]["e_daily_energy"] >= 1:
                            max_tile = get_max_tile(v_data, x, y, "v_number")
                            a = max_tile[0]
                            b = max_tile[1]
                            # if vegetation higher in near tile, stronger, non-social individuals will move
                            if v_data[a][b] > v_data[x][y]:
                                np.append(e_data[a][b], e_data[x][y])
                                e_data[a][b]["e_number"] += 1
                                np.delete(e_data[x][y], e_data[x][y])
                                e_data[x][y]["e_number"] -= 1
                                e_data[x][y][e]["e_daily_energy"] -= 1
                            else:
                                continue
                        # define moving for social individuals, (they always move if near other erbast)
                        if e_data[x][y]["e_social"] == 1 \
                            and check_for_animals(e_data, "e_number", [x, y]) is True\
                                and e_data[x][y][e]["e_daily_energy"] >= 1:
                            max_tile = get_max_tile(e_data, x, y, "e_number")
                            a = max_tile[0]
                            b = max_tile[1]
                            # if erbast present near and if no > max_heard
                            if check_for_animals(e_data, "e_number", [x, y]) is True \
                                and get_max_value(v_data, x, y, "v_number") < max_erbast_heard\
                                    and e_data[x][y][e]["e_daily_energy"] >= 1:
                                np.append(e_data[a][b], e_data[x][y])
                                e_data[a][b]["e_number"] += 1
                                np.delete(e_data[x][y], e_data[x][y])
                                e_data[x][y]["e_number"] -= 1
                                e_data[x][y][e]["e_daily_energy"] -= 1
                            else:
                                continue

                        # define grazing
                        if e_data[x][y][e]["e_daily_energy"] >= 1:
                            v_data[x][y]["v_number"] -= 1
                            e_data[x][y][e]["e_energy"] += 1
                            e_data[x][y][e]["e_daily_energy"] -= 1

                        # define aging
                        e_data[x][y][e]["e_age"] -= 1

                        # define natural energy loss
                        if e_data[x][y][e]["e_age"] % 10 == 0:
                            e_data[x][y][e]["e_energy"] -= 1

                        # define reproduction
                        if e_data[x][y][e]["e_age"] == e_data[x][y][e]["e_lifespan"]:
                            # create two new erbast with same stats except energy
                            new_erbast1 = dict(e_data[x][y])
                            new_erbast2 = dict(e_data[x][y])
                            new_erbast1["e_energy"] = e_data[x][y][e]["e_energy"] / 2
                            new_erbast2["e_energy"] = e_data[x][y][e]["e_energy"] / 2
                            # add new erbast to grid
                            low_a = get_max_tile(v_data, x, y, ["v_number"])
                            low_b = get_max_tile(v_data, x, y, ["v_number"])
                            low1a = low_a[0]
                            low2a = low_a[1]
                            low1b = low_b[0]
                            low2b = low_b[1]
                            np.append(e_data[low1a][low2a], new_erbast1)
                            np.append(e_data[low1b][low2b], new_erbast2)
                            # delete old erbast
                            e_data[x][y][e]["e_energy"] = 0

            # define Carniz behavior
            if t_data[x][y]["t_type"] == 1:  # if terrain is water, skip
                pass
            elif t_data[x][y]["t_type"] == 2:  # if terrain is ground
                if isinstance(c_data[x][y], int):  # check if erbast present
                    for c in range(c_data[x][y]["c_number"]):  # make every individual in a tile choose
                        c_data[x][y]["c_daily_energy"][c] += 1
                        c_data[x][y]["c_energy"][c] -= 1

                        # define death
                        if (v_data[x][y]["v_number"] + v_data[x + 1][y]["v_number"] +
                            v_data[x][y + 1]["v_number"] + v_data[x - 1][y]["v_number"] +
                                v_data[x][y - 1]["v_number"]) >= 390 or c_data[x][y]["c_energy"][c] == 0:
                            c_data[x][y]["c_number"] -= 1
                            c_data[x][y]["c_energy"][c] = 0
                            c_data[x][y]["c_lifespan"][c] = 0
                            c_data[x][y]["c_age"][c] = 0
                            c_data[x][y]["c_social"][c] = 0
                            c_data[x][y]["c_daily_energy"][c] = 0
                        # define moving
                        # moving for stronger, non-social individuals, (they move a third of the time)
                        if c_data[x][y]["c_social"][c] == 2 and random.randint(0, 100) <= 66:
                            max_tile = get_max_tile(e_data, x, y, "e_number")
                            a = max_tile[0]
                            b = max_tile[1]
                            # if vegetation higher in near tile, stronger, non-social individuals will move
                            if v_data[a][b] > v_data[x][y]:
                                np.append(c_data[a][b], c_data[x][y][c])
                                c_data[a][b]["c_number"] += 1
                                np.delete(c_data[x][y], c_data[x][y][c])
                                c_data[x][y]["c_number"] -= 1
                                c_data[x][y]["c_daily_energy"][c] -= 1
                            else:
                                continue
                        # define moving for social individuals, (they always move if near other erbast)
                        elif c_data[x][y]["c_social"][c] == 1 \
                                and check_for_animals(c_data, "c_number", [x, y]) is True:
                            max_tile = get_max_tile(c_data, x, y, "c_number")
                            a = max_tile[0]
                            b = max_tile[1]
                            # if carniz present near and if no > max_heard
                            if check_for_animals(c_data, "c_number", [x, y]) is True \
                                    and get_max_value(c_data, x, y, "c_number") < max_carniz_heard:
                                np.append(c_data[a][b], c_data[x][y][c])
                                c_data[a][b]["c_number"] += 1
                                np.delete(c_data[x][y], c_data[x][y][c])
                                c_data[x][y]["c_number"] -= 1
                                c_data[x][y]["c_daily_energy"][c] -= 1
                            else:
                                continue

                        # define hunting
                        elif c_data[x][y]["c_daily_energy"][c] >= 1:
                            if e_data[x][y]["e_number"] is None:
                                pass
                            else:
                                prey = min(e_data[x][y]["e_energy"])
                                c_data[x][y]["c_energy"][c] += prey
                                np.delete(e_data[x][y], prey)
                                c_data[x][y]["c_daily_energy"][c] -= 1

                        # define natural energy loss
                        elif c_data[x][y]["c_age"][c] % 10 == 0:
                            c_data[x][y]["c_energy"][c] -= 1

                        # define reproduction
                        elif c_data[x][y]["c_age"][c] == c_data[x][y]["c_lifespan"][c]:
                            # create two new erbast with same stats except energy
                            new_erbast1 = dict(c_data[x][y][c])
                            new_erbast2 = dict(c_data[x][y][c])
                            new_erbast1["c_energy"] = c_data[x][y]["c_energy"][c] / 2
                            new_erbast2["c_energy"] = c_data[x][y]["c_energy"][c] / 2
                            # add new erbast to grid
                            a = get_max_tile(v_data, x, y, ["v_number"])
                            b = get_max_tile(v_data, x, y, ["v_number"])
                            np.append(c_data[a][b], new_erbast1)
                            np.append(c_data[a][b], new_erbast2)
                            # delete old erbast
                            np.delete(c_data[x][y], c_data[x][y][c])

                        # define aging
                        c_data[x][y]["c_age"] -= 1

    # print(t_data["t_type"])
    # print(v_data["v_number"])
    # print(e_data["e_energy"])

    # clear graph
    plt.cla()

    # show updated vegetob
    v_number_filtered = np.where(v_data["v_number"] <= 3, np.nan, v_data["v_number"])
    ax.imshow(v_data["v_number"], cmap=vegetob_cmap, alpha=1)

    # show updated erbast
    e_number_filtered = np.where(e_data["e_number"] <= 3, np.nan, e_data["e_number"])
    ax.imshow(e_number_filtered, vmin=0, vmax=max_erbast_heard, cmap=erbast_cmap, alpha=0.8)

    # show updated carniz
    c_number_filtered = np.where(c_data["c_number"] <= 3, np.nan, c_data["c_number"])
    ax.imshow(c_number_filtered, cmap=carniz_cmap, alpha=0.7)

    # show updated water
    ax.imshow(t_data["t_type"], cmap=g_cmap, alpha=0.3)

    # print(e_data["e_number"])
    # print(c_data["c_number"])

    ax.set_xticks(np.arange(0, width, 1))
    ax.set_yticks(np.arange(0, height, 1))
    ax.set_xticks([])
    ax.set_yticks([])
    ax.grid(False)
    plt.draw()
    plt.pause(0.001)
