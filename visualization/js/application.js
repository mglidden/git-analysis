window.GA = Ember.Application.create({
  LOG_TRANSITIONS: true 
});

GA.ApplicationAdapter = DS.FixtureAdapter.extend();
GA.store = DS.Store.create()
