from manimlib.imports import *
import math

from math import pi

def chebyschev_polynomial(x, N):
    """
    Evaluates the Nth order Chebyschev polynomial at x and returns the value.
    """
    if x < 1 and x >= -1:
        return math.cos(N * math.acos(x))
    elif x < -1:
        if N % 2 == 0:
            return math.cosh(N * math.acosh(-x))
        else:
            return -math.cosh(N * math.acosh(-x))
    else:
        return math.cosh(N * math.acosh(x))

def chebyschev_lowpass(f_pass, f_stop, tol_pass, tol_stop):
    """
    Returns the Chebyschev analog lowpass filter function corresponding to
    passband and stopband frequencies and tolerances.

    Inputs:
    - f_pass: The passband boundary frequency in Hz
    - f_stop: The stopband boundary frequency in Hz
    - tol_pass: The tolerance required in the passband
    - tol_stop: The tolerance required in the stopband.

    Returns a function that takes a frequency (in Hz) as input and returns
    the filter magnitude at that frequency as the output.
    """

    if f_pass == f_stop:
        raise ValueError('The passband and stopband frequencies cannot be equal.')

    if tol_pass == 0 or tol_stop == 0:
        raise ValueError('Tolerance values cannot be zero.')

    D1 = 1 / (1 - tol_pass)**2 - 1
    D2 = 1 / tol_stop**2 - 1

    # Optimal epsilon to get minimum N possible
    # epsilon = math.sqrt(D1)
    
    # Minimum order of the filter that is required
    # (Note that D1 is the same as epsilon**2)
    N = math.acosh(D2 / D1) / math.acosh(f_stop / f_pass)
    N = math.ceil(N)

    def filter_func(f):
        # Note that D1 is the same as epsilon**2
        mag2 = 1 / (1 + D1*chebyshev_polynomial(f / f_pass, N)**2)
        return math.sqrt(mag2)

    return filter_func

