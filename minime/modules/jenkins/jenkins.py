import jenkins
import sys
import minime.env.environment as env


class Jenkins_Api:
    __jenkins = None

    def __init__(self, host, user, password):
        self.__jenkins = jenkins.Jenkins(host, user, password)

    def build_job(self, name, parameters):
        try:
            test = self.__jenkins.build_job(name, parameters)
            print('JENKINS BUILD: ' + test)
        except:
            print(print("Unexpected error:", sys.exc_info()[0]))

    def get_job_last_info(self, name):
        last_build_number = self.get_job_build_last(name)['number']

        return self.get_job_build_info(name, last_build_number)

    def get_job_build_last(self, name):
        return self.__jenkins.get_job_info(name)['lastCompletedBuild']

    def get_job_build_info(self, job_nam, number):
        return self.__jenkins.get_build_info(job_nam, number)

__jc = env.get_section('JENKINS')

jenkins_api = Jenkins_Api(
    __jc['HOST'],
    __jc['USER'],
    __jc['PASSWORD']
)
