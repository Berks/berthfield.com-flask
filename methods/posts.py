from methods.database import get_db
import datetime

class Post:
    """
    Post schema:
    - post (dict)
    """

    @classmethod
    def create(cls, head_img, title, sub, body, img):
        db = get_db()
        posts_ref = db.collection(u'posts')  # a reference to the posts collection
        post_ref = posts_ref.document()
          # create a post document reference
        # now you can create or update the post document (set: if it exists, update it. If not, create a new one).
        post_ref.set({
            u'header-image': u'{}'.format(head_img),
            u'title': u'{}'.format(title),  # Title of the post
            u'subtitle': u'{}'.format(sub),
            u'text': u'{}'.format(body),  # we could also name this smth else, like "text", to avoid confusion
            u'img': u'{}'.format(img),
            u'created': datetime.datetime.now(),
            # you could add other fields here, like "author", "email" etc.
        })

        # create message dict
        post_dict = post_ref.get().to_dict()
        post_dict["id"] = post_ref.id  # add ID to the message dict (because it's not added automatically)

        return post_dict

    @classmethod
    def fetch_all(cls):
        db = get_db()
        posts_ref = db.collection(u'posts')  # a reference to the messages collection

        # messages generator: holds all message documents (these documents need to be converted to dicts)
        posts_gen = posts_ref.stream()

        posts = []
        for post in posts_gen:
            post_dict = post.to_dict()  # converting DocumentSnapshot into a dictionary

            post_dict["id"] = post.id  # adding message ID to the dict, because it's not there by default
            posts.append(post_dict)  # appending the message dict to the messages list

        return posts


    @classmethod
    def fetch_post(cls, id):
        db = get_db()
        posts_ref = db.collection(u'posts')  # a reference to the messages collection

        # messages generator: holds all message documents (these documents need to be converted to dicts)
        posts_gen = posts_ref.stream()

        posts = []
        for post in posts_gen:
            if post.id == id:
                post_dict = post.to_dict()  # converting DocumentSnapshot into a dictionary

                post_dict["id"] = post.id  # adding message ID to the dict, because it's not there by default
                posts.append(post_dict)  # appending the message dict to the messages list

        return posts