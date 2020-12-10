import matplotlib.pyplot as plt
from satellite_constellation.utils import *
import plotly.graph_objects as go


def draw_walker_mplib(walker_constellation):
    r = walker_constellation.altitude + heavenly_body_radius[walker_constellation.focus]

    if walker_constellation.inclination % 90 == 0:
        plane_range = 180
    else:
        plane_range = 360

    t = np.linspace(0, 2 * math.pi, 100)

    x1, y1, z1 = r * np.cos(t), r * np.sin(t), 0 * t

    fig = plt.figure()

    perspectives = [[0, 0], [0, 45], [90, 0], [60, 60]]

    ax = [plt.subplot(2, 2, 1, projection='3d'), plt.subplot(2, 2, 2, projection='3d'),
          plt.subplot(2, 2, 3, projection='3d'), plt.subplot(2, 2, 4, projection='3d')]
    for idx in range(4):
        sat_coords = np.array([[0, 0, 0]])

        ax[idx].view_init(elev=perspectives[idx][0], azim=perspectives[idx][1])
        ax[idx].set_xlim(-r, r)
        ax[idx].set_ylim(-r, r)
        ax[idx].set_zlim(-r, r)
        ax[idx].plot(x1, y1, z1, '--', linewidth=1, color='r')  # Plot equatorial circle
        ax[idx].zaxis.set_tick_params(labelsize=3)
        ax[idx].xaxis.set_tick_params(labelsize=3)
        ax[idx].yaxis.set_tick_params(labelsize=3)
        ax[idx].set_xlabel("X", fontsize=3)
        ax[idx].set_ylabel("Y", fontsize=3)
        ax[idx].set_zlabel("Z", fontsize=3)

        # Plot target at revisit time
        xp, yp, zp = (r, 0, 0)
        target_ang = (walker_constellation.revisit_time / (24 * 60 * 60)) * 2 * math.pi
        target_coords = np.array([xp, yp, zp])
        ax[idx].scatter(xp, yp, zp, color='black', marker='x')
        target_coords = rotate(target_coords, target_ang, 'z')
        ax[idx].scatter(target_coords[0], target_coords[1], target_coords[2], color='green', marker='x')

        for idy in range(walker_constellation.num_planes):  # Plot orbital planes
            ang = idy * plane_range / walker_constellation.num_planes
            t = np.linspace(0, 2 * math.pi, 100)
            x, y, z = r * np.cos(t), r * np.sin(t), 0 * t
            for idz in range(100):
                coords = np.array([x[idz], y[idz], z[idz]])
                rot_coords = rotate(coords, walker_constellation.inclination * math.pi / 180, 'x')
                rot_coords = rotate(rot_coords, ang * math.pi / 180, 'z')
                x[idz] = rot_coords[0]
                y[idz] = rot_coords[1]
                z[idz] = rot_coords[2]
            ax[idx].plot(x, y, z, '--', linewidth=0.5)

        for idy in range(walker_constellation.num_planes):  # Plot satellites
            for idz in range(walker_constellation.sats_per_plane):
                ctr = idz + idy * walker_constellation.sats_per_plane

                x_i, y_i, z_i = polar2cart(r, 90 * math.pi / 180,
                                           (walker_constellation.perigee_positions[
                                                ctr] +
                                            + walker_constellation.ta[ctr]
                                            ) * math.pi / 180)
                coords = np.array([x_i, y_i, z_i])
                coords = rotate(coords, walker_constellation.inclination * math.pi / 180, 'x')
                coords = rotate(coords, (walker_constellation.raan[ctr]) * math.pi / 180, 'z')
                sat_coords = np.append(sat_coords, [coords], axis=0)
                ax[idx].scatter(coords[0], coords[1], coords[2])

        for idy in range(1, sat_coords.shape[0]):  # Draw line of sight between satellites
            for idz in range(1, sat_coords.shape[0]):
                if idz != idy:
                    temp_coords = np.append([sat_coords[idy, :]], [sat_coords[idz, :]], axis=0)
                    if sphere_intercept(temp_coords[0], temp_coords[1], 6371):
                        # print(temp_coords)
                        ax[idx].plot(temp_coords[:, 0], temp_coords[:, 1], temp_coords[:, 2], linewidth=0.1,
                                     color='black')
                    if not sphere_intercept(temp_coords[0], temp_coords[1], 6371):
                        # print(temp_coords)
                        ax[idx].plot(temp_coords[:, 0], temp_coords[:, 1], temp_coords[:, 2], linewidth=0.1,
                                     color='red')

    plt.savefig('../../walker_plot.png', dpi=300, bbox_inches='tight')


