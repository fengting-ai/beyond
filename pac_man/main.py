import os
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

print("[1] 开始导入模块")
try:
    from .game_manager import GameManager
    from .strategies import ChaseGhostBrain, GreedyPacManBrain
    from .config import config
except ImportError:
    from game_manager import GameManager
    from strategies import ChaseGhostBrain, GreedyPacManBrain
    from config import config
    from student_bots import StudentPacMan,StudentGhost
print("[2] 模块导入完成")
import cv2
import time
print("[3] cv2、time 导入完成")

print("[4] 准备初始化 GameManager")
gamemanager = GameManager(
    pacman_brain=StudentPacMan(),
    ghost_brains=[StudentGhost()],
)
print("[5] GameManager 初始化完毕")


def main():
    print("[6] 进入 main()，准备创建 cv2 窗口")
    cv2.namedWindow(config.window_name, cv2.WINDOW_AUTOSIZE)
    print("[7] cv2.namedWindow 创建成功")

    last = time.time()
    print("[7.1] 检查 config.is_end = ", config.is_end)
    while not config.is_end:
        key = cv2.waitKey(1) & 0xFF
        if key == 27:
            cv2.destroyAllWindows()
            return

        gamemanager.on_input(key)
        now = time.time()
        delta = now - last

        if delta <= 1 / config.fps:
            time.sleep(1 / config.fps - delta)
            gamemanager.on_update(1 / config.fps)
        else:
            gamemanager.on_update(delta)

        last = time.time()
        frame = gamemanager.on_render()
        cv2.imshow(config.window_name, frame)

    frame = gamemanager.show_win()
    cv2.imshow(config.window_name, frame)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    print("[8] 调用 main()")
    main()
