import re

from fossor.checks.check import Check

class JobServerOOM(Check):
    def run(self, variables):
        out, err, return_code = self.shell_call('kubectl get pods')
        log_since = variables.get('log_since', None)
        pods = out.splitlines()[1:]
        jobServerLine = [pod for pod in pods if "spark-jobserver" in pod and "Running" in pod][0]
        jobServerPod = jobServerLine.split()[0]

        if (log_since):
            out, err, return_code =  self.shell_call('kubectl logs --since=%s %s' % (log_since, jobServerPod))
            if (err):
                return err
        else:
            out, err, return_code = self.shell_call('kubectl logs --since=24h %s' % (jobServerPod))

        pattern = re.compile(r'(.*?)failed to allocate page(.*)', re.S|re.I)
        matchResult = re.match(pattern, ''.join(out))
        if matchResult != None:
            return "Jobserver 发生OOM, 请检查内存配置是否足够"
        return "没有Jobserver内存OOM问题"


if __name__ == '__main__':
    c = JobServerOOM()
    print(c.run({}))