def draw_flower_mplib(flower_constellation):
    a = flower_constellation.semi_major
    b = a * math.sqrt(1 - math.pow(flower_constellation.eccentricity, 2))
    f = (flower_constellation.altitude + heavenly_body_radius[flower_constellation.focus]) * 10 ** 3
    disp = a - f

    t = np.linspace(0, 2 * math.pi, 100)

    r = heavenly_body_radius[flower_constellation.focus] * 10 ** 3
    x1, y1, z1 = r * np.cos(t), r * np.sin(t), 0 * t
    x2, y2, z2 = r * np.cos(t), 0 * t, r * np.sin(t)
    x3, y3, z3 = 0 * t, r * np.cos(t), r * np.sin(t)

    fig = plt.figure()

    r = a

    perspectives = [[0, 0], [90, 0], [45, 45]]

    ax = [plt.subplot(2, 2, 1, projection='3d'), plt.subplot(2, 2, 2, projection='3d'),
          plt.subplot(2, 2, 3, projection='3d')]
    for idx in range(3):
        ax[idx].view_init(elev=perspectives[idx][0], azim=perspectives[idx][1])
        ax[idx].set_xlim(-3 / 2 * a, 3 / 2 * a)
        ax[idx].set_ylim(-3 / 2 * a, 3 / 2 * a)
        ax[idx].set_zlim(-3 / 2 * a, 3 / 2 * a)
        ax[idx].plot(x1, y1, z1, '--', linewidth=0.1, color='r')  # Plot equatorial circle
        ax[idx].plot(x2, y2, z2, '--', linewidth=0.1, color='r')  # Plot equatorial circle
        ax[idx].plot(x3, y3, z3, '--', linewidth=0.1, color='r')  # Plot equatorial circle

        # Plot target at revisit time
        xp, yp, zp = (6371 * 10 ** 3, 0, 0)
        target_ang = (flower_constellation.revisit_time) * 2 * math.pi
        target_coords = np.array([xp, yp, zp])
        ax[idx].scatter(xp, yp, zp, color='black', marker='x')
        target_coords = rotate(target_coords, target_ang, 'z')
        ax[idx].scatter(target_coords[0], target_coords[1], target_coords[2], color='green', marker='x')

        ax[idx].zaxis.set_tick_params(labelsize=3)
        ax[idx].xaxis.set_tick_params(labelsize=3)
        ax[idx].yaxis.set_tick_params(labelsize=3)
        ax[idx].set_xlabel("X", fontsize=3)
        ax[idx].set_ylabel("Y", fontsize=3)
        ax[idx].set_zlabel("Z", fontsize=3)
        for idy in range(
                min(flower_constellation.num_orbits, flower_constellation.num_satellites)):  # Plot orbital planes
            x, y, z = disp + a * np.cos(t), b * np.sin(t), 0 * t
            for idz in range(100):
                coords = np.array([x[idz], y[idz], z[idz]])
                coords = rotate(coords, flower_constellation.raan[idy] * math.pi / 180, 'z')
                coords = rotate(coords, flower_constellation.inclination * math.pi / 180, 'x')
                x[idz] = coords[0]
                y[idz] = coords[1]
                z[idz] = coords[2]
            ax[idx].plot(x, y, z, '--', linewidth=0.5)

        for idy in range(flower_constellation.num_satellites):  # Plot satellites
            ang = (flower_constellation.true_anomaly[idy] + 180) * math.pi / 180
            x_i, y_i, z_i = disp + a * np.cos(ang), b * np.sin(ang), 0
            coords = np.array([x_i, y_i, z_i])
            coords = rotate(coords, flower_constellation.raan[idy] * math.pi / 180, 'z')
            coords = rotate(coords, flower_constellation.inclination * math.pi / 180, 'x')
            ax[idx].scatter(coords[0], coords[1], coords[2], s=2)

    plt.savefig('../../flower_plot.png', dpi=300, bbox_inches='tight')


