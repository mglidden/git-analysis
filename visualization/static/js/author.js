var openAuthor = function(authorId) {
  console.log(authorId);
  d3.json('/author_classification.json/' + authorId, function(data) {
    d3.select('#stacked-chart svg')
      .datum(data)
      .transition().duration(500)
      .call(stackedChart);
  });
}
