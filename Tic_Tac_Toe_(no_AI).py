# -*- coding: utf-8 -*-
import pygame
import sys
from pygame.locals import *
import math

# 初始化参数
WINDOW_SIZE = 600
BOARD_SIZE = 3
LINE_WIDTH = 15
COLORS = {
    "BG": (28, 170, 156),       # 蓝绿色背景
    "LINE": (23, 145, 135),     # 深蓝色线条
    "X": (66, 66, 66),          # 深灰色X
    "O": (239, 231, 200),       # 米白色O
    "INFO_BG": (23, 145, 135),  # 信息栏背景色
    "INFO_TEXT": (255, 255, 255) # 信息栏文字颜色
}

INFO_HEIGHT = 60  # 信息栏高度

# 初始化Pygame
pygame.init()
screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE + INFO_HEIGHT))
pygame.display.set_caption('Tic Tac Toe - 井字棋')

# 计算单格尺寸
cell_size = WINDOW_SIZE // BOARD_SIZE

def draw_board(board, fading_piece=None):
    """绘制棋盘和棋子"""
    # 填充背景
    screen.fill(COLORS["BG"])
    x_long = 38
    
    # 绘制网格线（向下偏移 INFO_HEIGHT）
    for i in range(1, BOARD_SIZE):
        pygame.draw.line(screen, COLORS["LINE"],
                         (i * cell_size, INFO_HEIGHT), 
                         (i * cell_size, WINDOW_SIZE + INFO_HEIGHT), 
                         LINE_WIDTH)
        pygame.draw.line(screen, COLORS["LINE"],
                         (0, i * cell_size + INFO_HEIGHT), 
                         (WINDOW_SIZE, i * cell_size + INFO_HEIGHT), 
                         LINE_WIDTH)
    
    # 绘制棋子（需要考虑偏移量）
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            if board[row][col]:
                # 检查是否是即将消失的棋子
                if fading_piece and (row, col, board[row][col]) == fading_piece:
                    draw_fading_piece(board[row][col], row, col)
                else:
                    # 直接绘制棋子（需要加上偏移量）
                    if board[row][col] == 'X':
                        start_pos1 = (col * cell_size + x_long, row * cell_size + x_long + INFO_HEIGHT)
                        end_pos1 = (col * cell_size + cell_size - x_long, 
                                  row * cell_size + cell_size - x_long + INFO_HEIGHT)
                        start_pos2 = (col * cell_size + x_long, 
                                    row * cell_size + cell_size - x_long + INFO_HEIGHT)
                        end_pos2 = (col * cell_size + cell_size - x_long, 
                                  row * cell_size + x_long + INFO_HEIGHT)
                        pygame.draw.line(screen, COLORS["X"], start_pos1, end_pos1, LINE_WIDTH+7)
                        pygame.draw.line(screen, COLORS["X"], start_pos2, end_pos2, LINE_WIDTH+7)
                    else:
                        center = (col * cell_size + cell_size // 2, 
                                row * cell_size + cell_size // 2 + INFO_HEIGHT)
                        pygame.draw.circle(screen, COLORS["O"], center, 
                                        cell_size // 3, LINE_WIDTH)

def fade_in_piece(player, row, col):
    """为棋子添加淡入效果"""
    alpha_surface = pygame.Surface((cell_size, cell_size + INFO_HEIGHT), pygame.SRCALPHA)  # 创建透明表面
    alpha_surface.fill((0, 0, 0, 0))  # 初始化为完全透明
    center = (col * cell_size + cell_size // 2, row * cell_size + cell_size // 2 + INFO_HEIGHT)
    x_long = 38

    for alpha in range(0, 256, 15):  # 逐步增加透明度
        alpha_surface.fill((0, 0, 0, 0))  # 清空表面
        if player == 'X':
            # 绘制 X
            start_pos1 = (x_long, x_long + INFO_HEIGHT)
            end_pos1 = (cell_size - x_long, cell_size - x_long + INFO_HEIGHT)
            start_pos2 = (x_long, cell_size - x_long + INFO_HEIGHT)
            end_pos2 = (cell_size - x_long, x_long + INFO_HEIGHT)
            pygame.draw.line(alpha_surface, COLORS["X"], start_pos1, end_pos1, LINE_WIDTH+7)
            pygame.draw.line(alpha_surface, COLORS["X"], start_pos2, end_pos2, LINE_WIDTH+7)
        elif player == 'O':
            # 绘制 O
            pygame.draw.circle(alpha_surface, COLORS["O"], (cell_size // 2, cell_size // 2 + INFO_HEIGHT), cell_size // 3, LINE_WIDTH)

        alpha_surface.set_alpha(alpha)  # 设置透明度
        screen.blit(alpha_surface, (col * cell_size, row * cell_size))  # 绘制到屏幕
        pygame.display.update()
        pygame.time.delay(30)  # 控制淡入速度

def draw_fading_piece(player, row, col):
    """绘制闪烁的棋子"""
    alpha_surface = pygame.Surface((cell_size, cell_size + INFO_HEIGHT), pygame.SRCALPHA)
    alpha_surface.fill((0, 0, 0, 0))  # 初始化为完全透明
    x_long = 38

    # 使用正弦函数计算透明度，实现平滑的淡入淡出效果
    time = pygame.time.get_ticks() / 500  # 转换为秒
    alpha = int(((math.sin(time * 3) + 1) / 2) * 255)  # 使用正弦函数生成 0-255 之间的值

    if player == 'X':
        # 绘制 X
        start_pos1 = (x_long, x_long + INFO_HEIGHT)
        end_pos1 = (cell_size - x_long, cell_size - x_long + INFO_HEIGHT)
        start_pos2 = (x_long, cell_size - x_long + INFO_HEIGHT)
        end_pos2 = (cell_size - x_long, x_long + INFO_HEIGHT)
        pygame.draw.line(alpha_surface, COLORS["X"], start_pos1, end_pos1, LINE_WIDTH+7)
        pygame.draw.line(alpha_surface, COLORS["X"], start_pos2, end_pos2, LINE_WIDTH+7)
    elif player == 'O':
        # 绘制 O
        pygame.draw.circle(alpha_surface, COLORS["O"], (cell_size // 2, cell_size // 2 + INFO_HEIGHT), cell_size // 3, LINE_WIDTH)

    alpha_surface.set_alpha(alpha)  # 设置透明度
    screen.blit(alpha_surface, (col * cell_size, row * cell_size))  # 绘制到屏幕

def check_win(board, player):
    """检查胜利条件"""
    # 检查行和列
    for i in range(3):
        if all(board[i][j] == player for j in range(3)) or \
           all(board[j][i] == player for j in range(3)):
            return True
    # 检查对角线
    if all(board[i][i] == player for i in range(3)) or \
       all(board[i][2-i] == player for i in range(3)):
        return True
    return False

def show_message(message, board):
    """带动画和交互的弹窗"""
    # 弹窗参数
    popup_width = 400
    popup_height = 200
    final_rect = pygame.Rect(
        (WINDOW_SIZE - popup_width)//2, 
        (WINDOW_SIZE - popup_height)//2,
        popup_width,
        popup_height
    )
    
    # 缩放动画（弹窗出场）
    clock = pygame.time.Clock()
    scale_factor = 0.1
    while scale_factor < 1.0:
        # 更新尺寸
        scale_factor = min(scale_factor + 0.05, 1.0)
        current_rect = final_rect.copy()
        current_rect.width *= scale_factor
        current_rect.height *= scale_factor
        current_rect.center = final_rect.center
        
        # 绘制
        screen.fill(COLORS["BG"])
        draw_board(board)
        
        # 弹窗主体
        pygame.draw.rect(screen, (255, 255, 255), current_rect, border_radius=15)
        pygame.draw.rect(screen, (180, 180, 180), current_rect, 3, border_radius=15)
        
        # 文字渲染
        if scale_factor > 0.7:
            font = pygame.font.SysFont('simhei', int(54 * scale_factor))
            text = font.render(message, True, (0, 0, 0))
            text_rect = text.get_rect(center=current_rect.center)
            text_rect.y -= 15  # 向上移动 15 个单位
            screen.blit(text, text_rect)
        
        pygame.display.update()
        clock.tick(60)

    # 添加交互按钮
    button_rect = pygame.Rect(
        (WINDOW_SIZE-100)//2, 
        (WINDOW_SIZE+100)//2, 
        100, 40
    )
    pygame.draw.rect(screen, (50, 150, 50), button_rect, border_radius=10)
    btn_font = pygame.font.SysFont('simhei', 32)
    btn_text = btn_font.render("确定", True, (255, 255, 255))
    screen.blit(btn_text, (button_rect.x+18, button_rect.y+3))
    pygame.display.update()

    # 等待按钮点击
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    waiting = False
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

    # 缩放动画（弹窗退场）
    scale_factor = 1.0
    while scale_factor > 0.1:
        # 更新尺寸
        scale_factor = max(scale_factor - 0.05, 0.1)
        current_rect = final_rect.copy()
        current_rect.width *= scale_factor
        current_rect.height *= scale_factor
        current_rect.center = final_rect.center
        
        # 绘制
        screen.fill(COLORS["BG"])
        draw_board(board)
        
        # 弹窗主体
        pygame.draw.rect(screen, (255, 255, 255), current_rect, border_radius=15)
        pygame.draw.rect(screen, (180, 180, 180), current_rect, 3, border_radius=15)
        
        # 文字渲染
        if scale_factor > 0.7:
            font = pygame.font.SysFont('simhei', int(54 * scale_factor))
            text = font.render(message, True, (0, 0, 0))
            #text_rect = text.get_rect(center(current_rect.center))
            text_rect.y -= 15  # 向上移动 15 个单位
            screen.blit(text, text_rect)
        
        pygame.display.update()
        clock.tick(60)

def draw_info(current_player):
    """绘制信息栏"""
    # 绘制信息栏背景
    info_rect = pygame.Rect(0, 0, WINDOW_SIZE, INFO_HEIGHT)
    pygame.draw.rect(screen, COLORS["INFO_BG"], info_rect)
    
    # 绘制文本
    font = pygame.font.SysFont('simhei', 36)
    text = font.render(f"当前回合 - {'×' if current_player == 'X' else '○'}", True, COLORS["INFO_TEXT"])
    text_rect = text.get_rect(center=(WINDOW_SIZE // 2, INFO_HEIGHT // 2))
    screen.blit(text, text_rect)

def main():
    board = [[None]*3 for _ in range(3)]
    current_player = 'X'
    game_over = False
    move_count = 0  # 记录落子总数
    piece_positions = []  # 记录所有落子位置和玩家
    fading_piece = None  # 记录即将消失的棋子

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            
            if not game_over and event.type == MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                # 从鼠标的 y 坐标中减去信息栏高度，再计算行号
                y = y - INFO_HEIGHT
                # 只有当点击位置在棋盘范围内时才处理
                if 0 <= x < WINDOW_SIZE and 0 <= y < WINDOW_SIZE:
                    col = x // cell_size
                    row = y // cell_size
                    
                    if board[row][col] is None:
                        board[row][col] = current_player
                        move_count += 1
                        piece_positions.append((row, col, current_player))

                        # 执行淡入效果
                        fade_in_piece(current_player, row, col)

                        # 当落子数达到6个时，开始标记即将消失的棋子
                        if len(piece_positions) >= 6:
                            fading_piece = piece_positions[0]  # 标记最早的棋子

                        # 当落子数达到7个时，开始移除最早的棋子
                        if len(piece_positions) >= 7:
                            oldest_row, oldest_col, _ = piece_positions.pop(0)
                            board[oldest_row][oldest_col] = None  # 确保在board中也移除棋子
                            fading_piece = piece_positions[0] if piece_positions else None

                        # 检查胜负（只检查当前存在的棋子）
                        if check_win(board, current_player):
                            draw_board(board, fading_piece)
                            show_message("×获胜!" if current_player == 'X' else "○获胜!", board)
                            game_over = True
                        else:
                            current_player = 'O' if current_player == 'X' else 'X'

        # 更新画面
        draw_board(board, fading_piece)
        draw_info(current_player)
        pygame.display.update()

        # 游戏结束后重置
        if game_over:
            pygame.time.wait(1000)
            board = [[None]*3 for _ in range(3)]
            current_player = 'X'
            move_count = 0
            piece_positions = []
            fading_piece = None
            game_over = False

if __name__ == "__main__":
    main()