def draw_walker_plotly(walker_constellation, satellites=True, orbits=True, links=False, sensor_regions=False):
    sat_coords = np.empty([walker_constellation.num_satellites, 3])
    r = walker_constellation.altitude + heavenly_body_radius[walker_constellation.focus]
    fig = go.Figure()

    max_dist = np.array([])

    if orbits:
        for idy in range(walker_constellation.num_planes):  # Plot orbital planes
            ang = idy * 360 / walker_constellation.num_planes
            t = np.linspace(0, 2 * math.pi, 100)
            x, y, z = r * np.cos(t), r * np.sin(t), 0 * t
            for idz in range(100):
                coords = np.array([x[idz], y[idz], z[idz]])
                rot_coords = rotate(coords, walker_constellation.inclination * math.pi / 180, 'x')
                rot_coords = rotate(rot_coords, ang * math.pi / 180, 'z')
                x[idz] = rot_coords[0]
                y[idz] = rot_coords[1]
                z[idz] = rot_coords[2]

            fig.add_trace(go.Scatter3d(x=x, y=y, z=z, mode='lines', name='Orbit ' + str(idy + 1)))
            max_dist = np.append(math.sqrt(np.sum(coords ** 2)), np.max(y))

    if satellites:
        d_sat = 0

        for coords in walker_constellation.as_cartesian():
            sat_coords[d_sat] = coords

            fig.add_trace(
                go.Scatter3d(x=[coords[0]], y=[coords[1]], z=[coords[2]], mode='markers', name='real_sat '
                                                                                               + str(
                    d_sat), showlegend=False))
            d_sat += 1

    if links:
        for idy in range(0, sat_coords.shape[0]):  # Draw line of sight between satellites
            ctr = 0
            for idz in range(0, sat_coords.shape[0]):
                if idz != idy:

                    temp_coords = np.append([sat_coords[idy, :]], [sat_coords[idz, :]], axis=0)
                    if not sphere_intercept(temp_coords[0], temp_coords[1],
                                            heavenly_body_radius[walker_constellation.focus]):
                        ctr += 1
                        fig.add_trace(
                            go.Scatter3d(x=temp_coords[:, 0], y=temp_coords[:, 1], z=temp_coords[:, 2], mode='lines',
                                         name='link {0} to {1}'.format(idy, idz), showlegend=False,
                                         line=dict(color='green', width=0.5, dash='dash')))

    if sensor_regions:

        for idy in range(walker_constellation.num_satellites):
            rE = heavenly_body_radius[walker_constellation.focus]
            v_r = rE * sat_coords[idy] / math.sqrt(np.sum(sat_coords[idy] ** 2))
            t = np.linspace(0, 2 * math.pi, 100)
            projection_coords = np.array([[0, 0, 0]])

            ax1 = np.array([r, 0, 0])
            ax1 = rotate(ax1, walker_constellation.raan[idy] * math.pi / 180, 'z')
            ax2 = rotate(ax1, math.pi / 2, 'z')
            ax2 = rotate(ax2, walker_constellation.inclination * math.pi / 180, 'custom',
                         basis=ax1 / math.sqrt(np.sum(ax1 ** 2)))
            basis = np.cross(ax1 / math.sqrt(np.sum(ax1 ** 2)), ax2 / math.sqrt(np.sum(ax2 ** 2)))

            for idk in range(0, 100):
                coords = np.array(polar2cart(rE, walker_constellation.earth_coverage_angle/2, t[idk]))
                coords = rotate(coords, math.pi / 2, 'y')
                coords = rotate(coords, (walker_constellation.raan[idy]) * math.pi / 180, 'z')
                coords = rotate(coords, (walker_constellation.perigee_positions[idy] + walker_constellation.ta[idy])
                                * math.pi / 180, 'custom', basis=basis)
                projection_coords = np.append(projection_coords, [coords], axis=0)

            fig.add_trace(
                go.Scatter3d(x=projection_coords[:, 0], y=projection_coords[:, 1], z=projection_coords[:, 2],
                             mode='lines',
                             name='Projection ' + str(idy), line=dict(color='red', width=5), showlegend=False))

    r = heavenly_body_radius[walker_constellation.focus]
    pi = np.pi
    cos = np.cos
    sin = np.sin
    phi, theta = np.mgrid[0:pi:101j, 0:2 * pi:101j]
    x = r * sin(phi) * cos(theta)
    y = r * sin(phi) * sin(theta)
    z = r * cos(phi)

    fig.add_trace(go.Surface(x=x, y=y, z=z, name='Earth', showlegend=False, colorscale='blues'))

    max_dist = np.append(max_dist, np.max(y))
    max_val = np.max(max_dist)

    try:
        spherical_earth_map = np.load('map_sphere.npy')
    except FileNotFoundError:
        pass
    else:
        xm, ym, zm = spherical_earth_map.T * 6371
        fig.add_trace(
            go.Scatter3d(x=xm, y=ym, z=zm, name='Earth', mode='lines', showlegend=False,
                         line=dict(color='white', width=1)))

    fig.update_layout(
        scene=dict(
            xaxis=dict(range=[-max_val - 5000, max_val + 5000], ),
            yaxis=dict(range=[-max_val - 5000, max_val + 5000], ),
            zaxis=dict(range=[-max_val - 5000, max_val + 5000]), aspectmode='cube')
    )

    fig.show()


