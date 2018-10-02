import gitlab
import minime.modules.git.provider.class_base_provider as bp

class Gitlab_Provider(bp.Base_Provider):

    _gitlab = None

    def __init__(self, name, url, auth_type, **kwargs):
        super(Gitlab_Provider, self).__init__(name)
        self._create_client(url, auth_type, kwargs)


    def get_projects(self):
        projects = self._gitlab.projects.list(per_page=10, page=0)

        for project in projects:
            print(project)



    def _get_projects(self):
        pass


    def get_branches(self):
        pass

    def _create_client(self, url, auth_type, auth_data):
        clbck = '_auth_' + auth_type
        clbck_method = getattr(self, clbck)

        self._gitlab = clbck_method(url, auth_data)
        self._gitlab.auth()

    def _auth_private_token(self, url, auth_data):
        return gitlab.Gitlab(url, private_token=auth_data.get('private_token'))

    def _auth_oauth_token(self, url, auth_data):
        return gitlab.Gitlab(url, oauth_token=auth_data.get('oauth_token'))

    def _auth_email(self, url, auth_data):
        return gitlab.Gitlab(url, email=auth_data.get('email'), password=auth_data.get('password'))