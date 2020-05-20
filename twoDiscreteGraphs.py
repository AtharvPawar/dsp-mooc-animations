from manimlib.imports import *
import math

class TwoDiscreteGraphs(Scene):

    def construct(self):

        axes1 = Axes(
            x_min = -5,
            x_max = 5,
            y_min = -1,
            y_max = 1,
            x_labelled_nums = [-5,5],
            center_point = 2*UP,
            x_axis_config={
                "unit_size": 1,
                "tick_frequency": 1,
                "include_tip": False,
                "label_direction": DOWN+0.5*LEFT
            },
            y_axis_config={
                    "unit_size": 1.2,
                    "tick_frequency": 1,
                    "include_tip": False,
            })
        labels1x = axes1.get_x_axis().get_number_mobjects(*list(range(-5,6)))
        labels1y = axes1.get_y_axis().get_number_mobjects(*[-1,1])

        axes2 = Axes(
            x_min = -5,
            x_max = 5,
            y_min = -1,
            y_max = 1,
            x_labelled_nums = [-5,5],
            center_point = 1.5*DOWN,
            x_axis_config={
                "unit_size": 1,
                "tick_frequency": 1,
                "include_tip": False,
                "label_direction": DOWN+0.5*LEFT
            },
            y_axis_config={
                    "unit_size": 1.2,
                    "tick_frequency": 1,
                    "include_tip": False,
            })
        labels2x = axes2.get_x_axis().get_number_mobjects(*list(range(-5,6)))
        labels2y = axes2.get_y_axis().get_number_mobjects(*[-1,1])

        self.play(ShowCreation(axes1), ShowCreation(axes2))
        self.wait(0.5)
        self.play(ShowCreation(labels1x), ShowCreation(labels2x))
        # self.wait(0.5)
        # self.play(Uncreate(labels1x), Uncreate(labels2x))
        self.wait(0.5)
        self.play(ShowCreation(labels1y), ShowCreation(labels2y))
        # self.wait(0.5)
        # self.play(Uncreate(labels1y), Uncreate(labels2y))
        self.wait(1)

        x_points = np.array(range(-5,6))
        y_cos = [np.cos(x) for x in x_points]
        y_sin = [np.sin(x) for x in x_points]
        y_h = [max(1-abs(x)/3,0) for x in range(-5,6)]

        dots1, lines1 = self.plot_discrete(x_points, y_h, myaxes=axes1)
        dots2, lines2 = self.plot_discrete(x_points, np.zeros(len(x_points)), myaxes=axes1, mycolor=RED)
        self.wait(1)

        dots3, lines3 = self.plot_discrete(x_points, y_cos, myaxes=axes2)
        dots4, lines4 = self.plot_discrete(x_points, y_sin, myaxes=axes2, mycolor=RED)
        self.wait(2)        


    def plot_discrete(self, x_points, y_points, myaxes, mycolor=YELLOW):
        '''
        Plots a discrete function with points (x_points, y_points) on myaxes.
        '''

        dots = [Dot(myaxes.coords_to_point(x_points[i], y_points[i]), color=mycolor) for i in range(len(x_points))]
        lines = [Line(myaxes.coords_to_point(x_points[i], 0), myaxes.coords_to_point(x_points[i], y_points[i]), color=mycolor, fill_opacity=0.5)\
         for i in range(len(x_points))]
        self.play(

            *[AnimationGroup(
                Animation(Mobject(), run_time=0.1*i),
                ShowCreation(lines[i], run_time=0.5), lag_ratio=1) for i in range(len(lines))
                ],
            *[AnimationGroup(
                Animation(Mobject(), run_time=0.1*i+0.5),
                GrowFromCenter(dots[i], run_time=0.3), lag_ratio=1) for i in range(len(dots))
                ]
            )
        # self.play(*[GrowFromCenter(dot) for dot in dots], run_time=0.5)
        self.wait(0.1)
        return dots, lines