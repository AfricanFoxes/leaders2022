Выдает 1 - все объекты, 2 - объекты определенного типа.
1. api/objects/
2. api/objects/?o_type=type

Выдает 1 - все объекты, 2 - объекты определенного типа.
1. api/predictions/
2. api/predictions/?po_type=type

Выдает 1 - все регионы, 2 - регион.
1. api/regions/
2. api/regions/?r_name=NAME

Выдает все объекты, отсортированные по типам.
1. api/objects/typed/

Выдает все объекты, входящие в регион по okato.
1. api/objects/inregion/?r_name=NAME

Выдает все объекты, входящие в окружность.
1. api/objects/byradius/?lon=lon&lat=lat&radius=radius

Выдает топ объектов, по фильтрам.
1. api/objects/filtered/?ensemble_predict=0.5&count=5&pop=1000&postamats=20&type=Библиотека,...,

Выдает гексагоны определенного уровня: 7, 8, 9. При параметре heatmap=yes выдает только координаты и модели.
1. api/hexagon/?h_type=Hexagon_7&heatmap=yes