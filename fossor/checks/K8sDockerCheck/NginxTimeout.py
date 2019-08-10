import re

from fossor.checks.check import Check

class NginxTimeout(Check):
    def run(self, variables):
        out, err, return_code = self.shell_call('kubectl get pods')
        log_since = variables.get('log_since', None)
        pods = out.splitlines()[1:]
        webLine = [pod for pod in pods if "guandata-web" in pod and "Running" in pod][0]
        webPod = webLine.split()[0]

        if (log_since):
            out, err, return_code =  self.shell_call('kubectl logs --since=%s %s -c nginx' % (log_since, webPod))
        else:
            out, err, return_code = self.shell_call('kubectl logs --since=24h %s -c nginx' % (webPod))

        pattern = re.compile(r'(.*?)upstream timed out(.*?)Connection timed out', re.S|re.I)
        matchResult = re.match(pattern, ''.join(out))
        if matchResult != None:
            return "可能是已知问题, Nginx响应1分钟超时，可将nginx配置中的timeout时间调长,可参考Task-T6533"
        return "可能有其他问题"


if __name__ == '__main__':
    c = NginxTimeout()
    print(c.run({}))