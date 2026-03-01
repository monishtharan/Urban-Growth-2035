/**
 * Project: Urban Growth & Change Detection (Chennai)
 * Final Version: Classification + Area Stats + 2035 Prediction
 */

// 1. Define Study Area (Chennai)
var chennai_point = ee.Geometry.Point([80.27, 13.08]);
Map.centerObject(chennai_point, 11);

// 2. Load Satellite Imagery (Landsat 8 - 2024)
var dataset = ee.ImageCollection("LANDSAT/LC08/C02/T1_L2")
    .filterBounds(chennai_point)
    .filterDate('2024-01-01', '2025-12-31')
    .filter(ee.Filter.lt('CLOUD_COVER', 10))
    .median()
    .divide(10000);

// 3. Merge Training Samples (Builtup, Water, Veg layers imports)
var training_features = builtup.merge(water).merge(veg);

// 4. Sample the pixel values for Training
var training_data = dataset.sampleRegions({
  collection: training_features,
  properties: ['class'],
  scale: 30
});

// 5. Train Random Forest Classifier
var classifier = ee.Classifier.smileRandomForest(100).train({
  features: training_data,
  classProperty: 'class',
  inputProperties: dataset.bandNames()
});

// 6. Apply Classification (2024)
var classified_2024 = dataset.classify(classifier);

// 7. Visualization Settings
var classVis = {
  min: 0, 
  max: 2, 
  palette: ['red', 'blue', 'green'] // Red:Urban, Blue:Water, Green:Veg
};

Map.addLayer(classified_2024, classVis, 'Chennai Classification 2024');

// 8. Load & Classify 2014 Data
var dataset_2014 = ee.ImageCollection("LANDSAT/LC08/C02/T1_L2")
    .filterBounds(chennai_point)
    .filterDate('2014-01-01', '2014-12-31')
    .filter(ee.Filter.lt('CLOUD_COVER', 10))
    .median()
    .divide(10000);

var classified_2014 = dataset_2014.classify(classifier);
Map.addLayer(classified_2014, classVis, 'Chennai Classification 2014');

// 9. Change Detection (Highlight Growth in Yellow)
var urban_2014 = classified_2014.eq(0);
var urban_2024 = classified_2024.eq(0);
var urban_growth = urban_2024.gt(urban_2014);
Map.addLayer(urban_growth.updateMask(urban_growth), {palette: ['yellow']}, 'Urban Growth (2014-2024)');

// 10. Area Statistics & Accuracy
var trainAccuracy = classifier.confusionMatrix();
print('Accuracy Matrix:', trainAccuracy);
print('Overall Training Accuracy:', trainAccuracy.accuracy());

var calculateArea = function(image, name) {
  var area = image.multiply(ee.Image.pixelArea()).reduceRegion({
    reducer: ee.Reducer.sum(),
    geometry: chennai_point.buffer(20000).bounds(),
    scale: 30,
    maxPixels: 1e9
  });
  // Using 'classification' as the band name for results
  var areaVal = ee.Number(area.values().get(0)).divide(1000000);
  print(name + ' Area (sq km):', areaVal);
};

print('--- Final Area Statistics ---');
calculateArea(urban_2014, '2014 Urban');
calculateArea(urban_2024, '2024 Urban');

var growthStats = urban_growth.multiply(ee.Image.pixelArea()).reduceRegion({
  reducer: ee.Reducer.sum(),
  geometry: chennai_point.buffer(20000).bounds(),
  scale: 30,
  maxPixels: 1e9
});
print('Net Urban Growth (sq km):', ee.Number(growthStats.values().get(0)).divide(1000000));

// --- 2035 PREDICTION LOGIC ---
var growthRate = 5.79; // Annual rate from 99.5% accuracy result
var predictionYears = 11; 
var totalFutureGrowth = growthRate * predictionYears;

print('--- 2035 Forecast ---');
print('Predicted Additional Urban Growth by 2035 (sq km):', totalFutureGrowth);

// Orange Layer Logic - Fixing the Band Error
var predictedUrban2035 = urban_2024.focal_max(2500, 'square', 'meters')
                         .updateMask(urban_2024.not())
                         .selfMask();

Map.addLayer(predictedUrban2035, {palette: ['orange']}, 'Predicted Urban Growth 2035');

// Export to Drive
Export.image.toDrive({
  image: classified_2024,
  description: 'Chennai_Urban_Final_2024',
  scale: 30,
  region: chennai_point.buffer(20000).bounds(),
  fileFormat: 'GeoTIFF'
});
