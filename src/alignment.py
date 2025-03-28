import bpy
import mathutils

def get_world_bbox(obj):
    """
    Returns the object's bounding box in world coordinates, formatted as:
      ((xmin, xmax), (ymin, ymax), (zmin, zmax))
    """
    coords = [obj.matrix_world @ mathutils.Vector(corner) for corner in obj.bound_box]
    xs = [v.x for v in coords]
    ys = [v.y for v in coords]
    zs = [v.z for v in coords]
    return (min(xs), max(xs)), (min(ys), max(ys)), (min(zs), max(zs))

def get_extreme_value(bbox, axis='x', extreme='max'):
    """
    Extracts extreme value from bounding box along specified axis.
    Args:
      bbox: ((xmin, xmax), (ymin, ymax), (zmin, zmax))
      axis: 'x', 'y' or 'z'
      extreme: 'max' to get maximum value along axis; 'min' for minimum
    Returns:
      Corresponding extreme value (float)
    """
    if axis == 'x':
        return bbox[0][1] if extreme == 'max' else bbox[0][0]
    elif axis == 'y':
        return bbox[1][1] if extreme == 'max' else bbox[1][0]
    elif axis == 'z':
        return bbox[2][1] if extreme == 'max' else bbox[2][0]
    else:
        raise ValueError("Axis must be 'x', 'y', or 'z'.")

# Get two models (ensure their names are correct in the scene)
model1 = bpy.data.objects["model1"]
model2 = bpy.data.objects["model2"]

# Calculate world bounding boxes for both models
bbox1 = get_world_bbox(model1)
bbox2 = get_world_bbox(model2)

# For alignment:
# - Take 'max' extremes (right/top/front) from model1
# - Take 'min' extremes (left/bottom/back) from model2
diff_x = get_extreme_value(bbox1, 'x', 'max') - get_extreme_value(bbox2, 'x', 'min')
diff_y = get_extreme_value(bbox1, 'y', 'max') - get_extreme_value(bbox2, 'y', 'min')
diff_z = get_extreme_value(bbox1, 'z', 'max') - get_extreme_value(bbox2, 'z', 'min')

# Determine dominant axis for snapping
diff_components = [abs(diff_x), abs(diff_y), abs(diff_z)]
axes = ['x', 'y', 'z']
max_index = diff_components.index(max(diff_components))
snapping_axis = axes[max_index]

# Create translation vector only along the selected axis
translation_vector = mathutils.Vector((0.0, 0.0, 0.0))
if snapping_axis == 'x':
    translation_vector.x = diff_x
elif snapping_axis == 'y':
    translation_vector.y = diff_y
elif snapping_axis == 'z':
    translation_vector.z = diff_z

print("Model1 bounding box:")
print("  X:", bbox1[0])
print("  Y:", bbox1[1])
print("  Z:", bbox1[2])
print("Model2 bounding box:")
print("  X:", bbox2[0])
print("  Y:", bbox2[1])
print("  Z:", bbox2[2])
print("Diff: x={:.3f}, y={:.3f}, z={:.3f}".format(diff_x, diff_y, diff_z))
print("Selected snapping axis:", snapping_axis)
print("Translation vector along selected axis:", translation_vector)

# Move model2 to align with model1
model2.location += translation_vector