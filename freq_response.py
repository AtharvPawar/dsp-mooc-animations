from manimlib.imports import *
import math

class freqResponse(Scene):

    def construct(self):

        text1 = TextMobject("\\textsc{Representing frequency response \\\\ as an inner product}")
        
        self.play(ShowCreation(text1))
        self.wait(1.5)

        self.clear()

        text2 = TextMobject("Consider the following impulse response:")
        eq_RHS1 = TextMobject("$1-\\dfrac{|n|}{3}$, when $|n| \\le 3$", alignment="")
        eq_RHS2 = TextMobject("$0$, otherwise", alignment="")
        eq_RHS = VGroup(eq_RHS1, eq_RHS2)
        eq_RHS.arrange(DOWN, buff=MED_LARGE_BUFF, aligned_edge=LEFT)

        brace1 = Brace(eq_RHS, LEFT)
        eq_LHS = brace1.get_text("$h[n] = $")

        eq_group = VGroup(eq_LHS, brace1, eq_RHS)
        group1 = VGroup(text2, eq_group)

        group1.arrange(DOWN)

        self.play(Write(text2))
        self.play(Write(eq_group))
        self.wait(2)

        self.clear()

        text3 = TextMobject("The frequency response $H(\\omega)$ is obtained by calculating\\\\ \
            the inner product of the infinite sequences $h[n]$ and $e^{j\\omega n}$")
        text4 = TextMobject("For this special case, $h[n]$ is real and even function, \\\\ \
         we can write the $H(\\omega)$ as follows")
        group2 = VGroup(text3, text4)
        group2.arrange(DOWN, buff=MED_LARGE_BUFF)
        self.play(Write(group2))
        self.wait(5)
        self.clear()

        text41 = TexMobject("H(\\omega) = ")
        text42 = TexMobject("\\sum_{n=-\\infty}^{\\infty} \\overline{h[n]}\\, e^{j\\omega n}", color=GREEN)
        text43 = TexMobject("=")
        text44 = TexMobject("\\sum_{n=-\\infty}^{\\infty} h[n]\\, e^{j\\omega n}", color=GREEN)
        text4 = VGroup(text41, text42, text43, text44)
        text4.arrange(RIGHT, buff=MED_SMALL_BUFF)
        self.play(Write(text4))
        self.wait(2)
        self.clear()

        text5 = TextMobject("We can visualize this by plotting $h[n]$ and $e^{j\\omega n}$. \\\\ \
            As $\\omega$ changes, we get different sequences $e^{j\\omega n}$, and \\\\ \
            the inner product of $h[n]$ and $e^{j\\omega n}$ gives $H(\\omega)$. ")
        self.play(Write(text5))
        self.wait(2)
        self.clear()

        text6 = TextMobject("In the plots, yellow colour shows the real part, \\\\ \
            and red colour shows the \\\\ \
            imaginary part of the function value.")
        self.play(Write(text6))
        self.wait(1)
        self.clear()


        axes1 = Axes(
            x_min = -5,
            x_max = 5,
            y_min = -1,
            y_max = 1,
            y_axis_label = "$h[n]$",
            x_axis_label = "$n$",
            x_labelled_nums = list(range(-5,6)),
            y_labelled_nums = [-1,1],
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
        xlabel1 = TextMobject(axes1.x_axis_label)
        xlabel1.next_to(
            axes1.get_x_axis().get_tick_marks(), UP+RIGHT, buff=SMALL_BUFF)
        ylabel1 = TextMobject(axes1.y_axis_label)
        ylabel1.next_to(
            axes1.get_y_axis().get_tick_marks(), UP+RIGHT, buff=SMALL_BUFF)

        axes2 = Axes(
            x_min = -5,
            x_max = 5,
            y_min = -1,
            y_max = 1,
            y_axis_label = "$e^{j\\omega n}$",
            x_axis_label = "$n$",
            x_labelled_nums = list(range(-5,6)),
            y_labelled_nums = [-1,1],
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
        xlabel2 = TextMobject(axes2.x_axis_label)
        xlabel2.next_to(
            axes2.get_x_axis().get_tick_marks(), UP+RIGHT, buff=SMALL_BUFF)
        ylabel2 = TextMobject(axes2.y_axis_label)
        ylabel2.next_to(
            axes2.get_y_axis().get_tick_marks(), UP+RIGHT, buff=SMALL_BUFF)

        self.play(ShowCreation(axes1), ShowCreation(axes2))
        # self.wait(0.5)
        self.play(ShowCreation(labels1x), ShowCreation(labels2x), ShowCreation(xlabel1), ShowCreation(xlabel2))
        # self.wait(0.5)
        # self.play(Uncreate(labels1x), Uncreate(labels2x))
        # self.wait(0.5)
        self.play(ShowCreation(labels1y), ShowCreation(labels2y), ShowCreation(ylabel1), ShowCreation(ylabel2))
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
        graph_trig.append(axes2.get_graph(lambda x: np.cos(omega.get_value()*x), color=YELLOW, stroke_width=DEFAULT_STROKE_WIDTH/3))
        graph_trig.append(axes2.get_graph(lambda x: np.sin(omega.get_value()*x), color=RED, stroke_width=DEFAULT_STROKE_WIDTH/3))

        graph_trig[0].add_updater(
            lambda mob: mob.become(axes2.get_graph(lambda x: np.cos(omega.get_value()*x), color=YELLOW, stroke_width=DEFAULT_STROKE_WIDTH/3))
            )
        graph_trig[1].add_updater(
            lambda mob: mob.become(axes2.get_graph(lambda x: np.sin(omega.get_value()*x), color=RED, stroke_width=DEFAULT_STROKE_WIDTH/3))
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
            rate_func=linear,
            run_time=10)

        self.wait(2)
        self.clear()

        text7 = TextMobject("As $\\omega$ varies, the $e^{j\\omega n}$ sequence changes, hence \\\\ \
            $H(\\omega)$ changes. The plot of $H(\\omega)$ \\\\ \
            would be generated as follows.")
        self.play(Write(text7))
        self.wait(5)
        self.clear()

        axes3 = Axes(
            x_min = -PI,
            x_max = PI,
            y_min = -1,
            y_max = 3,
            y_axis_label = "$H(\\omega)$",
            x_axis_label = "$\\omega$",
            x_labelled_nums = list(range(-3,4)),
            y_labelled_nums = [-1,1],
            center_point = 1*DOWN,
            x_axis_config={
                "unit_size": 1.8,
                "tick_frequency": 2*PI,
                "include_tip": False,
                "label_direction": DOWN+0.5*LEFT
            },
            y_axis_config={
                    # "unit_size": 1.2,
                    "tick_frequency": 1,
                    "include_tip": False,
            })
        labelsx = axes3.get_x_axis().get_number_mobjects(*list(range(-3,4)))
        ticks = VGroup(*[axes3.get_x_axis().get_tick(x) for x in range(-3,4)])
        xlabel3 = TextMobject(axes3.x_axis_label)
        xlabel3.next_to(
            axes3.get_x_axis().get_tick(PI), DOWN+RIGHT, buff=SMALL_BUFF)
        ylabel3 = TextMobject(axes3.y_axis_label)
        ylabel3.next_to(
            axes3.get_y_axis().get_tick_marks(), UP+RIGHT, buff=SMALL_BUFF)
        omega.set_value(-PI)
        self.play(ShowCreation(axes3))
        self.play(ShowCreation(labelsx), ShowCreation(ticks), ShowCreation(xlabel3), ShowCreation(ylabel3))

        def H_om(x):
            return 1 + 4/3*np.cos(x) + 2/3*np.cos(2*x)
        graph_H_om = axes3.get_graph(H_om, color=BLUE)

        # self.play(ShowCreation(graph_H_om))
        # self.play(ShowCreation(omega_text), ShowCreation(omega_val))
        self.wait(1)

        vline = Line(axes3.c2p(omega.get_value(), 0),axes3.c2p(omega.get_value(), H_om(omega.get_value())))
        dot = Dot(axes3.c2p(omega.get_value(), H_om(omega.get_value())))

        vline.add_updater(
            lambda mob: mob.become(Line(axes3.c2p(omega.get_value(), 0),
                axes3.c2p(omega.get_value(), H_om(omega.get_value()))),
            )
        )
        dot.add_updater(
            lambda mob: mob.move_to(axes3.c2p(omega.get_value(), H_om(omega.get_value())))
        )

        self.play(
            ShowCreation(omega_text), ShowCreation(omega_val),
            ShowCreation(vline, run_time=0.5),
            AnimationGroup(
                Animation(Mobject(), run_time=0.5),
                ShowCreation(dot, run_time=0.3),
                lag_ratio=1)
            )
        self.wait(0.5)
        self.play(
            ShowCreation(graph_H_om, rate_func=smooth),
            omega.set_value, PI,
            rate_func=smooth,
            run_time=6)
        self.wait(3)






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
        # self.wait(0.1)

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
        # self.wait(0.1)
        return dots, lines
