import numpy as np
from numpy import inf

# Given distance matrix
d = np.array([
    [0, 10, 12, 11, 14],
    [10, 0, 13, 15, 8],
    [12, 13, 0, 9, 14],
    [11, 15, 9, 0, 16],
    [14, 8, 14, 16, 0]
])

iteration = 100
n_ants = 5
n_citys = 5

# Initialization
m = n_ants
n = n_citys
e = 0.5      # evaporation rate
alpha = 1    # pheromone importance
beta = 2     # visibility importance

# Visibility = 1/distance (except diagonal)
visibility = 1 / d
visibility[visibility == inf] = 0

# Initialize pheromone matrix
pheromone = 0.1 * np.ones((n, n))

# Initialize route matrix for ants
route = np.ones((m, n + 1))

for ite in range(iteration):
    route[:, 0] = 1  # starting city for all ants

    for i in range(m):  # for each ant
        temp_visibility = np.array(visibility)

        for j in range(n - 1):
            cur_loc = int(route[i, j] - 1)

            temp_visibility[:, cur_loc] = 0  # remove visibility of current city

            # Calculate pheromone and visibility influence
            p_feature = np.power(pheromone[cur_loc, :], alpha)
            v_feature = np.power(temp_visibility[cur_loc, :], beta)

            combine_feature = p_feature * v_feature
            total = np.sum(combine_feature)

            if total == 0:
                probs = np.ones(n) / n
            else:
                probs = combine_feature / total

            cum_prob = np.cumsum(probs)
            r = np.random.random_sample()

            city = np.nonzero(cum_prob > r)[0][0] + 1
            route[i, j + 1] = city

        # Add last unvisited city
        visited = list(route[i, :-1].astype(int))
        left = list(set(range(1, n + 1)) - set(visited))
        if left:
            route[i, -1] = left[0]
        else:
            route[i, -1] = 1  # fallback (shouldn't happen normally)

    # Compute distance cost
    route_opt = np.array(route)
    dist_cost = np.zeros((m, 1))

    for i in range(m):
        s = 0
        for j in range(n - 1):
            s += d[int(route_opt[i, j]) - 1, int(route_opt[i, j + 1]) - 1]
        # add return to starting city
        s += d[int(route_opt[i, -1]) - 1, int(route_opt[i, 0]) - 1]
        dist_cost[i] = s

    # Find best route of this iteration
    dist_min_loc = np.argmin(dist_cost)
    dist_min_cost = dist_cost[dist_min_loc]
    best_route = route_opt[dist_min_loc, :]

    # Pheromone evaporation
    pheromone = (1 - e) * pheromone

    # Update pheromone based on distance
    for i in range(m):
        for j in range(n - 1):
            dt = 1.0 / dist_cost[i]
            a = int(route_opt[i, j]) - 1
            b = int(route_opt[i, j + 1]) - 1
            pheromone[a, b] += dt
            pheromone[b, a] += dt  # symmetric

print("Route of all ants at the end:")
print(route_opt)
print()
print("Best path :", best_route)
print("Cost of the best path :", int(dist_min_cost))
