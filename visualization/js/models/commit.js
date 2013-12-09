GA.Commit = DS.Model.extend({
  message: DS.attr('string'),
  repo: DS.belongsTo('repo')
});

GA.Commit.FIXTURES = [
  {
    id: 1,
    repo: 1,
    message: 'commit message'
  }, {
    id: 2,
    repo: 1,
    message: 'second commit'
  }
];
