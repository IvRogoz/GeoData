import csv
import math


def distance_on_geoid(lat1, lon1, lat2, lon2):
    lat1 = math.radians(lat1)
    lon1 = math.radians(lon1)
    lat2 = math.radians(lat2)
    lon2 = math.radians(lon2)

    r = 6378100  # Radius of Earth in meters

    rho1 = r * math.cos(lat1)
    z1 = r * math.sin(lat1)
    x1 = rho1 * math.cos(lon1)
    y1 = rho1 * math.sin(lon1)

    rho2 = r * math.cos(lat2)
    z2 = r * math.sin(lat2)
    x2 = rho2 * math.cos(lon2)
    y2 = rho2 * math.sin(lon2)

    dot = x1 * x2 + y1 * y2 + z1 * z2
    cos_theta = dot / (r * r)
    theta = math.acos(cos_theta)

    return r * theta  # Distance in meters


def readCSV():
    output_data = []
    with open("NP.csv") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=" ")
        line_count = 0
        previous_coords = None
        previous_year = None
        for row in csv_reader:
            lat, lon = map(float, [row[1], row[0]])
            year = int(round(float(row[2])))

            if previous_coords is not None and previous_year is not None:
                distance = distance_on_geoid(
                    previous_coords[0],
                    previous_coords[1],
                    lat,
                    lon,
                )
                speed = round(distance / 1000, 2) / (year - previous_year)
                print(
                    f"Year {previous_year} - Year {year}: Distance = {round(distance/1000, 2)} km > Speed:{round(speed,2)} km/yr"
                )
                output_data.append(
                    [previous_year, year, round(distance / 1000, 2), round(speed, 2)]
                )

            previous_coords = [lat, lon]
            previous_year = year
            line_count += 1

        with open("NP_distance_speed.csv", mode="w", newline="") as output_file:
            csv_writer = csv.writer(output_file)
            csv_writer.writerow(
                ["Start Year", "End Year", "Distance (km)", "Speed (km/yr)"]
            )
            csv_writer.writerows(output_data)

        print(f"Processed {line_count} lines.")


readCSV()
