from instagram.data.config import *
from instagram.src.helper import *
from instagram.src.modify.modify_methods import pre_modify, compare_posts, compare_followers_following, compare_igtv, compare_hover_items
from instagram.src.instagram_object import InstagramObject

class InstagramMonitor:
    def __init__(self, monitoring_map):
        logger = logging.getLogger('instagram')
        logger.info("\n\n")
        logger.info("\t********MONITORING PHASE********")
        #Wir untersuchen nur noch die subdirectories fuer jede einzelne Anfrage:
        #Bspweise vergleichen wir nur die Posts Versionen miteinander, wenn auch der type Posts ist
        #Sonst kommt es zu mehrfachen Vergleichen, weil fuer jeden einzelne url('type=posts', 'type=igtv', 'type=tagged')
        #jedes mal alles durchgegangen wird(3*3=9 mal)
        for url in monitoring_map["instagram"]:
           
            html_type = get_type(url)
            old_html_path = get_old_html_path(url)
            new_html_path = get_new_html_path(url)

            logger.info("compare ("+old_html_path+") with ("+new_html_path+")") 
            
            if not pre_modify(url):
                logger.info("error while compare: "+old_html_path+" or "+new_html_path+" is missing")
                continue

            ig = (InstagramObject(url, "new"), InstagramObject(url, "old"))

            compare_followers_following(url, ig)

            if html_type == "posts":
                compare_posts(url, ig)
            elif html_type == "igtv":
                compare_igtv(url, ig)
            
            #compare_hover_items(url, ig)

""" Circular import
if __name__ == "__main__":
    Instagram(monitoring_map)
    print("\n\n")
"""
