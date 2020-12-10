from instagram.data.config import *
from instagram.src.helper import *
from lxml import etree, html

NEW = 0
OLD = 1

class InstagramObjects:
    def __init__(self, url):
            self.set_trees(self, url)
            self.set_followers(self, url)
            self.set_following(self, url)
            self.set_posts(self)
            self.set_igtvs(self)
            self.set_tags(self)

    def get_trees(self):
        return self.trees

    def get_followers(self):
        return self.followers

    def get_following(self):
        return self.following

    def get_posts(self):
        return self.posts

    def get_igtvs(self):
        return self.igtvs

    def get_tags(self):
        return self.tags

    def set_trees(self, url):
        new_tree = html.parse(get_new_html_path(url))
        old_tree = html.parse(get_old_html_path(url))
        self.trees = (new_tree, old_tree)

    def set_followers(self, url):
        newFollowersElement = list(self.trees[NEW].xpath("//a[@href='https://www.instagram.com/" + url["id"] +  "/followers/']")[0].iter())
        oldFollowersElement = list(self.trees[OLD].xpath("//a[@href='https://www.instagram.com/" + url["id"] +  "/followers/']")[0].iter())

        self.followers = (newFollowersElement, oldFollowersElement)

    def set_following(self, url):
        newFollowingElement = list(self.trees[NEW].xpath("//a[@href='https://www.instagram.com/" + url["id"] +  "/following/']")[0].iter())
        oldFollowingElement = list(self.trees[OLD].xpath("//a[@href='https://www.instagram.com/" + url["id"] +  "/followers/']")[0].iter())

        self.following = (newFollowingElement, oldFollowingElement)

    def set_posts(self):
        new_posts = self.trees[NEW].xpath("//div[@id='react-root']//article//a")
        old_posts = self.trees[OLD].xpath("//div[@id='react-root']//article//a")
        self.posts = (new_posts, old_posts)

    def set_igtvs(self):
        new_igtvs = self.trees[NEW].xpath("//div[@id='react-root']//main//div//a")
        old_igtvs = self.trees[OLD].xpath("//div[@id='react-root']//main//div//a")
        self.igtvs = (new_igtvs, old_igtvs)

    def set_tags(self):
        #TODO
        self.tags = (0, 0)