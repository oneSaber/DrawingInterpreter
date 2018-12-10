import matplotlib.pyplot as plt
import numpy as np

class DrawPricture:

    def __init__(self):
        self.origin_x = 0
        self.origin_y = 0
        self.scale_x = 1
        self.scale_y = 1
        self.rot = 0
        self.create_rot_matrix()
        self.min = 1000000
        self.max = -100000
        self.position_list = []
    # 配置全局设置
    def set_origin(self,x=0,y=0):
        self.origin_x = x
        self.origin_y = y
    def set_scale(self,x=1,y=1):
        self.scale_x = x
        self.origin_y = y
    def set_rot(self,rot = 0):
        self.rot = rot
        self.create_rot_matrix()
    
    # 对坐标矩阵进行缩放
    def scalex(self,x):
        return x * self.scale_x
    def scaley(self,y):
        return y * self.scale_y

    # 生成旋转矩阵
    def create_rot_matrix(self):
        self.rot_matrix = np.array([[np.cos(self.rot),-np.sin(self.rot)],[np.sin(self.rot),np.cos(self.rot)]])

    # 设定坐标轴大小
    def draw(self):
        for (pos,color) in self.position_list:
            plt.plot(pos[0],pos[1],color)
        plt.show()
    # x,y are postion of x,y
    def set_picture(self,x,y,color='black'):
        if end == 0:
            print("must have end!")
            return
        T = np.linspace(start,end,(end-start)/step * 50)
        # 然后进行缩放
        x = self.scalex(x)
        y = self.scaley(y)
        # 将x和y坐标矩阵组合成一个矩阵
        origin_postion = np.array([x,y])
        # 对坐标矩阵进行旋转，因为是二维的所以用
        # [[cos(rot),-sin(rot)],[sin(rot),cos(rot)]]
        # 这个矩阵就可以了
        rot_postion = np.matmul(self.rot_matrix,origin_postion)
        #  把该图形的矩阵加入到列表中
        self.position_list.append((rot_postion,color))

def x_expr1(T,origin_x):
    return T+origin_x
def y_expr1(T,origin_y):
    return T+origin_y
def x_expr2(T,origin_x):
    return np.cos(T)
def y_expr2(T,origin_y):
    return np.sin(T)

if __name__ == "__main__":
    dp = DrawPricture()
    dp.set_picture(np.pi/50,x_expr1,y_expr1,0,2*np.pi,color="red")
    dp.set_picture(np.pi/50,x_expr2,y_expr2,0,2*np.pi,color="blue")
    dp.draw()
    
