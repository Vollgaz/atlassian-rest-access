

class ConfluenceContent(object):

    def __init__(self, client):
        self._confluenceclient = client

    def get_page(self, pagename="", spacekey="", expand=""):
        return self._confluenceclient.get_page(pagename=pagename,
                                               spacekey=spacekey,
                                               expand=expand)

    def push_content(self, pagetitle="", pageparenttitle="", spacekey="", pagebody=""):
        # en spécifiant le nom de la page et la clé de l'espace, le tableau à 0 ou 1 élément
        listpages = self.get_page(pagename=pagetitle,
                                  spacekey=spacekey)
        if len(listpages) == 0:
            self.create_new_page(spacekey=spacekey,
                                 pagetitle=pagetitle,
                                 parentpagename=pageparenttitle,
                                 pagebody=pagebody)
        else:
            self.update_page_from_id(pagename=pagetitle,
                                     spacekey=spacekey,
                                     pagecontent=pagebody)

    def create_new_page(self, spacekey="", parentpagename="", pagetitle="", pagebody=""):
        response = self.get_page(pagename=parentpagename,
                                 spacekey=spacekey,
                                 expand='version')[0]
        parentpageid = response['id']
        self._confluenceclient.create_new_page(spacekey=spacekey,
                                               ancestors=[{'type': 'page', 'id': parentpageid}],
                                               pagetitle=pagetitle,
                                               pagebody=pagebody)

    def update_page_from_id(self, pagename="", spacekey="", pagecontent=""):
        response = self.get_page(pagename=pagename, spacekey=spacekey, expand='version')[0]
        newversion = (response['version']['number']) + 1
        pageid = response['id']
        self._confluenceclient.update_page(pageid=pageid,
                                           pageversion=str(newversion),
                                           pagebody=pagecontent)
