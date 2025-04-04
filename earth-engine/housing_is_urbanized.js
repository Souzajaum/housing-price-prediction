// 1. Carregar os dados das casas (suba o CSV para o GEE e substitua 'users/SEU_USUARIO/housing_features')
var houses = ee.FeatureCollection("projects/land-use-analysis/assets/housing_features");

// 2. Carregar a camada de áreas urbanizadas (suba o Shapefile para o GEE e substitua 'users/SEU_USUARIO/california_urbanized1990')
var urbanized = ee.FeatureCollection("projects/land-use-analysis/assets/data");

// 3. Criar uma nova variável indicando se a casa está ou não dentro da área urbanizada
var housesWithUrbanized = houses.map(function(feature) {
  var isUrban = urbanized.filterBounds(feature.geometry()).size().gt(0);
  return feature.set("urbanized", ee.Algorithms.If(isUrban, 1, 0));
});

// 4. Exportar os dados processados para o Google Drive
Export.table.toDrive({
  collection: housesWithUrbanized,
  description: "houses_with_urbanized_status",
  folder: "GEE_Exports",  // Nome da pasta no Google Drive
  fileFormat: "CSV"
});
