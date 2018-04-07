# This should have different parsers that plug-into the pipeline and can be used to extract
# Information such as crypto currencies mentioned and handle other bitcointalk objects


class CryptoCurrencyParser(object):
    pass


class ProfileParser(object):
    # TODO fix date issues around LocationTime, DateRegistered and LastActive
    # TODO signature can sometimes be a crypto related asset
    pass


class TopicParser(object):
    pass


class PostParser(object):
    # TODO if post and username are the same ignore i.e. 'post_text': '1523090284' and poster_username': '1523090284'
    pass


class BoardParser(object):
    pass


