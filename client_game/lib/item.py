from lib.gameObject import gameObject

class item(gameObject):
    def __init__(self, x, y):
        gameObject.__init__(self, x, y)
        self.kill = False
        self.dist = 100
        self.visible = True