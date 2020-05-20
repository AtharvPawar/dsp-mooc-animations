from manimlib.imports import *
import math

class freqVar(Scene):

    def construct(self):

        axes1 = Axes(
            x_min = -5,
            x_max = 5,
            y_min = -1,
            y_max = 1,
            x_axis_label = "$h[n]$",
            y_axis_label = "$n$",
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
            x_axis_label = "$e^{j\\omega n$",
            y_axis_label = "$n$",
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
        y_h = [max(1-abs(x)/3,0) for x in range(-5,6)]

        dots_h_real, lines_h_real = self.plot_discrete(x_points, y_h, myaxes=axes1)
        dots_h_img, lines_h_img = self.plot_discrete(x_points, np.zeros(len(x_points)), myaxes=axes1, mycolor=RED)
        self.wait(1)

        omega = ValueTracker(-PI)

        graph_trig = []
        graph_trig.append(axes2.get_graph(lambda x: np.cos(omega.get_value()*x), color=YELLOW, stroke_width=DEFAULT_STROKE_WIDTH/5))
        graph_trig.append(axes2.get_graph(lambda x: np.sin(omega.get_value()*x), color=RED, stroke_width=DEFAULT_STROKE_WIDTH/5))

        graph_trig[0].add_updater(
            lambda mob: mob.become(axes2.get_graph(lambda x: np.cos(omega.get_value()*x), color=YELLOW, stroke_width=DEFAULT_STROKE_WIDTH/5))
            )
        graph_trig[1].add_updater(
            lambda mob: mob.become(axes2.get_graph(lambda x: np.sin(omega.get_value()*x), color=RED, stroke_width=DEFAULT_STROKE_WIDTH/5))
            )

        omega_text = TextMobject('$\\omega = $')
        # omega_vals = [TexMobject(w/10, color=GREEN) for w in range(-30,31)]
        omega_val = DecimalNumber(omega.get_value(), num_decimal_places=3, color=GREEN)
        omega_val.add_updater(
            lambda mob: mob.set_value(omega.get_value()))

        omega_group = VGroup(omega_text, omega_val)
        omega_group.arrange(RIGHT, aligned_edge=DOWN)
        omega_group.to_edge(DOWN)

        self.play(ShowCreation(omega_text), ShowCreation(omega_val))
        self.play(ShowCreation(graph_trig[0]), ShowCreation(graph_trig[1]))

        y_cos = [np.cos(omega.get_value()*x) for x in x_points]
        y_sin = [np.sin(omega.get_value()*x) for x in x_points]

        dots_cos, lines_cos = self.plot_discrete(x_points, y_cos, axes2)
        dots_sin, lines_sin = self.plot_discrete(x_points, y_sin, axes2, RED)

        self.wait(1)

        for x, dot_cos, dot_sin, lin_cos, lin_sin in zip(x_points, dots_cos, dots_sin, lines_cos, lines_sin):
            dot_cos.add_updater(
                lambda mob, x=x: mob.move_to(axes2.c2p(x, np.cos(omega.get_value()*x))),
                # call_updater=False
                )
            # self.add(dots_cos[i])
            dot_sin.add_updater(
                lambda mob, x=x: mob.move_to(axes2.c2p(x, np.sin(omega.get_value()*x))),
                # call_updater=False
                )
            # self.add(dots_sin[i])
            lin_cos.add_updater(
                lambda mob, x=x: mob.become(Line(axes2.c2p(x, 0),
                    axes2.c2p(x, np.cos(omega.get_value()*x)), color=YELLOW)),
                # call_updater=False
                )
            # self.add(lines_cos[i])
            lin_sin.add_updater(
                lambda mob, x=x: mob.become(Line(axes2.c2p(x, 0),
                    axes2.c2p(x, np.sin(omega.get_value()*x)), color=RED)),
                # call_updater=False
                )
            # self.add(lines_sin[i])

        self.play(
            omega.set_value, PI,
            rate_func=smooth,
            run_time=10)

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
