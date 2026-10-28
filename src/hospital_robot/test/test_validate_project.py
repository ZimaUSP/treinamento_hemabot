"""Validação estática rápida dos materiais da oficina."""

import py_compile
import xml.etree.ElementTree as ET
from pathlib import Path


PACKAGE_ROOT = Path(__file__).resolve().parents[1]
REPOSITORY_ROOT = Path(__file__).resolve().parents[3]


def test_required_files_exist():
    required = [
        'package.xml',
        'setup.py',
        'launch/atividade.launch.py',
        'launch/demo.launch.py',
        'models/hospital_robot/model.config',
        'models/hospital_robot/model.sdf',
        'worlds/introduction.sdf',
        'worlds/hospital_l.sdf',
        'worlds/hospital_l_challenge.sdf',
        'hospital_robot/straight_line_gazebo.py',
        'hospital_robot/delivery_l.py',
        'hospital_robot/delivery_challenge.py',
    ]
    missing = [
        path for path in required
        if not (PACKAGE_ROOT / path).is_file()
    ]
    assert not missing, f'Arquivos ausentes: {missing}'


def test_repository_materials_exist():
    required = [
        'README.md',
        'LICENSE',
        'instalar_robotica.sh',
        'verificar_instalacao.sh',
        'scripts/compilar_workspace.sh',
        'scripts/executar_atividade.sh',
        'scripts/testar_projeto.sh',
        'docs/GUIA_INSTALACAO.md',
        'docs/ATIVIDADE.md',
        'docs/Guia_Instalacao_ROS2_Gazebo.docx',
        'docs/Atividade_Introducao_ROS2_Gazebo.docx',
    ]
    missing = [
        path for path in required
        if not (REPOSITORY_ROOT / path).is_file()
    ]
    assert not missing, f'Materiais ausentes: {missing}'


def test_student_template_contains_tasks():
    template = (
        PACKAGE_ROOT / 'student_templates/delivery_l.py'
    ).read_text(encoding='utf-8')
    assert template.count('TODO') >= 4
    assert 'LINEAR_SPEED = 0.0' in template
    assert 'ANGULAR_SPEED = 0.0' in template


def test_xml_files_are_well_formed():
    paths = [PACKAGE_ROOT / 'package.xml']
    paths.extend((PACKAGE_ROOT / 'models').rglob('*.sdf'))
    paths.extend((PACKAGE_ROOT / 'models').rglob('*.config'))
    paths.extend((PACKAGE_ROOT / 'worlds').glob('*.sdf'))

    for path in paths:
        ET.parse(path)


def test_python_files_compile():
    paths = [PACKAGE_ROOT / 'setup.py']
    paths.extend((PACKAGE_ROOT / 'launch').glob('*.py'))
    paths.extend((PACKAGE_ROOT / 'hospital_robot').glob('*.py'))
    paths.extend((PACKAGE_ROOT / 'student_templates').glob('*.py'))

    for path in paths:
        py_compile.compile(str(path), doraise=True)


def test_model_contains_required_systems():
    model = (PACKAGE_ROOT / 'models/hospital_robot/model.sdf').read_text()
    assert 'left_wheel_joint' in model
    assert 'right_wheel_joint' in model
    assert 'DiffDrive' in model
    assert '<topic>/cmd_vel</topic>' in model
    assert '<topic>/scan</topic>' in model
    assert 'gz-sim-diff-drive-system' in model
    assert 'gz::sim::systems::DiffDrive' in model


def test_launch_bridges_required_topics():
    launch = (PACKAGE_ROOT / 'launch/atividade.launch.py').read_text()
    for topic in ('/cmd_vel', '/scan', '/odom', '/clock'):
        assert topic in launch


def test_no_fortress_identifiers_remain():
    paths = list((PACKAGE_ROOT / 'models').rglob('*.sdf'))
    paths.extend((PACKAGE_ROOT / 'worlds').glob('*.sdf'))
    paths.extend((PACKAGE_ROOT / 'hospital_robot').glob('*.py'))

    for path in paths:
        content = path.read_text(encoding='utf-8')
        assert 'libignition-gazebo' not in content
        assert 'ignition::gazebo' not in content
        assert 'ignition.msgs' not in content
