import pi_switch

class Rcswitch():
    def __init__(self,socket_number,tran_pin): #tran_pin=0, na to oristo otan to ftiakso
        self.socket_on = ("000000010100010001010101","000000010101000001010101","000000010001010001010101")
        self.socket_off = ("000000010100010001010100","000000010101000001010100","000000010001010001010100")
        self.socket_number= socket_number
        self.tran_pin = tran_pin
        sender = pi_switch.RCSwitchSender()
        sender.enableTransmit(self.tran_pin)
    def send(self,function):
        if function == "on":
            sender.send(self.socket_on[self.socket_number-1])
        elif function == "off":
            sender.send(self.socket_off[self.socket_number-1])
