import golly as g

G_NW = g.parse('3o$o$bo!')
G_SW = g.parse('bo$o$3o!')

GS_NW = [g.evolve(G_NW, i) for i in range(4)]
GS_SW = [g.evolve(G_SW, i) for i in range(4)]

PAIR = g.parse('3o$o$bo2$10b2o$9b2o$11bo!')
PAIRS = [g.evolve(PAIR, i) for i in range(4)]

recipes = {

    'hb' : ('4b2o$3bo2bo$3bobo$b2obo$o2bo$obo$bo!',
            [(-11, 0, 2, -7), (-16, 0, 1, 8), (-17, 0, -4, -12)]),
    
    'block' : ('2o$2o!', [(1, 0, -1, 12)]),
    'blinker' : ('3o!', [(1, 0, -7, 10)]),
    'hive' : ('b2o$o2bo$b2o!', [(5, 0, 3, 12), (4, 0, 3, 1)]),
    'ship' : ('2o$obo$b2o!', [(1, 0, 5, 12), (-1, 0, 11, -6)]),
    'boat1' : ('2o$obo$bo!', [(2, 0, 0, 12), (2, 0, 2, -1)]),
    'boat2' : ('b2o$obo$bo!', [(-3, 0, 1, 12), (0, 0, -5, 24)]),
    'boat3' : ('bo$obo$2o!', [(-3, 0, 3, 12), (0, 0, 3, 9)]),
    
    }


GUN1 = [[], []]
GUN2 = [[], []]


def queue_orthogonal(l1, t1, l2, t2, isP2):

    t = max(get_delay(GUN1, l1, t1), get_delay(GUN2, l2, t2))

    queue_headon(GUN1, l1, t1 + t + (t % 2) * isP2)
    queue_headon(GUN2, l2, t2 + t + (t % 2) * isP2)


def get_new(l, t):

    if l % 2 == 0:
        new_l = [t, t + 118, t + 235]
        new_r = [t + 1 + 4 * l, t + 125 + 4 * l, t + 251 + 4 * l]
    else:
        new_l = [t + 32, t + 172, t + 289]
        new_r = [t - 67 + 4 * l, t + 51 + 4 * l, t + 206 + 4 * l]

    return new_l, new_r


def get_delay(gun, l, t):

    left, right = gun
    new_l, new_r = get_new(l, t)

    if left and right:

        return max(left[-1] + 117 - new_l[0], right[-1] + 117 - new_r[0])

    else:

        return 400 - min(new_l[0], new_r[0])
    

def queue_headon(gun, l, t):

    left, right = gun

    new_l, new_r = get_new(l, t)

    left += new_l
    right += new_r


def queue_recipe(recipe, x, y, isP2=False):
    
    for l1, t1, l2, t2 in recipe:
        queue_orthogonal(l1 - x - y, t1, l2 - x + y, t2, isP2)


