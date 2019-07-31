import re

from fossor.checks.check import Check

class SQLServerDeadLock(Check):
    def run(self, variables):
        out, err, return_code = self.shell_call('sudo kubectl get pods')
        log_since = variables.get('log_since', None)
        pods = out.splitlines()[1:]
        serverLine = [pod for pod in pods if "guandata-server-controller" in pod and "Running" in pod][0]
        serverPod = serverLine.split()[0]

        if (log_since):
            out, err, return_code =  self.shell_call('sudo kubectl logs --since=%s %s' % (log_since, serverPod))
        else:
            out, err, return_code = self.shell_call('sudo kubectl logs --since=24h %s' % (serverPod))

        pattern = re.compile(r'(.*?)was deadlocked on lock(.*?)communication buffer resources with another process and has been chosen as the deadlock victim(.*)', re.S|re.I)
        matchResult = re.match(pattern, ''.join(out))
        if matchResult != None:
            return "可能是已知问题, SQL-Server发生死锁，可参考Task-T6330"
        return "可能有其他问题"


if __name__ == '__main__':
    c = SQLServerDeadLock()
    print(c.run({}))