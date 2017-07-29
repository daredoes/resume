from resume import *


@Session.model_mixin
class User:
    contact_items = relationship('ContactItem', backref='user')
    job_experiences = relationship('JobExperience', backref='user')
    life_experiences = relationship('LifeExperience', backref='user')
    hobbies = relationship('Hobby', backref='user')
    languages = relationship('Language', backref='user')
    skills = relationship('Skill', backref='user')

class ContactItem(MainModel):
    name = Column(UnicodeText)
    link = Column(UnicodeText)
    description = Column(UnicodeText)
    icon = Column(UnicodeText, default="link")
    user_id = Column(UUID, ForeignKey('user.id'))


class JobExperience(MainModel):
    name = Column(UnicodeText)
    link = Column(UnicodeText)
    description = Column(UnicodeText)
    icon = Column(UnicodeText, default="link")
    user_id = Column(UUID, ForeignKey('user.id'))
    start_date = Column(UTCDateTime)
    end_date = Column(UTCDateTime, default=None, nullable=True)
    job_title = Column(UnicodeText)


class LifeExperience(MainModel):
    name = Column(UnicodeText)
    link = Column(UnicodeText)
    description = Column(UnicodeText)
    icon = Column(UnicodeText, default="link")
    user_id = Column(UUID, ForeignKey('user.id'))
    date = Column(UTCDateTime, default=datetime.now(UTC))


class Hobby(MainModel):
    name = Column(UnicodeText)
    user_id = Column(UUID, ForeignKey('user.id'))


class Language(MainModel):
    name = Column(UnicodeText)
    user_id = Column(UUID, ForeignKey('user.id'))
    level = Column(Integer, default=99)

class Skill(MainModel):
    name = Column(UnicodeText)
    user_id = Column(UUID, ForeignKey('user.id'))
    level = Column(Integer, default=99)
