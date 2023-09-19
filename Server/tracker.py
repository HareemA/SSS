import math

class Tracker:
    def __init__(self):
        self.center_points = {}
        self.id_count = 0
        self.max_inactive_frames = 10  # Maximum frames an object can be inactive before removing it

    def update(self, objects_rect):
        objects_bbs_ids = []

        for rect in objects_rect:
            x, y, w, h = rect
            cx = (x + x + w) // 2
            cy = (y + y + h) // 2

            # Find the closest object by calculating distance
            closest_id = None
            min_dist = float('inf')
            for object_id, (center, inactive_frames) in self.center_points.items():
                dist = math.hypot(cx - center[0], cy - center[1])
                if dist < min_dist:
                    min_dist = dist
                    closest_id = object_id

            if closest_id is not None and min_dist < 35:
                # Update existing object's position and reset inactive frames
                self.center_points[closest_id] = ((cx, cy), 0)
                objects_bbs_ids.append([x, y, w, h, closest_id])
            else:
                # New object detected
                self.center_points[self.id_count] = ((cx, cy), 0)
                objects_bbs_ids.append([x, y, w, h, self.id_count])
                self.id_count += 1

        # Clean up inactive objects
        inactive_ids = set()
        for obj_id, (_, inactive_frames) in self.center_points.items():
            if obj_id not in {obj_bb_id[4] for obj_bb_id in objects_bbs_ids}:
                inactive_frames += 1
                self.center_points[obj_id] = ((self.center_points[obj_id][0]), inactive_frames)
                if inactive_frames >= self.max_inactive_frames:
                    inactive_ids.add(obj_id)

        for obj_id in inactive_ids:
            del self.center_points[obj_id]

        return objects_bbs_ids
