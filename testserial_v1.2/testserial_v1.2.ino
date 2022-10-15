#define numOfValsRec 3
#define digitsPerValRec 3
int valsRec[numOfValsRec];
int stringLength=numOfValsRec*digitsPerValRec+1;
int counter =0;
bool counterStart=false;
String receivedString;

String myS="123,456";
int flag=1;
int sta=0;
int led5=5;
int led6=6;
int pushButton = 2;
int pushButton2 = 3;
int buttonState;
int buttonState2;
void setup() {
Serial.begin(9600);
pinMode(LED_BUILTIN, OUTPUT);
pinMode(7, INPUT);
valsRec[0]=1;
valsRec[1]=1;
valsRec[2]=1;
pinMode(pushButton, INPUT);
pinMode(pushButton2, INPUT);

pinMode(led5, OUTPUT);
pinMode(led6, OUTPUT);
}

void receiveData(){
if(flag==0){
 
  while (Serial.available()){
    //Serial.println(__LINE__);
    char c = Serial.read();
    if (c=='$'){
      counterStart=true;
    }
    if (counterStart){
      if(counter<stringLength){
        receivedString=String(receivedString+c);
      counter++;
      }
      if(counter>=stringLength){
       for (int i=0;i<numOfValsRec;i++){
        int num=(i*digitsPerValRec)+1;
        valsRec[i]=receivedString.substring(num,num+digitsPerValRec).toInt();
       }
       receivedString="";
       counter=0;
       counterStart=false;
      }
    }
    flag=1;
  }
  Serial.flush();

  }
}


void loop() {



if(flag==1){
myS="";
//Serial.println(__LINE__);
myS=String(valsRec[0]+','+valsRec[1]+','+valsRec[2]);
Serial.print(valsRec[0]);
Serial.print(",");
Serial.print(valsRec[1]);
Serial.print(",");
Serial.println(valsRec[2]);
Serial.flush();
flag=0;

  }

receiveData();

//-----------------------------do something -------------------------------

buttonState = digitalRead(pushButton);
buttonState2 = digitalRead(pushButton2);

valsRec[0]= buttonState * 1 + buttonState2*10;
valsRec[1]=111;
valsRec[2]=222;
// print out the state of the button:


delay(5);        // delay in between reads for stability

  
//-----------------------------end do something -------------------------------
}
