import argparse
import os
import sys

# 把当前文件路径加入python环境变量，避免导入本地文件失败
sys.path.append(os.path.dirname(__file__))

from src.auto_questionnaire import AutoQuestionnaireAnswer
from src.utils import cfg_from_yaml_file


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='arg parser')
    parser.add_argument('--cfg_file', type=str, default='example\zhangsan_config.yaml', help='specify the config for one custom')
    args = parser.parse_args()
    cfg = cfg_from_yaml_file(args.cfg_file)
    
    answer = AutoQuestionnaireAnswer(cfg)
    total_try = cfg.NUM_TO_ANS
    try:
        for one_try in range(total_try):
            answer.run()
            print(f"已填写 {one_try} 份问卷")
    except KeyboardInterrupt:
        handles = answer.driver.window_handles
        answer.driver.switch_to.window(handles[0])
        answer.driver.close()
        exit()
