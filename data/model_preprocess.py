import bpy
import math
from mathutils import Vector
import os


class ModelProcessor:
    def __init__(self, config):
        self.config = config
        self.target_obj = None

    def process(self):
        self._clear_scene()
        self._load_model()
        self._normalize_model()
        self._rotate_model()
        self._export_model()

    def _clear_scene(self):
        """清空场景"""
        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.object.delete()
        for material in bpy.data.materials:
            bpy.data.materials.remove(material)

    def _load_model(self):
        """加载并标准化模型"""
        ext = self.config['model_path'].split('.')[-1].lower()
        import_func = {
            'obj': bpy.ops.import_scene.obj,
            'glb': bpy.ops.import_scene.gltf,
            'fbx': bpy.ops.import_scene.fbx
        }.get(ext, None)

        if not import_func:
            raise ValueError(f"不支持的格式: {ext}")

        try:
            bpy.ops.object.select_all(action='DESELECT')
            import_func(filepath=self.config['model_path'])
            imported_objects = [obj for obj in bpy.context.selected_objects if obj.type == 'MESH']

            if not imported_objects:
                raise RuntimeError("没有找到有效的网格物体")

            bpy.context.view_layer.objects.active = imported_objects[0]

            if len(imported_objects) > 1:
                bpy.ops.object.mode_set(mode='OBJECT')
                for obj in imported_objects:
                    obj.select_set(True)
                bpy.ops.object.join()
                self.target_obj = bpy.context.active_object
            else:
                self.target_obj = imported_objects[0]

        except Exception as e:
            self._clear_scene()
            raise RuntimeError(f"模型加载失败: {str(e)}")

    def _normalize_model(self):
        """标准化模型尺寸"""
        bbox = [self.target_obj.matrix_world @ Vector(corner) for corner in self.target_obj.bound_box]
        bbox_min = Vector((min(v.x for v in bbox), min(v.y for v in bbox), min(v.z for v in bbox)))
        bbox_max = Vector((max(v.x for v in bbox), max(v.y for v in bbox), max(v.z for v in bbox)))

        current_size = bbox_max - bbox_min
        max_dim = max(current_size)
        scale_factor = 2.0 / max_dim if max_dim != 0 else 1.0
        self.target_obj.scale *= scale_factor
        bpy.context.view_layer.update()

    def _rotate_model(self):
        """绕Z轴旋转90度"""
        self.target_obj.rotation_euler.z = math.radians(90)
        bpy.context.view_layer.update()

    def _export_model(self):
        """导出模型（覆盖原文件）"""
        ext = self.config['model_path'].split('.')[-1].lower()
        export_path = self.config['model_path']

        # 确保目录存在
        os.makedirs(os.path.dirname(export_path), exist_ok=True)

        # 选择对象
        bpy.ops.object.select_all(action='DESELECT')
        self.target_obj.select_set(True)
        bpy.context.view_layer.objects.active = self.target_obj

        try:
            if ext == 'obj':
                bpy.ops.export_scene.obj(
                    filepath=export_path,
                    use_selection=True,
                    use_materials=False,
                    use_overwrite=True
                )
            elif ext in ('glb', 'gltf'):
                bpy.ops.export_scene.gltf(
                    filepath=export_path,
                    export_format='GLB' if ext == 'glb' else 'GLTF_SEPARATE',
                    use_selection=True,
                    export_draco_mesh_compression_enable=False
                )
            elif ext == 'fbx':
                bpy.ops.export_scene.fbx(
                    filepath=export_path,
                    use_selection=True,
                    bake_space_transform=True
                )
            else:
                raise ValueError(f"不支持的导出格式: {ext}")

            print(f"成功导出模型到: {export_path}")

        except Exception as e:
            raise RuntimeError(f"导出失败: {str(e)}")


if __name__ == "__main__":
    config = {
        'model_path': 'D:/models/test_model.glb'
    }

    processor = ModelProcessor(config)
    processor.process()