import os
import json
from project.apps.projects import models

class SkipException(Exception): pass
    
class ModelsEncoder(json.JSONEncoder):
    def default(self, obj):
        if obj.__class__ in (
            models.Programme, models.District, models.Municipality, 
            models.Milestone, models.Project
        ):
            return obj.id
        return json.JSONEncoder.default(self, obj)

class UserDialogue(object):
    def __init__(self):
        self.progmap = {}
        self.distmap = {}
        self.municmap = {}
        self.nextmilestonemap = {}
        self.projectmap = {}
        self.cache_path = "/tmp/pmis-dialogue.cache"
        self.load_cache()

    def save_cache(self, map, key, val):
        if val: map[key] = val

        f = open(self.cache_path, "w")
        js = json.dumps({
            "programmes" : self.progmap,
            "districts" : self.distmap,
            "municipalities" : self.municmap,
            "next_milestones" : self.nextmilestonemap,
            "projects" : self.projectmap,
        }, f, cls=ModelsEncoder, indent=4)
        f.write(js)
        f.close()

    def load_cache(self):
        def load_obj(model, id):
            try:
                return model.objects.get(id=id)
            except model.DoesNotExist:
                return None

        sections = {
            "programmes" : {
                "map" : self.progmap,
                "model" : models.Programme
            },
            "districts" : {
                "map" : self.distmap,
                "model" : models.District
            },
            "municipalities" : {
                "map" : self.municmap,
                "model" : models.Municipality
            },
            "next_milestones" : {
                "map" : self.nextmilestonemap,
                "model" : models.Milestone
            },
            "projects" : {
                "map" : self.projectmap,
                "model" : models.Project
            },
        }
        if os.path.exists(self.cache_path):
            js = json.load(open(self.cache_path))
            for section in js.keys():
                details = sections[section]
                for key, val in js[section].items():
                    obj = load_obj(details["model"], int(val))
                    if obj:
                        details["map"][key] = obj

    def _listresponse(self, lst, allow_none=False):
        while True:
            i = 0
            for i, el in enumerate(lst):
                print "%d) %s" % (i, el)
            ignore = i + 1
            none = ignore + 1

            print "%d) Skip this item" % ignore
            if allow_none:
                print "%d) None match" % none

            try:
                result = int(raw_input(""))
                index = int(result)
                if index == ignore:
                    raise SkipException()
                elif index == none:
                    return None

                return lst[index]

            except (ValueError, IndexError, TypeError):
                print ""
                print "%s was not one of the available options - please choose again:" % result

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

            programme = self._listresponse(programmes, allow_none=True)
            self.save_cache(self.progmap, prog, programme)
            return programme
        return self.progmap[prog]

    def ask_district(self, dist):
        if not dist in self.distmap:
            districts = models.District.objects.all()

            print "Which district are you processing?"
            print dist
            print ""

            district = self._listresponse(districts)
            self.save_cache(self.distmap, dist, district)
        return self.distmap[dist]

    def ask_municipality(self, munic, district):
        if not munic in self.municmap:
            try:
                municipality = models.Municipality.objects.get(name=munic)
            except models.Municipality.DoesNotExist:
                municipalities = models.Municipality.objects.filter(district=district)

                print "Which municipality are you processing?"
                print munic, district
                print ""

                municipality = self._listresponse(municipalities, allow_none=True)
                return municipality
            self.save_cache(self.municmap, munic, municipality)
        return self.municmap[munic]

    def ask_project(self, project, **kwargs):
        proj = project["description"]

        if not proj in self.projectmap:
            print "Which project are you processing?"
            print proj
            projects = models.Project.objects.filter(**kwargs)
            project = self._listresponse(projects, allow_none=True)
            self.save_cache(self.projectmap, proj, project)
            return project
        
        return self.projectmap[proj]

    def ask_next_milestone(self, project, **kwargs):
        if not project["comments"] in self.nextmilestonemap:
            print ""
            print "What is the next milestone for this project?"
            print "Here are the comments from the IDIP:"
            print project["comments"]

            milestones = models.Milestone.objects.filter(**kwargs)
            milestone = self._listresponse(milestones, allow_none=True)
            self.save_cache(self.nextmilestonemap, project["comments"], milestone)
        return self.nextmilestonemap[project["comments"]]
