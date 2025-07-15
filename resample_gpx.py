import gpxpy
import gpxpy.gpx
from geopy.distance import geodesic
from datetime import timedelta
import argparse

def unwrap_longitude(lon1, lon2):
    # Adjust lon2 so that it's continuous with respect to lon1
    delta = lon2 - lon1
    if delta > 180:
        lon2 -= 360
    elif delta < -180:
        lon2 += 360
    return lon2

def calculate_distance(point1, point2):
    lon1, lon2 = point1.longitude, point2.longitude
    lon2 = unwrap_longitude(lon1, lon2)
    return geodesic((point1.latitude, lon1), (point2.latitude, lon2)).meters

def interpolate_point(p1, p2, ratio):
    lon1 = p1.longitude
    lon2 = unwrap_longitude(lon1, p2.longitude)

    lat = p1.latitude + (p2.latitude - p1.latitude) * ratio
    lon = lon1 + (lon2 - lon1) * ratio

    # Normalize lon to [-180, 180] after interpolation
    if lon > 180:
        lon -= 360
    elif lon < -180:
        lon += 360

    ele = None
    if p1.elevation is not None and p2.elevation is not None:
        ele = p1.elevation + (p2.elevation - p1.elevation) * ratio
    time = None
    if p1.time is not None and p2.time is not None:
        delta = p2.time - p1.time
        time = p1.time + timedelta(seconds=delta.total_seconds() * ratio)
    return gpxpy.gpx.GPXTrackPoint(lat, lon, elevation=ele, time=time)

def resample_gpx(input_file, output_file, target_distance):
    with open(input_file, 'r') as gpx_file:
        gpx = gpxpy.parse(gpx_file)

    new_gpx = gpxpy.gpx.GPX()
    new_track = gpxpy.gpx.GPXTrack()
    new_segment = gpxpy.gpx.GPXTrackSegment()
    new_gpx.tracks.append(new_track)
    new_track.segments.append(new_segment)

    for track in gpx.tracks:
        for segment in track.segments:
            if not segment.points:
                print(f"Warning: Track segment is empty, skipping")
                continue
            points = segment.points
            last_point = points[0]
            new_segment.points.append(last_point)

            accumulated = 0.0

            for i in range(1, len(points)):
                p1 = last_point
                p2 = points[i]
                seg_dist = calculate_distance(p1, p2)
                if seg_dist == 0:
                    continue

                while accumulated + target_distance <= seg_dist:
                    ratio = (accumulated + target_distance) / seg_dist
                    new_point = interpolate_point(p1, p2, ratio)
                    new_segment.points.append(new_point)
                    last_point = new_point
                    accumulated = 0.0
                    p1 = new_point
                    seg_dist = calculate_distance(p1, p2)
                accumulated += seg_dist
                last_point = p2

            if last_point != new_segment.points[-1]:
                new_segment.points.append(last_point)

    # Save the new GPX file
    try:    
        with open(output_file, 'w') as f:
            f.write(new_gpx.to_xml())
        print(f"Successfully generated resampled GPX file: '{output_file}'")
    except Exception as e:
        print(f"Error saving GPX file: {e}")

def main():
    parser = argparse.ArgumentParser(description="Resample a GPX file to a specified point interval (in meters).")
    parser.add_argument("input_file", help="Path to the input GPX file")
    parser.add_argument("output_file", help="Path to the output GPX file")
    parser.add_argument("distance", type=float, default=200, nargs='?', help="Target distance between points (in meters, default is 200)")
    args = parser.parse_args()
    resample_gpx(args.input_file, args.output_file, args.distance)

    if args.distance <= 0:
        print("Error: Target distance must be positive")
        return

if __name__ == "__main__":
    main()
