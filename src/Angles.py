import math

class turret:
    def __init__(self, obj_x, obj_y, obj_z):
        self.obj_x = obj_x
        self.obj_y = obj_y
        self.obj_z = obj_z
        self.x_fromTurret = 0
        self.y_fromTurret = 0
        self.z_fromTurret = 0
        self.dir_x = "R"
        self.dir_y = "T"

    def offsets(self, offs_x=0, offs_y=0, offs_z=0):
        self.offs_x = offs_x
        self.offs_y = offs_y
        self.offs_z = offs_z


    def getAngles(self):
        # Z axis
        self.z_fromTurret = self.obj_z - self.offs_z

        # X axis
        # object on right
        if self.obj_x > 0:
            self.dir_x = "R"
            self.x_fromTurret = abs(self.obj_x) + self.offs_x

        # object on left
        if self.obj_x < 0:
            self.dir_x = "L"
            self.x_fromTurret = abs(self.obj_x) - self.offs_x

        # theta X
        self.theta_x = (math.atan(self.x_fromTurret/self.z_fromTurret))*(180/math.pi)
        if self.dir_x == "R":
            self.theta_x = 90 + self.theta_x
        if self.dir_x == "L":
            self.theta_x = 90 - self.theta_x

        # Y axis
        # object on top
        if self.obj_y > 0:
            self.dir_y = "T"
            self.y_fromTurret = abs(self.obj_y) - self.offs_y

        # object on bottom
        if self.obj_y < 0:
            self.dir_y = "B"
            self.y_fromTurret = abs(self.obj_y) + self.offs_y

        # theta Y
        self.theta_y = (math.atan(self.y_fromTurret/self.z_fromTurret))*(180/math.pi)
        if self.dir_y == "T":
            self.theta_y = 90 - self.theta_y
        if self.dir_y == "B":
            self.theta_y = 90 + self.theta_y

    def getTheta_x(self):
        return self.theta_x
    def getTheta_y(self):
        return self.theta_y
