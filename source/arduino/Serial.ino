#define MOTOR_A_a 3     //motorA의 + 3
#define MOTOR_A_b 11    //motorA의 - 11
#define MOTOR_B_a 5     //motorB의 + 5
#define MOTOR_B_b 6     //motorB의 - 6

// Valid motorSpeed: 125~255

String Speed;
char  cmd;
int  i, s;

int m_a_spd = 0, m_b_spd = 0;
boolean m_a_dir, m_b_dir = 0;

char DataToRead[6];

void setup() {
  // motor control pins
  pinMode(MOTOR_A_a, OUTPUT);
  pinMode(MOTOR_A_b, OUTPUT);
  pinMode(MOTOR_B_a, OUTPUT);
  pinMode(MOTOR_B_b, OUTPUT);

  Serial.begin(9600);
}

void loop() {
  DataToRead[5] = '\n';
  Serial.readBytesUntil(char(13), DataToRead, 5);

  cmd = DataToRead[0];
  Speed = "";
  for (i = 1; (DataToRead[i] != '\n') && (i < 6); i++) {
    Speed += DataToRead[i];
  }
  s = Speed.toInt();
  set_motor_ctrl(cmd, s);
  motor_drive();
}


void set_motor_ctrl(unsigned char cmd, int s) {
// direction
  // 0: forward, 1: reverse
  if (cmd == 'L') {
    // set direction
    m_a_dir = 1;  // reverse
    m_b_dir = 0;  // forward
    // set speed
    m_a_spd = s;
    m_b_spd = s;
  } else if (cmd == 'R') {
    // set direction
    m_a_dir = 0;
    m_b_dir = 1;
    // set speed
    m_a_spd = s;
    m_b_spd = s;
  } else if (cmd == 'F') {
    // set direction
    m_a_dir = 0;
    m_b_dir = 0;
    // set speed
    m_a_spd = s;
    m_b_spd = s;
  } else if (cmd == 'X') {
    m_a_dir = 0;
    m_b_dir = 0;
    m_a_spd = 0;
    m_b_spd = 0;
  }
}

void motor_drive() {
  if(m_b_dir == 1) {
    digitalWrite(MOTOR_B_a, LOW);     //motorB+ LOW
    analogWrite(MOTOR_B_b, m_b_spd);  //motorB- spd
  } else {
    analogWrite(MOTOR_B_a, m_b_spd);  //motorB+ spd
    digitalWrite(MOTOR_B_b, LOW);     //motorB- LOW
  }
  
  if(m_a_dir == 0) {
    digitalWrite(MOTOR_A_a, LOW);     //motorA+ LOW
    analogWrite(MOTOR_A_b, m_a_spd);  //motorA- spd
  } else {
    analogWrite(MOTOR_A_a, m_a_spd);  //motorA+ spd
    digitalWrite(MOTOR_A_b, LOW);     //motorA- LOW
  }
}
