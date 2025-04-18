### README.md

# AI Tic Tac Toe - 井字棋

这是一个基于蒙特卡罗树搜索（MCTS）算法实现的AI井字棋游戏。项目包含两个版本的井字棋游戏：一个带有AI对手，另一个则是纯粹的双人对战。

<img width="450" alt="Snipaste_2025-04-13_16-43-39" src="https://github.com/user-attachments/assets/45689365-b113-4dc0-a7c8-5cd46a5dece5" />


## 项目简介
本项目实现了经典的井字棋游戏，并在此基础上增加了棋子消失机制。当棋盘上的棋子数量达到7颗时，最早放置的棋子将会消失，以此类推，保证棋盘上始终最多只有6颗棋子。这一机制为游戏增添了新的策略元素。

### 版本说明
- **有AI版本**：`Tic_Tac_Toe.py` 是带有AI对手的井字棋游戏，玩家可以与AI进行对战。AI的决策逻辑基于 `mcts_ai.py` 中实现的蒙特卡罗树搜索算法。
- **无AI版本**：`Tic_Tac_Toe_(no_AI).py` 是纯粹的双人对战井字棋游戏，两名玩家可以轮流在棋盘上落子。

### AI实现
`Tic_Tac_Toe.py` 只是一个交互界面，其AI功能依赖于 `mcts_ai.py` 中的模型。如果你想调试AI的参数或者尝试更换其他模型进行研究，可以直接在 `mcts_ai.py` 中进行操作。主代码会将当前的棋盘状态（`state`）传递给模型，模型最终会返回下棋的坐标。

## 安装与运行
### 环境要求
- Python 3.x
- Pygame库

### 安装依赖
```bash
pip install pygame
```

### 运行游戏
- **有AI版本**：
```bash
python Tic_Tac_Toe.py
```
- **无AI版本**：
```bash
python Tic_Tac_Toe_(no_AI).py
```

## 代码结构
- `Tic_Tac_Toe.py`：带有AI对手的井字棋游戏主程序，负责游戏的交互界面和逻辑控制。
- `Tic_Tac_Toe_(no_AI).py`：纯粹的双人对战井字棋游戏主程序。
- `mcts_ai.py`：实现了蒙特卡罗树搜索（MCTS）算法，为AI对手提供决策支持。