class chebyschev(Scene):
    """
    Class inheriting from the Scene class, which is used to generate the animation.
    """
    
    def construct(self):
        """
        Construct method used in place of __init__ as per standard manimlib usage.

        This method includes the instructions to create the complete animation for Lecture 22.
        We first show the variation of the lower limit of N with epsilon (as defined in the lecture).
        Then we show how the Chebyschev filter magnitude function changes as we change epsilon and N.
        """

        # defining the specifications for a Chebyschev filter
        f_pass = 10e3
        f_stop = 12e3
        tol_pass = 0.05
        tol_stop = 0.05

        # defining some useful constants
        epsilon_max = math.sqrt(1 / (1 - tol_pass)**2 - 1)
        D2 = 1 / tol_stop**2 - 1

        N_min = math.acosh(math.sqrt(D2) / epsilon_max) / math.acosh(f_stop / f_pass)
        N_min = math.ceil(N_min)

        # define a function to get minimum required filter order N (non integral value)
        def get_N(epsilon, D2, f_ratio):
            return math.acosh(math.sqrt(D2) / epsilon) / math.acosh(f_ratio)

        # define a function to get filter function corresponding to an epsilon and N
        def get_filter(epsilon, N):
            return lambda x: math.sqrt(1 / (1 + (epsilon * chebyschev_polynomial(x, N))**2))

        ####

        text1 = TextMobject("\\textsc{Chebyschev Magnitude Filter Function \\\\ and its Parameters}")
        
        self.play(ShowCreation(text1))

        self.wait(1.5)
        self.clear()

        text2 = TextMobject("Consider the following filter specifications:")

        specs = TextMobject("\\rm\\begin{align*} \\text{Passband Edge} &= \\Omega_P = \\text{10 kHz}\\\\\
            \\text{Stopband Edge} &= \\Omega_S = \\text{12 kHz}\\\\\
            \\text{Passband Tolerance} &= \\delta_1 = \\text{0.05}\\\\\
            \\text{Stopband Tolerance} &= \\delta_2 = \\text{0.05}\\end{align*}")

        specs_group = VGroup(text2, specs)
        specs_group.arrange(DOWN)

        self.play(Write(specs_group))

        self.wait(4)
        self.clear()

        text3_1 = TextMobject("The Chebyschev magnitude filter\\\\ function is given by:")
        text3_2 = TexMobject("H^2(\\Omega)", " = \\dfrac{1}{1 + \\epsilon^2\\, C^2_N({\\Omega \\over \\Omega_P})}")
        text3_2[0].set_color(YELLOW)
        text3_3 = TextMobject("where, $C_N(\\cdot)$ is the $N$th order\\\\ Chebyschev polynomial")
        text3 = VGroup(text3_1, text3_2, text3_3)
        text3.arrange(DOWN)

        self.play(Write(text3))

        self.wait(4)
        self.clear()

        text4_1 = TextMobject("To satisfy tolerance requirements, we must have:")
        text4_2 = TexMobject("\\epsilon^2", "\\le \\frac{1}{(1-\\delta_1)^2} - 1")
        text4_2[0].set_color(GREEN)
        text4_3 = TexMobject("N", "\\ge \
            \\dfrac{ \\cosh^{-1} \\left( \\frac{1}{\\epsilon}\\sqrt{\\frac{1}{\\delta^2} - 1} \\right) }{\
            \\cosh^{-1}(\\Omega_S / \\Omega_P)}")
        text4_3[0].set_color(BLUE)
        text4 = VGroup(text4_1, text4_2, text4_3)
        text4.arrange(DOWN)

        self.play(Write(text4))

        self.wait(4)
        self.clear()

        text5 = TextMobject(f"For our specifications, $\\epsilon_{{\\rm max}} = {epsilon_max:.3f}$. \\\\"
            "Then the minimum required order of the \\\\ Chebyschev polynomial, $N_{\\rm min}$, "
            "can be plotted as follows.")

        self.play(Write(text5))

        self.wait(4)
        self.clear()

        ####

        x_min1, x_max1 = 0, epsilon_max
        y_min1, y_max1 = 0, 15
        x_us1, y_us1 = 20, 0.5

        axes1 = Axes(
                x_min = x_min1,
                x_max = x_max1,
                y_min = y_min1,
                y_max = y_max1,
                x_axis_label = "\\epsilon",
                y_axis_label = "N_{\\rm min}",
                x_labelled_nums = np.arange(0.0, x_max1, 0.05),
                y_labelled_nums = np.arange(y_min1+2, y_max1, 2),
                center_point = x_us1 * (x_min1 + x_max1) / 2 * LEFT + y_us1 * (y_min1 + y_max1) / 2 * DOWN,
                x_axis_config={
                    "unit_size": x_us1,
                    "tick_frequency": 0.05,
                    "include_tip": False,
                    "label_direction": DOWN+RIGHT,
                    "include_ticks": True,
                    "decimal_number_config": {
                        "num_decimal_places": 1,
                    },
                },
                y_axis_config={
                    "unit_size": y_us1,
                    "tick_frequency": 2,
                    "include_tip": False,
                    "label_direction": UP+LEFT,
                    "include_ticks": True,
                })

        axis_labels1 = VGroup(
            axes1.get_x_axis_label("\\epsilon", direction=UR*0.5),
            axes1.get_y_axis_label("N_{\\rm min}", direction=LEFT)
            )
        coord_labels1 = VGroup(
            axes1.get_x_axis().get_number_mobjects(*axes1.x_labelled_nums.tolist(), scale_val=0.6, direction=DOWN),
            axes1.get_y_axis().get_number_mobjects(*axes1.y_labelled_nums.tolist(), scale_val=0.7, direction=LEFT)
            )

        N_vs_epsilon_graph = axes1.get_graph(
            lambda x: get_N(x, D2, f_stop / f_pass),
            stroke_width = DEFAULT_STROKE_WIDTH,
            color=BLUE)

        self.play(ShowCreation(axes1), ShowCreation(axis_labels1), ShowCreation(coord_labels1))
        self.play(ShowCreation(N_vs_epsilon_graph))

        self.wait(5)
        self.clear()

        text6 = TextMobject("We can also see the filter magnitude \\\\ \
            function and how it changes on \\\\ independently \
            varying $\\epsilon$ and $N$", tex_to_color_map={"$\\epsilon$":GREEN, "$N$":BLUE})

        self.play(Write(text6))
        self.wait(3)

        self.clear()

        # ####

        x_min2, x_max2 = 0, 2
        y_min2, y_max2 = 0, 1.5
        x_us2, y_us2 = 3, 3

        axes2 = Axes(
                x_min = x_min2,
                x_max = x_max2,
                y_min = y_min2,
                y_max = y_max2,
                y_axis_label = "$H(\\Omega)$",
                x_axis_label = "$\\Omega$",
                # x_labelled_nums = [1, f_stop / f_pass],
                # y_labelled_nums = [tol_stop, 1-tol_pass],
                center_point = x_us2 * (x_min2 + x_max2) / 2 * LEFT + y_us2 * (y_min2 + y_max2) / 2 * DOWN,
                x_axis_config={
                    "unit_size": x_us2,
                    # "tick_frequency": 1,
                    "include_tip": False,
                    "label_direction": DOWN+RIGHT,
                    "include_ticks": False,
                },
                y_axis_config={
                    "unit_size": y_us2,
                    # "tick_frequency": 1,
                    "include_tip": False,
                    "label_direction": UP+LEFT,
                    "include_ticks": False,
                })

        axis_labels2 = VGroup(
            axes2.get_x_axis_label("\\Omega", direction=0.5*DR),
            axes2.get_y_axis_label("H(\\Omega)", direction=0.5*UL)
            )

        # defining tick marks mobjects
        f_pass_tick = axes2.get_x_axis().get_tick(1.0)
        f_stop_tick = axes2.get_x_axis().get_tick(f_stop / f_pass)

        tol_stop_tick = axes2.get_y_axis().get_tick(tol_stop)
        tol_pass_tick = axes2.get_y_axis().get_tick(1 - tol_pass)
        unity_tick = axes2.get_y_axis().get_tick(1.0)

        ticks1 = VGroup(f_pass_tick, f_stop_tick, tol_pass_tick, tol_stop_tick, unity_tick)

        # now get the labels for the tick marks
        f_pass_mob = TexMobject("\\Omega_P").scale(0.8)
        f_pass_mob.next_to(f_pass_tick, DOWN+0.5*LEFT, buff=SMALL_BUFF)
        f_stop_mob = TexMobject("\\Omega_S").scale(0.8)
        f_stop_mob.next_to(f_stop_tick, DOWN+0.5*RIGHT, buff=SMALL_BUFF)
        
        tol_stop_mob = TexMobject("\\delta_2").scale(0.8)
        tol_stop_mob.next_to(tol_stop_tick, LEFT, buff=SMALL_BUFF)
        tol_pass_mob = TexMobject("1 - \\delta_1").scale(0.8)
        tol_pass_mob.next_to(tol_pass_tick, 0.5*DOWN+LEFT, buff=SMALL_BUFF)
        unity_mob = TexMobject("1").scale(0.8)
        unity_mob.next_to(unity_tick, 0.5*UP+LEFT, buff=SMALL_BUFF)

        mobs1 = VGroup(f_pass_mob, f_stop_mob, tol_pass_mob, tol_stop_mob, unity_mob)

        # define value trackers to track how the filter function changes as epsilon and N are changed
        epsilon = ValueTracker(epsilon_max)
        N = ValueTracker(N_min)

        # create odometers for N and epsilon
        epsilon_text = TexMobject("\\epsilon = ")
        epsilon_val = DecimalNumber(epsilon.get_value(), num_decimal_places=3, color=GREEN)
        epsilon_val.add_updater(lambda mob: mob.set_value(epsilon.get_value()))
        epsilon_group = VGroup(epsilon_text, epsilon_val)
        epsilon_group.arrange(RIGHT, aligned_edge=DOWN)

        N_text = TexMobject("N = ")
        N_val = DecimalNumber(N.get_value(), num_decimal_places=0, color=BLUE)
        N_val.add_updater(lambda mob: mob.set_value(math.floor(N.get_value())))
        N_group = VGroup(N_text, N_val)
        N_group.arrange(RIGHT, aligned_edge=DOWN)

        odo_group = VGroup(epsilon_group, N_group)
        odo_group.arrange(RIGHT, aligned_edge=DOWN, buff=LARGE_BUFF)
        odo_group.move_to(3.25*DOWN)

        filter_graph = axes2.get_graph(get_filter(
            epsilon=epsilon.get_value(),
            N=N.get_value()),
        stroke_width = DEFAULT_STROKE_WIDTH * 0.6,
        color=YELLOW)

         # create rectangles highlighting the valid region
        passband_region = Rectangle(
            width = 1 * axes2.get_x_axis().unit_size,
            height = tol_pass * axes2.get_y_axis().unit_size,
            fill_color=GREEN,
            fill_opacity=0.5,
            background_stroke_color=GREEN,
            background_stroke_opacity = 0.5,
            stroke_opacity=0
            # stroke_width=0.0
            )
        stopband_region = Rectangle(
            width = (axes2.x_max - f_stop / f_pass) * axes2.get_x_axis().unit_size,
            height = tol_stop * axes2.get_y_axis().unit_size,
            fill_color=GREEN,
            fill_opacity=0.5,
            background_stroke_color=GREEN,
            background_stroke_opacity = 0.5,
            stroke_opacity=0
            # stroke_width=0.0
            )
        passband_region.align_to(tol_pass_tick, direction=DOWN)
        passband_region.align_to(axes2.get_x_axis(), direction=LEFT)
        stopband_region.align_to(f_stop_tick, direction=LEFT)
        stopband_region.align_to(axes2.get_y_axis(), direction=DOWN)

        # plot the filter function now
        self.play(ShowCreation(axes2), ShowCreation(axis_labels2))

        self.play(
            ShowCreation(ticks1),
            ShowCreation(mobs1),
            ShowCreation(odo_group)
            )

        self.wait(0.1)
        
        self.play(
            ShowCreation(passband_region),
            ShowCreation(stopband_region),
            )
        self.play(ShowCreation(filter_graph))

        # now we add updater for the graph
        filter_graph.add_updater(
            lambda mob: mob.become(axes2.get_graph( get_filter( epsilon=epsilon.get_value(), N=N.get_value() ),
                color=YELLOW, stroke_width = DEFAULT_STROKE_WIDTH * 0.6) ),
            )

        # now we show the variation in the filter function with epsilon and N
        self.play(
            epsilon.set_value, epsilon_max / 100,
            rate_func=linear,
            run_time=5)
        self.wait(2)

        self.play(
            epsilon.set_value, epsilon_max,
            rate_func=linear,
            run_time=2)
        self.wait(2)

        self.play(
            N.set_value, N_min * 2,
            rate_func=linear,
            run_time=5)
        self.wait(2)

        self.play(
            N.set_value, N_min,
            rate_func=linear,
            run_time=2)
        self.wait(2)

        self.play(
            N.set_value, N_min // 2,
            rate_func=linear,
            run_time=5)
        self.wait(2)

        self.play(
            N.set_value, N_min,
            rate_func=linear,
            run_time=2)

        self.wait(5)