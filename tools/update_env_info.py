import argparse
import github
import json


class EnvInfoUploader(object):
    def __init__(self, user, password, job_name, patch_set, public_ip,
                 result_url, keeping_env):
        self.github_obj = github.Github(user, password)
        self.repo = self.github_obj.get_user().get_repo('moo-ai.github.io')
        self.job_name = job_name
        self.patch_set = patch_set
        self.public_ip = public_ip
        self.result_url = result_url
        self.keeping_env = keeping_env
        self.remote_env_file = ('task_list_sleep.json' if keeping_env
                                else 'task_list.json')
        self.content = self.repo.get_contents(
            'env_info/%s' % self.remote_env_file, ref="master")
        self.content_json = json.loads(self.content.decoded_content)

    def _update_env_info(self):
        self.content_json[self.job_name] = {
            "patch_set": self.patch_set,
        }
        if self.keeping_env:
            self.content_json[self.job_name]["ip"] = self.public_ip
            self.content_json[self.job_name]["credential"] = "demo/demo"
        else:
            self.content_json[self.job_name]["result_url"] = self.result_url

    def _refresh_env_info(self):

        self.repo.update_file(self.content.path,
                              "upload %s ci job" % args.job,
                              json.dumps(self.content_json), self.content.sha,
                              branch="master")
        print("Success update %s" % self.remote_env_file)

    def upload_env_info(self):
        self._update_env_info()
        self._refresh_env_info()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='MOO env info refresh tool',
        formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument('--user',  metavar='<user_name>', required=True,
                        help="Github user name")
    parser.add_argument('--password', metavar='<password>', required=True,
                        help="Github user password")
    parser.add_argument('--job', metavar='<job>', required=True,
                        help="The moo job name")
    parser.add_argument('--patch', metavar='<patch>', required=True,
                        help="The moo pull request id")
    parser.add_argument('--ip', metavar='<ip>', required=True,
                        help="Environment IP")
    parser.add_argument('--url', metavar='<url>', required=True,
                        help="Result Url")
    parser.add_argument('--keeping', metavar='<keeping>', required=True,
                        help="Keep the environment or not")
    args = parser.parse_args()

    if args.keeping == 'true':
        keep_env = True
    else:
        keep_env = False

    uploader = EnvInfoUploader(args.user, args.password, args.job, args.patch,
                               args.ip, args.url, keep_env)

    uploader.upload_env_info()
