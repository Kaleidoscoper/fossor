import re

from fossor.checks.check import Check

class DuplicateEntry(Check):
    def run(self, variables):
        out, err, return_code = self.shell_call('kubectl get pods')
        log_since = variables.get('log_since', None)
        pods = out.splitlines()[1:]
        serverLine = [pod for pod in pods if "guandata-server" in pod and "Running" in pod][0]
        serverPod = serverLine.split()[0]

        if (log_since):
            out, err, return_code = self.shell_call('kubectl logs --since=%s %s' % (log_since, serverPod))
            if (err):
                return err
        else:
            out, err, return_code = self.shell_call('kubectl logs --since=24h %s' % (serverPod))

        pattern = re.compile(r'(.*?)Duplicate Entry(.*?)For Key(.*?)',re.S | re.I)
        matchResult = re.match(pattern, ''.join(out))
        if matchResult != None:
            return "可能是已知问题, 由于 Mysql Unique key约束造成的Insert报错, 可参考Task-T7350"
        return "暂无该问题"




if __name__ == '__main__':
    c = DuplicateEntry()
    print(c.run({}))