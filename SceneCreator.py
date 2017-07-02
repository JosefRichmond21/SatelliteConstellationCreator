"""
Recreation of the Octave SceneCreator script for use within Flask or other python projects
@creator: Aidan O'Brien
"""

from Constellation import Constellation
from GroundStation import GroundStation
from itertools import zip_longest
from utils import mod


def scene_xml_generator(scene):
    scene_start = '<Pigi>\n' \
                  '\t<Entities>\n' \
                  '\t\t<Entity Type="Planet" Name="Mercury">\n' \
                  '\t\t\t<PropertySection Name="UserProperties">\n' \
                  '\t\t\t\t<StringPropertyValue name="PlanetName" value="Mercury"/>\n' \
                  '\t\t\t\t<FloatPropertyValue name="obliquity" value="0.1"/>\n' \
                  '\t\t\t\t<FloatPropertyValue name="scale" value="0.244"/>\n' \
                  '\t\t\t\t<IntPropertyValue name="Atmosphere" value="0"/>\n' \
                  '\t\t\t</PropertySection>\n' \
                  '\t\t</Entity>\n' \
                  '\t\t<Entity Type="Planet" Name="Venus">\n' \
                  '\t\t\t<PropertySection Name="UserProperties">\n' \
                  '\t\t\t\t<StringPropertyValue name="PlanetName" value="Venus"/>\n' \
                  '\t\t\t\t<FloatPropertyValue name="obliquity" value="177"/>\n' \
                  '\t\t\t\t<FloatPropertyValue name="scale" value="0.605"/>\n' \
                  '\t\t\t\t<IntPropertyValue name="Atmosphere" value="1"/>\n' \
                  '\t\t\t</PropertySection>\n' \
                  '\t\t</Entity>\n' \
                  '\t\t<Entity Type="Planet" Name="Earth">\n' \
                  '\t\t\t<PropertySection Name="UserProperties">\n' \
                  '\t\t\t\t<StringPropertyValue name="PlanetName" value="Earth"/>\n' \
                  '\t\t\t\t<FloatPropertyValue name="obliquity" value="23.4"/>\n' \
                  '\t\t\t\t<FloatPropertyValue name="scale" value="0.6371"/>\n' \
                  '\t\t\t\t<IntPropertyValue name="Atmosphere" value="1"/>\n' \
                  '\t\t\t</PropertySection>\n' \
                  '\t\t</Entity>\n' \
                  '\t\t<Entity Type="Planet" Name="Mars">\n' \
                  '\t\t\t<PropertySection Name="UserProperties">\n' \
                  '\t\t\t\t<StringPropertyValue name="PlanetName" value="Mars"/>\n' \
                  '\t\t\t\t<FloatPropertyValue name="obliquity" value="25"/>\n' \
                  '\t\t\t\t<FloatPropertyValue name="scale" value="0.3371"/>\n' \
                  '\t\t\t\t<IntPropertyValue name="Atmosphere" value="1"/>\n' \
                  '\t\t\t</PropertySection>\n' \
                  '\t\t</Entity>\n' \
                  '\t\t<Entity Type="Planet" Name="Jupiter">\n' \
                  '\t\t\t<PropertySection Name="UserProperties">\n' \
                  '\t\t\t\t<StringPropertyValue name="PlanetName" value="Jupiter"/>\n' \
                  '\t\t\t\t<FloatPropertyValue name="obliquity" value="3"/>\n' \
                  '\t\t\t\t<FloatPropertyValue name="scale" value="6.99"/>\n' \
                  '\t\t\t\t<IntPropertyValue name="Atmosphere" value="0"/>\n' \
                  '\t\t\t</PropertySection>\n' \
                  '\t\t</Entity>\n' \
                  '\t\t<Entity Type="Planet" Name="Saturn">\n' \
                  '\t\t\t<PropertySection Name="UserProperties">\n' \
                  '\t\t\t\t<StringPropertyValue name="PlanetName" value="Saturn"/>\n' \
                  '\t\t\t\t<FloatPropertyValue name="obliquity" value="27"/>\n' \
                  '\t\t\t\t<FloatPropertyValue name="scale" value="6.033"/>\n' \
                  '\t\t\t\t<IntPropertyValue name="Atmosphere" value="0"/>\n' \
                  '\t\t\t</PropertySection>\n' \
                  '\t\t</Entity>\n' \
                  '\t\t<Entity Type="Planet" Name="Neptune">\n' \
                  '\t\t\t<PropertySection Name="UserProperties">\n' \
                  '\t\t\t\t<StringPropertyValue name="PlanetName" value="Neptune"/>\n' \
                  '\t\t\t\t<FloatPropertyValue name="obliquity" value="30"/>\n' \
                  '\t\t\t\t<FloatPropertyValue name="scale" value="2.46"/>\n' \
                  '\t\t\t\t<IntPropertyValue name="Atmosphere" value="0"/>\n' \
                  '\t\t\t</PropertySection>\n' \
                  '\t\t</Entity>\n' \
                  '\t\t<Entity Type="Planet" Name="Pluto">\n' \
                  '\t\t\t<PropertySection Name="UserProperties">\n' \
                  '\t\t\t\t<StringPropertyValue name="PlanetName" value="Pluto"/>\n' \
                  '\t\t\t\t<FloatPropertyValue name="obliquity" value="120"/>\n' \
                  '\t\t\t\t<FloatPropertyValue name="scale" value="0.186"/>\n' \
                  '\t\t\t\t<IntPropertyValue name="Atmosphere" value="0"/>\n' \
                  '\t\t\t</PropertySection>\n' \
                  '\t\t</Entity>\n'

    scene_end = '\t</Entities>\n' \
                '</Pigi>'

    scene_xml = ""
    for item in scene:
        scene_xml += item.as_xml()

    return "{0} {1} {2}".format(scene_start, scene_xml, scene_end)


