var _loadChartData = function(dataURL) {
  d3.json(dataURL, function(data) {
    d3.select('#stacked-chart svg')
      .datum(data)
      .transition().duration(500)
      .call(stackedChart);
  });
}

var openAuthor = function(authorId) {
  console.log(authorId);
  _loadChartData('/author_classification.json/' + authorId);

  $('#authors-back').slideDown();
}

var openRepo = function() {
  _loadChartData('/repo_classification.json');

  $('#authors-back').slideUp();
}
