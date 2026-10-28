#!/usr/bin/env bash
set -euo pipefail

workspace_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

if [[ ! -r /opt/ros/jazzy/setup.bash ]]; then
  echo 'ROS 2 Jazzy não encontrado. Execute bash instalar_robotica.sh.' >&2
  exit 1
fi

if [[ ! -r "$workspace_dir/install/setup.bash" ]]; then
  echo 'Workspace ainda não compilado.' >&2
  echo 'Execute bash scripts/compilar_workspace.sh.' >&2
  exit 1
fi

source /opt/ros/jazzy/setup.bash
source "$workspace_dir/install/setup.bash"

exec ros2 launch hospital_robot atividade.launch.py "$@"
