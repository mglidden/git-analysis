GA.Router.map(function() {
  this.resource('repos', {path: '/'});
//  this.resource('commit', {path: '/commit/:commit_id'});
  this.resource('repo', {path: '/repos/:repo_id'}, function() {
    this.resource('commits');
  });
});

GA.RepoRoute = Ember.Route.extend({
});

GA.CommitRoute = Ember.Router.extend({
});
