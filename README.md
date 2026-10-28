# HemaBot — ROS 2 e Gazebo

O HemaBot é um projeto introdutório de robótica móvel que orienta os
alunos desde a preparação do ambiente no WSL 2 até o controle de um robô
diferencial em um hospital simulado. Com ROS 2, Gazebo e Python, os participantes
exploram nós e tópicos, enviam comandos de movimento e programam uma missão de
entrega, observando na simulação os efeitos do código sobre o robô.

## Ambiente adotado

- Windows 10 21H2 ou mais recente, ou Windows 11;
- WSL 2 com Ubuntu 24.04 LTS;
- ROS 2 Jazzy Jalisco;
- Gazebo Harmonic;
- integração `ros_gz`.

O nome deste repositório é `treinamento_hemabot`. O pacote ROS 2 interno chama-se
`hospital_robot`, preservando os comandos usados nos guias da atividade.

## Conteúdo

```text
treinamento_hemabot/
├── docs/                       # guias em Markdown e DOCX
├── scripts/                    # compilação, execução e testes
├── src/hospital_robot/
│   ├── hospital_robot/         # nós Python prontos
│   ├── launch/                 # inicialização do Gazebo e das missões
│   ├── models/                 # robô diferencial com LiDAR
│   ├── student_templates/      # arquivos incompletos para os alunos
│   ├── test/                   # validações estáticas
│   └── worlds/                 # mundos da atividade
├── instalar_robotica.sh        # instala ROS 2, Gazebo e ferramentas
└── verificar_instalacao.sh     # diagnostica o ambiente
```

## Início rápido

No terminal do Ubuntu 24.04:

```bash
cd ~/treinamento_hemabot
bash instalar_robotica.sh
```

Feche e abra o terminal. Depois execute:

```bash
cd ~/treinamento_hemabot
bash verificar_instalacao.sh
bash scripts/compilar_workspace.sh
source install/setup.bash
ros2 launch hospital_robot atividade.launch.py
```

Em outro terminal, ative o ambiente e explore o ROS 2:

```bash
cd ~/treinamento_hemabot
source /opt/ros/jazzy/setup.bash
source install/setup.bash
ros2 node list
ros2 topic list
ros2 topic echo /odom
```

Para iniciar a solução de demonstração:

```bash
ros2 run hospital_robot entrega_programada
```

## Atividade do aluno

O exercício de Python está em
`src/hospital_robot/student_templates/delivery_l.py`. O aluno copia esse modelo
para o pacote, completa os trechos `TODO`, recompila e executa a missão:

```bash
cp src/hospital_robot/student_templates/delivery_l.py \
  src/hospital_robot/hospital_robot/delivery_l.py
nano src/hospital_robot/hospital_robot/delivery_l.py
bash scripts/compilar_workspace.sh
source install/setup.bash
ros2 run hospital_robot delivery_l
```

Como o repositório usa Git, a solução original pode ser restaurada com:

```bash
git restore src/hospital_robot/hospital_robot/delivery_l.py
```

## Documentação

- [Guia de instalação](docs/GUIA_INSTALACAO.md)
- [Roteiro da atividade](docs/ATIVIDADE.md)
- `docs/Guia_Instalacao_ROS2_Gazebo.docx`
- `docs/Atividade_Introducao_ROS2_Gazebo.docx`

## Validação do material

Os testes estáticos não exigem uma sessão gráfica do Gazebo:

```bash
bash scripts/testar_projeto.sh
```

Para uma verificação manual completa, compile o workspace, inicie a simulação e
confirme que `/cmd_vel`, `/odom`, `/scan` e `/clock` aparecem em
`ros2 topic list`.
