import cv2
from cvzone.HandTrackingModule import HandDetector



class Button:
    def __init__(self,pos,width,height,value):
        self.pos = pos
        self.width = width
        self.height = height
        self.value = value
    def draw(self,img):
        width = self.width + self.pos[0]
        height = self.height + self.pos[1]
        cv2.rectangle(img,self.pos,(width,height),(225,225,225),cv2.FILLED)
        cv2.rectangle(img,self.pos,(width,height),(50,50,50),2) 
        cv2.putText(img,self.value,(int(width * 0.91),int(height*0.9)),cv2.FONT_HERSHEY_PLAIN,2,(50,50,50),2)
    def check_click(self,x,y):
        if self.pos[0] < x < self.pos[0] + self.width and self.pos[1] < y < self.pos[1] + self.height:
            return True
        return False

cap = cv2.VideoCapture(0)
cap.set(3,2000) #width
cap.set(4,1000)#height
detect = HandDetector(detectionCon=0.8,maxHands=1)


button_list = []


ypos = 100
SQUARE_SIZE = 70
buttons = [["7",'8','9','*'],

['4','5','6','-'],
['3','2','1','+'],
['0','/','C','=']
]

equation = ""

for x in range(4):
    xpos = 230
    for y in range(4):
        xpos = xpos + SQUARE_SIZE #320
        button1 = Button((xpos,ypos),SQUARE_SIZE,SQUARE_SIZE,buttons[x][y])

        button_list.append(button1)

    ypos += SQUARE_SIZE


screenx = 230+SQUARE_SIZE
screeny = 25
screenWidth = screenx + SQUARE_SIZE*4
screenHeight = 30+SQUARE_SIZE


one_tap = True
operations = ["+","-","*","/"]


def perform_operation():
    global equation
    equation_list = equation.split(" ")
    current_operation = ""
    a = 0
    print(equation_list)
    for equ in equation_list:
        if equ != "":
            if equ in operations:
                current_operation = equ
            elif a == 0:
                a = int(equ)
            else:
                b = int(equ)
                if current_operation == "+":
                    a = a+b
                elif current_operation == "-":
                    a = a-b
                elif current_operation == "*":
                    a = a*b
                elif current_operation == "/":
                    a = a/b
    return a
    


    
    
while True:
    success,img = cap.read()
    img = cv2.flip(img,1)

    hands, img = detect.findHands(img,flipType=False)
    

    #draw screen
    cv2.rectangle(img,(screenx,screeny),(screenWidth,screenHeight),(225,225,225),cv2.FILLED)
    cv2.rectangle(img,(screenx,screeny),(screenWidth,screenHeight),(50,50,50),2)

    
    #draw buttons
    for button in button_list:
        button.draw(img)

    #processing
    if hands:
        lmlist = hands[0]['lmList']
        length,_,img = detect.findDistance(lmlist[8],lmlist[12],img)
        x,y = lmlist[8]
        #print(length)
        if length < 18 and one_tap:
            one_tap = False
            for button in button_list:
                if button.check_click(x,y):
                    if button.value == "C":
                        equation = ""
    
                    elif button.value == "=":
                        equation = str(perform_operation()) + " "
                    else:
                        if button.value in operations:
                            equation +=" " + button.value +" "
                        else:
                            equation += button.value
                    
        elif length > 20 and not one_tap:
            one_tap = True

    #displying the equation
    cv2.putText(img,equation.replace(" ",""),(screenx + 10,screenHeight - 10),cv2.FONT_HERSHEY_PLAIN,2,(50,50,50),2)

    cv2.imshow("frame",img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cv2.destroyAllWindows()