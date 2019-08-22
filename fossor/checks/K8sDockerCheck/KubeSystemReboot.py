import re,datetime

from fossor.checks.check import Check

class KubeSystemReboot(Check):
    def run(self,variables):
        out, err, return_code = self.shell_call('kubectl get pods --all-namespaces')
        pods = out.splitlines()[1:]
        kubeSystemPods = [pod.split()[1] for pod in pods if "kube-system" in pod and "Running" in pod]
        pattern = re.compile(r'(.*?)State:(.*?)Running(.*?)Started:(.*?)\+0800', re.S | re.I)
        for kubeSystemPod in kubeSystemPods:
            if self.checkIfRebootInLast24Hours(kubeSystemPod, pattern):
                return '过去24h内，kube-system组件: %s 发生过重启，可能是kubelet异常，请检查' % (kubeSystemPod)
        return "kubelet无异常"

    def checkIfRebootInLast24Hours(self, systemPodTocheck, pattern):
        out, err, return_code = self.shell_call('kubectl describe pod %s -nkube-system' % (systemPodTocheck))
        startedTimeStr = re.match(pattern, ''.join(out)).group(4).strip()
        startedTime = datetime.datetime.strptime(startedTimeStr, "%a, %d %b %Y %H:%M:%S")
        nowDay = datetime.datetime.today()
        print(startedTime)
        print(nowDay)
        return (nowDay-startedTime).days < 1


if __name__ == '__main__':
    c = KubeSystemReboot()
    print(c.run({}))