def draw_flower_plotly(flower_constellation, satellites=True, orbits=True, links=False):
    sat_coords = np.array([[0, 0, 0]])

    fig = go.Figure()

    a = flower_constellation.semi_major
    b = a * math.sqrt(1 - math.pow(flower_constellation.eccentricity, 2))
    f = (flower_constellation.altitude + heavenly_body_radius[flower_constellation.focus]) * 10 ** 3
    disp = a - f

    t = np.linspace(0, 2 * math.pi, 100)

    max_dist = np.array([])

    if orbits:
        for idy in range(
                min(flower_constellation.num_orbits, flower_constellation.num_satellites)):  # Plot orbital planes
            x, y, z = disp + a * np.cos(t), b * np.sin(t), 0 * t
            for idz in range(100):
                coords = np.array([x[idz], y[idz], z[idz]]) * 10 ** -3
                coords = rotate(coords, flower_constellation.raan[idy] * math.pi / 180, 'z')
                coords = rotate(coords, flower_constellation.inclination * math.pi / 180, 'x')
                x[idz] = coords[0]
                y[idz] = coords[1]
                z[idz] = coords[2]

            fig.add_trace(go.Scatter3d(x=x, y=y, z=z, mode='lines', name='Orbit ' + str(idy + 1), showlegend=False))
            max_dist = np.append(math.sqrt(np.sum(coords ** 2)), np.max(y))

    if satellites:

        flower_constellation.as_cartesian()
        if satellites:
            d_sat = 0

            for coords in flower_constellation.as_cartesian():
                sat_coords = np.append(sat_coords, [coords], axis=0)

                fig.add_trace(
                    go.Scatter3d(x=[coords[0]], y=[coords[1]], z=[coords[2]], mode='markers', name='real_sat '
                                                                                                   + str(
                        idy), showlegend=False))
                d_sat += 1

    if satellites and links:
        for idy in range(1, sat_coords.shape[0]):  # Draw line of sight between satellites
            for idz in range(1, sat_coords.shape[0]):
                if idz != idy:
                    temp_coords = np.append([sat_coords[idy, :]], [sat_coords[idz, :]], axis=0)
                    if not sphere_intercept(temp_coords[0], temp_coords[1],
                                            heavenly_body_radius[flower_constellation.focus]):
                        fig.add_trace(
                            go.Scatter3d(x=temp_coords[:, 0], y=temp_coords[:, 1], z=temp_coords[:, 2], mode='lines',
                                         name='link {0} to {1}'.format(idy, idz), showlegend=False,
                                         line=dict(color='green', width=0.5, dash='dash')))

    r = heavenly_body_radius[flower_constellation.focus]

    pi = np.pi
    cos = np.cos
    sin = np.sin
    phi, theta = np.mgrid[0:pi:101j, 0:2 * pi:101j]
    x = r * sin(phi) * cos(theta)
    y = r * sin(phi) * sin(theta)
    z = r * cos(phi)

    fig.add_trace(go.Surface(x=x, y=y, z=z, name='Earth', showlegend=False, colorscale='blues'))

    max_dist = np.append(max_dist, np.max(y))
    max_val = np.max(max_dist)

    try:
        spherical_earth_map = np.load('map_sphere.npy')
    except FileNotFoundError:
        pass
    else:
        xm, ym, zm = spherical_earth_map.T * 6371
        fig.add_trace(
            go.Scatter3d(x=xm, y=ym, z=zm, name='Earth', mode='lines', showlegend=False,
                         line=dict(color='white', width=1)))

    fig.update_layout(
        scene=dict(
            xaxis=dict(range=[-max_val - 5000, max_val + 5000], ),
            yaxis=dict(range=[-max_val - 5000, max_val + 5000], ),
            zaxis=dict(range=[-max_val - 5000, max_val + 5000]), aspectmode='cube')
    )

    fig.show()


