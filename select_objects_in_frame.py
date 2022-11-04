import geopandas as gpd
PATH_DATASET = "datasets/"
K_LAT = 111.134861111
K_LON = 64.87434

def get_items_by_radius(df, center, radius):
    """
    Выбираем все объекты в квадрате, куда вписана окружность радиуса 3км
    !Важно для быстрого поиска используется поиск не по радиусу а по квадрату
    df - Pandas DataFrame (либо GeoPandas), где объекты имеют колонки долготу "lon" и широту "lat"
    center - центральная точка от которой будут искаться объекты в радиусе
    radius - радиус от центра в км
    """
    assert center[0] < center[1], "Перепутаны местами долгота широта у `center`, сначала долготу 37.ххх, затем широту 55.ххх"
    min_lon = center[0] - radius/K_LON
    max_lon = center[0] + radius/K_LON
    min_lat = center[1] - radius/K_LAT
    max_lat = center[1] + radius/K_LAT
    return df[(df.lat >= min_lat)&(df.lat <= max_lat)&(df.lon >= min_lon)&(df.lon <= max_lon)]

def get_items_by_frame(df, p1, p2):
    """
    df - Pandas DataFrame (либо GeoPandas), где объекты имеют колонки долготу "lon" и широту "lat"
    p1, p2 - массивы координаты противолежаших углов (вершин) квадрата (фрейма)
    """
    assert (p1[0] < p1[1])and(p2[0] < p2[1]), "Перепутаны местами долгота широта в `p1`,`p2` , сначала долготу 37.ххх, затем широту 55.ххх"
    min_lon, max_lon = min(p1[0],p2[0]), max(p1[0],p2[0])
    min_lat, max_lat = min(p1[1],p2[1]), max(p1[1],p2[1])
    return df[(df.lat >= min_lat)&(df.lat <=max_lat)&(df.lon >= min_lon)&(df.lon<=max_lon)]


# Загружаем данные из json сразу в geopandas (можно использовать и pandas)
objects = gpd.read_file(PATH_DATASET + "objects_dataset.json", driver="GeoJSON")
print(objects.shape)

# Определяем произвольную точку
center_point = (objects.iloc[42].lon, objects.iloc[42].lat)

# Выбираем все объекты в квадрате, куда вписана окружность радиуса 3км и центром
select_objects = get_items_by_radius(objects, center=center_point, radius=3)
print(select_objects.shape)