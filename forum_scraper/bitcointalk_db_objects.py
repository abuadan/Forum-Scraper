# Will probably be using a neo4j model to load the data into a graphDB

from neomodel import StringProperty, RelationshipFrom, RelationshipTo, db, StructuredNode, UniqueIdProperty,\
    IntegerProperty, DateProperty, EmailProperty

db.set_connection()


class Board(StructuredNode):
    @classmethod
    def category(cls):
        pass

    board_title = StringProperty()
    board_moderator = StringProperty()
    board_link = StringProperty()


class Topic(StructuredNode):
    @classmethod
    def category(cls):
        pass

    uid = UniqueIdProperty()
    topic = StringProperty(unique_index=True, required=True)
    topic_page_html = StringProperty()
    board_title = StringProperty()
    board_link = StringProperty()
    board_moderator = StringProperty()
    board_moderator_profile_link = StringProperty()
    topic_title = StringProperty()
    topic_link = StringProperty()
    post = StringProperty()
    topic_page_number = IntegerProperty()
    board_ = RelationshipTo('Board', 'belongs_to')
    posted_by = RelationshipFrom('Profile', 'posted_in')


class Post(StructuredNode):
    @classmethod
    def category(cls):
        pass

    message_count_in_post = IntegerProperty()
    message_date = DateProperty()
    message_date_time_stamp = IntegerProperty()
    message_link = StringProperty()
    post_text = StringProperty()
    poster_profile_url = StringProperty()
    poster_username = StringProperty()
    topic = RelationshipTo('Topic', 'belongs_to')
    written_by = RelationshipTo('Profile', 'written_by')


class Profile(StructuredNode):
    @classmethod
    def category(cls):
        pass

    poster_username = StringProperty()
    poster_profile_url = StringProperty()
    poster_profile_id = IntegerProperty()
    aim = StringProperty()
    activity = IntegerProperty()
    age = IntegerProperty()
    date_registered = IntegerProperty()
    email = EmailProperty()
    gender = StringProperty()
    icq = StringProperty()
    last_active = DateProperty()
    location = StringProperty()
    msn = StringProperty()
    merit = StringProperty()
    position = StringProperty()
    post_count = IntegerProperty()
    signature = StringProperty()
    website = StringProperty()
    yim = StringProperty()
    posted = RelationshipTo('Post', 'written')


class CryptoCurrency(StructuredNode):
    @classmethod
    def category(cls):
        pass

    # bitcoin_address = StringProperty()
    # bitcoin_transaction = StringProperty()
    pass
