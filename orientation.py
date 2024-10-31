import time
import threading
from icm20948 import ICM20948 
import numpy as np

GRAVITY_CONSTANT = 9.80665 # en m/s
TIME_INTERVAL = 0.05 # 50 ms
BIAS_SAMPLES = 100 # Nombre de mesure a prendre pour la moyenne de biais

class Orientation:
    def __init__(self):
        self.__imu = ICM20948()
        self.__ax, self.__ay, self.__az, self.__gx, self.__gy, self.__gz = self.__imu.read_accelerometer_gyro_data() 
        self.__mx, self.__my, self.__mz = self.__imu.read_magnetometer_data()
        self.__vx, self.__vy, self.__vz = 0, 0, 0  # vitesse Initiale
        self.__x, self.__y, self.__z = 0, 0, 0     # position initiale
        self.__ax_bias, self.__ay_bias, self.__az_bias = 0, 0, 0 #initialisation des biais
        self.__gx_bias, self.__gy_bias, self.__gz_bias = 0, 0, 0
        self.__angleX = 0
        self.__angleY = 0
        self.__angleZ = 0
        self.__deltatime = 0
        self.__initial_time = 0
        self.__end_time = 0
        self.__state = "immobile"
        self.__state_rotation = ""
        self.__running = True
        self.thread = threading.Thread(target=self.update_orientation)
        self.thread.start()
    
    #region getters and setters
    def get_state(self):
        return self.__state

    def set_state(self, new_state):
        if new_state in ["immobile", "rotation"]:
            self.__state = new_state
        else:
            raise ValueError("Invalid state. Must be 'immobile' or 'rotation'.")

    def get_state_rotation(self):
        return self.__state_rotation

    def set_state_rotation(self, new_state_rotation):
        self.__state_rotation = new_state_rotation

    def get_running(self):
        return self.__running

    def set_running(self, new_running):
        if isinstance(new_running, bool):
            self.__running = new_running
        else:
            raise ValueError("Running must be a boolean value.")
    
    def get_biases(self):
        return {
            'ax_bias': self.__ax_bias, 'ay_bias': self.__ay_bias, 'az_bias': self.__az_bias,
            'gx_bias': self.__gx_bias, 'gy_bias': self.__gy_bias, 'gz_bias': self.__gz_bias
        }
    def reset_timer(self):
        self.__initial_time = 0
        self.__end_time = 0
    #endregion
    
    #region Orientation Calculations
    def update_orientation(self):
        previous_ax, previous_ay, previous_az, previous_gx, previous_gy, previous_gz = 0, 0, 0, 0, 0, 0
        while self.__running:
            self.__initial_time = time.time()
            ax, ay, az, gx, gy, gz = self.__imu.read_accelerometer_gyro_data()
            if self.__state == "immobile":
                self.calculate_bias()
            elif self.__state == "rotation":
                #il faut corriger les valeurs, car le gyroscope continu de lire des valeurs minuscules, même quand arrêté
                gx_corrected = gx - self.__gx_bias
                gy_corrected = gy - self.__gy_bias
                gz_corrected = gz - self.__gz_bias
                ax_corrected = ax - self.__ax_bias
                ay_corrected = ay - self.__ay_bias
                az_corrected = az - self.__az_bias
                
                self.calculate_velocity_position(ax_corrected, ay_corrected, az_corrected, previous_ax, previous_ay, previous_az, 
                                                 gx_corrected, gy_corrected, gz_corrected)
                
                previous_ax, previous_ay, previous_az = ax, ay, az
                previous_gx, previous_gy, previous_gz = gx, gy, gz
            self.calculate_orientation(previous_gx, previous_gy, previous_gz)
            self.__end_time = time.time()
            self.__deltatime = self.__end_time - self.__initial_time
            self.reset_timer() 
            time.sleep(TIME_INTERVAL)

    def calculate_orientation(self, previous_gx, previous_gy, previous_gz):
        self.__angleX += self.__deltatime * (self.__gx + previous_gx) / 2
        self.__angleY += self.__deltatime * (self.__gy + previous_gy) / 2
        self.__angleZ += self.__deltatime * (self.__gz + previous_gz) / 2
    
    def calculate_velocity_position(self, ax, ay, az, prev_ax, prev_ay, prev_az, prev_gx, prev_gy, prev_gz):
        self.__vx += self.__deltatime * ((ax + prev_ax) / 2) * GRAVITY_CONSTANT
        self.__vy += self.__deltatime * ((ay + prev_ay) / 2) * GRAVITY_CONSTANT
        self.__vz += self.__deltatime * ((az + prev_az) / 2) * GRAVITY_CONSTANT
        
        self.__x += self.__deltatime * ((self.__vx + (self.__vx - self.__deltatime * ((ax + prev_ax) / 2) * GRAVITY_CONSTANT)) / 2)
        self.__y += self.__deltatime * ((self.__vy + (self.__vy - self.__deltatime * ((ay + prev_ay) / 2) * GRAVITY_CONSTANT)) / 2)
        self.__z += self.__deltatime * ((self.__vz + (self.__vz - self.__deltatime * ((az + prev_az) / 2) * GRAVITY_CONSTANT)) / 2)
        
        return {
            'vx': self.__vx, 'vy': self.__vy, 'vz': self.__vz,
            'x': self.__x, 'y': self.__y, 'z': self.__z
        }
        
    def calculate_bias(self):
        ax_sum, ay_sum, az_sum = 0, 0, 0
        gx_sum, gy_sum, gz_sum = 0, 0, 0
        
        for i in range(BIAS_SAMPLES):
            ax, ay, az, gx, gy, gz = self.__imu.read_accelerometer_gyro_data()

            ax_sum += ax
            ay_sum += ay
            az_sum += az
            gx_sum += gx
            gy_sum += gy
            gz_sum += gz
            
            # time.sleep(0.01) #Je ne sais pas si c'est nécessaire de faire un sleep icitte
        
        # Calculer la moyenne des biais
        self.__ax_bias = ax_sum / BIAS_SAMPLES
        self.__ay_bias = ay_sum / BIAS_SAMPLES
        self.__az_bias = az_sum / BIAS_SAMPLES
        self.__gx_bias = gx_sum / BIAS_SAMPLES
        self.__gy_bias = gy_sum / BIAS_SAMPLES
        self.__gz_bias = gz_sum / BIAS_SAMPLES    
    #endregion