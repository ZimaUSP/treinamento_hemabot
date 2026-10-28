#!/usr/bin/env bash
set -euo pipefail

workspace_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

if [[ ! -r /opt/ros/jazzy/setup.bash ]]; then
  echo 'ROS 2 Jazzy não encontrado. Execute bash instalar_robotica.sh.' >&2
  exit 1
fi

source /opt/ros/jazzy/setup.bash
cd "$workspace_dir"

if [[ ! -e /etc/ros/rosdep/sources.list.d/20-default.list ]]; then
  sudo rosdep init
fi

rosdep update
rosdep install --from-paths src --ignore-src -r -y --rosdistro jazzy
colcon build --symlink-install

echo
echo 'Compilação concluída. Ative o workspace neste terminal com:'
echo "  source $workspace_dir/install/setup.bash"
