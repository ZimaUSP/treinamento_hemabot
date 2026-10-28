# Guia de instalação — ROS 2 e Gazebo

Este guia prepara o Windows para executar a atividade no Ubuntu pelo WSL 2.

> **Atenção:** comandos indicados como PowerShell são executados no Windows. Os
> demais comandos são executados no terminal do Ubuntu.

## 1. Requisitos

- Windows 10 versão 21H2 ou mais recente, ou Windows 11;
- acesso de administrador no Windows;
- conexão com a internet;
- pelo menos 8 GB de memória RAM recomendados;
- arquivo ou clone do repositório `treinamento_hemabot`.

## 2. Instalar WSL 2 e Ubuntu 24.04

Abra o **PowerShell como administrador**:

```powershell
wsl --update
wsl --install -d Ubuntu-24.04
```

Reinicie o computador se for solicitado. Abra Ubuntu 24.04 no menu Iniciar e
crie o usuário e a senha. A senha não aparece na tela durante a digitação.

No PowerShell, confira a versão:

```powershell
wsl --list --verbose
```

A coluna `VERSION` deve mostrar `2`. Se mostrar `1`:

```powershell
wsl --set-version Ubuntu-24.04 2
```

## 3. Colocar o repositório no Ubuntu

Copie a pasta para a pasta pessoal do Ubuntu. No terminal, o caminho esperado é
`~/treinamento_hemabot`.

```bash
cd ~/treinamento_hemabot
ls
```

A listagem deve incluir `README.md`, `instalar_robotica.sh`, `scripts` e `src`.
Evite compilar em `/mnt/c`: o sistema de arquivos do Ubuntu costuma ser mais
rápido e evita problemas de permissões e links simbólicos.

## 4. Instalar ROS 2, Gazebo e ferramentas

```bash
cd ~/treinamento_hemabot
bash instalar_robotica.sh
```

O script instala ROS 2 Jazzy Desktop, Gazebo Harmonic, `ros_gz`, `rosdep` e
`colcon`. Digite a senha do Ubuntu quando for solicitada. Ao terminar, feche e
abra o terminal.

## 5. Verificar e compilar

```bash
cd ~/treinamento_hemabot
bash verificar_instalacao.sh
bash scripts/compilar_workspace.sh
source install/setup.bash
```

Confirme o pacote:

```bash
ros2 pkg prefix hospital_robot
```

## 6. Testar a interface gráfica

```bash
gz sim shapes.sdf
```

Feche o Gazebo após o teste. Se a janela não abrir, execute no PowerShell:

```powershell
wsl --update
wsl --shutdown
```

Abra novamente o Ubuntu e repita o teste. Também pode ser necessário atualizar
o driver gráfico Intel, AMD ou NVIDIA no Windows.

## 7. Teste final do repositório

```bash
cd ~/treinamento_hemabot
source /opt/ros/jazzy/setup.bash
source install/setup.bash
ros2 launch hospital_robot atividade.launch.py
```

O Gazebo deve abrir o corredor hospitalar com o robô na posição inicial. Use
`Ctrl+C` para encerrar.

Em cada terminal novo, execute:

```bash
source /opt/ros/jazzy/setup.bash
source ~/treinamento_hemabot/install/setup.bash
```

## Problemas frequentes

- `ros2` não encontrado: execute `source /opt/ros/jazzy/setup.bash`.
- Pacote não encontrado: compile novamente e ative `install/setup.bash`.
- Gazebo não abre: atualize o WSL e o driver gráfico do Windows.
- Compilação lenta: mantenha o repositório em `~/treinamento_hemabot`.
- Versão incorreta: `printenv ROS_DISTRO` deve mostrar `jazzy`.
