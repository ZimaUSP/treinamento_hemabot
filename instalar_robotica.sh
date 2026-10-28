#!/usr/bin/env bash
set -euo pipefail

if [[ ! -r /etc/os-release ]]; then
  echo 'Não foi possível identificar o sistema operacional.' >&2
  exit 1
fi

source /etc/os-release

if [[ "${ID:-}" != 'ubuntu' || "${VERSION_ID:-}" != '24.04' ]]; then
  echo 'Este instalador requer Ubuntu 24.04.' >&2
  echo "Sistema detectado: ${PRETTY_NAME:-desconhecido}" >&2
  exit 1
fi

sudo apt update
sudo apt install -y curl locales software-properties-common

sudo locale-gen en_US en_US.UTF-8
sudo update-locale LC_ALL=en_US.UTF-8 LANG=en_US.UTF-8
export LANG=en_US.UTF-8

sudo add-apt-repository -y universe
sudo apt update

ros_apt_source_version="$({
  curl -fsSL \
    https://api.github.com/repos/ros-infrastructure/ros-apt-source/releases/latest
} | awk -F\" '/tag_name/ {print $4; exit}')"

if [[ -z "$ros_apt_source_version" ]]; then
  echo 'Não foi possível descobrir a versão de ros2-apt-source.' >&2
  exit 1
fi

ros_apt_source_deb="/tmp/ros2-apt-source.deb"
curl -fL -o "$ros_apt_source_deb" \
  "https://github.com/ros-infrastructure/ros-apt-source/releases/download/${ros_apt_source_version}/ros2-apt-source_${ros_apt_source_version}.noble_all.deb"

sudo dpkg -i "$ros_apt_source_deb"
sudo apt update
sudo apt install -y \
  python3-colcon-common-extensions \
  ros-dev-tools \
  ros-jazzy-desktop \
  ros-jazzy-ros-gz

setup_line='source /opt/ros/jazzy/setup.bash'
if ! grep -Fxq "$setup_line" "$HOME/.bashrc"; then
  printf '\n%s\n' "$setup_line" >> "$HOME/.bashrc"
fi

echo
echo 'Instalação concluída.'
echo 'Feche e abra o terminal ou execute:'
echo '  source /opt/ros/jazzy/setup.bash'
