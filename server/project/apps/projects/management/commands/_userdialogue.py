from project.apps.projects import models

class UserDialogue(object):
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

