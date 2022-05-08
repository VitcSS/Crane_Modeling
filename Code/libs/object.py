from libs.zmqRemoteApi import RemoteAPIClient
import numpy as np
import cv2
# Define the template class :
class object:
    sim = RemoteAPIClient().getObject('sim')
    def __init__(self,alias : str):
        self.handle = self.sim.getObject(alias)
        self.alias = alias

# Define the template joint class :
class joint(object):
    def __init__(self, alias: str, V_m = np.inf):
        super().__init__(alias)
        if V_m < 0:
            self.V_max = -V_m
            self.V_min = V_m
        else :
            self.V_max = V_m
            self.V_min = -V_m

    # Get the current position of the joint as property :
    def getPosition(self):
        return self.sim.getJointPosition(self.handle)

    # Set the desired velocity for the joint :
    def setVelocity(self, Vel = 0):
        if Vel < self.V_min:
            print("Velocity out of limits, changed to minimum")
            Vel = self.V_min
        elif Vel > self.V_max:
            print("Velocity out of limits, changed to maximum")
            Vel = self.V_max
        self.sim.setJointTargetVelocity(self.handle, Vel)

    # Set the desired position for the joint
    def setPosition(self,pos = 0):
        self.sim.setJointTargetPosition(self.handle,pos)
        
# Define class for the prismatic joint for the sake of parity : 
class Prismatic(joint):
    def __init__(self, alias: str, V_m=np.inf):
        super().__init__(alias, V_m)

# Define class for the revolute joint :
class Revolute(joint):
    # Change limiter input to rads:
    def __init__(self, alias: str, V_m=360):
        super().__init__(alias, np.deg2rad(V_m))

    def setVelocity(self, Vel=0):
        return super().setVelocity(np.deg2rad(Vel))

    def getPosition(self):
        return np.deg2rad(super().getPosition)
    
    def setPosition(self, pos=0):
        pos = np.deg2rad(pos)
        return super().setPosition(pos)

# Define class for use a Ray type proximity sensor :
class Ray_Sensor(object):
    def __init__(self, alias: str):
        super().__init__(alias)
    # Return the distance and handle of the closest object, if it exists one :
    def detect(self):
        self.sim.checkProximitySensor(self.handle, self.sim.handle_all)
        result = None
        try :
            result,distance,_,handle,_ = self.sim.readProximitySensor(self.handle)
        except :
            result = self.sim.readProximitySensor(self.handle)
        if result == 1:
            return distance, handle
        else:
            return np.inf

# Define class for use a vision sensor :
class Vision_Sensor(object):

    def __init__(self, alias: str):
        super().__init__(alias)

    # Return a array-like image based on the vision sensor specs :
    @property
    def get_image(self):
        img, resX, resY = self.sim.getVisionSensorCharImage(self.handle)
        img = np.frombuffer(img, dtype=np.uint8).reshape(resY, resX, 3)
        img = cv2.flip(cv2.cvtColor(img, cv2.COLOR_BGR2RGB), 0)
        return img

class Magnet(object):

    def __init__(self, alias: str, sensor : str = '/Link', distance : str = '/Finder'):
        super().__init__(alias)
        self.F_sensor = object(sensor)
        self.Ray = Ray_Sensor(distance)

    def find(self):
        try :
            _,target = self.Ray.detect()
            return target
        except :
            return None
    def has_something(self):
        if self.sim.getObjectChild(self.F_sensor.handle,0) != -1: 
            return True
        else : 
            return False
    def on(self):
        target = self.find()
        if target != None:
            self.sim.setObjectParent(target, self.F_sensor.handle, True)
    
    def off(self):
        if self.has_something() == True:
            self.sim.setObjectParent(self.sim.getObjectChild(self.F_sensor.handle,0),-1,True)


