"""
KARA Simulation Package
"""

from enum import StrEnum
import pathlib
from types import MappingProxyType

REPO_ROOT = pathlib.Path(__file__).resolve().parents[2]
SO101_SCENE = (
    REPO_ROOT / "assets" / "robots" / "SO-ARM100" / "Simulation" / "SO101" / "scene.xml"
)

class KaraArmSimModelType(StrEnum):
    """
    Enum for different Kara arm simulation models.
    """
    SO101 = "SO101"

_model_scene_path_map: dict[KaraArmSimModelType, pathlib.Path] = {
    KaraArmSimModelType.SO101: SO101_SCENE,
}

MODEL_SCENE_PATH_MAP = MappingProxyType(_model_scene_path_map)
