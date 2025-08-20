import json
from collections import defaultdict

import ifcopenshell
from ifcopenshell.util.element import get_psets
from ifcopenshell.util.placement import get_local_placement



def parse_bim_file(fail_path):
    ifc_file = ifcopenshell.open(fail_path)
    # 初始化存储结果的字典
    result = {
        "doors": [],
        "windows": [],
        "floor_heights": []
    }

    # 提取门的信息
    doors = ifc_file.by_type('IfcDoor')
    for door in doors:
        door_data = {
            "name": door.Name if door.Name else "Unnamed Door",
            "height": door.OverallHeight if hasattr(door, 'OverallHeight') else None,
            "width": door.OverallWidth if hasattr(door, 'OverallWidth') else None,
            "properties": {}
        }

        for definition in door.IsDefinedBy:
            if definition.is_a('IfcRelDefinesByProperties'):
                property_set = definition.RelatingPropertyDefinition
                if property_set.Name == 'Pset_DoorFireRating':
                    for prop in property_set.HasProperties:
                        if prop.is_a('IfcPropertySingleValue'):
                            door_data["properties"][prop.Name] = prop.NominalValue.wrappedValue

        result["doors"].append(door_data)

    # 提取窗的信息
    windows = ifc_file.by_type('IfcWindow')
    for window in windows:
        window_data = {
            "name": window.Name if window.Name else "Unnamed Window",
            "height": window.OverallHeight if hasattr(window, 'OverallHeight') else None,
            "width": window.OverallWidth if hasattr(window, 'OverallWidth') else None
        }
        result["windows"].append(window_data)

    # 提取楼板和楼层信息
    slabs = ifc_file.by_type('IfcSlab')
    storeys = ifc_file.by_type('IfcBuildingStorey')

    storey_elevations = defaultdict(list)
    for slab in slabs:
        if not slab.ObjectPlacement:
            continue

        placement = slab.ObjectPlacement
        if placement.is_a('IfcLocalPlacement'):
            matrix = get_local_placement(placement)
            elevation = matrix[2][3]

            if slab.ContainedInStructure:
                for rel in slab.ContainedInStructure:
                    if rel.is_a('IfcRelContainedInSpatialStructure'):
                        storey = rel.RelatingStructure
                        if storey.is_a('IfcBuildingStorey'):
                            storey_elevations[storey].append(elevation)

    # 计算每个楼层的层高（最高楼板 - 最低楼板）
    storey_heights = {}
    for storey, elevations in storey_elevations.items():
        if elevations:
            storey_height = max(elevations) - min(elevations)
            storey_heights[storey.Name] = storey_height

    # 按楼层标高排序（从低到高）
    sorted_storeys = sorted(
        storeys,
        key=lambda s: ifcopenshell.util.placement.get_storey_elevation(s)
    )

    # 计算相邻楼层的层高差（标准层高）
    floor_heights = []
    for i in range(1, len(sorted_storeys)):
        lower_storey = sorted_storeys[i - 1]
        upper_storey = sorted_storeys[i]

        lower_elevation = ifcopenshell.util.placement.get_storey_elevation(lower_storey)
        upper_elevation = ifcopenshell.util.placement.get_storey_elevation(upper_storey)

        floor_height = upper_elevation - lower_elevation
        floor_heights.append(floor_height)


    result["floor_heights"] = floor_heights

    # 将结果转换为 JSON 字符串
    json_result = json.dumps(result, indent=4, ensure_ascii=False)

    # 将结果保存到文件
    output_file = r'C:\Users\16021\Desktop\毕设\文件\result.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(json_result)

    print(f"结果已保存到 {output_file}")
    return output_file