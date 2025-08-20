import ifcopenshell

# 加载IFC文件
file_path = r"C:\Users\16021\Desktop\毕设\文件\别墅项目.ifc"
ifc_file = ifcopenshell.open(file_path)

# 提取所有物理对象（IfcProduct及其子类）
all_objects = ifc_file.by_type("IfcProduct")  # 包括墙、楼板、门、窗等

# 统计对象数量
object_count = len(all_objects)
print(f"物理对象总个数: {object_count}")

# 可选：打印对象类型分布
from collections import defaultdict
type_counter = defaultdict(int)
for obj in all_objects:
    type_counter[obj.is_a()] += 1

print("\n对象类型分布:")
for obj_type, count in sorted(type_counter.items()):
    print(f"{obj_type}: {count}")