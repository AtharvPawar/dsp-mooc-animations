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
        mag2 = 1 / (1 + D1*chebyshev_polynomial(f / f_pass, N))
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

        N_min = math.acosh(D2 / epsilon_max**2) / math.acosh(f_stop / f_pass)
        N_min = math.ceil(N_min)

        # define a function to get minimum required filter order N (non integral value)
        def get_N(epsilon, D2, f_ratio):
            return math.acosh(D2 / epsilon**2) / math.acosh(f_ratio)

        # define a function to get filter function corresponding to an epsilon and N
        def get_filter(epsilon, N):
            return lambda x: math.sqrt(1 / (1 + epsilon**2 * chebyschev_polynomial(x, N)))

        axes1 = Axes(
                x_min = 0,
                x_max = 2,
                y_min = 0,
                y_max = 1.5,
                y_axis_label = "$H(\\Omega)$",
                x_axis_label = "$\\Omega$",
                # x_labelled_nums = [1, f_stop / f_pass],
                # y_labelled_nums = [tol_stop, 1-tol_pass],
                center_point = 2.25*DOWN+3*LEFT,
                x_axis_config={
                    "unit_size": 3,
                    # "tick_frequency": 1,
                    "include_tip": False,
                    "label_direction": DOWN,
                    "include_ticks": False
                },
                y_axis_config={
                    "unit_size": 3,
                    # "tick_frequency": 1,
                    "include_tip": False,
                    "include_ticks": False
                })

        # defining tick marks mobjects
        f_pass_tick = axes1.get_x_axis().get_tick(1.0)
        f_stop_tick = axes1.get_x_axis().get_tick(f_stop / f_pass)

        tol_stop_tick = axes1.get_y_axis().get_tick(tol_stop)
        tol_pass_tick = axes1.get_y_axis().get_tick(1 - tol_pass)
        unity_tick = axes1.get_y_axis().get_tick(1.0)

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

        filter_graph = axes1.get_graph(get_filter(epsilon=epsilon.get_value(), N=N.get_value()), color=YELLOW)

        # plot the filter function now
        self.play(
            ShowCreation(axes1),
            ShowCreation(ticks1),
            ShowCreation(mobs1)
            )

        self.wait(0.1)
        
        self.play(ShowCreation(filter_graph))

        # now we add updater for the graph
        filter_graph.add_updater(
            lambda mob: mob.become(axes1.get_graph( get_filter( epsilon=epsilon.get_value(), N=N.get_value() ),
                color=YELLOW) ),
            )

        # now we show the variation in the filter function with epsilon and N
        self.play(
            epsilon.set_value, epsilon_max / 100,
            rate_func=linear,
            run_time=5)

        self.play(
            epsilon.set_value, epsilon_max,
            rate_func=linear,
            run_time=2)

        self.play(
            N.set_value, N_min * 2,
            rate_func=linear,
            run_time=5)

        self.play(
            N.set_value, N_min,
            rate_func=linear,
            run_time=2)

        self.play(
            N.set_value, N_min // 2,
            rate_func=linear,
            run_time=5)

        self.play(
            N.set_value, N_min,
            rate_func=linear,
            run_time=2)

        self.wait(2)