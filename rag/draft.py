"""
Draft for testing syntax some methods
"""

from get_project_root import root_path
project_root = root_path(ignore_cwd=False)
project_root = project_root[:project_root.rfind('\\')]
print(project_root)