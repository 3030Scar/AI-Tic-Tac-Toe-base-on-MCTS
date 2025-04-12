import math
import random
from copy import deepcopy
import time

class Node:
    def __init__(self, game_state, parent=None):
        self.parent = parent
        self.children = []
        self.wins = 0
        self.visits = 0
        self.untried_actions = None
        self.game_state = game_state  # (board, piece_positions)
        
    def ucb_score(self, exploration=1.5):
        if self.visits == 0:
            return float('inf')
        return (self.wins / self.visits) + exploration * math.sqrt(math.log(self.parent.visits) / self.visits)

class MCTS:
    def __init__(self, iterations=3000, timeout=3):
        self.iterations = iterations
        self.timeout = timeout
    
    def get_legal_actions(self, game_state):
        board, _ = game_state
        return [(i, j) for i in range(3) for j in range(3) if board[i][j] is None]

    def simulate_move(self, game_state, action):
        new_board = deepcopy(game_state[0])
        new_pieces = deepcopy(game_state[1])
        player = 'O' if len(new_pieces) % 2 == 1 else 'X'
        
        # 应用新移动
        row, col = action
        new_board[row][col] = player
        new_pieces.append((row, col, player))
        
        # 处理棋子消失
        if len(new_pieces) > 6:
            removed = new_pieces.pop(0)
            new_board[removed[0]][removed[1]] = None
            
        return (new_board, new_pieces)

    # 防御性检查方法
    def find_urgent_actions(self, game_state):
        """优先处理必须防御的位置"""
        board, pieces = game_state
        urgent_actions = []
        
        # 检查所有空位：如果玩家下这里会立即获胜吗？
        for i in range(3):
            for j in range(3):
                if board[i][j] is None:
                    # 模拟玩家下这里
                    temp_board = deepcopy(board)
                    temp_board[i][j] = 'X'
                    if self.check_win(temp_board, 'X'):
                        urgent_actions.append((i, j))
        
        return urgent_actions

    def selection(self, node):
        while node.untried_actions == [] and node.children != []:
            node = max(node.children, key=lambda x: x.ucb_score())
        return node

    def expansion(self, node):
        if node.untried_actions is None:
            node.untried_actions = self.get_legal_actions(node.game_state)
            
        if node.untried_actions:
            # 修正：确保urgent动作存在于未尝试列表中
            urgent = [a for a in self.find_urgent_actions(node.game_state) 
                    if a in node.untried_actions]
            
            if urgent:
                action = random.choice(urgent)
            else:
                action = random.choice(node.untried_actions)
            
            try:
                node.untried_actions.remove(action)
            except ValueError:
                # 防御性异常处理
                print(f"Warning: Tried to remove invalid action {action}")
                return node
                
            new_state = self.simulate_move(node.game_state, action)
            child = Node(new_state, parent=node)
            node.children.append(child)
            return child
        return node

    def simulation(self, game_state):
        state = deepcopy(game_state)
        steps = 0
        while steps < 20:
            actions = self.get_legal_actions(state)
            if not actions:
                return 0
                
            # 防御优先策略
            urgent = self.find_urgent_moves(state)
            if urgent:
                action = random.choice(urgent)
                state = self.simulate_move(state, action)
                steps += 1
                continue
                
            # 进攻策略
            player = 'O' if (len(state[1]) + steps) % 2 == 1 else 'X'
            win_move = self.find_winning_move(state, player)
            if win_move:
                state = self.simulate_move(state, win_move)
                return 1 if player == 'O' else -1
                
            # 启发式选择
            action = self.heuristic_choice(state, actions)
            state = self.simulate_move(state, action)
            steps += 1
        return 0

    # 防御性检查
    def find_urgent_moves(self, state):
        """寻找需要立即防御的位置"""
        board, _ = state
        opponent = 'X'
        urgent = []
        
        # 检查所有空位
        for i in range(3):
            for j in range(3):
                if board[i][j] is None:
                    temp = deepcopy(board)
                    temp[i][j] = opponent
                    if self.check_win(temp, opponent):
                        urgent.append((i, j))
        return urgent

    def find_winning_move(self, state, player):
        """寻找指定玩家的必胜位置"""
        board, _ = state
        for i in range(3):
            for j in range(3):
                if board[i][j] is None:
                    temp = deepcopy(board)
                    temp[i][j] = player
                    if self.check_win(temp, player):
                        return (i, j)
        return None

    def heuristic_choice(self, state, actions):
        board, _ = state
        player = 'O' if len(state[1]) % 2 == 1 else 'X'
        
        # 防御：阻止对手的潜在胜利
        opponent = 'X' if player == 'O' else 'O'
        for action in actions:
            temp = deepcopy(board)
            temp[action[0]][action[1]] = opponent
            if self.check_win(temp, opponent):
                return action
                
        # 进攻：寻找潜在胜利路径
        for action in actions:
            temp = deepcopy(board)
            temp[action[0]][action[1]] = player
            if self.check_win(temp, player):
                return action
                
        # 增强的潜在威胁检测
        threat_actions = []
        for action in actions:
            if self.is_potential_threat(board, action, opponent):
                threat_actions.append(action)
        if threat_actions:
            return random.choice(threat_actions)
            
        # 原启发式策略
        if (1,1) in actions:
            return (1,1)
        corners = [(0,0), (0,2), (2,0), (2,2)]
        for corner in corners:
            if corner in actions:
                return corner
        return random.choice(actions)

    def is_potential_threat(self, board, action, opponent):
        """检查该位置是否可能形成双重威胁"""
        i, j = action
        # 检查行
        row = board[i]
        if row.count(opponent) == 1 and row.count(None) == 2:
            return True
        # 检查列
        col = [board[x][j] for x in range(3)]
        if col.count(opponent) == 1 and col.count(None) == 2:
            return True
        # 检查对角线
        if i == j:
            diag = [board[x][x] for x in range(3)]
            if diag.count(opponent) == 1 and diag.count(None) == 2:
                return True
        if i + j == 2:
            diag = [board[x][2-x] for x in range(3)]
            if diag.count(opponent) == 1 and diag.count(None) == 2:
                return True
        return False

    def backpropagation(self, node, result):
        while node is not None:
            node.visits += 1
            node.wins += result
            node = node.parent

    def check_win(self, board, player):
        for i in range(3):
            if all(board[i][j] == player for j in range(3)) or \
               all(board[j][i] == player for j in range(3)):
                return True
        if all(board[i][i] == player for i in range(3)) or \
           all(board[i][2-i] == player for i in range(3)):
            return True
        return False

    def make_move(self, game_state):
        start_time = time.time()
        board, pieces = game_state
        
        # 防御优先：立即阻止玩家的必胜棋（增加有效性检查）
        urgent_actions = [a for a in self.find_urgent_actions(game_state)
                        if board[a[0]][a[1]] is None]
        if urgent_actions:
            return random.choice(urgent_actions)
        
        # 进攻优先：寻找自己的必胜棋
        for i in range(3):
            for j in range(3):
                if board[i][j] is None:
                    temp = deepcopy(board)
                    temp[i][j] = 'O'
                    if self.check_win(temp, 'O'):
                        return (i, j)
        
        root = Node(game_state)
        iterations = 0
        
        while time.time() - start_time < self.timeout and iterations < self.iterations:
            node = self.selection(root)
            node = self.expansion(node)
            if node.game_state != root.game_state:
                result = self.simulation(node.game_state)
                self.backpropagation(node, result)
            iterations += 1
            
        if not root.children:
            return random.choice(self.get_legal_actions(game_state))
            
        best_child = max(root.children, key=lambda x: x.visits)
        for action in self.get_legal_actions(game_state):
            temp_state = self.simulate_move(game_state, action)
            if temp_state[0] == best_child.game_state[0]:
                return action
        return random.choice(self.get_legal_actions(game_state))