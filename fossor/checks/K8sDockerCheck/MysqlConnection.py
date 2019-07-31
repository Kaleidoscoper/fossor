from fossor.checks.check import Check

class MysqlConnection(Check):
    def run(self, variables):
        out, err, return_code = self.shell_call('curl localhost:3306')

        output = out.splitlines()[0]

        if "Failed" in output:
            return "Mysql容器连接出现故障"
        return "可能有其他问题"


if __name__ == '__main__':
    c = MysqlConnection()
    print(c.run({}))