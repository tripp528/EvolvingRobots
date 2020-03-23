from environment import ENVIRONMENT

class ENVIRONMENTS:

    def __init__(self, numEnvs=4, eval_time=400):
        self.envs = {}
        self.numEnvs = numEnvs
        self.eval_time = eval_time

        for i in range(self.numEnvs):
            self.envs[i] = ENVIRONMENT(i, eval_time=self.eval_time)
