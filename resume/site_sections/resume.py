from resume import *


@all_renderable()
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
