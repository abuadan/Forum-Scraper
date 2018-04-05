from mongoengine import *

connect('bitcoin_talk_data')


class Profile(Document):
    profile_url = URLField(required=True)
    profile_id = StringField()
    user_name = StringField()


meta = {'allow_inheritance': True}


class ProfilePostCount(Profile):
    post_count = IntField()


class ProfileMerit(Profile):
    merit = StringField()


class ProfilePosition(Profile):
    position = StringField()


class RegistrationDate(Profile):
    date_registered = DateTimeField()


class ProfileICQ(Profile):
    icq = StringField()


class ProfileAIM(Profile):
    aim = StringField()


class ProfileMSN(Profile):
    msn = StringField()


class ProfileEmail(Profile):
    email = EmailField()


class ProfileSkype(Profile):
    skype = StringField()


class ProfileGender(Profile):
    gender = StringField()


class ProfileAge(Profile):
    age = IntField()


class ProfileLocation(Profile):
    location = StringField()


class ProfileSignature(Profile):
    signature = StringField()


class Message(Document):
    user_details = ReferenceField(Profile)
    post_title = StringField()
    post_count = IntField()
    post_time = DateTimeField()
    post_text = StringField()
    links_mentioned = ListField(URLField())
    # images = BytesField() TODO Define a bytes field


class Post(EmbeddedDocument):
    url = URLField()
    board = StringField()
    topic = StringField()
    topic_id = IntField()
    message = ListField(EmbeddedDocumentField(Message))
    post_page = IntField()
    advert = DynamicField()
    post_language = StringField()
