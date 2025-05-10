from random import randrange

class Anim:
    def __init__(self, name, iter):
        self.name, self.iter = name, iter


class AnimStatic(Anim):
    # deprecated function
    def __init__(self, name, iter):
        super(AnimStatic, self).__init__(name, iter)

    def __repr__(self):
        return f"Static({self.name},{self.iter})"


class AnimMove(Anim):
    def __init__(self, name, iter, from_iter):
        super(AnimMove, self).__init__(name, iter)
        self.from_iter = from_iter

    def __repr__(self):
        return f"Move({self.name},{self.from_iter}->{self.iter})"


class AnimMerge(Anim):
    def __init__(self, name, iter):
        super(AnimMerge, self).__init__(name, iter)

    def __repr__(self):
        return f"Merge({self.name},{self.iter})"




class AnimAppear(Anim):
    def __init__(self, name, iter):
        super(AnimAppear, self).__init__(name, iter)

    def __repr__(self):
        return f"Appear({self.name},{self.iter})"
class Core:
    def __init__(self, type_iter: type, side_iters: list, valid, keys: dict, size: int):
        """
        type_iter: 迭代器类型
        side_iter: 迭代器的邻居们
        valid: 是否合法
        size: 生成大小
        """
        self.type_iter = type_iter
        self.side_iters = side_iters
        self.keys = keys
        self.valid = valid
        self.size = size
        self.board = [[[None, False] for _ in range(size)] for _ in range(size)]
        self.score=0
        self.trav_iters = [[type_iter(i, j) for i in range(size) for j in range(size)
                            if valid(type_iter(i, j), self.size) and not valid(type_iter(i, j) + add_iter, self.size)]
                           for add_iter in side_iters]
        self.lst_anims = [[]]
        self.nxt_anims = [[]]

    def __getitem__(self, iter):
        return self.board[iter[0]][iter[1]]

    def __setitem__(self, iter, value: list):
        self.board[iter[0]][iter[1]] = value

    def __str__(self):
        return "----------\n" + "\n".join([",".join(
            ["%4d" % (self[i, j][0] if self[i, j][0] is not None else 0 if self.valid(self.type_iter(i, j),
                                                                                      self.size) else -1) for
             i in range(self.size)])
            for j in range(self.size - 1, -1, -1)]) + "\n----------"

    def __repr__(self):
        return "Game2048(type_iter:%s game_size:%d)" % (self.type_iter, self.size)

    def move_once(self, add_iter,force_anim=False):
        moved = False
        tmp_anim_moves = []
        tmp_anim_merges = []
        for trav_iter in self.trav_iters[self.side_iters.index(add_iter)]:
            to_iter = self.type_iter(trav_iter)
            from_iter = to_iter - add_iter
            if self[to_iter][0] is not None:
                tmp_anim_moves.append(AnimStatic(self[to_iter][0],to_iter))
            while self.valid(from_iter, self.size):
                if self[from_iter][0] is not None:
                    if self[to_iter][0] is None:
                        tmp_anim_moves.append(AnimMove(self[from_iter][0], to_iter, from_iter))
                        self[to_iter] = [self[from_iter][0], False]
                        self[from_iter] = [None, False]
                        moved = True
                    elif self[to_iter][0] == self[from_iter][0] and not (self[to_iter][1] or self[from_iter][1]):
                        tmp_anim_moves.append(AnimMove(self[from_iter][0], to_iter, from_iter))
                        self[to_iter] = [self[to_iter][0] + self[from_iter][0], True]
                        self.score+=self[to_iter][0]
                        self[from_iter] = [None, False]
                        tmp_anim_merges.append(AnimMerge(self[to_iter][0], to_iter))
                        moved = True
                    else:
                        tmp_anim_moves.append(AnimStatic(self[from_iter][0],from_iter))

                to_iter, from_iter = from_iter, from_iter - add_iter
        if moved or force_anim:
            self.nxt_anims[-1].extend(tmp_anim_moves)
            self.nxt_anims.append(tmp_anim_merges)
        return moved

    def move(self, add_iter):
        self.nxt_anims = [[]]
        for i in range(self.size):
            for j in range(self.size):
                self[i, j][1] = False
        moved = False
        for i in range(self.size):
            moved = self.move_once(add_iter,i==self.size-1) or moved
        self.nxt_anims.pop(-1)
        if moved:
            # print(self.nxt_anims)
            self.lst_anims = self.nxt_anims
            self.nxt_anims = [[]]

        return moved

    def user_move(self, add_iter):
        if self.move(add_iter):
            self.gen_new()
            # print(self.lst_anims)
            return True
        return False

    def check(self):
        for i in range(self.size):
            for j in range(self.size):
                if self.valid(self.type_iter(i, j), self.size):
                    if self[i, j][0] is None:
                        return True
                    for add_iter in self.side_iters:
                        if self.valid(self.type_iter(i, j) + add_iter, self.size):
                            if self[i, j][0] == self[self.type_iter(i, j) + add_iter][0]:
                                return True
        return False

    def gen_new(self):
        if self.check():
            usable = [self.type_iter(i, j) for i in range(self.size) for j in range(self.size) if (
                    self.valid(self.type_iter(i, j), self.size) and self[i, j][0] is None)]
            choice = usable[randrange(0, len(usable))]
            # print(choice)
            self[choice][0] = 2 if randrange(0, 5) else 4
            self.lst_anims[-1].append(AnimAppear(self[choice][0], choice))

    def copy(self):
        return Core(self.type_iter,self.side_iters,self.valid,self.keys,self.size)
