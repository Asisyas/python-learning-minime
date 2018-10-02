import minime.bot.actions.class_base_action as ba
import minime.env.environment as env
import minime.modules.jenkins.jenkins as jnkns
import random

class Action_Environment(ba.Base_Action):

    __build_pr_conf = None

    __branch = None
    __brand = None
    __env = None
    __synchronize_db = None
    __debugEnable = False

    __state: None

    SESSION_PREFIX = '_Action_Environment_'
    SESSION_STATUS_ACTION = 'env_act_status'
    SESSION_BRANCH = 'ea_brnch'
    SESSION_ENV = 'env'

    STATUS_BRANCH = 'branch'
    STATUS_ENV = 'env'
    STATUS_DEV = 'dev'
    STATUS_DEV_SELF = 'dev_self'
    STATUS_DB_SYNC = 'db'
    STATUS_DEBUG = 'dbg'
    STATUS_SUCCESS = 'success'
    STATUS_ANSWERS = {
        STATUS_BRANCH : [ 'Какой бранч юзать', 'Из какой ветки', 'Ветка ?' ],
        STATUS_ENV: ['Какой брэнд ?', 'Чо за брэнд?', 'Брэнд какой ?'],
        STATUS_DEV_SELF: ['Юзать твой энв ?', 'На твоем энве ?', 'Пересобрать твой энв ?'],
        STATUS_DEV: ['А какой тогда юзать ? ', 'Чей тогда ?', 'Чей билдим тогда энв?'],
        STATUS_DB_SYNC: ['БД синкать ?'],
        STATUS_DEBUG: ['Дебаг включаем ?'],
        STATUS_SUCCESS: ['Запустил', 'Готово, стартанул', 'Запустил, жди', 'Стартанул, жди']
    }


    def __init__(self):
        self.__build_pr_conf = env.get_section('BUILD_PR')

    def get_tag(self):
        return 'build_run'

    def run(self, **kwargs):
        status = self._prepare()
        session = kwargs.get('session')

        ready_status = self._repare_status(session)

        if ready_status != self.STATUS_SUCCESS:
            session.tag = self.get_tag()
            session.answers = ['']
            return status

        return self._run_jenkins_job()

    def _repare_status(self, session):
        curr_status = self.STATUS_SUCCESS
        sess_status = session.get_param(self.SESSION_STATUS_ACTION)

        if self.__branch is None:
            curr_status = self.STATUS_BRANCH
        if self.__env is None:
            if sess_status == self.STATUS_DEV_SELF:
                curr_status = self.STATUS_DEV
            else:
                curr_status = self.STATUS_DEV_SELF
        if self.__synchronize_db is None:
            curr_status = self.STATUS_DB_SYNC


        return curr_status

    def _prepare(self, session):
        curr_status = self.STATUS_SUCCESS
        sess_status = self._set_session_var(self.SESSION_STATUS_ACTION)
        if self.__branch is None:
            curr_status = self.STATUS_BRANCH
        if self.__env is None:
            if sess_status == self.STATUS_DEV_SELF:
                curr_status = self.STATUS_DEV
            else:
                curr_status = self.STATUS_DEV_SELF
        if self.__synchronize_db is None:
            curr_status = self.STATUS_DB_SYNC

        if(curr_status == self.STATUS_SUCCESS):
            return True

        answer = random.choice(self.STATUS_ANSWERS[curr_status])
        session.set_param(self.SESSION_STATUS_ACTION, curr_status)

        return answer

    def _get_answer(self, status):
        return random.choice(self.STATUS_ANSWERS[status])

    def _set_session_var(self, session, key, value):
        session.set_param(self.SESSION_PREFIX + key, value)

    def _get_session_var(self, session, key):
        return session.get_param(self.SESSION_PREFIX + key)

    def _run_jenkins_job(self):
        act = self.__build_pr_conf['JOB_NAME']

        jnkns.jenkins_api.build_job(act, {
            'branch': self.__branch,
            'developer': self.__env,
            'brand': self.__brand,
            'syncronizeDb': self.__synchronize_db,
            'debugEnabled': self.__debugEnable
        })