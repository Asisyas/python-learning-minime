import minime.bot.actions.class_base_action as ba
import minime.env.environment as env
import minime.modules.jenkins.jenkins as jnkns


class Action_Environment(ba.Base_Action):

    __build_pr_conf = None

    __branch = None
    __brand = None
    __env = None
    __syncronizeDb = None
    __debugEnable = False

    __state: None


    def __init__(self):
        self.__build_pr_conf = env.get_section('BUILD_PR')

    def get_tag(self):
        return 'build_run'

    def run(self, **kwargs):
        status = self._prepare()
        if status is not True:
            return status

        return self._run_jenkins_job()


    def _prepare(self):
        if(self.__branch is None):
            return 'Какой бранч заюзать ?'
        if(self.__env is None):
            return 'На какой энвайрмент ?'
        if(self.__syncronizeDb is None):
            return 'базу синкануть ?'

        return True

    def _run_jenkins_job(self):
        act = self.__build_pr_conf['JOB_NAME']

        jnkns.jenkins_api.build_job( act, {
            'branch': self.__branch,
            'developer': self.__env,
            'brand': self.__brand,
            'syncronizeDb': self.__syncronizeDb,
            'debugEnabled': self.__debugEnable
        } )