def constellation_creator(num_constellations, satellite_nums, satellite_planes, plane_phasing, inclination, altitude,
                          eccentricity, constellation_beam_width, sat_name="Sat"):
    """

    :param num_constellations: Integer of the number of constellations that are for the scene
    :param satellite_nums: List of numbers of satellites for each constellation
    :param satellite_planes: List of number of planes of satellites for each constellation.
    :param plane_phasing: The planar phases for their respective constellations
    :param inclination: List of inclinations for constellations
    :param altitude: List of altitudes for constellations
    :param eccentricity: List of eccentricities for each constellation
    :param constellation_beam_width: List of Beam widths for satellites in each constellation
    :param sat_name: Root name for satellites, defaults to Sat
    :return: Returns a list of constellations that have been formatted
    """

    if num_constellations < 1 or (num_constellations % 1):
        return -1

    if num_constellations != len(satellite_nums):
        return -1

    if any(mod(satellite_nums, satellite_planes)):
        return -1

    for idx, phase in enumerate(plane_phasing):
        if phase < 0:
            return -1
        elif phase >= satellite_planes[idx]:
            return -1
        elif phase % 1:
            return -1

    if any(abs(x) > 90 for x in inclination):
        return -1

    if any(x < 0 for x in altitude):
        return -1

    if any(x < 0 or x >= 1 for x in eccentricity):
        return -1

    if any(x < 0 or x > 180 for x in constellation_beam_width):
        return -1

    scene = []
    for idx in range(num_constellations):
        start_num = sum(satellite_nums[0:idx])
        scene.append(Constellation(satellite_nums[idx], satellite_planes[idx], plane_phasing[idx], inclination[idx],
                                   altitude[idx], eccentricity[idx], constellation_beam_width[idx], name=sat_name,
                                   starting_number=start_num))

    return scene


def ground_array_creator(num_ground_stations, latitudes, longitudes, elevations, beam_widths, name="GS"):
    """

    :param num_ground_stations:
    :param latitudes:
    :param longitudes:
    :param elevations:
    :param beam_widths:
    :param name:
    :return:
    """

    if num_ground_stations < 1 or (num_ground_stations % 1):
        return -1

    if num_ground_stations != len(latitudes):
        return -1

    try:
        zip_longest(latitudes, longitudes, elevations)
    except IndexError:
        return -1

    if (len(latitudes) != len(beam_widths)) or (len(beam_widths) == 1):
        return -1

    scene = []
    for idx in range(num_ground_stations):
        gs_name = name + str(idx)
        if len(beam_widths) > 1:
            beam = beam_widths[idx]
        else:
            beam = beam_widths
        scene.append(GroundStation(gs_name, latitudes[idx], longitudes[idx], elevations[idx], beam))

    return scene


def create_scene(num_constellations, num_sats, sat_planes, plane_phasing, sat_inclination, sat_alt,
                 sat_eccentricity, const_beam_width,
                 num_ground_stations, latitudes, longitudes, elevations, beam_widths,
                 sat_name="Sat", gsname="GS"):
    """
    Creates the scene list from constellations and ground stations
    :param num_constellations:
    :param num_sats:
    :param sat_planes:
    :param plane_phasing:
    :param sat_inclination:
    :param sat_altitude:
    :param sat_eccentricity:
    :param const_beam_width:
    :param num_ground_stations:
    :param latitudes:
    :param longitudes:
    :param elevations:
    :param beam_widths: List of beam widths for the ground stations
    :param sat_name: Root of satellite names
    :param gsname: Root of ground station names
    :return: List of constellation and ground station objects
    """

    scene = constellation_creator(num_constellations, num_sats, sat_planes, plane_phasing, sat_inclination, sat_alt,
                                  sat_eccentricity, const_beam_width, sat_name=sat_name)
    scene.extend(ground_array_creator(num_ground_stations, latitudes, longitudes, elevations, beam_widths, name=gsname))

    return scene