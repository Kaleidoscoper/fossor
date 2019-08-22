import re

from fossor.checks.check import Check

class CellStyleExceed(Check):
    def run(self, variables):
        out, err, return_code = self.shell_call('kubectl get pods')
        log_since = variables.get('log_since', None)
        pods = out.splitlines()[1:]
        serverLine = [pod for pod in pods if "guandata-server" in pod and "Running" in pod][0]
        serverPod = serverLine.split()[0]

        if (log_since):
            out, err, return_code =  self.shell_call('kubectl logs --since=%s %s' % (log_since, serverPod))
            if (err):
                return err
        else:
            out, err, return_code = self.shell_call('kubectl logs --since=24h %s' % (serverPod))

        pattern = re.compile(r'(.*?)The maximum number of Cell Styles was exceeded. You can define up to 64000 style in a .xlsx Workbook(.*)', re.S|re.I)
        matchResult = re.match(pattern, ''.join(out))
        if matchResult != None:
            return "可能是已知问题, 客户导出的cellStyle超过64000, 可参考Task-T5239"
        return "暂无该问题"

if __name__ == '__main__':
    c = CellStyleExceed()
    print(c.run({}))