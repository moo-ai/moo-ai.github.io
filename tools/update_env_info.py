import argparse
import contextlib
import github
import json
import time


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

    @contextlib.contextmanager
    def _lock(self):
        for i in range(10):
            lock_content = self.repo.get_contents(
                'env_info/lock.json', ref="master")
            lock_json = json.loads(lock_content.decoded_content)

            if lock_json[self.remote_env_file] == 0:
                lock_json[self.remote_env_file] = 1
                self.repo.update_file(lock_content.path,
                                      "lock %s" % self.remote_env_file,
                                      json.dumps(lock_json),
                                      lock_content.sha,
                                      branch="master")
                break
            else:
                time.sleep(2)
        else:
            raise Exception

        yield

        lock_content = self.repo.get_contents(
            'env_info/lock.json', ref="master")
        lock_json = json.loads(lock_content.decoded_content)
        lock_json[self.remote_env_file] = 0
        self.repo.update_file(lock_content.path,
                              "unlock %s" % self.remote_env_file,
                              json.dumps(lock_json),
                              lock_content.sha,
                              branch="master")

    def _update_env_info(self):
        env_content = self.repo.get_contents(
            'env_info/%s' % self.remote_env_file, ref="master")
        env_content_json = json.loads(env_content.decoded_content)
        env_content_json[self.job_name] = {
            "patch_set": self.patch_set,
        }
        if self.keeping_env:
            env_content_json[self.job_name]["ip"] = self.public_ip
            env_content_json[self.job_name]["credential"] = "demo/demo"
        else:
            env_content_json[self.job_name]["result_url"] = self.result_url
        return env_content, env_content_json

    def _refresh_env_info(self, env_content, env_content_json):

        self.repo.update_file(env_content.path,
                              "upload %s ci job" % args.job,
                              json.dumps(env_content_json), env_content.sha,
                              branch="master")
        print("Success update %s" % self.remote_env_file)

    def upload_env_info(self):
        with self._lock():
            env_content, env_content_json = self._update_env_info()
            self._refresh_env_info(env_content, env_content_json)


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
