from libs.Crane import Crane
from libs.object import object
from numpy import deg2rad, rad2deg
Model = Crane()
print(object.sim.getObjectFloatParam(object.sim.jointfloatparam_upper_limit, Model.XY.handle))
object.sim.startSimulation()
Model.XY.setVelocity(5)
while Model.XY.getPosition() < 90 : pass
object.sim.stopSimulation()
