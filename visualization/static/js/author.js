// todo: move this method to a common JS file
var _loadChartData = function(dataURL) {
  d3.json(dataURL, function(data) {
    d3.select('#stacked-chart svg')
      .datum(data)
      .transition().duration(500)
      .call(stackedChart);
  });
}

var currentAuthorId = -1;
var openAuthor = function(authorId) {
  _loadChartData('/author_classification.json/' + authorId);

  $('#authors-back').slideDown();

  $('#author-' + currentAuthorId).removeClass('author-selected');
  $('#author-' + authorId).addClass('author-selected');
  currentAuthorId = authorId
}

var openRepo = function() {
  _loadChartData('/repo_classification.json');

  $('#authors-back').slideUp();

  $('#author-' + currentAuthorId).removeClass('author-selected');
  currentAuthorId = -1
}
