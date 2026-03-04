# Import necessary libraries
import ee
import geemap

# Dictionary of dynamic world classes and colors
DW_CLASSES = {
    'water' : '419bdf', # blue
    'trees' : '397d49', # green
    'grass' : '88b053', # light green
    'flooded_vegetation' : '7a87c6', # greyish blue
    'crops' : 'e49635', # orange
    'shrub_and_scrub' : 'dfc35a', # yellow
    'built' : 'c4281b', # red
    'bare' : 'a59b8f', # grey
    'snow_and_ice' : 'b39fe1', # purple
}

DW_BANDS = [*DW_CLASSES,'label']

# Dictionary with the visualization parameters for dynamic world classes
DW_VIZ_PARAMS = {
  'min' : 0,
  'max' : 8,
  'palette' : list(DW_CLASSES.values()),
  'bands' : 'label'
}

# Dictionary with the visualization parameters for Sentinel-2 images
S2_VIZ_PARAMS = {
  'min' : 0,
  'max' : 3000,
  'bands' : ['B4', 'B3', 'B2']
}

def get_dw_map(img, zoom = 12):
    """
    Function to map image from linked collection (Dynamic World + Sentinel-2)

    Args:
        image (ee.Image): must include [ label, B2, B3, B4 ] bands
        zoom (float): zoom value of the map
    Returns:
        geemap map with two layers
    """
    map = geemap.Map(scroll_wheel_zoom = False)
    map.centerObject(img, zoom)

    map.add_layer(
        img,
        S2_VIZ_PARAMS, 
        'Sentinel-2 L1C',
    )
    map.add_layer(
        img,
        DW_VIZ_PARAMS,
        'Dynamic World',
    )

    return map

def get_hillshade_map(img, zoom = 12):
    """
    Function to display Dynamic World confidence of class prediction using the elevation
    property of a hillshade map.  Higher confidence of a class membership represents higher elevation 
    and lower confidence represents lower elevation. 

    Args:
        image (ee.Image): must include [ DW_probability_classes, label, B2, B3, B4 ] bands
        zoom (float): zoom value of the map
    Returns:
        geemap map with two layers
    """
    # Create map object and center it in image center
    map = geemap.Map(scroll_wheel_zoom = False)
    map.centerObject(img, zoom)

    # For each pixel get the highest probability value among all class probabilities
    top1_prob = img.select(*DW_CLASSES).reduce(ee.Reducer.max())

    # Create a hillshade of the most likely class probability on [0, 1]
    # The algorithm expects values in meters so we convert probabilities by multiplying them by 100
    # The algorithm returns an RGB image, we convert it back to probabilities by diving by 255
    top1_prob_hillshade = ee.Terrain.hillshade(top1_prob.multiply(100)).divide(255)

    # Combine RGB information and hillshade
    dw_rgb_hillshade = img.visualize(**DW_VIZ_PARAMS).divide(255).multiply(top1_prob_hillshade)

    map.add_layer(
        img,
        S2_VIZ_PARAMS, 
        'Sentinel-2 L1C',
    )
    map.add_layer(
        dw_rgb_hillshade,
        {min: 0, max: 0.65},
        'Dynamic World V1 - label hillshade',
    )

    return map

def get_annual_classification(collection, year, method):
    """
    Function to calculate the year classification of a collection

    Args:
        collection (ee.ImageCollection): image collection with dynamic world bands
        year (int): year of desired classification
        method (mean, mode, median): the method to reduce the collection
            - mean: image with mean of probabilities of dw classes, label is determined by the class with the highest mean probability
            - mode: image with mode of probabilities of dw classes and mode of the label
            - median: image with median of probabilities of dw classes, label is determined by the class with the highest median probability
    Returns:
        eeImage which represents the classification for year
    """

    start_date='{}-01-01' 
    end_date='{}-12-31'

    year_collection = collection.filterDate(start_date.format(year),end_date.format(year))

    if method == 'mean':
        reducer = ee.Reducer.mean().setOuputs(*DW_CLASSES)
        year_mean_probabilities = year_collection.select(*DW_CLASSES).reduce(reducer).reproject(crs='EPSG:3857', scale=10)
        highest_bands = year_mean_probabilities.toArray().arrayArgmax().arrayGet(0)
        new_label = highest_bands.rename(['label'])
        year_classification = year_mean_probabilities.addBands(new_label)

    elif method == 'mode':
        reducer = ee.Reducer.mode().setOutputs(DW_BANDS)
        year_classification = year_collection.reduce(reducer).reproject(crs='EPSG:3857', scale=10)

    elif method == 'median':
        reducer = ee.Reducer.median().setOutputs(*DW_CLASSES)
        year_median_probabilities = year_collection.select(*DW_CLASSES).reduce(reducer).reproject(crs='EPSG:3857', scale=10)
        highest_bands = year_median_probabilities.toArray().arrayArgmax().arrayGet(0)
        new_label = highest_bands.rename(['label'])
        year_classification = year_median_probabilities.addBands(new_label)
    
    year_classification = year_classification.set('system:time_start',ee.Date(start_date.format(year)))
    year_classification = year_classification.set('system:time_end',ee.Date(end_date.format(year)))
    return year_classification

    