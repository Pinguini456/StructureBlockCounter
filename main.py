from window import *
import os



def main():
    try:
        os.mkdir('SavedBuilds')
    except FileExistsError:
        print("")


    root = InputWindow()
    root.mainloop()


if __name__ == "__main__":
    main()








