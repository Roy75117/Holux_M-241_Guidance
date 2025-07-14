import gpxpy
import gpxpy.gpx
from geopy.distance import geodesic
import numpy as np
from datetime import timedelta
import argparse

def calculate_distance(point1, point2):
    """Calculate the geodesic distance (in meters) between two points (latitude, longitude)."""
    return geodesic((point1.latitude, point1.longitude), (point2.latitude, point2.longitude)).meters

def copy_point(point):
    """Manually copy a GPXTrackPoint object."""
    return gpxpy.gpx.GPXTrackPoint(
        latitude=point.latitude,
        longitude=point.longitude,
        elevation=point.elevation,
        time=point.time
    )

def interpolate_point(p1, p2, ratio):
    """Interpolate between two points based on a ratio (0 to 1)."""
    lat = p1.latitude + (p2.latitude - p1.latitude) * ratio
    lon = p1.longitude + (p2.longitude - p1.longitude) * ratio
    elev = p1.elevation + (p2.elevation - p1.elevation) * ratio if p1.elevation and p2.elevation else None
    return lat, lon, elev

def resample_gpx(input_file, output_file, target_distance):
    """Resample a GPX file to points approximately target_distance meters apart."""
    # Parse the GPX file
    try:
        with open(input_file, 'r') as gpx_file:
            gpx = gpxpy.parse(gpx_file)
    except FileNotFoundError:
        print(f"Error: Input file '{input_file}' not found")
        return
    except Exception as e:
        print(f"Error parsing GPX file: {e}")
        return

    # Initialize a new GPX file
    new_gpx = gpxpy.gpx.GPX()
    new_track = gpxpy.gpx.GPXTrack()
    new_segment = gpxpy.gpx.GPXTrackSegment()
    new_gpx.tracks.append(new_track)
    new_track.segments.append(new_segment)

    # Process each track and segment
    for track in gpx.tracks:
        for segment in track.segments:
            if not segment.points:
                print(f"Warning: Track segment is empty, skipping")
                continue

            # Add the first point
            new_segment.points.append(copy_point(segment.points[0]))
            current_distance = 0.0
            target = target_distance

            # Iterate through track points
            for i in range(len(segment.points) - 1):
                p1 = segment.points[i]
                p2 = segment.points[i + 1]
                segment_distance = calculate_distance(p1, p2)

                current_distance += segment_distance

                # When accumulated distance exceeds target, insert a new point
                while current_distance >= target:
                    remaining = target - (current_distance - segment_distance)
                    ratio = remaining / segment_distance if segment_distance > 0 else 0
                    lat, lon, elev = interpolate_point(p1, p2, ratio)

                    # Create a new point
                    new_point = gpxpy.gpx.GPXTrackPoint(latitude=lat, longitude=lon, elevation=elev)
                    if p1.time and p2.time:
                        # Interpolate time if timestamps are available
                        time_diff = (p2.time - p1.time).total_seconds()
                        new_point.time = p1.time + timedelta(seconds=time_diff * ratio)
                    new_segment.points.append(new_point)

                    # Update the next target distance
                    target += target_distance
                    current_distance = (1 - ratio) * segment_distance

            # If the last point is less than half the target distance, add it
            if current_distance < target_distance * 0.5:
                new_segment.points.append(copy_point(segment.points[-1]))

    # Save the new GPX file
    try:
        with open(output_file, 'w') as f:
            f.write(new_gpx.to_xml())
        print(f"Successfully generated resampled GPX file: '{output_file}'")
    except Exception as e:
        print(f"Error saving GPX file: {e}")

def main():
    """Parse command-line arguments and perform resampling."""
    parser = argparse.ArgumentParser(description="Resample a GPX file to a specified point interval (in meters).")
    parser.add_argument("input_file", help="Path to the input GPX file")
    parser.add_argument("output_file", help="Path to the output GPX file")
    parser.add_argument("distance", type=float, default=200, nargs='?', help="Target distance between points (in meters, default is 200)")
    args = parser.parse_args()

    if args.distance <= 0:
        print("Error: Target distance must be positive")
        return

    resample_gpx(args.input_file, args.output_file, args.distance)

if __name__ == "__main__":
    main()