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


int curcheckservo1=0;
int curcheckservo2=0;
int precheckservo1=0;
int precheckservo2=0;
int statusservo1=0;
int statusservo2=0;

Servo myservo1;
Servo myservo2;
void setup() {
valsRec[0]=1;
valsRec[1]=0;
valsRec[2]=1;
Serial.begin(9600);
pinMode(LED_BUILTIN, OUTPUT);
pinMode(pushButton, INPUT);
pinMode(pushButton2, INPUT);
myservo1.attach(9); 
myservo2.attach(10); 
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

valsRec[2]=222;

// servo1

if(valsRec[1] & 1){
  curcheckservo1=1;
}
else{
  curcheckservo1=0;
}

if(valsRec[1] & 10){
  curcheckservo2=1;
}
else{
  curcheckservo2=0;
}

if(precheckservo1 == curcheckservo1){
  statusservo1=0;
}

if(precheckservo1 == 0 && curcheckservo1 == 1){
  statusservo1=1;
}

if(precheckservo2 == curcheckservo2){
  statusservo2=0;
}

if(precheckservo2 == 0 && curcheckservo2 == 1){
  statusservo2=1;
}




if( statusservo1 && statusservo2){
  for(int i=0;i<=180;i++){
    myservo1.write(i);
    myservo2.write(i); 
    delay(3);
  }
for (int i = 180; i >= 0; i -= 1) { 
    myservo1.write(i);   
    myservo2.write(i);           
    delay(3);
  }
  
}

else if( statusservo1){
  for(int i=0;i<=180;i++){
    myservo1.write(i);

    delay(3);
  }
for (int i = 180; i >= 0; i -= 1) { 
    myservo1.write(i);   
         
    delay(3);
  }
  
}

else if( statusservo2 ){
  for(int i=0;i<=180;i++){

    myservo2.write(i); 
    delay(3);
  }
for (int i = 180; i >= 0; i -= 1) { 
 
    myservo2.write(i);           
    delay(3);
  }
  
}

precheckservo1 = curcheckservo1;
precheckservo2 = curcheckservo2;
  
//-----------------------------end do something -------------------------------
}
