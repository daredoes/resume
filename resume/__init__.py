from darecms.common import *

from ._version import __version__
from .config import *
from .models import *
from .model_checks import *

static_overrides(join(resume_config['module_root'], 'static'))
template_overrides(join(resume_config['module_root'], 'templates'))
mount_site_sections(resume_config['module_root'])

resume_menu = MenuItem(name='Resume', access=[c.RESUME], submenu=[
    MenuItem(name='Edit', href='{{ c.PATH }}/resume/edit?id={{ c.CURRENT_ADMIN.id }}'),
    MenuItem(name='View', href='{{ c.PATH }}/resume/?id={{ c.CURRENT_ADMIN.id }}')
])

c.MENU.append_menu_item(resume_menu)