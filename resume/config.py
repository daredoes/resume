from resume import *

resume_config = parse_config(__file__)
c.include_plugin_config(resume_config)

c.ACCESS.update(c.RESUME_ACCESS_LEVELS)
c.ACCESS_OPTS.extend(c.RESUME_ACCESS_LEVEL_OPTS)
c.ACCESS_VARS.extend(c.RESUME_ACCESS_LEVEL_VARS)