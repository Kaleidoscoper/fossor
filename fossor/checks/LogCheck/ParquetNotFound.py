import re

from fossor.checks.check import Check

class ParquetNotFound(Check):
    def run(self, variables):
        out, err, return_code = self.shell_call('sudo kubectl get pods')
        log_since = variables.get('log_since', None)
        # podsAll = subprocess.check_output('sudo kubectl get pods ', shell=True).strip()
        pods = out.splitlines()[1:]
        result = filter(lambda test: test[0] == "s", pods)
        #serverLine = [pod.decode() for pod in pods if "guandata-server-controller" in pod.decode() and "Running" in pod.decode()][0]
        serverLine = [pod for pod in pods if "guandata-server-controller" in pod and "Running" in pod][0]
        serverPod = serverLine.split()[0]

        if (log_since):
            out, err, return_code =  self.shell_call('sudo kubectl logs --since=%s %s' % (log_since, serverPod))
        else:
            out, err, return_code = self.shell_call('sudo kubectl logs --since=24h %s' % (serverPod))

        pattern = re.compile(r'(.*?)java.io.FileNotFoundException(.*?)/guandata-store/table_cache/(.*?).snappy.parquet(.*)', re.S|re.I)
        matchResult = re.match(pattern, ''.join(out))
        if matchResult != None:
            return "可能是已知问题, 旧version的parquet文件被删除, 可参考Task-T6293"
        return "可能有其他问题"


if __name__ == '__main__':
    c = ParquetNotFound()
    print(c.run({}))