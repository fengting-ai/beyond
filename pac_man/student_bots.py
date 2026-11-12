"""学生策略模板：只修改两个 decide 方法中的寻路逻辑。"""

import heapq
import random

try:
    from .interfaces import Direction
except ImportError:
    from interfaces import Direction


def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def astar_path(start, goal, state):
    if start == goal:
        return []
    
    counter = 0
    open_set = []
    heapq.heappush(open_set, (0, counter, start, []))
    counter += 1
    
    visited = set()
    
    while open_set:
        f, _, current, path = heapq.heappop(open_set)
        
        if current in visited:
            continue
        visited.add(current)
        
        if current == goal:
            return path
        
        for direction, next_pos in state.neighbors(current):
            if next_pos in visited:
                continue
            
            new_path = path + [direction]
            g = len(new_path)
            h = heuristic(next_pos, goal)
            f = g + h
            
            heapq.heappush(open_set, (f, counter, next_pos, new_path))
            counter += 1
    
    return []


class StudentPacMan:
    last_target = None  # 记录上次吃的豆子，吃完再换
    
    def decide(self, state):
        pac_pos = state.pacman_position
        
        if not state.bean_positions:
            return None
        
        # 1. 先看附近有没有鬼
        danger = False
        for ghost_pos in state.ghost_positions:
            dist = heuristic(pac_pos, ghost_pos)
            if dist <= 3:
                danger = True
                break
        
        # 2. 有危险：找一个安全的方向跑
        if danger:
            StudentPacMan.last_target = None  # 躲鬼的时候忘记原来的目标
            best_dir = None
            best_score = -999
            
            for direction, next_pos in state.neighbors(pac_pos):
                min_ghost_dist = min(heuristic(next_pos, g) for g in state.ghost_positions)
                exit_count = len(list(state.neighbors(next_pos)))
                score = min_ghost_dist * 10 + exit_count
                
                if score > best_score:
                    best_score = score
                    best_dir = direction
            
            if best_dir:
                return best_dir
        
        # 3. 没危险：认准一个豆子吃完它
        # 如果上次的豆子还在，就继续吃它
        if StudentPacMan.last_target and StudentPacMan.last_target in state.bean_positions:
            target = StudentPacMan.last_target
        else:
            # 上次的豆子吃完了，找新的最近豆子
            target = min(
                state.bean_positions,
                key=lambda bean: heuristic(pac_pos, bean),
            )
            StudentPacMan.last_target = target
        
        path = astar_path(pac_pos, target, state)
        if path:
            return path[0]
        
        neighbors = list(state.neighbors(pac_pos))
        if neighbors:
            return neighbors[0][0]
        return None


class StudentGhost:
    def decide(self, state, ghost_index=0):
        start = state.ghost_positions[ghost_index]
        goal = state.pacman_position
        
        # 出错概率，你调成多少就是多少
        if random.random() < 0.9:
            neighbors = list(state.neighbors(start))
            if neighbors:
                return random.choice(neighbors)[0]
        
        path = astar_path(start, goal, state)
        if path:
            return path[0]
        
        neighbors = list(state.neighbors(start))
        if neighbors:
            return neighbors[0][0]
        return None