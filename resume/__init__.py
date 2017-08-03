from darecms.common import *

from ._version import __version__
from .config import *
from .models import *
from .model_checks import *

static_overrides(join(resume_config['module_root'], 'static'))
template_overrides(join(resume_config['module_root'], 'templates'))
mount_site_sections(resume_config['module_root'])

c.MENU['{{ c.CURRENT_ADMIN.first_name }} {{ c.CURRENT_ADMIN.last_name }}'].append_menu_item(
    MenuItem(name='My Resume', href='../resume/?id={{ c.CURRENT_ADMIN.id }}')
)

c.MENU['{{ c.CURRENT_ADMIN.first_name }} {{ c.CURRENT_ADMIN.last_name }}'].append_menu_item(
    MenuItem(name='Edit Resume', href='../resume/edit?id={{ c.CURRENT_ADMIN.id }}')
)