def draw_loop(ts, d_offset, v_offset, diag, vert):

    circuit = g.parse('39b2o$39bo24b2o$40b3o6b2o13bo$42bo6b2o11bobo$62b2o13b2o$6b2o69b2o$5bobo$3b3o$2bo3bo76b2o$2b2ob2o76b2o$31b2o46b2o$31b2o46b2o3$2obo$ob2o80b2o$84b2o$34b2o$35bo24b2o3bo$15b2o17bo13b2o3b2o5bo3bobo$15bo18b2o13bo3bo7bo3b2o$16b3o27b3o5b3o5bo$18bo27bo9bo3bob5o$60b2o4bo$63b3o$60b2obo$60bobo15$72b2o$72b2o2$79bob2o$79b2obo7$77bo$76bobo$77b2o14$53b2o$53b2o$57b2o$57b2o$71b2o$71b2o5$74bo$73bobo7b2o$73bobo7b2o$61b2o11bo$62bo$59b3o$59bo$63b2o$63b2o!')

    eater = g.parse('2b2o$bobo$bo$2o!', 62, 31)

    circA = g.transform(circuit, -100 + 2 * diag, -110 + 2 * diag)

    circuit = g.join(circuit, eater)

    circB = g.transform(circuit, 10102 + 2 * diag, -10278 + 2 * diag, 0, -1, 1, 0)
    circC = g.transform(circuit, 10315 + 2 * diag,  -10031 + 2 * diag, -1, 0, 0, -1)
    circD = g.transform(circuit, 113 + 2 * diag,  137 + 2 * diag, 0, 1, -1, 0)

    a, b, c, d  = (0, 1, 1, 0) if diag else (1, 0, 0, 1)

    if vert:
        sgn = -1
        c, d = -c, -d
    else:
        sgn = 1
        

    if not diag:
        d_offset = 0

    for i, t in enumerate(ts):
        if i % 1000 == 0:
            g.show(str(i))
        x = -d_offset - (-t // 4)
        y =  d_offset - (-t // 4)
        g.putcells(PAIRS[-t % 4], x, sgn * y + v_offset, a, b, c, d)

    GUN_PERIOD = 512 * 245912

    l_offset = (GUN_PERIOD - 84096) // 8 # magic number alert

    g.putcells(circA, -d_offset, sgn * d_offset + v_offset, a, b, c, d)
    g.putcells(circB, -d_offset, sgn * d_offset + v_offset, a, b, c, d)
    g.putcells(circC, -d_offset + l_offset, sgn * (d_offset + l_offset) + v_offset, a, b, c, d)
    g.putcells(circD, -d_offset + l_offset, sgn * (d_offset + l_offset) + v_offset, a, b, c, d)


def draw_sniper(gun, width, offset, vert):

    left, right = gun

    draw_loop(left, 0, offset, False, vert)
    draw_loop(right, width, offset, True, vert)
    

all_cells = g.getcells(g.getrect())

gs_nw = []
for t, glider in enumerate(GS_NW):
    x0, y0 = 0, 0 # this is always a live cell in first 4 iterations
    w, h = max(glider[::2]) + 1, max(glider[1::2]) + 1
    glider = zip(glider[::2], glider[1::2])

    for i in range(0, len(all_cells), 2):
        x, y = all_cells[i] - x0, all_cells[i+1] - y0
        if all(g.getcell(x + a, y + b) for (a, b) in glider):
            if len(g.getcells([x-1, y-1, w+2, h+2])) == 2 * len(glider):
                gs_nw.append((y-x, 4 * x - t))
    
gs_nw.sort(key=lambda (l, t) : t)


gs_sw = []
for t, glider in enumerate(GS_SW):
    x0, y0 = 0, 2 # this is always a live cell in first 4 iterations
    w, h = max(glider[::2]) + 1, max(glider[1::2]) + 1
    glider = zip(glider[::2], glider[1::2])

    for i in range(0, len(all_cells), 2):
        x, y = all_cells[i] - x0, all_cells[i+1] - y0
        if all(g.getcell(x + a, y + b) for (a, b) in glider):
            if len(g.getcells([x-1, y-1, w+2, h+2])) == 2 * len(glider):
                gs_sw.append((-y-x, 4 * x - t))

gs_sw.sort(key=lambda (l, t) : t)
    
    

components = {}

for name in recipes:
    
    coords = []
    cells = g.parse(recipes[name][0])
    if not cells:
        continue
    x0, y0 = cells[:2]
    w, h = max(cells[::2]) + 1, max(cells[1::2]) + 1
    cells = zip(cells[::2], cells[1::2])

    for i in range(0, len(all_cells), 2):
        x, y = all_cells[i] - x0, all_cells[i+1] - y0
        if all(g.getcell(x + a, y + b) for (a, b) in cells):
            if len(g.getcells([x-1, y-1, w+2, h+2])) == 2 * len(cells):
                coords.append((x, y))
    
    components[name] = coords


# sort hbs into trails
hbs = components['hb']
hbs.sort(key=lambda (x, y) : y-x)


num_hbs = len(hbs)
done_hbs = 0
trails = []

while done_hbs < num_hbs:
    
    new_trail = []

    for i in range(len(hbs)):
        if hbs[i]:
            j = i
            break

    target_lane = hbs[j][0] + hbs[j][1]
    dist = hbs[j][1] - hbs[j][0]

    for i in range(j, len(hbs)):

        if not hbs[i]:
            continue

        # treat really big jumps as separate trails
        if hbs[i][1] - hbs[i][0] > dist + 2000:
            break

        if hbs[i][0] + hbs[i][1] == target_lane:
            new_trail.append(hbs[i])
            dist = hbs[i][1] - hbs[i][0]
            hbs[i] = 0
            target_lane += 2
            done_hbs += 1

    trails.append(new_trail)

del components['hb']

trails.sort(key=lambda trail: trail[-1][0] + trail[-1][1])

assert(len(trails) == 15)

# make the first 3 trails
hb_rec = recipes['hb'][1]

for trail in trails[:3]:
    for x, y in trail[::-1]:
        queue_recipe(hb_rec, x, y, True)

# make blinkers
blinkers = components['blinker']
blinkers.sort()
blinker_rec = recipes['blinker'][1]
for x, y in blinkers:
    queue_recipe(blinker_rec, x, y, True)

del components['blinker']

# make SE hbs
for trail in trails[-4:]:
    for x, y in trail[::-1]:
        queue_recipe(hb_rec, x, y)

# make junk
junk_list = []

for name in components:
    for x, y in components[name]:
        junk_list.append((x, y, recipes[name][1]))

junk_list.sort()

for x, y, rec in junk_list:
    queue_recipe(rec, x, y)

# make more hbs
for trail in trails[7:11]:
    for x, y in trail[::-1]:
        queue_recipe(hb_rec, x, y)

# make final hbs
for trail in trails[3:7]:
    for x, y in trail[::-1]:
        queue_recipe(hb_rec, x, y)


if gs_nw:
    l, t = gs_nw[0]
    d = get_delay(GUN2, l, t)
    d += d % 2 # make gliders of correct parity
    for l, t in gs_nw:
        queue_headon(GUN2, l, t + d)

    if gs_sw:
        for l, t in gs_sw:
            queue_headon(GUN1, l, t + d)


g.new('')

draw_sniper(GUN1, 40000, 0, True)
draw_sniper(GUN2, 40000, 22000, False)

g.fit()

g.show("Build time: " + str(GUN2[0][-1]))
