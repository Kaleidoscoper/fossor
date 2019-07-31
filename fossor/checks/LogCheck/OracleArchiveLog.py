import re

from fossor.checks.check import Check

class OracleArchiveLog(Check):
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

        # pattern = re.compile(r'(.*?)Exception(.*)', re.S|re.I)
        pattern = re.compile(r'(.*?)归档程序错误。在释放之前仅限于内部连接(.*)', re.S|re.I)
        matchResult = re.match(pattern, ''.join(out))
        if matchResult != None:
            return "可能是已知问题, 客户的Oracle服务器磁盘已满, 可参考Task-T6281"
        return "可能有其他问题"
        # print(re.match(pattern,log).group(3))


if __name__ == '__main__':
    c = ParquetNotFound()
    print(c.run({}))