GA.Repo = DS.Model.extend({
  commits: DS.hasMany('commit', {async:true}),
  name: DS.attr('string')
});

GA.Repo.FIXTURES = [
  {
    commits: [1, 2],
    id: 1,
    name: 'edX'
  }, {
    id: 2,
    name: 'Yelp iPhone'
  }
];

