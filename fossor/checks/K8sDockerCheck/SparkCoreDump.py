import re

from fossor.checks.check import Check

class SparkCoreDump(Check):
    def run(self, variables):
        out, err, return_code = self.shell_call('kubectl get pods')
        pods = out.splitlines()[1:]
        sparkWorkerLines = [pod for pod in pods if "spark-worker" in pod and "Running" in pod]
        for sparkWorkLine in sparkWorkerLines:
            sparkWorkerPod = sparkWorkLine.split()[0]
            out, err, return_code = self.shell_call('kubectl exec -ti %s -- du -sh /opt/spark/work' % (sparkWorkerPod))
            if "G" in out:
                return "Spark Worker产生CoreDump数据，磁盘空间即将耗尽，请尽快处理"
        return "没有Spark CoreDump问题"