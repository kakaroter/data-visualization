#!/bin/bash
find ./ -type f -name "*.txt" ! -name "*input.txt" -exec rm {} +
echo "文件清理完毕，可使用命令【python caseandbug.py <输入文件> <输出文件>】重新生成新的list！！！"