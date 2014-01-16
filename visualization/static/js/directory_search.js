var openDirectory = function() {
  var directoryName = $('#dir-search-field').val().replace('/', '-');
  _loadChartData('/directory_classification.json/' + directoryName);
}

