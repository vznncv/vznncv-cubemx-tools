from os.path import join, dirname
from jinja2 import Environment, FileSystemLoader, select_autoescape


def get_resource_dir():
    """
    Get resource directory.

    This function is made for pyinstaller support in the future.
    """
    return join(dirname(__file__), "resources")


_env = None


def get_template_environment():
    """
    Get configure jinja2 ``Environment`` object.

    :return: ``Environment`` object
    """
    global _env
    if _env is None:
        _env = Environment(
            loader=FileSystemLoader(join(get_resource_dir(), 'templates')),
            autoescape=select_autoescape(),
            trim_blocks=True,
            lstrip_blocks=True
        )
    return _env
