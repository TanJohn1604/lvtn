#define numOfValsRec 2
#define digitsPerValRec 3
int valsRec[numOfValsRec];
int stringLength=numOfValsRec*digitsPerValRec+1;
int counter =0;
bool counterStart=false;
String receivedString;
int buttonState;
String myS="123,456";
int flag=1;
int sta=0;


void setup() {
Serial.begin(9600);
pinMode(LED_BUILTIN, OUTPUT);
pinMode(7, INPUT);
valsRec[0]=90;
valsRec[1]=90;
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
myS=String(valsRec[0]+','+valsRec[1]);
Serial.print(valsRec[0]);
Serial.print(",");
Serial.println(valsRec[1]);
Serial.flush();
flag=0;

  }

receiveData();

//-----------------------------do something -------------------------------
buttonState = digitalRead(7);
if (buttonState == HIGH) {
  // turn LED on:
  valsRec[1]=1;
} else {
  // turn LED off:
  valsRec[1]=0;
}
sta=!sta;
delay(500);
digitalWrite(LED_BUILTIN, sta);
}
