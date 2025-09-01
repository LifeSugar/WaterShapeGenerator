class CN_Translation:
    translations = {
        "Water Body Properties": "水体属性",
        "Current Object:": "当前物体:",
        "No editable properties found": "没有找到可编辑的属性",
        "Found {count} properties": "共找到 {count} 个属性",
        "Generate Water Flow and Splash": "生成水流和水花",
        "Select a water body": "请选择一个水体",
        "Water Flow and Splash Generator": "水流和水花生成器",
        "Select an image for preview": "选择一张图片作为预览",
        "Generate Water": "生成水体",
        "No image selected": "未选择图片",
        "Selected image: {image_name}": "已选择图片: {image_name}",
    }

    @classmethod
    def translate(cls, text):
        return cls.translations.get(text, text)