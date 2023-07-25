char command[100];
int state = true;

//0 = input 1 = output

struct Pole{

  int Pin = -1;
  int Func = -1;

  
}pins[100];


void setup() {
    Serial.begin(115200);
    
}

void cls(){
  digitalWrite(5, LOW);
  digitalWrite(6, LOW);
}

void Read_Command(){
  if(Serial.available()){   
    Serial.readBytesUntil('e',command,100);
    state = false;
  }
}

void Set_Pins(){
    for(int i = 0; i != 100; i++){
        if(pins[i].Pin == -1)
          break;
        pinMode(pins[i].Pin, pins[i].Func);
        pins[i].Pin = -1;
        pins[i].Func = -1;   
    }
}

void Execute_Command(){
    String output = "o";
    for(int i = 0; i != 100; i++){
        if(pins[i].Pin == -1)
          break;
        if(pins[i].Func == -1){
          output += "/";
          if(pins[i].Pin >= 14)
             output += (String(pins[i].Pin) + analogRead(pins[i].Pin));
          if(pins[i].Pin < 14)
             output += (String(pins[i].Pin) + "k" + String(digitalRead(pins[i].Pin))); 
        }
        if(pins[i].Func == 0){
             digitalWrite(pins[i].Pin, LOW);
        }
        if(pins[i].Func == 1){
             digitalWrite(pins[i].Pin, HIGH);
        }
        if(pins[i].Func > 1){
             analogWrite(pins[i].Pin, pins[i].Func);
        }
        pins[i].Pin = -1;
        pins[i].Func = -1; 
    }
    if(output != "o"){
      output += 'e';
      char out[100];
      output.toCharArray(out, 100);
      for(int i = 0; i != 100; i++){
        if(out[i] == '\0')
        break;
        Serial.write(out[i]);
      }
    }
}

void Proceed_Command(){
    if(command[0] == '0'){
      command[0] = "";
      command[1] = "";
      bool new_pin = true;
      int index = 0;
      for(int i = 2; i != 100; i++){
        if(command[i] == '/'){
          command[i] = "";
          new_pin = true;
          continue;
        }
        if(new_pin){
          String p = "";
          
          p = command[i];
          command[i] = "";
          if(command[i+1] != 'k'){
            p += command[i+1];
            command[i+1] = "";
          }
          pins[index].Pin = p.toInt();
          pins[index].Func = String(command[i+2]).toInt();
          command[i+2] = "";
          i = i + 2;
          index++;
          new_pin = false;
        }
        
      }
      Set_Pins();
    }
    if(command[0] == '1'){
      command[0] = "";
      command[1] = "";
      bool new_com = true;
      int index = 0;
      for(int i = 2; i != 100; i++){
        if(command[i] == '/'){
          command[i] = "";
          new_com = true;
          continue;
        }
        if(new_com){
          String p = "";
          p = command[i];
          command[i] = "";
          if(command[i+1] != 'k'){
            p += command[i+1];
            command[i+1] = "";
          }
          pins[index].Pin = p.toInt();
          if(command[i+2] != 'i'){
            p = String(command[i+2]);
            command[i+2] = "";
            int idx = 3;
            while(command[i+idx] != '/' && command[i+idx] != '\0'){
              p += command[i+idx];
              command[i+idx] = "";
              idx++;
            }
            new_com = true;
            i += idx;
            pins[index].Func = p.toInt();
          }else{
            i = i + 2;
            new_com = false; 
          }

          index++;
          
        }
        if(command[i] == '\0')
          break;
      }

      Execute_Command();
    }
    if (command[0] == 'c'){
        cls();
        while(Serial.available())
          Serial.read();
      
    }
    
    state = true;
    
}
 
void loop()
{

    if(state)
      Read_Command();
    if (!state){
      Proceed_Command();
    }
    
    
    
}
