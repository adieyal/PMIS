import os
import json
from project.apps.projects import models

class SkipException(Exception): pass
    
class ModelsEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, models.Programme):
            return obj.id
        elif isinstance(obj, models.District):
            return obj.id
        elif isinstance(obj, models.Municipality):
            return obj.id
        return json.JSONEncoder.default(self, obj)

class UserDialogue(object):
    def __init__(self):
        self.progmap = {}
        self.distmap = {}
        self.municmap = {}
        self.cache_path = "/tmp/pmis-dialogue.cache"
        self.load_cache()

    def save_cache(self):
        f = open(self.cache_path, "w")
        json.dump({
            "programmes" : self.progmap,
            "districts" : self.distmap,
            "municipalities" : self.municmap,
        }, f, cls=ModelsEncoder, indent=4)
        f.close()

    def load_cache(self):
        if os.path.exists(self.cache_path):
            js = json.load(open(self.cache_path))
            if "programmes" in js:
                for key, val in js["programmes"].items():
                    self.progmap[key] = models.Programme.objects.get(id=int(val))
            if "districts" in js:
                for key, val in js["districts"].items():
                    self.distmap[key] = models.District.objects.get(id=int(val))
            if "municipalities" in js:
                for key, val in js["municipalities"].items():
                    self.municmap[key] = models.Municipality.objects.get(id=int(val))

    def _listresponse(self, lst, allow_none=False):
        i = 0
        for i, el in enumerate(lst):
            print "%d) %s" % (i, el)
        ignore = i + 1
        none = ignore + 1

        print "%d) Skip this item" % ignore
        if allow_none:
            print "%d) None match" % none

        index = int(raw_input(""))
        if index == ignore:
            raise SkipException()
        elif index == none:
            return None

        return lst[index]

    def ask_month(self):
        print "What month are you processing? (1 - 12): "
        month = raw_input("")
        return int(month)

    def ask_year(self):
        print "Which financial year are you processing? (e.g 2013): "
        month = raw_input("")
        return int(month)

    def ask_client(self):
        clients = list(models.Client.objects.all())
        for i, client in enumerate(clients):
            print "%d) %s" % (i, client.name)
            
        index = raw_input("Which client are you processing?\n")
        return clients[int(index)]

    def ask_programme(self, prog, client=None):
        if not prog in self.progmap:
            programmes = models.Programme.objects.all()
            if client:
                programmes = programmes.filter(client=client)

            print "Which programme are you processing?"
            print prog
            print ""

            programme = self._listresponse(programmes)
            self.progmap[prog] = programme
        self.save_cache()
        return self.progmap[prog]

    def ask_district(self, dist):
        if not dist in self.distmap:
            districts = models.District.objects.all()

            print "Which district are you processing?"
            print dist
            print ""

            district = self._listresponse(districts)
            self.distmap[dist] = district
        self.save_cache()
        return self.distmap[dist]

    def ask_municipality(self, munic, district):
        if not munic in self.municmap:
            municipalities = models.Municipality.objects.filter(district=district)

            print "Which municipality are you processing?"
            print munic, district
            print ""

            municipality = self._listresponse(municipalities)
            self.municmap[munic] = municipality
        self.save_cache()
        return self.municmap[munic]

    def ask_project(self, project, **kwargs):
        print "Which project are you processing?"
        print project["description"]
        projects = models.Project.objects.filter(**kwargs)
        project = self._listresponse(projects, allow_none=True)
        
        return project
