import main
import data as d
import os

if __name__ == '__main__':
    os.environ['SDL_VIDEO_WINDOW_POS'] = str(350) + "," + str(40)
    d.main = main.Main()
    d.main.main()