
class shape(object):
    """
    图形类
    """
    def __init__(self, poses):
        self._poses = poses
        self.max_x = -0xffff
        self.max_y = -0xffff
        self.min_x = 0xffff
        self.min_y = 0xffff
        self._edges = []
        self.N = len(poses)
        # 至少三个点
        assert (self.N >= 3)
        # 最小外接矩形
        for i in range(len(self._poses)):
            self.max_x = max(self._poses[i][0], self.max_x)
            self.max_y = max(self._poses[i][1], self.max_y)
            self.min_x = min(self._poses[i][0], self.min_x)
            self.min_y = min(self._poses[i][1], self.min_y)
            self._edges.append((self._poses[i], self._poses[(i+1)%self.N]))

    def get_max_pair(self):
        assert (self.max_x > -0xffff and self.max_y > -0xffff)
        return self.max_x, self.max_y
    def get_min_pair(self):
        assert (self.min_x < 0xffff and self.min_y < 0xffff)
        return self.min_x, self.min_y
    def get_poses(self):
        return self._poses
    def get_edges(self):
        return self._edges

def input_poses(n):
    """
    输入函数
    :param n: 边数
    :return: 点坐标list
    """
    poses = []
    for i in range(n):
        line = input().replace(" ", "").split(",")
        poses.append((int(line[0],10), int(line[1],10)))
    return poses

def judge_point_in(pos, shape):
    """
    判断点是否在内部
    :param pos: 点坐标
    :param shape: 形状
    :return:
    """
    x_max, y_max = shape.get_max_pair()
    x_min, y_min = shape.get_min_pair()

    if pos[0] >= x_min and pos[0] <= x_max and \
        pos[1] <= y_max and pos[1] >= y_min:

        edges = shape.get_edges()
        cnt = 0
        for edge in edges:
            Maxx = edge[0][0] if edge[0][0] > edge[1][0] else edge[1][0]
            Maxy = edge[0][1] if edge[0][1] > edge[1][1] else edge[1][1]
            Minx = edge[0][0] if edge[0][0] < edge[1][0] else edge[1][0]
            Miny = edge[0][1] if edge[0][1] < edge[1][1] else edge[1][1]
            if pos[0] > Maxx or pos[1] > Maxy or pos[1] < Miny:
                pass
            else:
                cnt += 1
            if (cnt & 0x1) == 1:
                return True
    return False

"""
exp1:
2,1
3,4
4,2

0,1
0,4
2,5
4,4
4,1

不在

exp2:
2,1
3,4
4,2

0,0
0,4
2,5
4,4
5,1

不在

"""

def judge_outer_contour(shape_3, shape_5):
    """
    判断边界轮廓问题
    :param shape_3: 三角形
    :param shape_5: 五边形
    :return: ...
    """
    x_max_3, y_max_3 = shape_3.get_max_pair()
    x_min_3, y_min_3 = shape_3.get_min_pair()

    x_max_5, y_max_5 = shape_5.get_max_pair()
    x_min_5, y_min_5 = shape_5.get_min_pair()

    if x_max_3 < x_max_5 and \
        x_min_3 > x_min_5 and \
        y_max_3 < y_max_5 and \
        y_min_3 > y_min_5:

        poses = shape_3.get_poses()
        for pos in poses:
            if judge_point_in(pos, shape_5) is False:
                print("error! 三角形不在五边形内!")
        print("三角形在五边形内！")
    else:
        print("error! 三角形不在五边形内!")

if __name__ == '__main__':
    print("usage:\n" + \
          "4,5回车\n" + \
          "0,0回车\n" + \
          "1,1回车\nover...\n" + \
          "connection sequence is (4,5)-(0,0)-(1,1)-[4,5]")
    print("输入三角形的边:\n")
    triangle = shape(input_poses(3))

    print("输入五边形坐标:\n")
    pentagon = shape(input_poses(5))

    judge_outer_contour(triangle, pentagon)

    print("over")
