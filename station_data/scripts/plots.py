import cartopy.crs as ccrs
import proplot as pplt
from adjustText import adjust_text


def plot_stations(
    station_cubes: list, extent: tuple = (11, 22, 52, 68), adjust: bool = True
):
    fig, ax = pplt.subplots(
        figwidth="15cm",
        # figheight="14cm",
        projection=ccrs.epsg(3006),
    )
    annotations = []
    lats = []
    lons = []
    for cube in station_cubes:
        lat = cube.coord("latitude").points
        lats.append(lat)
        lon = cube.coord("longitude").points
        lons.append(lon)
        name = cube.attributes["station_name"]
        ax.scatter(lon, lat, s=30, c="C1",
                   transform=ccrs.PlateCarree(), zorder=3)
        annotations.append(
            ax.text(
                lon,
                lat,
                name,
                c="k",
                # bbox={"boxstyle": "round", "alpha": 0.4},
                transform=ccrs.PlateCarree(),
            )
        )
    ax.coastlines()
    ax.set_extent(extent)
    if adjust:
        adjust_text(annotations, x=lons, y=lats, ax=ax)
