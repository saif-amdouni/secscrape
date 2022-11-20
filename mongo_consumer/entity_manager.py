from enum import Enum
import mongoengine as me




#### Entities ####


class theHackerNewsArticle(me.Document):
    alertType = me.StringField(required=True)
    date = me.DateTimeField(required=True)
    title = me.StringField()
    link = me.StringField()


