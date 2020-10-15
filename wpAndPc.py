import BLS_Request
import pc
import wp

print("Choose an option:")
print("1: pc        (Industry)")
print("2: wp        (Commodity)")
wpORpc = str(input("Type either pc or wp: "))
while wpORpc != "wp" and wpORpc != "pc":
    wpORpc = str(input("Type either pc or wp: "))
if wpORpc == "wp":
    wp.wpProcessing()
elif wpORpc == "pc":
    pc.pcProcessing()


radio = QRadioButton()
radio.setText("Commodity")
radio.move(20,40)
datasetGroup.addButton(radio)
layout.addWidget(radio)
 
radio2 = QRadioButton()
radio2.setText("Industry")
radio2.move(100,40)
layout.addWidget(radio, 0, 1)
datasetGroup.addButton(radio2)
layout.addWidget(radio2)

label1 = QLabel(window)
label1.setText("Time Period Format: ")
label1.adjustSize()
label1.move(10,70)

layout1 = QGridLayout()

radio3 = QRadioButton(window)
radio3.setText("Yearly")
radio3.move(20,150)
layout1.addWidget(radio3, 0, 0)
 
radio4 = QRadioButton(window)
radio4.setText("Quarterly")
radio4.move(100,150)
layout1.addWidget(radio3, 0, 1)

radio5 = QRadioButton(window)
radio5.setText("Monthly")
radio5.move(120,150)
layout1.addWidget(radio3, 0, 2)

