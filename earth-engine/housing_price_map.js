// ===== 0. Carregar a camada de estados e estilizar para destacar a Califórnia =====

// Carregar os estados dos EUA (dataset TIGER/2018/States)
var states = ee.FeatureCollection("TIGER/2018/States");

// Separar a Califórnia dos demais estados
var california = states.filter(ee.Filter.eq('NAME', 'California'));
var others = states.filter(ee.Filter.neq('NAME', 'California'));

// Estilizar os estados que não são a Califórnia: preenchimento cinza escuro e bordas cinza escuro
var othersStyled = others.style({
  fillColor: 'darkgray',
  color: 'darkgray'
});

// Estilizar a Califórnia para evidenciar (preenchimento transparente com contorno preto)
var californiaStyled = california.style({
  fillColor: '00000000',  // transparente
  color: 'black',
  width: 2
});

// Adicionar os estados ao mapa (camada de fundo)
Map.addLayer(othersStyled, {}, 'Outros Estados (Cinza Escuro)');
Map.addLayer(californiaStyled, {}, 'California');

// ===== 1. Carregar os dados das casas e estilizar os pontos =====

// Carregar os dados das casas a partir do asset CSV
var houses = ee.FeatureCollection("projects/land-use-analysis/assets/housing_features");

// Calcular o mínimo e o máximo do 'median_house_value'
var stats = houses.reduceColumns(ee.Reducer.minMax(), ['median_house_value']);
var minValue = ee.Number(stats.get('min'));
var maxValue = ee.Number(stats.get('max'));

// Obter os valores do lado do cliente para a legenda (são apenas 2 números)
var minVal = minValue.getInfo();
var maxVal = maxValue.getInfo();

// Definir a paleta de cores (gradiente do verde ao vermelho)
var palette = ee.List(['green', 'yellow', 'red']);

// Mapear cada feature para definir a cor conforme o 'median_house_value'
// e armazenar o objeto de estilo na propriedade 'style'
var housesStyled = houses.map(function(feature) {
  var value = feature.getNumber('median_house_value');
  // Normalizar o valor: 0 (mínimo) a 1 (máximo)
  var norm = value.subtract(minValue).divide(maxValue.subtract(minValue));
  // Converter o valor normalizado para um índice da paleta
  var index = norm.multiply(ee.Number(palette.length().subtract(1))).round();
  var selectedColor = ee.List(palette).get(index);
  
  // Definir o objeto de estilo (apenas a cor do ponto)
  var style = {color: selectedColor};
  return feature.set({style: style});
});

// Aplicar o estilo usando a propriedade 'style'
var styledLayer = housesStyled.style({styleProperty: 'style'});

// Adicionar a camada de casas ao mapa, centralizando na Califórnia
Map.centerObject(houses, 6);
Map.addLayer(styledLayer, {}, 'Median House Value');

// ===== 2. Criar a legenda com o gradiente de cor =====

var legendPanel = ui.Panel({
  style: {
    position: 'bottom-left',
    padding: '8px',
    backgroundColor: 'white'
  }
});

legendPanel.add(ui.Label({
  value: 'Median House Value',
  style: {fontWeight: 'bold', fontSize: '14px'}
}));

// Criar o gradiente para a legenda usando ui.Thumbnail
var colorBar = ui.Thumbnail({
  image: ee.Image.pixelLonLat().select(0)
    .multiply(maxValue.subtract(minValue))
    .add(minValue)
    .visualize({min: minVal, max: maxVal, palette: palette.getInfo()}),
  params: {bbox: [0, 0, 1, 0.1], dimensions: '200x20'},
  style: {stretch: 'horizontal', margin: '8px 0'}
});

legendPanel.add(colorBar);
legendPanel.add(ui.Label('Min: ' + minVal));
legendPanel.add(ui.Label('Max: ' + maxVal, {textAlign: 'right'}));
Map.add(legendPanel);