def draw_soc_plotly(SOC_Constellation, satellites=True, orbits=True, links=False, sensor_regions=False):
    sat_coords = np.array([[0, 0, 0]])
    r = SOC_Constellation.altitude + heavenly_body_radius[SOC_Constellation.focus]
    rE = heavenly_body_radius[SOC_Constellation.focus]
    fig = go.Figure()

    max_dist = np.array([])

    t = np.linspace(0, 2 * math.pi, 100)

    if orbits:
        for idy in range(SOC_Constellation.num_streets):  # Plot orbital planes
            # ang = idy * 360 / SOC_Constellation.num_streets
            ang = SOC_Constellation.raan[idy]
            t = np.linspace(0, 2 * math.pi, 100)
            x, y, z = r * np.cos(t), r * np.sin(t), 0 * t
            for idz in range(100):
                coords = np.array([x[idz], y[idz], z[idz]])
                rot_coords = rotate(coords, SOC_Constellation.inclination * math.pi / 180, 'x')
                rot_coords = rotate(rot_coords, ang * math.pi / 180, 'z')
                x[idz] = rot_coords[0]
                y[idz] = rot_coords[1]
                z[idz] = rot_coords[2]

            fig.add_trace(go.Scatter3d(x=x, y=y, z=z, mode='lines', name='Orbit ' + str(idy + 1)))
            max_dist = np.append(max_dist, math.sqrt(np.sum(coords ** 2)))

    if satellites:
        for idy in range(SOC_Constellation.num_streets):  # Plot satellites
            for idz in range(SOC_Constellation.sats_per_street):
                ctr = idz + idy * SOC_Constellation.sats_per_street
                x_i, y_i, z_i = polar2cart(r, 90 * math.pi / 180,
                                           (SOC_Constellation.perigee_positions[
                                                ctr] +
                                            + SOC_Constellation.ta[ctr]
                                            ) * math.pi / 180)
                coords = np.array([x_i, y_i, z_i])
                coords = rotate(coords, SOC_Constellation.inclination * math.pi / 180, 'x')
                coords = rotate(coords, (SOC_Constellation.raan[idy]) * math.pi / 180, 'z')

                spherical_coords = cart2polar(coords[0], coords[1], coords[2])

                sat_coords = np.append(sat_coords, [coords], axis=0)
                fig.add_trace(
                    go.Scatter3d(x=[coords[0]], y=[coords[1]], z=[coords[2]], mode='markers', name='satellite '
                                                                                                   + str(
                        1 + idz + SOC_Constellation.sats_per_street * idy), showlegend=False))

    if sensor_regions:
        for idy in range(SOC_Constellation.num_streets):  # Plot sensor regions
            for idz in range(SOC_Constellation.sats_per_street):
                projection_coords = np.array([[0, 0, 0]])
                ctr = idz + idy * SOC_Constellation.sats_per_street
                for idk in range(0, 100):
                    coords = np.array(polar2cart(rE, SOC_Constellation.earth_coverage_angle/2, t[idk]))
                    coords = rotate(coords, (SOC_Constellation.perigee_positions[ctr] + SOC_Constellation.ta[
                        ctr] + 90) * math.pi / 180, 'x')
                    coords = rotate(coords, (SOC_Constellation.raan[idy] + 90) * math.pi / 180, 'z')

                    projection_coords = np.append(projection_coords, [coords], axis=0)

                fig.add_trace(
                    go.Scatter3d(x=projection_coords[:, 0], y=projection_coords[:, 1], z=projection_coords[:, 2],
                                 mode='lines',
                                 name='Projection ' + str(idz), line=dict(color='red', width=5), showlegend=False))
        street_width = heavenly_body_radius[SOC_Constellation.focus] * SOC_Constellation.street_width * math.pi / 180

        t = np.linspace(0, 2 * math.pi, 100)
        x, y, z = rE * np.cos(t), rE * np.sin(t), 0 * t
        for idz in range(100):
            coords = np.array([x[idz], y[idz], z[idz]])
            coords = rotate(coords, SOC_Constellation.inclination * math.pi / 180, 'x')
            x[idz] = coords[0]
            y[idz] = coords[1] + street_width / 2
            z[idz] = coords[2]
        fig.add_trace(go.Scatter3d(x=x, y=y, z=z, mode='lines', name='Street', line=dict(color='green', width=5)))

        x, y, z = rE * np.cos(t), rE * np.sin(t), 0 * t
        for idz in range(100):
            coords = np.array([x[idz], y[idz], z[idz]])
            coords = rotate(coords, SOC_Constellation.inclination * math.pi / 180, 'x')
            x[idz] = coords[0]
            y[idz] = coords[1] - street_width / 2
            z[idz] = coords[2]
        fig.add_trace(go.Scatter3d(x=x, y=y, z=z, mode='lines', name='Street', line=dict(color='green', width=5)))

    if satellites and links:  # Draw line of sight between satellites
        for idy in range(1, sat_coords.shape[0]):
            for idz in range(1, sat_coords.shape[0]):
                if idz != idy:
                    temp_coords = np.append([sat_coords[idy, :]], [sat_coords[idz, :]], axis=0)
                    if not sphere_intercept(temp_coords[0], temp_coords[1],
                                            heavenly_body_radius[SOC_Constellation.focus]):
                        fig.add_trace(
                            go.Scatter3d(x=temp_coords[:, 0], y=temp_coords[:, 1], z=temp_coords[:, 2], mode='lines',
                                         name='link {0} to {1}'.format(idy, idz), showlegend=False,
                                         line=dict(color='green', width=0.5, dash='dash')))

    r = heavenly_body_radius[SOC_Constellation.focus]

    pi = np.pi
    cos = np.cos
    sin = np.sin
    phi, theta = np.mgrid[0:pi:101j, 0:2 * pi:101j]
    x = r * sin(phi) * cos(theta)
    y = r * sin(phi) * sin(theta)
    z = r * cos(phi)

    fig.add_trace(go.Surface(x=x, y=y, z=z, name='Earth', showlegend=False, colorscale='blues'))

    try:
        spherical_earth_map = np.load('map_sphere.npy')
    except FileNotFoundError:
        pass
    else:
        xm, ym, zm = spherical_earth_map.T * 6371
        fig.add_trace(
            go.Scatter3d(x=xm, y=ym, z=zm, name='Earth', mode='lines', showlegend=False,
                         line=dict(color='white', width=1)))

    max_dist = np.append(max_dist, np.max(y))
    max_val = np.max(max_dist)

    fig.update_layout(
        scene=dict(
            xaxis=dict(range=[-max_val - 5000, max_val + 5000], ),
            yaxis=dict(range=[-max_val - 5000, max_val + 5000], ),
            zaxis=dict(range=[-max_val - 5000, max_val + 5000]), aspectmode='cube')
    )

    fig.show()
