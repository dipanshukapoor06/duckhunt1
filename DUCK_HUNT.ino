void setup() {
Serial.begin(9600);
pinMode(2,INPUT);
}
/************/
unsigned int xmin=295;
unsigned int xmax=450;
unsigned int ymin=295;
unsigned int ymax=440;
/************/


unsigned int a,b,flag=0;
float xfactor,yfactor;

void loop() {

a=analogRead(A0);
b=analogRead(A1);

if(a<xmin)
  xmin=a-10;
else if (a>xmax)
  xmax=a+10;
if(b<ymin)
  ymin=b-10;
else if (b>ymax)
  ymax=b+10;
  

a=map(a,xmin,xmax,0,21);
b=map(b,ymin,ymax,0,21);

Serial.write('*');
Serial.write(a);
Serial.write(b);
if(digitalRead(2)==LOW)
  flag=1;

if(flag==1)
  Serial.print('1');
else
  Serial.print('0');

Serial.print('\n');
delay(200);

if(Serial.available()>0)
  while(Serial.available()>0)
      if(Serial.read()=='#')
         flag=0;
}
