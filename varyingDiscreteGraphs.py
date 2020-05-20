from manimlib.imports import *
import math

class varDG(Scene):

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

        dots_h_real, lines_h_real = self.plot_discrete(x_points, y_h, myaxes=axes1)
        dots_h_img, lines_h_img = self.plot_discrete(x_points, np.zeros(len(x_points)), myaxes=axes1, mycolor=RED)
        self.wait(1)

        y_cosw = [[np.cos(w*x/10) for x in x_points] for w in range(-30, 31)]
        y_sinw = [[np.sin(w*x/10) for x in x_points] for w in range(-30, 31)]
        
        dots_cosw = [self.to_dots(x_points, y_cosw[i], axes2) for i in range(len(range(-30, 31)))]
        lines_cosw = [self.to_lines(x_points, y_cosw[i], axes2) for i in range(len(range(-30, 31)))]
        dots_sinw = [self.to_dots(x_points, y_sinw[i], axes2, RED) for i in range(len(range(-30, 31)))]
        lines_sinw = [self.to_lines(x_points, y_sinw[i], axes2, RED) for i in range(len(range(-30, 31)))]

        graph_cosw = [axes2.get_graph(lambda x: np.cos(w*x/10), color=YELLOW, stroke_width=DEFAULT_STROKE_WIDTH/5) for w in range(-30,31)]
        graph_sinw = [axes2.get_graph(lambda x: np.sin(w*x/10), color=RED, stroke_width=DEFAULT_STROKE_WIDTH/5) for w in range(-30,31)]

        omega_vals = [w/10 for w in range(-30,31)]
        
        omega_text = TextMobject('$\\omega = $')
        # omega_vals = [TexMobject(w/10, color=GREEN) for w in range(-30,31)]
        omega_val = DecimalNumber(-3.0, num_decimal_places=1, color=GREEN)

        omega = VGroup(omega_text, omega_val)
        omega.arrange(RIGHT, aligned_edge=DOWN)
        omega.to_edge(DOWN)
        
        # for om_val in omega_vals:
        #     om_val.shift(3.5*DOWN)
        #     om_val.next_to(omega_text, RIGHT)

        self.play(ShowCreation(omega_text), ShowCreation(omega_val))
        self.play(ShowCreation(graph_cosw[0]), ShowCreation(graph_sinw[0]))
        self.plot_discrete_from_obs(dots_cosw[0], lines_cosw[0])
        self.plot_discrete_from_obs(dots_sinw[0], lines_sinw[0])
        self.wait(1)

        for i in range(1, len(range(-30, 31))):
            self.play(
                *[ReplacementTransform(dots_cosw[i-1][j], dots_cosw[i][j]) for j in range(len(dots_cosw[0]))],
                *[ReplacementTransform(lines_cosw[i-1][j], lines_cosw[i][j]) for j in range(len(lines_cosw[0]))],
                *[ReplacementTransform(dots_sinw[i-1][j], dots_sinw[i][j]) for j in range(len(dots_sinw[0]))],
                *[ReplacementTransform(lines_sinw[i-1][j], lines_sinw[i][j]) for j in range(len(lines_sinw[0]))],
                ReplacementTransform(graph_cosw[i-1], graph_cosw[i]),
                ReplacementTransform(graph_sinw[i-1], graph_sinw[i]),
                ChangeDecimalToValue(omega_val, omega_vals[i]),
                run_time=0.1
                )
        self.wait(2)


    def to_dots(self, x_points, y_points, myaxes, mycolor=YELLOW):
        '''
        Converts point coordinates to Dots objects
        '''
        return [Dot(myaxes.coords_to_point(x_points[i], y_points[i]), color=mycolor) for i in range(len(x_points))]        

    def to_lines(self, x_points, y_points, myaxes, mycolor=YELLOW):
        '''
        Converts point coordinates to Lines objects
        '''
        return [Line(myaxes.coords_to_point(x_points[i], 0), myaxes.coords_to_point(x_points[i], y_points[i]), color=mycolor, fill_opacity=0.5)\
         for i in range(len(x_points))]

    def plot_discrete_from_obs(self, dots, lines):
        '''
        Plots a discrete function from dots and lines objects
        '''
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

    def plot_discrete(self, x_points, y_points, myaxes, mycolor=YELLOW):
        '''
        Plots a discrete function with points (x_points, y_points) on myaxes.
        '''

        dots = self.to_dots(x_points, y_points, myaxes, mycolor)
        lines = self.to_lines(x_points, y_points, myaxes, mycolor)
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