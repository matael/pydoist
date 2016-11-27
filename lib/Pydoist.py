# Pydoist.py
#
# Copyright © 2016 Mathieu Gaborit (matael) <mathieu@matael.org>
#
#
# Distributed under WTFPL terms
#
#            DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
#                    Version 2, December 2004
#
# Copyright (C) 2004 Sam Hocevar <sam@hocevar.net>
#
# Everyone is permitted to copy and distribute verbatim or modified
# copies of this license document, and changing it is allowed as long
# as the name is changed.
#
#            DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
#   TERMS AND CONDITIONS FOR COPYING, DISTRIBUTION AND MODIFICATION
#
#  0. You just DO WHAT THE FUCK YOU WANT TO.
#

import todoist
from Levenshtein import distance as Ldistance


class Pydoist:
    """ Pydoist -- Python-Todoist minimal interface

    token -- Todoist API token
    """

    def __init__(self, token):
        self.token = token
        self.api = todoist.TodoistAPI(self.token)
        self.sync = self.api.sync()
        self.markers = {
            '%%': {
                'name': 'priority',
                'validate': self._validate_priority
            },
            '#': {
                'name': 'project_id',
                'validate': self._validate_project
            },
            '@': {
                'name': 'date_string',
                'validate': lambda _:_
            }
        }

    def get_project(self, candidate, criterion=2):
        """ Return the project closer to the candidate's name
        The Levenshtein distance is used to determine closeness of names

        candidate -- name to test against projects list
        criterion -- (optional) high bound for distance before dropout
        """

        distances =  {
            _['id']:Ldistance(_['name'], candidate)
            for _ in self.api.projects.all()
            if Ldistance(_['name'], candidate) <= criterion
        }
        if len(distances):
            project_id = sorted(distances.keys(), key=distances.get)[0]
            return self.api.projects.get_by_id(project_id)
        else:
            return None

    def _validate_priority(self, candidate):
        """ Validation and serialisation of priority setting

        candidate -- priority to validate
        """
        candidate = int(candidate)
        if candidate<1: return 1
        elif candidate>4: return 4
        else: return candidate

    def _validate_project(self, candidate):
        """ Validation and serialisation of project names

        candidate -- name to validate
        """
        project = self.get_project(candidate)
        if project:
            return project['id']
        else:
            return None

    def shoot_todo(self, todostr, markers=None):
        """ Convert the string passed on the CLI into a correct todo items

        todostr -- list of strings (choped at spaces)
        markers -- (optional) dict of markers specifying the marker, the name of the final
        property and the validation function (example in self.markers)
        """

        if not markers:
            markers=self.markers

        tododict = {'project_id': None}
        text = []

        for w in todostr:
            for m,mdic in markers.items():
                if w.startswith(m):
                    tododict[mdic['name']] = mdic['validate'](w.replace(m, ''))
                    break
            else:
                text.append(w)

        self.api.items.add(
            ' '.join(text),
            **tododict
        )
        return self.api.commit()

