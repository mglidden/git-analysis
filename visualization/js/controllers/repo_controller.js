GA.ReposController = Ember.ObjectController.extend({
  foo: function() {
    return this.get('model');
  }
});
