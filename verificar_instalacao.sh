#!/usr/bin/env bash
set -uo pipefail

failures=0

check_command() {
  local command_name="$1"
  if command -v "$command_name" >/dev/null 2>&1; then
    printf '[OK] comando %s\n' "$command_name"
  else
    printf '[ERRO] comando %s não encontrado\n' "$command_name"
    failures=$((failures + 1))
  fi
}

if [[ -r /etc/os-release ]]; then
  source /etc/os-release
  if [[ "${ID:-}" == 'ubuntu' && "${VERSION_ID:-}" == '24.04' ]]; then
    printf '[OK] %s\n' "${PRETTY_NAME}"
  else
    printf '[ERRO] esperado Ubuntu 24.04; encontrado %s\n' \
      "${PRETTY_NAME:-sistema desconhecido}"
    failures=$((failures + 1))
  fi
fi

if [[ -r /opt/ros/jazzy/setup.bash ]]; then
  source /opt/ros/jazzy/setup.bash
  printf '[OK] ROS 2 Jazzy instalado\n'
else
  printf '[ERRO] /opt/ros/jazzy/setup.bash não encontrado\n'
  failures=$((failures + 1))
fi

check_command ros2
check_command gz
check_command colcon

if command -v ros2 >/dev/null 2>&1; then
  if ros2 pkg prefix ros_gz_bridge >/dev/null 2>&1; then
    printf '[OK] pacote ros_gz_bridge\n'
  else
    printf '[ERRO] pacote ros_gz_bridge não encontrado\n'
    failures=$((failures + 1))
  fi
fi

if [[ -d /mnt/wslg ]]; then
  printf '[OK] WSLg detectado\n'
else
  printf '[AVISO] WSLg não detectado; a interface do Gazebo pode não abrir\n'
fi

if (( failures > 0 )); then
  printf '\nDiagnóstico concluído com %d erro(s).\n' "$failures"
  exit 1
fi

printf '\nAmbiente básico pronto para a atividade.\n'
