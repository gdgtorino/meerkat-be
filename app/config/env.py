import os

from envyaml import EnvYAML


def get_env():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    yaml_file_path = os.path.join(current_dir, "resource", "env_dev_fest_alps_test.yaml")
    return EnvYAML(yaml_file_path)