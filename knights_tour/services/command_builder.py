from knights_tour.domain.task import Task
from knights_tour.domain.pos import Pos
import knights_tour.utils.localizations as loc
import knights_tour.utils.file_manager as fm

import os 
import re 

from knights_tour.utils.env import Env


class CommandBuilder(object):
    ''' This class is used for building a bash script form a Task
        The script will contain all the information needed to launch
        Minizinc or Clingo on a certain problem instance
    '''


    @staticmethod
    def build_command(task: Task):
        if task.target == loc.CLINGO:
            return CommandBuilder.build_clingo_command(task)
        else:
            return CommandBuilder.build_mzn_command(task)


    @staticmethod
    def build_mzn_command(task: Task):
        cmd = fm.from_txt(loc.MINIZINC_CMD_PATH)
        cmd = cmd.replace("[[MZN_PATH]]", Env.get_value(Env.MINIZINC))
        for m in re.findall(r'\[\[[^\[]+\]\]', cmd):
            t = m.replace("[[", "").replace("]]", "")
            cmd = cmd.replace(m, task.params[t])
        fm.to_txt(cmd, loc.abs_path([task.folder, "command.sh"]))
        return f"sh {os.path.join(task.folder, 'command.sh')} {os.path.join(task.folder, loc.MINIZINC_MODEL)} {os.path.join(task.folder, loc.MINIZINC_DATABASE)}"


    @staticmethod
    def build_clingo_command(task: Task):
        cmd = fm.from_txt(loc.CLINGO_CMD_PATH)
        cmd = cmd.replace('[[n]]', str(task.n))
        cmd = cmd.replace('[[model_path]]', os.path.join(task.folder,'knights_tour.lp'))
        cmd = cmd.replace('[[database_path]]', os.path.join(task.folder,'database.lp'))
        fm.to_txt(cmd, loc.abs_path([task.folder, "command.sh"]))
        return f"sh {os.path.join(task.folder, 'command.sh')}"