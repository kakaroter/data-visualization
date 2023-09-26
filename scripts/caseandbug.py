import os
import sys
import re

def remove_duplicate_links(input_file, output_file):
    links = {}  # 创建一个空字典来存储链接和它们的出现次数

    # 打开输入文件并读取链接
    with open(input_file, 'r') as f:
        for line in f:
            link = line.strip()
            # 如果链接已经在字典中，增加它的计数；否则，将它添加到字典中并设置计数为1
            if link in links and link.startswith('https'):
                links[link] += 1
            elif link.startswith('https'):
                links[link] = 1

                # 打开输出文件并写入结果
    with open(output_file, 'w') as f:
        for link, count in links.items():
            if count > 1:  # 如果链接出现了多次，打印一个消息
                f.write(f'{link} 出现了 {count} 次\n')
            else:  # 否则，只打印链接
                f.write(link + '\n')

    with open(output_file, 'r') as f:
        for line in f:
            link = line.strip()
            if link.endswith('次'):
                cmd = f'echo {link} >> repeatlist.txt'
                os.system(cmd)
            elif 'bug' in link:
                cmd = f'echo {link} >> buglist.txt'
                os.system(cmd)
            elif 'testcase' in link:
                cmd = f'echo {link} >> caselist.txt'
                os.system(cmd)
            else:
                print('someting wrong')

    with open('repeatlist.txt', 'r') as f:
        content = f.read()
        urls = re.findall(r'https://pms.uniontech.com/[^\s]+', content)
        for i in urls:
            if 'testcase' in i:
                cmd = f'echo {i} >> caselist.txt'
                os.system(cmd)
            elif 'bug' in i:
                cmd = f'echo {i} >> buglist.txt'
                os.system(cmd)
            else:
                print('someting wrong')



if __name__ == "__main__":
    if len(sys.argv) < 3:
        print('用法: python caseandbug.py <输入文件> <输出文件>')
    else:
        remove_duplicate_links(sys.argv[1], sys.argv[2])