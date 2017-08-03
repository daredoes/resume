from resume import *


@all_renderable(c.ACCOUNTS)
class Root:
    def index(self, session, id=None, message=''):
        if id:
            user = session.query(User).filter(User.id == id).first()
        else:
            user = session.query(User).first()
        return {
            'message': message,
            'user': user
        }

    def form(self, session, message='', return_to='', **params):
        user = session.user(params, checkgroups=User.all_checkgroups, bools=User.all_bools)
        if 'first_name' in params:
            message = ''
            if not message:
                message = check(user)
            session.add(user)
            msg_text = '{} has been saved'.format(user.full_name)
            if params.get('save') == 'save_return_to_search':
                if return_to:
                    raise HTTPRedirect(return_to + '&message={}', 'Attendee data saved')
                else:
                    raise HTTPRedirect('index?uploaded_id={}&message={}&search_text={}', user.id, msg_text,
                        '{} {}'.format(user.first_name, user.last_name) if c.AT_THE_CON else '')
            else:
                raise HTTPRedirect('form?id={}&message={}&return_to={}', user.id, msg_text, return_to)
        return {
            'message': message,
            'user': user
        }

    def edit(self, option='index', session=None, bio_pic=None, message='', return_to='', **params):
        if option:
            options = {
                "index": session.user,
                "info": session.user,
                "skills": session.skill,
                "jobs": session.job_experience,
                "experiences": session.life_experience,
                "contact": session.contact_item,
                "hobbies": session.hobby,
                "hobby": session.hobby,
            }
            choice = None
            template = None
            for type in options.keys():
                if fuzz.ratio(option, type) > 80:
                    choice = options[type]
                    template = type
            if not choice:
                raise HTTPRedirect()

            item = choice(params, ignore_csrf=True)

            if choice is not session.user:
                user = session.user(params['user_id'], ignore_csrf=True) if 'user_id' in params else item.user

            else:
                user = item
                if bio_pic:
                    user.pic_filename = bio_pic.filename
                    user.pic_content_type = bio_pic.content_type.value
                    if os.path.isfile(user.pic_fpath):
                        os.remove(user.pic_fpath)
                    with open(user.pic_fpath, 'wb') as f:
                        shutil.copyfileobj(bio_pic.file, f)
            user_items = {
                "index": session.query(User).all(),
                "info": session.query(User).all(),
                "skills": user.skills,
                "jobs": user.job_experiences,
                "experiences": user.life_experiences,
                "contact": user.contact_items,
                "hobbies": user.hobbies,
                "hobby": user.hobbies,
            }
            others = user_items[template]
            if 'name' in params:
                message = ''
                if not message:
                    message = check(item)
                session.add(item)
                msg_text = '{} has been saved'.format(item.name)
                raise HTTPRedirect('edit/{}?id={}&message={}&return_to={}', template, item.id, msg_text, return_to)
            return {
                'message': message,
                'user': user,
                'item': item,
                'type': template,
                'others': others
            }
        raise HTTPRedirect()

    def delete(self, option=None, session=None, message='', **params):
        if 'id' in params:
            if option:
                options = {
                    "skills": Skill,
                    "jobs": JobExperience,
                    "experiences": LifeExperience,
                    "contact": ContactItem,
                    "hobbies": Hobby,
                    "hobby": Hobby,
                }
                choice = None
                template = None
                for type in options.keys():
                    if fuzz.ratio(option, type) > 80:
                        choice = options[type]
                        template = type
                if not choice:
                    raise HTTPRedirect()
                item = session.query(choice).filter(choice.id == params['id']).first()
                user_id = item.user.id
                if item:
                    message = "Item '%s' deleted" % item.name
                    session.delete(item)
                    session.commit()
                    raise HTTPRedirect('edit/%s?user_id=%s&message=%s' % (template, user_id, message))


    @ajax
    def add_contact(self, session, **params):
        if 'user_id' and 'name' in params:
            user = session.query(User).filter(User.id == params['user_id']).first()
            if user:
                _item = session.contact_item(params)
                _item.user = user
                session.add(_item)
                session.commit()
                return {
                    'id': _item.id,
                    'name': _item.name
                }

    @ajax
    def delete_contact(self, session, **params):
        if 'id' in params:
            item = session.query(ContactItem).filter(ContactItem.id == params['id']).first()
            if item:
                session.delete(item)
                session.commit()
                return True

    @ajax
    def delete_job(self, session, **params):
        if 'id' in params:
            item = session.query(JobExperience).filter(JobExperience.id == params['id']).first()
            if item:
                session.delete(item)
                session.commit()
                return True

    @ajax
    def delete_experience(self, session, **params):
        if 'id' in params:
            item = session.query(LifeExperience).filter(LifeExperience.id == params['id']).first()
            if item:
                session.delete(item)
                session.commit()
                return True

    @ajax
    def add_hobby(self, session, **params):
        if 'user_id' and 'name' in params:
            user = session.query(User).filter(User.id == params['user_id']).first()
            if user:
                _item = session.hobby(params, ignore_csrf=True)
                _item.user = user
                session.add(_item)
                session.commit()
                return {
                    'id': _item.id,
                    'name': _item.name
                }

    @ajax
    def delete_hobby(self, session, **params):
        if 'id' in params:
            hobby = session.query(Hobby).filter(Hobby.id == params['id']).first()
            if hobby:
                session.delete(hobby)
                session.commit()
                return True

    @ajax
    def add_new_hobby(self, session, message='Hobby Not Added', **params):
        id = params.pop('div_id')
        html = ''
        if 'user_id' and 'name' in params:
            user = session.query(User).filter(User.id == params['user_id']).first()
            if user:
                _hobby = session.hobby(params, ignore_csrf=True)
                _hobby.user = user
                session.add(_hobby)
                session.commit()

                html = """
                <div class="hobby">{hobby.name}</div>
                """.format(hobby=_hobby)
        return {
            'message': message,
            'id': id,
            'html': html
        }

    @ajax
    def add_new_skill(self, session, message='Skill Not Added', **params):
        id = params.pop('div_id')
        html = ''
        if 'user_id' and 'name' and 'level' in params:
            user = session.query(User).filter(User.id == params['user_id']).first()
            if user:
                _skill = session.skill(params, ignore_csrf=True)
                _skill.user = user
                session.add(_skill)
                session.commit()
                html = """
                <div class="item-skills" data-percent="0.{s.level}">{s.name}</div>
                """.format(s=_skill)
        return {
            'message': message,
            'id': id,
            'html': html
        }

    @ajax
    def add_new_language(self, session, message='Language Not Added', **params):
        id = params.pop('div_id')
        html = ''
        if 'user_id' and 'name' and 'level' in params:
            user = session.query(User).filter(User.id == params['user_id']).first()
            if user:
                _language = session.language(params, ignore_csrf=True)
                _language.user = user
                session.add(_language)
                session.commit()
                html = """
                <div class="skill">{language.name}
                <div class="icons pull-right">
                  <div style="width: {language.level}%;" class="icons-red">

                  </div>
                </div>
              </div>
                """.format(language=_language)
        return {
            'message': message,
            'id': id,
            'html': html
        }

    @ajax
    def add_new_contact(self, session, message='Contact Option Not Added', **params):
        id = params.pop('div_id')
        html = ''
        if 'user_id' and 'name' and 'link' and 'description' in params:
            user = session.query(User).filter(User.id == params['user_id']).first()
            if user:
                params['icon'] = params.get('icon', 'link').lstrip('fa-')
                _contact = session.contact_item(params, ignore_csrf=True)
                _contact.user = user
                session.add(_contact)
                session.commit()
                message = "Contact Option %s Added" % _contact.name
                html = """
                <div class="contact-item">
              <a href="{contact.link}"><div class="icon pull-left text-center"><span class="fa fa-{contact.icon} fa-fw"></span></div></a>
              <div class="title pull-right">{contact.name}</div>
              <div class="description pull-right">{contact.description}</div>
                """.format(contact=_contact)
        return {
            'message': message,
            'id': id,
            'html': html
        }

    @ajax
    def delete_contact_item(self, session, message='Item Not Deleted', **params):
        if 'user_id' and 'id' in params:
            _item = session.query(ContactItem).filter(ContactItem.id == params['id']).first()
            session.delete(_item)
            session.commit()
            message = 'Item Deleted'
        return {
            'message': message
        }

    @ajax
    def delete_item(self, session, message='Item Not Deleted', **params):
        if 'id' and 'user_id' in params:
            _item = session.query(ContactItem).filter(ContactItem.id == params['id']).first()
            _item = session.query(Skill).filter(Skill.id == params['id']).first() if not _item else _item
            _item = session.query(Hobby).filter(Hobby.id == params['id']).first() if not _item else _item
            _item = session.query(Language).filter(Language.id == params['id']).first() if not _item else _item
            _item = session.query(JobExperience).filter(JobExperience.id == params['id']).first() if not _item else _item
            _item = session.query(LifeExperience).filter(LifeExperience.id == params['id']).first() if not _item else _item
            if _item:
                if _item.user_id == params['user_id']:
                    message = "Item '%s' deleted." % _item.name
                    session.delete(_item)
                    session.commit()
                else:
                    message = 'Wrong User ID Supplied"'
        return {
            'message': message
        }
