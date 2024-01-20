from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button

class CalcLaout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.orientation="vertical"
        self.operands=[]
        self.operations=[]
        self.is_finished=False

        self.label = Label(text="", font_size=40)
        self.add_widget(self.label)

        keys = [["7", "8", "9", "/"], 
                ["4", "5", "6", "*"],
                ["1", "2", "3", "-"],
                [".", "0", "C", "+"]]
        
        for i in range(len(keys)):
            horiz_layout=BoxLayout()

            for j in range(4):
                btn = Button(text=keys[i][j], font_size=20)
                btn.bind(on_press=self.pressed)
                horiz_layout.add_widget(btn)

            self.add_widget(horiz_layout)

        self.add_widget(Button(text="=", on_press=self.pressed))


    def pressed(self, instance):
        key = instance.text
        ops = ["+", "-", "*", "/", "="]

        if key=="C":
            self.label.text=""
            self.operands=[]
            self.operations=[]
            return
        

        # first key is *, /, +, -
        # two sucessive operators: **, //, ++, --
        if len(self.operands)==len(self.operations) and key in ops:
            return

        # starting with a period then operation
        # operation on a single period: num*.*, num*.+, num*./, .....
        if len(self.operands)>=1 and self.operands[-1]=="." and key in ops:
            return
        
        # repetion of a period for the same number
        if key=="." and len(self.operands)>=1 and len(self.operands)!=len(self.operations) and "." in self.operands[-1]:
            return
        
        # deviding by zero: num/0*, num/0+
        if key in ops and len(self.operands)>=2 and self.operations[-1]=="/" and self.get_numeric(self.operands[-1])==0:
            return

        if key!="=":
            text=self.label.text
            self.label.text+=key

            if len(text)==0:
                self.operands.append(key)
                return
            
            elif key in ops: 
                self.new_operator()
                self.operations.append(key)
                return

            else:  # numeric or period
                if len(self.operands)==len(self.operations):
                    self.operands.append(key)
                else:
                    self.operands[-1]+=key
                return
            
        # key is "="
        else:
            # non-complete operation 
            if len(self.operands)==len(self.operations) or self.get_numeric(self.operands[-1])==0:
                return
            
            self.new_operator()

            i=1
            result=self.operands[0]
            for operation in self.operations:
                if operation=="+":
                    result+=self.operands[i]
                elif operation=="-":
                    result-=self.operands[i]
                i+=1
            
            result=str(result)
            if result[-2:]==".0":
                result=result[:-2]
            self.label.text=str(result)
            self.operands=[str(result)]
            self.operations=[]
        

    def new_operator(self):
        # converting the last operand into a float datatype
            self.operands[-1]=self.get_numeric(self.operands[-1])
            # abbreviating multiplication and division operations at once
            if len(self.operations)>0 and self.operations[-1] in "*/":
                result=self.apply_operation(self.operands[-2], self.operands[-1], self.operations[-1])
                self.operands=self.operands[:-2]+[result]
                self.operations=self.operations[:-1]



    def get_numeric(self, string):
        lst = string.split(".")
        if lst[0]=="": # ".975" or "."
            num=0
        else:
            num = float(lst[0])

        if len(lst)==1:
            return num
        
        else:
            dividor=10
            for digit in lst[1]:
                num+=float(digit)/dividor
                dividor*=10
                
            return num
        
    def apply_operation(self, num1, num2, oper):
        if oper=="/":
            return num1/num2

        elif oper=="*":
            return num1*num2

        elif oper=="-":
            return num1-num2

        elif oper=="+":
            return num1+num2


class CalcApp(App):
    def build(self):
        return CalcLaout()
    

if __name__=="__main__":
    CalcApp().run()
