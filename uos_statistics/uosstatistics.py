from pyecharts import options as opts
from pyecharts.charts import Bar, Line, Pie
import pandas as pd
import re
from pyecharts.globals import ThemeType


class UosStatistics:
    def __init__(self, file_path='/home/qjx/Downloads/DDE-1061.xlsx'):
        self.df = pd.read_excel(file_path)

    def get_module_data(self):
        original_module = self.df['所属模块'].value_counts().to_dict()
        new_module = {}
        for key, value in original_module.items():
            new_key = re.sub(r'\(#\d+\)', '', key)
            new_module[new_key] = value
        return new_module

    def get_level_data(self):
        original_level = self.df['严重程度'].value_counts().to_dict()
        return original_level

    def get_bar_data(self, data):
        x_data = []
        y_data = []
        for i in data.keys():
            if int(data[i]) > 1:
                x_data.append(i)
                y_data.append(data[i])
        return x_data, y_data

    def generate_bar_chart(self, data):
        # data_sorted = reversed(data[1])
        bar = Bar(init_opts=opts.InitOpts(width='1650px',
                                          height='700px',
                                          is_horizontal_center=True,
                                          theme=ThemeType.WONDERLAND))
        bar.add_xaxis(data[0])
        bar.add_yaxis('bug模块分布', data[1])
        # bar.add_yaxis('bug等级分布', data2[1])
        # bar.reversal_axis()
        bar.set_series_opts(label_opts=opts.LabelOpts(position="right"))
        bar.set_global_opts(title_opts={"text": "DDE模块bug分布图", "subtext": ""},
                            # datazoom_opts=opts.DataZoomOpts(type_="inside"),
                            datazoom_opts=[opts.DataZoomOpts(), opts.DataZoomOpts(type_="inside")],
                            toolbox_opts=opts.ToolboxOpts(),
                            legend_opts=opts.LegendOpts(is_show=False),
                            # xaxis_opts=opts.AxisOpts(name="我是 X 轴"),
                            # yaxis_opts=opts.AxisOpts(name="bug数量"),

                            )
        bar.set_series_opts(
            label_opts=opts.LabelOpts(is_show=False),
            markpoint_opts=opts.MarkPointOpts(
                data=[
                    opts.MarkPointItem(type_="max", name="最大值"),
                    opts.MarkPointItem(type_="min", name="最小值"),
                    opts.MarkPointItem(type_="average", name="平均值"),
                ]
            )
        )
        bar.render()

    def generate_pie_chart(self, data):
        pie = Pie(init_opts=opts.InitOpts(width='1650px',
                                          height='700px',
                                          theme=ThemeType.WONDERLAND
                                          ))
        pie.add(series_name='bug数量', data_pair=data)
        # pie.center = ["40%", "50%"]
        pie.set_global_opts(
            title_opts=opts.TitleOpts(title="DDE模块bug分布"),
            legend_opts=opts.LegendOpts(type_="scroll",
                                        pos_left="80%",
                                        orient="vertical"),
        )
        pie.set_series_opts(label_opts=opts.LabelOpts(formatter="{b}:{c} {d}%"))

        pie.render()

    def read_html(self):
        with open('render.html', 'r', encoding='utf-8') as f:
            html_content = f.read()
            new_title = '缺陷分析平台'
            html_content = html_content.replace("<title>Awesome-pyecharts</title>", f"<title>{new_title}</title>")
        with open('render.html', 'w', encoding='utf-8') as f:
            f.write(html_content)


if __name__ == '__main__':
    u = UosStatistics('/home/qjx/Downloads/DDE-10551061.xlsx')
    # level_data = u.get_level_data()
    module_data = u.get_module_data()
    print(module_data)
    # new_level = u.get_bar_data(level_data)
    # new_module = u.get_bar_data(module_data)
    # # uos_statistics().generate_bar_chart(new_level)
    # u.generate_bar_chart(new_module)
    u.generate_pie_chart([(key, value) for key, value in module_data.items()])
