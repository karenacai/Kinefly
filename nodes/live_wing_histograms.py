#!/usr/bin/env python
import roslib; roslib.load_manifest('StrokelitudeROS')
import rospy

import time

import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy
np = numpy

from StrokelitudeROS.srv import *

class Live_Plotter:
    
    def __init__(self):
        
        rospy.init_node('liveplotter', anonymous=True)
        
        # right wing
        service_name = "wing_intensity_right"
        rospy.wait_for_service(service_name)
        self.get_wing_intensity_right = rospy.ServiceProxy(service_name, float32list)
        
        service_name = "wing_bins_right"
        rospy.wait_for_service(service_name)
        self.get_wing_bins_right = rospy.ServiceProxy(service_name, float32list)
        
        service_name = "wing_edges_right"
        rospy.wait_for_service(service_name)
        self.get_wing_edges_right = rospy.ServiceProxy(service_name, float32list)
        
        # left wing
        service_name = "wing_intensity_left"
        rospy.wait_for_service(service_name)
        self.get_wing_intensity_left = rospy.ServiceProxy(service_name, float32list)
        
        service_name = "wing_bins_left"
        rospy.wait_for_service(service_name)
        self.get_wing_bins_left = rospy.ServiceProxy(service_name, float32list)
        
        service_name = "wing_edges_left"
        rospy.wait_for_service(service_name)
        self.get_wing_edges_left = rospy.ServiceProxy(service_name, float32list)
        
        #
        
        self.last_update = time.time()
        
        # live plot
        self.fig = plt.figure()
        self.bins_right = self.get_wing_bins_right(1).data
        self.bins_left = self.get_wing_bins_left(1).data
        self.limits_right = [-np.pi, np.pi]
        self.limits_left = [-np.pi, np.pi]
        self.edges_right = [-np.pi, np.pi]
        self.edges_left = [-np.pi, np.pi]
        
        data_right = np.random.random(len(self.bins_right))
        data_left = np.random.random(len(self.bins_left))
        
        colorRight = 'red'
        colorLeft = 'green'
        
        self.line_right, = plt.plot(self.bins_right, data_right, '.', color=colorRight)
        self.line_left, = plt.plot(self.bins_left, data_left, '.', color=colorLeft)
        self.line_lo, = plt.plot([self.limits_right[0], self.limits_right[0]], [0,200], color='black', linewidth=2)
        self.line_hi, = plt.plot([self.limits_right[1], self.limits_right[1]], [0,200], color='black', linewidth=2)
        
        self.line_trailing_right, = plt.plot([self.edges_right[0], self.edges_right[0]], [0,200], color=colorRight, linewidth=2)
        self.line_leading_right, = plt.plot([self.edges_right[1], self.edges_right[1]], [0,200], color=colorRight, linewidth=2)
        
        self.line_trailing_left, = plt.plot([self.edges_left[0], self.edges_right[0]], [0,200], color=colorLeft, linewidth=2)
        self.line_leading_left, = plt.plot([self.edges_left[1], self.edges_left[1]], [0,200], color=colorLeft, linewidth=2)
        
        #plt.ylim(0.1, 0.1)
        plt.ylim(0,200)
        #plt.autoscale(True)
                
        self.image_animation = animation.FuncAnimation(self.fig, self.update_line, self.bins_right, init_func=self.init_plot, interval=50, blit=True)
        
        plt.show()
        
        
    def update_line(self, i):
        try:
            if time.time() - self.last_update > 1:
                self.bins_right = self.get_wing_bins_right(1).data
                self.bins_left = self.get_wing_bins_left(1).data
                
                self.limits_right = [rospy.get_param('strokelitude/right/angle_lo'), rospy.get_param('strokelitude/right/angle_hi')]
                self.limits_left = [rospy.get_param('strokelitude/left/angle_lo'), rospy.get_param('strokelitude/left/angle_hi')]
                self.last_update = time.time()
                
            data_right = self.get_wing_intensity_right(1).data
            data_left = self.get_wing_intensity_left(1).data
            
            self.edges_right = self.get_wing_edges_right(1).data
            self.edges_left = self.get_wing_edges_left(1).data
            
            if data_right is not None:
                self.line_right.set_data(self.bins_right, data_right)
            if data_left is not None:
                self.line_left.set_data(self.bins_left, data_left)
            self.line_lo.set_data([self.limits_right[0], self.limits_right[0]], [0,200])
            self.line_hi.set_data([self.limits_right[1], self.limits_right[1]], [0,200])
            
            self.line_trailing_right.set_data([self.edges_right[0], self.edges_right[0]], [0,200])
            self.line_leading_right.set_data([self.edges_right[1], self.edges_right[1]], [0,200])
            
            self.line_trailing_left.set_data([self.edges_left[0], self.edges_left[0]], [0,200])
            self.line_leading_left.set_data([self.edges_left[1], self.edges_left[1]], [0,200])
        except:
            pass
            
        return self.line_right, self.line_left, self.line_lo, self.line_hi, self.line_trailing_right, self.line_leading_right, self.line_trailing_left, self.line_leading_left
        
    def init_plot(self): # required to start with clean slate
        self.line_right.set_data([],[])
        self.line_left.set_data([],[])
        self.line_hi.set_data([],[])
        self.line_lo.set_data([],[])
        self.line_trailing_right.set_data([],[])
        self.line_leading_right.set_data([],[])
        self.line_trailing_left.set_data([],[])
        self.line_leading_left.set_data([],[])
        return self.line_right, self.line_left, self.line_lo, self.line_hi, self.line_trailing_right, self.line_leading_right, self.line_trailing_left, self.line_leading_left
        

if __name__ == '__main__':
    live_plotter = Live_Plotter()
