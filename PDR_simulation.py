from rocketpy import Environment, SolidMotor, Rocket, Flight

env = Environment(
    latitude=55,
    longitude=-5,
    elevation=83.6,
)

env.set_date(
  (2024, 2, 29, 6), timezone="UTC"
)  # Tomorrow's date in year, month, day, hour UTC format

'''
env.set_atmospheric_model(
    type='Forecast', file='GFS')
'''

# env.info()

Cesaroni_L645 = SolidMotor(
    thrust_source="data/motors/Cesaroni_L645.eng",
    dry_mass=1.544,
    dry_inertia=(0.125, 0.125, 0.002),
    center_of_dry_mass_position=0.317,
    grains_center_of_mass_position=0.397,
    burn_time=5.3,
    grain_number=3,
    grain_separation=0.0065,
    grain_density=1815,
    grain_outer_radius=0.0431,
    grain_initial_inner_radius=0.0144,
    grain_initial_height=0.12,  # To be changed (TBC)
    # nozzle_radius=0.033,  # TBC
    throat_radius=0.011,  # TBC
    interpolation_method="linear",
    # nozzle_position=0,  # TBC
    coordinate_system_orientation="nozzle_to_combustion_chamber",  # TBC
)

# Motor.info()

violin = Rocket(
    radius=0.0522,
    mass=7.504,  # without motor
    inertia=(6.6, 6.6, 0.03238),
    # distance_rocket_nozzle=-1.114,
    # distance_rocket_propellant=-0.626,
    power_off_drag="data/violin/powerOffDragCurve.csv",
    power_on_drag="data/violin/powerOnDragCurve.csv",
    center_of_mass_without_motor=-0.4,
    coordinate_system_orientation="tail_to_nose",
)

buttons = violin.set_rail_buttons(
    upper_button_position=0.2,
    lower_button_position=-0.5,
)

violin.add_motor(Cesaroni_L645, position=-1.37) #initial value -1.255

nose = violin.add_nose(
    length=0.277, kind="vonKarman", position=0.60 #initial value 1.114
)

fins = violin.add_trapezoidal_fins(
    n=4,
    root_chord=0.12,
    tip_chord=0.077,
    span=0.093,
    sweep_length=None,
    cant_angle=0,
    position=-1.046,
)

tail = violin.add_tail(
    top_radius=0.0635, bottom_radius=0.0435, length=0.060, position= -1.15 # -1.194656
)


def drogue_chute_trigger(p, h, y):
    # p = pressure
    # h = height
    # y = state vector [x, y, z, vx, vy, vz, e0, e1, e2, e3, w1, w2, w3]
    # activate drogue when vz < 0 m/s.
    return True if y[5] < 0 else False


def main_chute_trigger(p, h, y):
    # p = pressure
    # h = height
    # y = state vector [x, y, z, vx, vy, vz, e0, e1, e2, e3, w1, w2, w3]
    # activate main when vz < 0 m/s and z < 800 + 1400 m (+1400 due to surface elevation).
    return True if y[5] < 0 and y[2] < 500 else False


main_chute = violin.add_parachute(
    name="main chute",
    cd_s=5.84,
    trigger=main_chute_trigger,
    sampling_rate=105,
    lag=1.5,
    noise=(0, 8.3, 0.5),
)

drogue_chute = violin.add_parachute(
    name="drogue chute",
    cd_s=1.0,
    trigger=drogue_chute_trigger,
    sampling_rate=105,
    lag=1.5,
    noise=(0, 8.3, 0.5),
)

violin.draw()
violin.plots.static_margin()

'''
test_flight = Flight(
    rocket=violin, environment=env, rail_length=4, inclination=85, heading=270
)
'''

# test_flight.info() # to get a summary of the results (no plots)

# test_flight.all_info()

# test_flight.export_kml(file_name="Mach24_PDR_flight.kml")
