import numpy as np
import matplotlib.pyplot as plt
import random

# the neighbor function of up/down/left/right moves
def get_neib_fun(maze):
    H,W = maze.shape
    def neib(x,y):
        ret = []
        for cand in [(x-1,y), (x+1,y), (x,y-1), (x,y+1)]:
            xx,yy = cand
            if xx < 0 or xx >= W:
                continue
            if yy < 0 or yy >= H:
                continue
            if maze[yy,xx] == 1:
                continue
            ret.append(cand)
        return ret
    return neib

def make_path(maze):
    H,W = maze.shape
    neib = get_neib_fun(maze)
    def get_neib_vals(neibs, dists):
        return [dists[yy,xx] for xx,yy in neibs] + [np.inf]

    # instantiate to -1 across maze
    dists = np.full(maze.shape, np.inf)
    # make the goal-zone have distance of 0
    dists[-1, :] = 0
    live_coords = [(x,y) for y in range(H-1) for x in range(W)]
    ctr = 0
    while len(live_coords) > 0 and ctr < W*H:
        ctr += 1
        new_coords = []
        for x,y in live_coords:
            if maze[y,x] == 1:
                continue
            else:
                neib_vals = get_neib_vals(neib(x,y),dists)
                new_dist_val = min(neib_vals)+1
                if new_dist_val != np.inf:
                    dists[y,x] = new_dist_val
                else:
                    new_coords.append((x,y))
        live_coords = new_coords
    return dists

# make a maze of width and height
def make_maze(W,H,density):
    maze = np.random.binomial(1, density, size=(H,W))
    spawn_zone = np.zeros((2, W))
    goal_zone = np.zeros((1, W))
    maze = np.concatenate((spawn_zone, maze, goal_zone))
    return maze

def make_valid_maze(W,H,density):
    maze = make_maze(W,H,density)
    dists = make_path(maze)
    if dists[0][0] != np.inf:
        return maze, dists
    else:
        return make_valid_maze(W,H,density)

def draw_maze(maze):
    plt.imshow(maze)
    plt.colorbar()
    plt.savefig('drawings/maze_path.png')

def get_1_move(maze, dists, particles, particles_move_mask):
    neib_fun = get_neib_fun(maze)
    for x,y in particles:
        assert dists[y][x] != np.inf, "oy ur standing on impossible blocks"

    particles = [_ for _ in particles]

    for i,p in enumerate(particles):
        if particles_move_mask[i] is False:
            continue
        p_neib = neib_fun(*p)
        random.shuffle(p_neib)
        for p_n in p_neib:
            if p_n not in particles:
                cur_dist = dists[p[1]][p[0]]
                new_dist = dists[p_n[1]][p_n[0]]
                if new_dist < cur_dist:
                    particles[i] = p_n
                    return True, i, particles
    return False, None, particles

def get_group_move(maze, dists, particles):
    move_mask = [True for _ in range(len(particles))]

    while True:
        can_move, moved_id, particles = get_1_move(maze, dists, particles, move_mask)
        if can_move is False:
            return particles
        else:
            move_mask[moved_id] = False


if __name__ == '__main__':
    maze,dists = make_valid_maze(10, 16, 0.2)
    print (maze)
    print (dists)
    draw_maze(dists)

    particles = [(i,0) for i in range(10)]
    for i in range(100):
        print (particles)
        particles = get_group_move(maze, dists, particles)

