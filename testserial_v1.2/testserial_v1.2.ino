#include <Servo.h>
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

int pushButton = 2;
int pushButton2 = 3;
int buttonState;
int buttonState2;


int curcheckservo_red=0;
int curcheckservo_blue=0;
int precheckservo_red=0;
int precheckservo_blue=0;
int statusservo_red=0;
int statusservo_blue=0;

Servo myservo_red;
Servo myservo_blue;
void setup() {
valsRec[0]=1;
valsRec[1]=0;
valsRec[2]=1;
Serial.begin(9600);
pinMode(LED_BUILTIN, OUTPUT);
pinMode(pushButton, INPUT);
pinMode(pushButton2, INPUT);
myservo_red.attach(9); 
myservo_blue.attach(10); 
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

valsRec[0]= buttonState * 1 + buttonState2*100;

valsRec[2]=222;

// servo1

if(valsRec[1] & 1){
  curcheckservo_red=1;
}
else{
  curcheckservo_red=0;
}

if(valsRec[1] & 100){
  curcheckservo_blue=1;
}
else{
  curcheckservo_blue=0;
}

if(precheckservo_red == curcheckservo_red){
  statusservo_red=0;
}

if(precheckservo_red == 0 && curcheckservo_red == 1){
  statusservo_red=1;
}

if(precheckservo_blue == curcheckservo_blue){
  statusservo_blue=0;
}

if(precheckservo_blue == 0 && curcheckservo_blue == 1){
  statusservo_blue=1;
}




if( statusservo_red && statusservo_blue){
  for(int i=0;i<=180;i++){
    myservo_red.write(i);
    myservo_blue.write(i); 
    delay(3);
  }
for (int i = 180; i >= 0; i -= 1) { 
    myservo_red.write(i);   
    myservo_blue.write(i);           
    delay(3);
  }
  
}

else if( statusservo_red){
  for(int i=0;i<=180;i++){
    myservo_red.write(i);

    delay(3);
  }
for (int i = 180; i >= 0; i -= 1) { 
    myservo_red.write(i);   
         
    delay(3);
  }
  
}

else if( statusservo_blue ){
  for(int i=0;i<=180;i++){

    myservo_blue.write(i); 
    delay(3);
  }
for (int i = 180; i >= 0; i -= 1) { 
 
    myservo_blue.write(i);           
    delay(3);
  }
  
}

precheckservo_red = curcheckservo_red;
precheckservo_blue = curcheckservo_blue;
  
//-----------------------------end do something -------------------------------
}
