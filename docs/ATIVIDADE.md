# Atividade — introdução ao ROS 2 e Gazebo

## Objetivo

Conhecer a comunicação do ROS 2, iniciar uma simulação no Gazebo, movimentar um
robô diferencial e completar uma missão simples em Python.

## 1. Comunicação entre nós

Abra dois terminais e ative o ROS 2 em ambos:

```bash
source /opt/ros/jazzy/setup.bash
```
No primeiro terminal:

```bash
ros2 run demo_nodes_cpp talker
```

No segundo:

```bash
ros2 run demo_nodes_py listener
```

Observe quem publica e quem recebe as mensagens. Encerre com `Ctrl+C`.

## 2. Iniciar o hospital simulado

```bash
cd ~/treinamento_hemabot
source /opt/ros/jazzy/setup.bash
source install/setup.bash
ros2 launch hospital_robot atividade.launch.py
```

Mantenha esse terminal aberto. Use outro terminal para os próximos comandos.

## 3. Explorar tópicos

```bash
cd ~/treinamento_hemabot
source /opt/ros/jazzy/setup.bash
source install/setup.bash
ros2 node list
ros2 topic list
ros2 topic info /cmd_vel
ros2 topic echo /odom
```

`/cmd_vel` recebe comandos de movimento e `/odom` informa o deslocamento do
robô.

## 4. Movimentar o robô pelo terminal

Movimento para frente:

```bash
ros2 topic pub --rate 10 /cmd_vel geometry_msgs/msg/Twist \
  "{linear: {x: 0.2}, angular: {z: 0.0}}"
```

Interrompa com `Ctrl+C` e envie a parada:

```bash
ros2 topic pub --once /cmd_vel geometry_msgs/msg/Twist \
  "{linear: {x: 0.0}, angular: {z: 0.0}}"
```

Teste também uma curva lenta usando `angular.z` igual a `0.4`.

## 5. Programar a missão em Python

Copie o modelo incompleto sobre o programa da missão:

```bash
cd ~/treinamento_hemabot
cp src/hospital_robot/student_templates/delivery_l.py \
  src/hospital_robot/hospital_robot/delivery_l.py
nano src/hospital_robot/hospital_robot/delivery_l.py
```

Complete os trechos marcados com `TODO`:

1. defina velocidades linear e angular seguras;
2. publique a velocidade linear durante a primeira reta;
3. publique a velocidade angular durante a curva de 90 graus;
4. publique a velocidade linear durante a segunda reta.

Use valores iniciais entre `0.10` e `0.25` m/s para velocidade linear e entre
`0.30` e `0.60` rad/s para velocidade angular.

Compile e execute com a simulação aberta:

```bash
bash scripts/compilar_workspace.sh
source install/setup.bash
ros2 run hospital_robot delivery_l
```

Ajuste uma velocidade ou um tempo, compile novamente e compare o trajeto. O
programa deve publicar velocidade zero ao terminar.

Para recuperar a versão funcional original:

```bash
git restore src/hospital_robot/hospital_robot/delivery_l.py
bash scripts/compilar_workspace.sh
```

## Demonstração pronta

A solução fornecida pode ser executada junto com a simulação:

```bash
ros2 launch hospital_robot demo.launch.py
```

O desafio adicional com obstáculo e LiDAR usa:

```bash
ros2 launch hospital_robot demo.launch.py \
  world:=hospital_l_challenge challenge:=true
```
