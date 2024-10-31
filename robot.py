from motor import Motor
from window import Window
from orientation import Orientation
import cv2
FORWARD_KEY = 'w'
BACKWARD_KEY = 's'
RIGHT_TURN_KEY = 'd'
LEFT_TURN_KEY = 'a'
BRAKE_KEY = ' '
STOP_KEY = 'x'
SPEED_UP_KEY = '.'
SPEED_DOWN_KEY = ','
FORWARD_LEFT_KEY = 'q'
FORWARD_RIGHT_KEY = 'e'
FORWARD_DISTANCE = 'p'

class Robot:
    IN1 = 8 #Sonar gauche trigger
    IN2 = 25 #Sonar gauche echo
    IN3 = 21 #Sonar droite trigger
    IN4 = 20 #Sonar droite echo
    
    IN5 = 10 #Del jaune
    IN6 = 9 #Del Verte
    
    IN7 = 27 #Encodeur Gauche
    IN8 = 22 # Encodeur Droite
    FONT = cv2.FONT_HERSHEY_SIMPLEX
    def __init__(self):
        self.arret = False
        self.moteur = Motor()
        self.orentation = Orientation()
    
    def start_program(self):
        while not self.arret:
            key = cv2.waitKey(100)

            if key==ord(FORWARD_KEY):
                self.avancer()
            elif key==ord(BACKWARD_KEY):
                self.reculer()
            elif key==ord(LEFT_TURN_KEY):
                self.tourner_gauche()
            elif key==ord(RIGHT_TURN_KEY):
                self.tourner_droite()
            elif key==ord(BRAKE_KEY):
                self.freiner()
            elif key==ord(SPEED_UP_KEY):
                self.augmenter()
            elif key==ord(SPEED_DOWN_KEY):
                self.diminuer()
            elif key==ord(STOP_KEY):
                self.stop()
                self.arret = True
            elif key==ord(FORWARD_LEFT_KEY):
                self.avancer_gauche()
            elif key==ord(FORWARD_RIGHT_KEY):
                self.avancer_droite()
            elif key==ord(FORWARD_DISTANCE):
                self.move_by_meter()
                
            self.window.display()
            
    def avancer(self):
        self.moteur.change_normal_speed()
        self.moteur.move(1,1,0,0)
        self.orentation.set_state("rotation")

    def reculer(self):
        self.moteur.change_normal_speed()
        self.moteur.move(0,0,1,1)
        self.orentation.set_state("rotation")


    def tourner_droite(self):
        self.moteur.change_turn_speed()
        self.moteur.move(1,0,0,1)
        self.orentation.set_state("rotation")

    def tourner_gauche(self):
        self.moteur.change_turn_speed()
        self.moteur.move(0,1,1,0)
        self.orentation.set_state("rotation")

    
    def avancer_droite(self):
        self.moteur.change_normal_speed()
        self.moteur.move(1,1,0,1)
        self.orentation.set_state("rotation")

        
    def avancer_gauche(self):
        self.moteur.change_normal_speed()
        self.moteur.move(1,1,1,0)
        self.orentation.set_state("rotation")

    def freiner(self):
        self.moteur.move(0,0,0,0)
        self.orentation.set_state("immobile")

    def augmenter(self):
        self.moteur.change_normal_speed()
        self.moteur.speed_up()

    def diminuer(self):
        self.moteur.change_normal_speed()
        self.moteur.speed_down()

    def stop(self):
        self.moteur.stop_motors()
        self.orentation.set_state("immobile")

            