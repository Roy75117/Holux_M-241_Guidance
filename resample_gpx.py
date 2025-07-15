import gpxpy
import gpxpy.gpx
from geopy.distance import geodesic
from datetime import timedelta
import argparse

def calculate_distance(point1, point2):
    return geodesic((point1.latitude, point1.longitude), (point2.latitude, point2.longitude)).meters

def interpolate_point(p1, p2, ratio):
    lat = p1.latitude + (p2.latitude - p1.latitude) * ratio
    lon = p1.longitude + (p2.longitude - p1.longitude) * ratio
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

    with open(output_file, 'w') as f:
        f.write(new_gpx.to_xml())
    print(f"Improved GPX saved to: {output_file}")

def main():
    parser = argparse.ArgumentParser(description="Improved GPX resampler with better curve fidelity.")
    parser.add_argument("input_file", help="Input GPX file")
    parser.add_argument("output_file", help="Output GPX file")
    parser.add_argument("distance", type=float, help="Target spacing in meters")
    args = parser.parse_args()
    resample_gpx(args.input_file, args.output_file, args.distance)

if __name__ == "__main__":
    main()
