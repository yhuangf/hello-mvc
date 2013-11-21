/* The model for simple-mvc item */

function Simple(db, url) {
  // local cached content
  db = db || DB("simple-riot");
  var self = $.observable(this);
  
  
  self.url = url || 'http://0.0.0.0:5000/api/bills';

  /* model events */
  self.add = function(name){
    var item = {id: "_" + ("" + Math.random()).slice(2),
                name: name}
    items[item.id] = item;
    self.trigger("add", item)
  }
  
  var items = getdata();

  function getdata() {
    // load remotely
    items = db.get();
    self.add("item1");
    $.ajax({
      url: self.url,
      context: self,
      success:  function(data) { 
        $.each(data, self.add(item))
      }
    });
    return items
  }
  
  self.remove = function(filter) {
    var els = self.items(filter);
    $.each(els, function(){
      delete items[this.id]
    })
    self.trigger("remove", els);
  }
  
  // @param filter: <empty>, id, "active", "completed"
  self.items = function(filter) {
    var ret = [];
    $.each(items, function(id, item) {
      if (!filter || filter == id || filter == (item.done ? "completed" : "active"))
        ret.push(item)
    })
    return ret;
  }

  self.on("add remove toggle edit", function() {
    db.put(items);
  })
}
